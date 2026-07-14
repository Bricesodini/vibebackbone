# ADR — 0034-consumer-managed-runtime-assets

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Décideurs**: Brice (`Go`, 2026-07-14), Codex (formalisation)
**Liée à**: ADR 0012, ADR 0023, ADR 0027, SEC-CRED-005, TER-001
**Liée à POC**: `docs/runs/2026-07-14_1242_consumer-managed-hook-bundle/POC.md`

## Contexte

L'initialiseur mélange deux catégories : les documents contenant la vérité du
projet consommateur et les assets exécutables fournis par VBB. Le mode par défaut
préserve tout mais ne met rien à jour ; l'overwrite global remplace la vérité
projet et ses sauvegardes répétées. En parallèle, `--install-hook` ne copie qu'un
redirecteur obsolète, omet l'installateur canonique et ses dépendances, masque
l'échec comme un skip puis retourne 0.

## Décision

Nous séparons explicitement deux régimes :

1. les documents projet sont **project-owned / generated-once** ; ils restent
   ignorés lors d'un init répété sauf overwrite documentaire explicite ;
2. le bundle runtime de hooks est **VBB-managed / non-customizable** ; son état
   installé est enregistré dans un manifeste versionné par hashes SHA-256 ;
3. un refresh est automatique seulement si chaque cible est absente ou identique
   au dernier hash VBB enregistré ; le preflight refuse tout le bundle si une
   cible a été personnalisée ou n'a pas de provenance connue ;
4. un remplacement forcé d'asset géré ou de hook Git requiert son option dédiée
   (`--overwrite-managed` ou `--overwrite-hook`), distincte de l'overwrite
   documentaire ;
5. une erreur de copie ou d'installation est une erreur terminale, jamais un
   skip ni un succès.

La première application est bornée au bundle nécessaire au hook canonique. Elle
ne transforme pas l'initialiseur en moteur général de merge documentaire.

## Alternatives considérées

### Overwrite systématique des assets déclarés non personnalisables

- **Avantages** : implémentation minimale, refresh assuré.
- **Inconvénients** : aucune protection contre une customisation accidentelle ;
  perte silencieuse contraire au constat TER-001.

### Hooks pointant vers le checkout VBB source

- **Avantages** : aucun bundle à copier, mise à jour instantanée.
- **Inconvénients** : chemins non portables, dépendance à un autre checkout,
  consommateurs inutilisables isolément.

### Fusion automatique à trois voies

- **Avantages** : pourrait conserver certaines adaptations.
- **Inconvénients** : complexité disproportionnée, conflits ambigus sur scripts
  de sécurité, fausse promesse pour les documents projet.

### Statu quo

- **Avantages** : aucun changement.
- **Inconvénients** : hook absent avec exit 0 et aucune voie de refresh sûre.

## Rationale

Un manifeste de provenance fournit la preuve minimale permettant de distinguer
un fichier VBB inchangé d'un fichier localement modifié. Le preflight du bundle
évite les mises à jour partielles. La séparation des flags empêche qu'une demande
d'overwrite documentaire autorise implicitement le remplacement d'un contrôle
Git ou de sécurité.

## Conséquences

### Positives

- Installation consommateur autonome et vérifiable.
- Refresh idempotent des assets VBB inchangés.
- Préservation et signalement des personnalisations locales.
- Frontière durable entre vérité projet et runtime fourni.

### Négatives / coûts

- Un manifeste supplémentaire doit être versionné par le consommateur.
- Une ancienne installation sans manifeste est traitée comme non possédée et
  nécessite une adoption/force explicite.
- Le bundle doit déclarer toutes ses dépendances transitives.

### Neutres / à surveiller

- TER-001 n'est fermé que pour la frontière d'ownership et le bundle runtime ;
  aucun refresh de document projet n'est promis.
- Les quatre distributions héritent de ce comportement Core sans glue provider.

## Références

- `docs/runs/2026-07-14_0721_consumer-refresh-poc/POC.md`
- `tools/vbb-project-init.py`
- `scripts/install-vbb-hooks.sh`
- `docs/AUDIT_STATUS.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: CONSUMER_OWNERSHIP
reversible: true
depends_on:
  - docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md
blocks: []
supersedes: []
verified_at: "2026-07-14T12:46:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-human-approval + bounded-poc-required"
```
