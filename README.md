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

## Liste des cartes par classe

**Mage**:

```
Fireball, Frostbolt, Arcane Intellect, Blizzard, Flamestrike, Polymorph, Mirror Image, Counterspell, Ice Block, Ice Barrier, Arcane Missiles, Mana Wyrm, Sorcerer's Apprentice, Flamewaker, Antonidas, Frost Nova
```

**Warrior**:

```
Execute, Shield Slam, Brawl, Whirlwind, Armorsmith, Fiery War Axe, Shield Block, Battle Rage, Slam, Grommash Hellscream, Frothing Berserker, Bloodhoof Brave, Mortal Strike, Revenge, Death's Bite
```

**Druid**:

```
Force of Nature, Keeper of the Grove, Ancient of Lore, Ancient of War, Mark of the Wild, Claw, Feral Rage, Druid of the Claw, Malfurion the Pestilent
```

**Hunter**:

```
Kill Command, Explosive Trap, Animal Companion, Unleash the Hounds, Tracking, Eaglehorn Bow, Houndmaster, Savannah Highmane, Freezing Trap, Deadly Shot, Multi-Shot, Flare, Quick Shot, Call of the Wild, King Krush
```

**Paladin**:

```
Consecration, Blessing of Kings, Truesilver Champion, Equality, Hammer of Wrath, Holy Light, Lay on Hands, Avenging Wrath, Aldor Peacekeeper, Tirion Fordring, Murloc Knight, Lightforged Zealot, Righteous Protector, Argent Protector, Sunkeeper Tarim
```

**Priest**:

```
Shadow Word: Pain, Shadow Word: Death, Mind Control, Holy Nova, Power Word: Shield, Thoughtsteal, Northshire Cleric, Auchenai Soulpriest, Lightspawn, Cabal Shadow Priest, Prophet Velen, Shadow Madness, Circle of Healing, Anduin Wrynn, Psychic Scream
```

**Rogue**:

```
Backstab, Sap, Eviscerate, Assassinate, Fan of Knives, Preparation, Deadly Poison, Edwin VanCleef, SI:7 Agent, Shadowstep, Blade Flurry, Shiv, Betrayal, Vanish, Plague Scientist, Valeera the Hollow
```

**Shaman**:

```
Lightning Bolt, Lava Burst, Hex, Feral Spirit, Bloodlust, Ancestral Spirit, Stormforged Axe, Doomhammer, Earth Shock, Rockbiter Weapon, Flametongue Totem, Mana Tide Totem, Thunder Bluff Valiant, The Lich King, Hagatha the Witch
```

**Warlock**:

```
Soulfire, Hellfire, Shadow Bolt, Drain Life, Mortal Coil, Voidwalker, Flame Imp, Imp Gang Boss, Doomguard, Lord Jaraxxus, Void Terror, Siphon Soul, Twisting Nether, Darkbomb, Defile, Gul'dan the Destroyer
```

**Demon Hunter** (ajout récent) :

```
Twin Slice, Chaos Strike, Blade Dance, Immolation Aura, Spectral Sight, Aldrachi Warblades, Metamorphosis, Skull of Gul'dan, Warglaives of Azzinoth, Illidan Stormrage, Eye Beam, Fel Barrage, Wrathspike Brute, Nethrandamus
```

**Neutral**:

```
Chillwind Yeti, Boulderfist Ogre, Acidic Swamp Ooze, Novice Engineer, Harvest Golem, Ragnaros the Firelord, Alexstrasza, Ysera, Deathwing, Leeroy Jenkins, Knife Juggler, Doomsayer, Sludge Belcher, Piloted Shredder, Cairne Bloodhoof, The Black Knight, Sylvanas Windrunner
```
