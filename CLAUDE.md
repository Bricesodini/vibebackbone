# CLAUDE.md — vibebackbone

Tu operationnes sous la gouvernance **vibebackbone**.

**vibebackbone = 57 skills · 24 prompts · 4 voies (rapide, structurée, audit, clôture)**

## Fichiers de gouvernance

- `AGENTS.md` — Grammaire opérationnelle canonique (à la racine vibebackbone)
- `SYSTEM.md` — Comportement runtime Pi
- `skills/vibebackbone/docs/PILOTAGE.md` — Pilotage opérationnel v2.0

## Raccourcis (chemins relatifs au repo vibebackbone)

- Skills : `skills/` (57 dossiers, chacun contient un SKILL.md)
- Prompts : `prompts/` (24 templates)
- Catalogue complet : `skills/0-vbb-guide/SKILL.md`

## 🎯 Triage opérationnel (règle fondamentale)

**Avant toute action, classifier la tâche dans UNE des 4 voies :**

| Voie | Signaux | Approche |
|------|---------|----------|
| **RAPIDE** | Risque faible, pas de contrats, pas de multi-fichiers | Agir directement, zéro plan requis |
| **STRUCTURÉE** | Contrats de données, multi-fichiers, plan avant modification | Lire PROJECT_MODE.md → lancer skill approprié → placer le plan |
| **AUDIT** | Sécurité, intégrité données, réglementaire, prod | Exécuter séquence [0→1→2→3] canonique, générer rapports |
| **CLÔTURE** | Fin de session, reprise d'une session antérieure | Lancer session-handoff, compacter contexte |

**Pour plus de détails** → [AGENTS.md § 3](AGENTS.md) (triage opérationnel complet)

**Cas courants :**
- Correction typo README → RAPIDE
- Ajouter skill → STRUCTURÉE (skill = contrat, donc plan)
- Vulnérabilité sécurité découverte → AUDIT
- Fin de journée de travail → CLÔTURE

## 📖 Lecture recommandée (par ordre)

1. **Ce fichier** (CLAUDE.md) — vue générale
2. **AGENTS.md § 3** — détail du triage et escalade
3. **skills/0-vbb-guide/SKILL.md** — guide interactif des 57 skills
4. **skills/vibebackbone/docs/PILOTAGE.md** — source de vérité opérationnelle complète

## 🔧 Utilisation typique

```bash
# 1. Classifier votre tâche (RAPIDE, STRUCTURÉE, AUDIT, ou CLÔTURE)
# → Relire le tableau "Triage opérationnel" ci-dessus

# 2. Si RAPIDE → agir directement
#    Si autre voie → voir correspondances ci-dessous

# 3. Lister les skills disponibles
ls skills/

# 4. Appliquer un skill (exemple : audit de sécurité)
cat skills/2-vbb-security/SKILL.md
# Puis suivre les étapes INPUT CONTRACT → PROCESS → OUTPUT CONTRACT
```

## ⚡ Optimisations

### Prompt caching (Claude / Claude Code)

Les fichiers suivants sont excellents candidats pour prompt caching (valent la peine d'être réutilisés) :

- **AGENTS.md** (325 lignes) — grammaire opérationnelle, stable
- **SYSTEM.md** (146 lignes) — comportement runtime Pi, stable
- **skills/vibebackbone/docs/PILOTAGE.md** (323 lignes) — source de vérité, stable

Ces fichiers changent rarement et sont lus par de nombreux agents. Caching = économies contextuelles.
