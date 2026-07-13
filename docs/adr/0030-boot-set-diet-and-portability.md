# ADR — 0030-boot-set-diet-and-portability

**Status**: ACCEPTED
**Date**: 2026-07-13
**Route**: STRUCTUREE
**Décideurs**: Brice (GO « boucler le ponçage »), Claude (formalisation)
**Liée à**: ADR 0027 (V2-R1) ; TD-105/TD-107 ; évaluation externe 2026-07-13
**Liée à POC**: aucune — déduplication documentaire, pas d'hypothèse d'intégration

## Contexte

Le boot set (CLAUDE.md + AGENTS.md + SYSTEM.md, ~2 156 mots) est chargé par les
quatre agents à chaque session. Il duplique des règles entre AGENTS et SYSTEM
(planification, closeout, discipline de risque, conventions qualité), porte des
compteurs maintenus à la main qui dérivent (« 63/64 skills »), et cite des
chemins morts (`~/02_Dev`, `/Users/bot`) hérités du HOME du mainteneur
historique (TD-105). AUDIT_STATUS/TECH_DEBT contiennent des entrées contredites
par l'état mesuré (TD-107 : QOA-003 corrigé par V2-R1 mais marqué REOPENED ;
PyYAML noté absent alors que 6.0.2 est actif). Enfin, `~/.claude/CLAUDE.md`
global véhicule une grammaire VibeCodex concurrente du canon VBB.

## Décision

1. **Portabilité** : toute référence active à `~/02_Dev/...` ou `/Users/bot/...`
   est remplacée par un chemin relatif au dépôt (les outils se lancent depuis la
   racine) ou par `$VBB_HOME` quand le contexte est hors repo. La prompt library
   est documentée comme chemin résolu par le setup de chaque distribution.
2. **Compteurs** : les fichiers de boot ne portent plus de dénombrements
   maintenus à la main (skills/prompts) ; la volumétrie vit dans le dashboard.
3. **Diète à contenu constant** : SYSTEM.md est recentré sur le comportement
   runtime (posture, plan-first, MVP gate, style) et **pointe** vers AGENTS.md
   pour tout ce qui y est déjà canonique (triage, gates, closeout, Rule 12,
   qualité). Aucune exigence n'est supprimée ; cible boot ≤ ~1 200 mots.
   Découverte en exécution : `SYSTEM.md` racine est un **symlink** vers
   `distributions/pi/SYSTEM.md` (fichier réel) — synchronisation structurelle,
   aucune copie manuelle à maintenir.
4. **Réconciliation d'état** (TD-107) : QOA-003 → RESOLVED (preuve : V2-R1,
   commit `ca70f4a`, tests) ; TD-001 → PyYAML 6.0.2 installé et utilisé par les
   gates (entrée mise à jour, pas réécrite).
5. **État externe** : `~/.claude/CLAUDE.md` est sauvegardé
   (`CLAUDE.md.bak-YYYYMMDD`) puis ses sections de gouvernance VibeCodex sont
   remplacées par un pointeur vers le canon VBB du dépôt ; la section
   « Délégation au LLM local » (infrastructure) est conservée telle quelle.

## Conséquences

### Positives
- Une seule grammaire de triage pour tous les agents ; fin des chemins morts.
- ~45 % de tokens de boot en moins à chaque session, sur quatre agents.
- AUDIT_STATUS/TECH_DEBT redeviennent plus fiables que les commandes qu'ils résument.

### Négatives / coûts
- Risque de perte de règle pendant la déduplication — mitigé par vérification
  avant/après (liste des règles canoniques) et CCP.
- (levé en exécution : la « copie » pi/SYSTEM.md est en réalité la cible du
  symlink racine — aucun point de synchronisation manuel).

### Neutres
- Le fond des règles est inchangé ; seuls l'emplacement et la forme bougent.

## Alternatives rejetées (≥ 2)

### Alternative A — Générer les boot files depuis le canon (ADR-0012 codegen)
- **Pourquoi rejetée (ici)** : bon horizon, mais c'est un outillage nouveau —
  contraire au moratoire de la phase de ponçage ; la diète manuelle est le
  prérequis qui rend le codegen simple plus tard.

### Alternative B — Supprimer SYSTEM.md et tout fusionner dans AGENTS.md
- **Pourquoi rejetée** : SYSTEM.md porte le comportement runtime Pi/OpenCode
  (consommé par symlink/copie) ; fusionner casserait les setups existants.
