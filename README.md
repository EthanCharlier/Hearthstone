`python -m unittest discover -s tests -p "test_*.py"`

`for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"`

## Déroulement d'une partie

### **1. Préparation :**

- **Choix du deck :** Chaque joueur sélectionne un héros et un deck de 30 cartes. Chaque héros représente une classe, avec des cartes spécifiques et un pouvoir héroïque unique.

---

### **2. Début de la partie :**

- Le jeu choisit au hasard qui commence :
  - **Le joueur 1 :** Dispose de 1 cristal de mana au tour 1.
  - **Le joueur 2 :** Dispose de 1 cristal de mana au tour 1.

---

### **3. Déroulement des tours :**

Chaque tour suit une structure définie :

1. **Gain de mana :** Au début de chaque tour, vous gagnez un cristal de mana supplémentaire (jusqu’à un maximum de 10).
2. **Pioche d’une carte :** Vous piochez une carte au début de chaque tour.
3. **Jouer des cartes :**
   - **Serviteurs :** Cartes posées sur le plateau qui peuvent attaquer ou défendre.
   - **Sorts :** Effets ponctuels qui influencent la partie (infliger des dégâts, soigner, etc.).
4. **Pouvoir héroïque :** Chaque héros peut utiliser son pouvoir spécifique en échange de 2 cristaux de mana.
5. **Attaques :** Les serviteurs ou le héros peuvent attaquer si possible.
6. **Fin du tour :** Vous passez la main à votre adversaire.

---

### **4. Objectifs et conditions de victoire :**

- Le but est de réduire les **points de vie de l’adversaire** (30 au départ) à 0.

---

### **5. Fin de la partie :**

- La partie se termine quand un héros atteint 0 point de vie ou qu’un joueur abandonne.

---

### **Stratégie :**

- Gérer ses ressources (mana, cartes en main).
- Anticiper les actions adverses.
- Maximiser l'efficacité de chaque tour en utilisant les cartes de manière optimale.

## TODO

- GameLogic
- GameLoop
- Interfaces
- Spell effects
