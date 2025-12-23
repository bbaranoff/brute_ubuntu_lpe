Download dictionnary
```
wget https://github.com/RykerWilder/rockyou.txt/raw/refs/heads/main/rockyou.txt.zip
```

# PAM Exploit

## 1. Principe Technique : Timing Oracle (CWE-208)

Ce script exploite une vulnérabilité de type **canal auxiliaire temporel** (Timing Side-Channel) dans le processus d'authentification Linux. 

### Le concept "Oracle"
Contrairement à un bruteforce classique qui attend une réponse binaire (vrai/faux), PAM utilise un chronomètre précis. Si le module PAM ou `sudo` met un temps anormalement long ou court pour valider une étape, le script identifie cette latence.

* **L'Oracle** : Une limite de temps (`ORACLE_TIMEOUT`) est fixée.
* **Action** : Si le système ne répond pas dans ce délai, le processus est tué immédiatement pour passer au mot de passe suivant.
* **Bypass** : Cette méthode permet de tester les mots de passe à une vitesse dépassant les limites habituelles des services d'authentification en ignorant les délais d'échec (fail-delay).



## 2. Usage et Optimisation

Le script est optimisé pour les processeurs multi-cœurs (testé sur architecture 16 cœurs).

### Configuration du script
Les variables doivent être ajustées selon la latence de votre machine :
* `MAX_WORKERS` : f(CPU). Nombre de threads simultanés (recommandé : 1.5x à 2x le nombre de cœurs physiques).
* `ORACLE_TIMEOUT` : f(Latence). Le seuil de coupure (ex: `0.080` pour 80ms). Si trop bas, vous raterez le bon mot de passe.

### Lancement optimal
```bash
# 1. Charger la wordlist en RAM pour supprimer la latence disque
cp rockyou.txt /dev/shm/

# 2. Lancer le script
python3 bruteforce_ultra.py --wordlist /dev/shm/rockyou.txt

```

## 3. Statistiques de Compromission

Basé sur une vitesse de **168 mdp/s** sur un parc informatique standard utilisant la liste `RockYou.txt`.

### Temps de succès (Probabilités)

| Cible | Position (Ligne) | Temps estimé |
| --- | --- | --- |
| **Top 1%** | 1 - 140k | ~14 minutes |
| **Utilisateur Standard** | Milieu de liste | **~11 heures 45** |
| **Liste Complète** | 14,3M | ~23 heures 30 |

### Efficacité sur 100 machines

Statistiquement, sur un échantillon de 100 machines Linux non durcies :

* **35%** seront compromises en moins de **12 heures** (une nuit).
* **65%** seront compromises en moins de **24 heures**.
* **35%** résisteront (mots de passe complexes hors dictionnaire ou clés SSH).

## 4. Avertissement

Ce script est destiné à des fins de tests d'intrusion et d'audit de sécurité uniquement. L'exploitation des vulnérabilités de type CWE-208 souligne l'importance d'utiliser des fonctions de comparaison de temps constant et des délais d'authentification fixes.

```bash
nirvana@acer:~/brute_ubuntu_lpe$ python bruteforce_ultra.py --wordlist rockyou.txt
🚀 Bruteforce it !!! | Workers: 16 | Oracle: 0.08s
------------------------------------------------------------
[*] Tentatives : 4970 | Speed: ~175 mdp/s | Test: manuelito   

✅ TROUVÉ : limpbizkit
[*] Stats finales : 4972 tests en 28.25s (176.02 mdp/s)
```

```

