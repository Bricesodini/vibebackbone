# ADR — 0029-risk-triggered-closeout-quality-pass

**Status**: ACCEPTED
**Date**: 2026-07-13
**Route**: STRUCTUREE
**Décideurs**: Brice (GO roadmap V2 + réserve « déclenchée selon le risque »), Claude (formalisation)
**Liée à**: ADR 0028 (audits scopés — prérequis), ADR 0026 (pas de nettoyage pendant le scan)
**Liée à POC**: aucune — pas d'hypothèse d'intégration à prototyper

## Contexte

L'évaluation externe du 2026-07-13 a montré que les skills qualité-code
n'atteignent jamais le code des projets consommateurs : sur trame, un doublon
de 699 lignes et un monolithe de 1 513 lignes ont traversé des dizaines de
chantiers sans être détectés. La cause n'est pas l'absence d'outils (janitor,
tech-debt, db-robustness existent) mais l'absence de **routage** : rien ne
déclenche ces audits au moment où le code vient d'être touché. Brice a arbitré :
déclenchement **selon le risque**, pas systématique (réserve du 2026-07-13 sur
la V2). Par ailleurs, la discipline de compaction de contexte qu'il pratique
(seuil ~40 %) n'était écrite nulle part ; seul « context <75% » existait comme
critère de changement de session.

## Décision

1. **Passe qualité scopée au closeout, déclenchée par le risque.** Le prompt
   canonique `07-p-vbb-closeout.md` et le template `07_CLOSEOUT.md.template`
   intègrent une étape : si le chantier touche données / auth / sécurité /
   compliance / état de production, **ou** modifie 4+ fichiers de code produit
   (seuil FAST-STANDARD), une passe janitor (et tech-debt / db-robustness si
   pertinent) est exécutée avec `scope` = périmètre touché par le chantier,
   selon `docs/REFERENCE/scoped-audit-protocol.md`. Routes FAST-ZERO /
   FAST-MINIMAL et chantiers docs-only : passe optionnelle. Les P0/P1 trouvés
   partent en runs de remédiation (jamais corrigés pendant le closeout,
   ADR-0026). Le closeout **trace** la décision : `EXECUTED` / `SKIPPED
   (risque faible)` / `N/A (docs-only)` — un skip est déclaré, jamais silencieux.
2. **Règle de compaction 40/75 dans SESSION_RULES.md** : à ~40 % de fenêtre
   consommée, compaction recommandée (`tools/vbb-context-compactor.py` +
   mini-handoff) ; à 75 %, **limite dure** — compaction ou changement de session
   obligatoire avant toute nouvelle action (aligne le critère existant
   « context <75% » avec une conduite prescrite, pas seulement un constat).

## Conséquences

### Positives
- La dette des projets consommateurs est détectée au moment où le code est chaud.
- Le coût reste proportionné : pas de passe sur les micro-changements.
- La pratique de compaction de Brice devient une règle transmissible aux 4 agents.

### Négatives / coûts
- Closeout des chantiers à risque plus long (une passe scopée en plus).
- Un déclencheur mal calibré peut sur- ou sous-déclencher ; le seuil
  « 4+ fichiers de code produit » est révisable après V2-R5a (terrain).

### Neutres
- Aucun canon CONVENTIONS/PILOTAGE modifié ; SESSION_RULES et template/prompt
  seulement (précédent : Run 7).

## Alternatives rejetées (≥ 2)

### Alternative A — Passe qualité systématique à chaque closeout
- **Pourquoi rejetée** : réserve explicite de Brice (2026-07-13) ; coût token
  disproportionné sur les petits chantiers ; produirait du théâtre de process.

### Alternative B — Hook git post-commit déclenchant l'audit
- **Pourquoi rejetée** : un audit LLM n'est pas exécutable en hook local ;
  le closeout est le point de passage humain-visible où la décision se trace.
