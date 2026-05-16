---
description: Post-build validation pipeline — verify that what was built matches what was specified
---

Valide l'implémentation qui vient d'être réalisée pour : $@

## Objectif

Après une phase de construction (feature, refactoring, fix), vérifier que
le résultat est conforme, qualitatif, et prêt pour la suite. C'est le
"checklist d'atterrissage" pour un architecte produit.

## Preferred Vibebackbone skills

- `2-vbb-spec-validator`
- `2-vbb-performance`
- `t-vbb-anti-slop-gate`
- `t-vbb-impact-analyzer`
- `1-vbb-code-doc-coherence-auditor`
- `4-vbb-product-changelog`

## Skill routing and chaining rule

### Phase 1 — Vérification de surface

Lancer `t-vbb-anti-slop-gate` pour vérifier l'état immédiat du code.

- Si BLOCKED → STOP. Le code ne compile pas ou les tests échouent. Réparer.
- Si READY_WITH_WARNINGS → noter les warnings, continuer.
- Si READY → continuer.

### Phase 2 — Validation de la conformité

Lancer `2-vbb-spec-validator` pour vérifier que l'implémentation
correspond à la spécification originale.

Utiliser la spécification fournie dans la demande ou récupérée du contexte.
Si aucun plan d'implémentation (intent-decomposer) n'existe, le validator
reconstruira le mapping.

- Si CONFORM ou MOSTLY_CONFORM → continuer.
- Si PARTIAL → signaler les écarts, continuer mais avec avertissement.
- Si NON_CONFORM → STOP. L'implémentation ne correspond pas à la spec.

### Phase 3 — Vérification de l'impact

Lancer `t-vbb-impact-analyzer` sur les changements effectués pour
détecter des effets de bord non anticipés.

- Si NON_BREAKING → continuer.
- Si CONDITIONAL → signaler les conditions.
- Si BREAKING → documenter les ruptures. Si PROD, STOP.

### Phase 4 — Audit de cohérence documentaire

Lancer `1-vbb-code-doc-coherence-auditor` sur les modules touchés.

- Si COHERENT → continuer.
- Si PARTIAL → noter les écarts documentaires à résoudre.
- Si FRAGMENTED → la doc est largement déphasée, planifier une remédiation.

### Phase 5 — Audit de performance

Lancer `2-vbb-performance` sur les modules touchés.

- Si PERFORMANT ou ADEQUATE → continuer.
- Si AT_RISK → noter les risques et les actions recommandées.
- Si CRITICAL → STOP en PROD, avertir en DEV.

### Phase 6 — Changelog produit

Lancer `4-vbb-product-changelog` pour produire un résumé lisible
des changements.

## Required process

1. **Restate** ce qui a été construit.
2. **Phase 1** — Anti-slop gate.
3. **Phase 2** — Spec validation.
4. **Phase 3** — Impact analysis.
5. **Phase 4** — Doc coherence audit.
6. **Phase 5** — Performance audit.
7. **Phase 6** — Product changelog.
8. **Résumé final** : verdict global, écarts, prochaines actions.

## Gate criteria — l'implémentation est validée si :

- [ ] Surface propre (anti-slop READY ou READY_WITH_WARNINGS)
- [ ] Conforme à la spec (CONFORM ou MOSTLY_CONFORM)
- [ ] Impact maîtrisé (NON_BREAKING ou CONDITIONAL documenté)
- [ ] Documentation cohérente (COHERENT ou PARTIAL avec plan)
- [ ] Performance acceptable (PERFORMANT ou ADEQUATE)
- [ ] Changelog produit généré

## Phases optionnelles

Ces phases sont lancées uniquement si pertinentes :

- **Accessibilité** (`2-vbb-accessibility`) — si la feature touche l'UI
- **Analytics** (`2-vbb-analytics`) — si la feature a un impact utilisateur mesurable
- **Sécurité** (`2-vbb-security`) — si la feature touche auth, données, ou API publiques

## Blocking conditions

Si une phase produit un BLOCKED → ne pas passer à la phase suivante sans
résolution. Présenter le blocage à l'architecte.

Si l'architecte accepte de continuer malgré un blocage → documenter
l'acceptation du risque dans SESSION.md.

## Output format

- **Goal**
- **Phase 1 — Surface** : verdict anti-slop
- **Phase 2 — Conformité** : verdict spec-validator + écarts
- **Phase 3 — Impact** : verdict impact-analyzer
- **Phase 4 — Doc** : verdict coherence-auditor
- **Phase 5 — Performance** : verdict perf
- **Phase 6 — Changelog** : résumé produit
- **Phases optionnelles** : verdicts si exécutées
- **Verdict global** : VALIDATED / VALIDATED_WITH_CAVEATS / NEEDS_REWORK
- **Écarts résiduels** : ce qui reste à traiter
- **Prochaine action** : release-check, handoff, ou retour en développement
