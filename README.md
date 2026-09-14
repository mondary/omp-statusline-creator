# OMP Status Line Creator

[🇫🇷 FR](README.md) · [🇬🇧 EN](README_en.md)

![OMP Status Line Creator](icon.png)

Composer la status line d'Oh My Pi à la souris, la prévisualiser, et exporter la config — sans éditer de YAML à l'aveugle.

![Aperçu du configurateur](store/screenshots/01-configurateur.png)

Thème clair : ![Configurateur en thème clair](store/screenshots/02-configurateur-clair.png)

## ✅ Fonctionnalités

- **Catalogue complet** : les 26 segments d'OMP (`pi`, `status`, `model`, `mode`, `path`, `git`,
  `pr`, `subagents`, `session`, `session_name`, `collab`, `vim`, `hostname`, `token_in`,
  `token_out`, `token_total`, `token_rate`, `cache_read`, `cache_write`, `cache_hit`, `cost`,
  `context_pct`, `context_total`, `time_spent`, `time`, `usage`) — description, exemple de rendu,
  bascule gauche/droite, ajout au clic.
- **Presets d'origine** copiés à l'identique (`default`, `minimal`, `compact`, `full`, `nerd`,
  `ascii`, `custom`) en pilules, preset actif surligné — plus les pilules **customPK1** et
  **customPK2**, tes sélections. Un preset local se sérialise en `preset: custom`, seul format
  qu'OMP sait relire.
- **Options réelles** : seuls `model`, `path`, `git` et `time` lisent des options ; l'app les
  édite avec leurs défauts OMP affichés.
- **Aperçu fidèle** : deux rangées comme dans le TUI (métriques incrustées dans la bordure haute,
  identité sous l'éditeur), trois jeux de données — **`exemple riche` par défaut** (on voit tout
  ce qui peut s'afficher), `ma session type` (ce que tu vois réellement) et `session vide` (quels
  segments se masquent tout seuls) — avec les glyphes réels des presets `nerd` / `unicode` / `ascii`.
- **Catalogue avec aperçu et état d'usage** : chaque ligne montre le **rendu réel du segment**
  (glyphe du preset choisi + valeur d'exemple, tronqué si trop long), puis un badge `◀`/`▶`/`◀▶`
  et `×n` quand il est déjà présent, le compteur `n/26`, un filtre **« masquer les segments déjà
  utilisés »** et le détail au survol (« utilisé : gauche ×2 »).
- **Version visible** : la version courante s'affiche en permanence dans l'en-tête (badge `v…`) —
  elle vient du `VERSION` du hub et est réécrite dans `index.html` par `python3 bump.py`
  (contre-vérification : `python3 bump.py --check`).
- **Version OMP affichée** : le sous-titre montre la version d'OMP **contre laquelle les glyphes
  ont été extraits** (lue par `extract-symbols.py` sur `omp --version`, écrite dans `symbols.js`),
  avec binaire et date en infobulle — plus de numéro figé dans le HTML.
- **Interface responsive** : 3 colonnes au-delà de 1240 px, 2 au-delà de 1040, empilée en dessous ;
  les deux listes passent sur une seule colonne sous 780 px, et le tiroir occupe alors toute la
  largeur. Aucun débordement horizontal de 420 px à 1500 px.
- **Deux surfaces distinctes** : `Exporter ▾` (action primaire, `⌘E`) ouvre **l'export**
  uniquement ; `Importer` ouvre **l'import** uniquement — même tiroir, vues exclusives, titre
  adapté.
- **Thème clair / sombre** : `Auto` (suit le système), `Clair`, `Sombre` — le thème sombre est
  **Catppuccin Frappé** (`#303446`, texte `#c6d0f5`, accent `#8caaee`), mémorisé par le navigateur.
  L'aperçu reste volontairement sombre — c'est une maquette de terminal.
- **Composition en deux colonnes** : `leftSegments` à gauche, `rightSegments` à droite, chaque
  tuile affichant son **rendu réel** (glyphe + valeur d'exemple). Au glisser, un **repère pointillé
  « déposer ici »** montre la position d'arrivée exacte (la tuile glissée passe en pointillé
  translucide) ; déposer dans l'autre colonne change de bord. `Alt`+`↑`/`↓` déplace la tuile
  sélectionnée au clavier.
- **Bascules automatiques** : `preset` passe à `custom` dès qu'on retouche une liste ou une
  option (hors `custom`, OMP ignore `leftSegments`/`rightSegments`/`segmentOptions` du fichier).
- **Garde-fous** : alerte listes vides (`[]` n'hérite d'aucun preset → barre vide), signalement
  des ids inconnus à l'import.

## 🧠 Utilisation

1. Ouvrir `index.html` ; l'app démarre sur la config courante (`Ma config actuelle`).
   Panneaux : catalogue à gauche, aperçu + listes au centre, presets / réglages / options à droite.
2. Cliquer les segments du catalogue, réordonner par glisser-déposer, `⇄` change de côté, `×` retire.
3. Vérifier l'aperçu, puis ouvrir **Export / Import** dans l'en-tête, onglet **Commandes**,
   copier et appliquer.
4. Relancer la session OMP : **la status line n'est pas rechargée à chaud**.

## ⚙️ Réglages

Les réglages exportés sont ceux du schéma OMP : `preset`, `separator`, `contextLine`,
`sessionAccent`, `transparent`, `showHookStatus`, `leftSegments`, `rightSegments`,
`segmentOptions`.

Deux points vérifiés dans le binaire, et signalés dans l'interface :

- `separator` n'a **aucun effet** en mode d'affichage `plain-*` (celui du terminal) : le
  séparateur y est `·` en dur ; le réglage ne compte qu'en mode `box`/`band`.
- le libellé de plan du segment `usage` (« OpenCode Go ») est toujours rendu : aucune option
  ne le coupe.

## 🧾 Commandes

```bash
open index.html                 # lancer l'app (aucun serveur, aucune dépendance)
python3 extract-symbols.py      # régénérer symbols.js depuis le binaire omp du PATH
python3 extract-symbols.py /chemin/vers/omp
python3 bump.py                 # bump CalVer : VERSION du hub + constantes index.html + READMEs
python3 bump.py 2026.10.01      # forcer une version (synchronise les 4 porteurs)
python3 bump.py --check         # vérifie VERSION <-> interface <-> READMEs FR/EN

omp config get statusLine.leftSegments          # vérifier ce qui est appliqué
omp config set statusLine.preset custom         # ce que produit l'onglet « Commandes »
```

## 📦 Build & Package

Aucun build : `index.html` + `symbols.js` sont servis tels quels (ouvrir le fichier suffit).
`symbols.js` est **généré** — ne pas l'éditer à la main. La constante `APP_VERSION` d'`index.html`
est écrite par `bump.py` (elle alimente le badge de version de l'en-tête) — ne pas l'éditer non
plus. `favicon.svg` est la source de l'icône ; `icon.png`, `apple-touch-icon.png` et
`favicon-32.png` en sont dérivés (rendu navigateur).

## 🧪 Installation

Rien à installer : récupérer le dossier du hub (`tools/omp-statusline-creator/`) et ouvrir
`index.html`. L'état du composeur est conservé dans le `localStorage` du navigateur ; l'app
n'écrit jamais sur le disque.

## 📋 Voir le [CHANGELOG](../../CHANGELOG.md) pour l'historique complet

## 🔗 Liens

- [Oh My Posh Configurator](https://github.com/jamesmontemagno/ohmyposh-configurator) — l'équivalent qui a inspiré cet outil.
- [omp.sh](https://omp.sh) — Oh My Pi.
- `omp://settings.md` et `omp://models.md` — docs embarquées dans l'app OMP.

## 🚧 Limites connues

- Ce que OMP ne sait pas faire, le configurateur ne l'invente pas : une option d'aperçu qui
  contredirait le rendu réel du terminal (par exemple masquer les libellés `5h/7d/mo` du segment
  `usage`) n'a pas sa place ici.
- L'aperçu reproduit **la disposition**, pas les échappements ANSI : les couleurs suivent le
  thème `titanium` de façon schématique.
- Les glyphes `nerd` exigent une police Nerd Font installée pour s'afficher ; les presets
  `unicode` et `ascii` passent partout.
- Si Stencil ajoute ou renomme un segment, le catalogue doit être mis à jour à la main
  (`extract-symbols.py` ne rafraîchit que les glyphes).
