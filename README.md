Install dépendencies
```
sudo apt install git unzip wget
```

Clone repo
```
git clone https://github.com/bbaranoff/brute_ubuntu_lpe && cd brute_ubuntu_lpe
```

Download dictionnary
```
wget https://github.com/RykerWilder/rockyou.txt/raw/refs/heads/main/rockyou.txt.zip
```

Unzip
```
unzip rockyou.txt.zip
```

Bruteforce
```
bash brute.sh rockyou.txt
```

