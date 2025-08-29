import threading
import time
import queue

# ✅ Fonction worker
def worker(thread_id, password_queue):
    while True:
        try:
            pw = password_queue.get(timeout=1)
        except queue.Empty:
            break  # Plus rien à traiter, le thread peut s'arrêter

        pw = pw.strip()
        if not pw:
            continue

        print(f"[Thread {thread_id}] Test du mot de passe: {pw}")
        # test_password(pw)  # À activer selon ton code

# ✅ Lancement des threads
if __name__ == "__main__":
    password_queue = queue.Queue()

    # 📄 Remplir la queue depuis un fichier (ex : rockyou.txt)
    with open("/home/nirvana/Téléchargements/rockyou.txt", "r", encoding="latin-1", errors="ignore") as f:
        for line in f:
            password_queue.put(line)

    threads = []
    for i in range(4):  # 4 workers par exemple
        t = threading.Thread(target=worker, args=(i, password_queue), daemon=True)
        t.start()
        threads.append(t)

    print("Threads lancés. Appuie sur Ctrl+C pour arrêter.")

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Arrêt demandé, fin du programme.")
