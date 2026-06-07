# 🤖 Bot Discord — Rôles & Salons

## Installation

```bash
# 1. Installe les dépendances
pip install -r requirements.txt

# 2. Configure ton token
# Ouvre le fichier .env et remplace "ton_token_ici" par ton vrai token

# 3. Lance le bot
python bot.py
```

---

## Commandes disponibles

| Commande | Description | Permission requise |
|----------|-------------|-------------------|
| `/roles` | Affiche le panneau de rôles avec boutons | Gérer les rôles |
| `/creer-salon` | Crée un salon texte ou vocal | Gérer les salons |

---

## Personnaliser les rôles

Dans `bot.py`, trouve la liste `ROLES` dans la classe `RoleView` :

```python
ROLES = [
    ("Annonces", "Annonces", "📢", discord.ButtonStyle.primary),
    ("Gaming",   "Gaming",   "🎮", discord.ButtonStyle.success),
    ...
]
```

Format de chaque ligne :
- **"Nom affiché"** → texte sur le bouton
- **"Nom exact du rôle Discord"** → doit correspondre exactement au rôle dans ton serveur
- **emoji** → affiché sur le bouton
- **style** → `primary` (bleu), `success` (vert), `secondary` (gris), `danger` (rouge)

---

## Important — Ordre des rôles Discord

Le bot doit avoir un rôle **au-dessus** des rôles qu'il distribue dans la hiérarchie Discord.
(Paramètres du serveur → Rôles → glisse le rôle du bot vers le haut)
