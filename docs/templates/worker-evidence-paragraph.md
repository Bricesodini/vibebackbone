# Worker Evidence Paragraph (canon template, Core)

> Added 2026-06-13 (Phase 2 Run 1, P0-1 §4.3). Template canonique du
> paragraphe "Evidence classification" à propager dans les 4 worker
> SOUL.md (vbb-fast-worker, vbb-struct-worker, vbb-audit-worker,
> vbb-close-worker).
>
> **Distinction Core ↔ Distribution** : ce paragraphe vit en **Core**
> (`docs/templates/`) car c'est un invariant méthodologique générique.
> Le script de sync qui patche les 4 SOUL.md vit en **distribution**
> (`distributions/hermes/install/sync-evidence-model.sh` — out of scope
> pour Phase 2 Run 1). C'est la séparation Core/Distribution correcte
> (DISTRIBUTIONS.md §5 Rule A : Core ne référence pas une distribution).

---

## Evidence classification (synchronisé avec Cody SOUL.md §2)

Toute observation que ce worker produit doit être catégorisée :

- **VERIFIED_FINDING** : assertion prouvée par une commande exécutée
  dans ce run (output cité, exit code documenté).
- **SIGNAL** : observation non-prouvée, à investiguer.
- **HYPOTHESIS** : explication possible, non-vérifiée.

Ne JAMAIS écrire "fixed" / "passes" / "repaired" sans VERIFIED_FINDING.
Les SIGNAL/HYPOTHESIS vont dans `07_CLOSEOUT §Points ouverts`, pas
dans `§Décisions prises`. Le paragraphe est validable par
`tools/vbb-loop-closure-check.py --validate-claims` (P0-1 §4.1).

---

**Règles d'application par voie :**

- `vbb-fast-worker` (route RAPIDE) : applique ce paragraphe en
  **FAST-STANDARD+**, peut SKIP en **FAST-MINIMAL/FAST-ZERO**
  (le closeout doit alors déclarer la voie explicitement).
- `vbb-struct-worker` (STRUCTUREE) : applique **toujours**.
- `vbb-audit-worker` (AUDIT, READ-ONLY) : applique **strictement**.
- `vbb-close-worker` (CLOSEOUT) : applique en bout de chaîne (valide
  que les claims upstream ont une VERIFIED_FINDING).

**Source** : `docs/strategy/phase-1-contractualisation/phase-1-p0-1-evidence-claims.md` §4.3.
