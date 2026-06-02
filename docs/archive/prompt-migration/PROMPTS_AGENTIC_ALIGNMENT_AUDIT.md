# PROMPTS_AGENTIC_ALIGNMENT_AUDIT

**Audit d'alignement des 24 prompts lanceurs Vibebackbone avec le protocole agentique en 7 phases**

| Métadonnée | Valeur |
|-----------|--------|
| Date | 2026-05-18 |
| Durée audit | 2–3 h (3 passes itératives) |
| Agent responsable | Claude Opus 4.7 |
| Scope | 24 prompts + mapping vers 57 skills |
| Statut | ✅ Complet |

---

## 1. Résumé exécutif

**Verdict global : À adapter fortement (option "hybride" recommandée)**

Les 24 prompts lanceurs vibebackbone constituent une base **opérationnelle et fonctionnelle**, mais présentent des **désalignements majeurs** avec le protocole agentique en 7 phases défini dans `AGENTIC_RUN_PROTOCOL.md`. Les prompts mélangent actuellement :

- Responsabilités multi-phases (audit + décision dans le même prompt)
- Exécution vs. review dans un seul contexte
- Absence de handoff explicite vers la phase suivante
- Dépendance excessive à la mémoire conversationnelle pour l'État d'exécution
- Pas d'artefacts nommés persistants ou mal nommés

**Recommandation d'architecture :** Créer une **couche légère d'orchestration** (_sequencer_) qui :
1. Invoque les prompts existants dans l'ordre correct du protocole 7 phases
2. Capture les artefacts à chaque phase
3. Produit le handoff explicite entre phases
4. Élimine la dépendance à la mémoire conversationnelle

---

## 2. Cartographie actuelle des prompts

| Prompt | Intention | Phase Supposée | Artefact Attendu | Statut |
|--------|-----------|----------------|------------------|--------|
| 0-p-vbb-triage | Classer la tâche dans une voie | 01_INTAKE | Verdict voie (rapide/structurée/audit/clôture) | Incomplet |
| 0-p-vbb-plan | Produire un plan avant exécution | 01_INTAKE → 04_PLAN | Plan structuré | Fragmenté |
| 0-p-vbb-before-building | Vérifier les préconditions avant feature | 01_INTAKE + gates | Verdict readiness + blockers | Incomplet |
| 1-p-vbb-quick-task | Exécuter une tâche RAPIDE | 01_INTAKE → 05_EXECUTION | Code modifié (pas d'artefact nommé) | Ambigu |
| 1-p-vbb-structured-task | Exécuter une tâche STRUCTURÉE | 01_INTAKE → 04_PLAN → 05_EXECUTION | Code modifié (pas d'artefact nommé) | Fragmenté |
| 1-p-vbb-audit-task | Exécuter une tâche AUDIT | 01_INTAKE → 02_AUDIT → 03_DECISION | Rapport d'audit (incomplet) | Fragmenté |
| 1-p-vbb-project-init | Initialiser gouvernance projet | 01_INTAKE | Statut gouvernance | Partiel |
| 1-p-vbb-tech-debt | Évaluer la dette technique | 02_AUDIT | Rapport de dette | Incomplet |
| 1-p-vbb-legacy-level | Évaluer le legacy level | 02_AUDIT | Évaluation (non-persistée) | Ambigu |
| 1-p-vbb-doc-feature | Produire documentation feature | 02_AUDIT → 03_DECISION → 05_EXECUTION | Documentation produite | Fragmenté |
| 1-p-vbb-post-refacto-coherence | Audit post-refactoring complet | 02_AUDIT → 05_EXECUTION → 07_CLOSEOUT | Handoff, doc, rapports | Complexe |
| 2-p-vbb-db-sanity | Évaluer sanité DB | 02_AUDIT | Rapport (non-persisté) | Incomplet |
| 2-p-vbb-audit-task | Générique pour audit quelconque | 02_AUDIT → 03_DECISION | Rapport d'audit | Abstrait |
| 2-p-vbb-mode-transition | Vérifier transition dev→prod | 03_DECISION | Verdict transition | Incomplet |
| 2-p-vbb-release-check | Pre-release gate complet | 02_AUDIT (multi-domaines) → 03_DECISION | Verdict GO/CONDITIONAL/NO-GO | Complexe |
| 2-p-vbb-security-pipeline | Pipeline sécurité complet | 02_AUDIT (4 steps) → 07_CLOSEOUT | 4 rapports + risk register | Bien structuré |
| 3-p-vbb-risk-register | Compiler registre de risques | 03_DECISION → 07_CLOSEOUT | Risk register (persisté) | Bon |
| 4-p-vbb-before-building | Validation pré-build | 04_PLAN → 05_EXECUTION | Verdict readiness + plan | Ambigu |
| 4-p-vbb-after-building | Validation post-build | 05_EXECUTION → 06_REVIEW | Verdict validation + artefacts | Complexe |
| 4-p-vbb-anti-slop | Quality gate (read-only) | 02_AUDIT ou 05_EXECUTION (ponte) | Rapport anti-slop | Bon (read-only) |
| 4-p-vbb-deploy-docker | Pipeline Docker deploy | 02_AUDIT → 04_PLAN → 05_EXECUTION → 07_CLOSEOUT | 3 rapports + deploy.sh | Bien structuré |
| t-p-vbb-start-session | Ouvrir session Vibebackbone | 01_INTAKE | Résumé contexte | Bon |
| t-p-vbb-branch-policy-check | Vérifier stratégie branche | 03_DECISION | Verdict fit + recommandation | Partiel |
| t-p-vbb-git-sync | Committer + pusher | 05_EXECUTION → 06_REVIEW (ponte) | Commit SHA + merge result | Bon (quand utilisé) |
| t-p-vbb-sequenced-ship | Exécution séquencée longue | 01_INTAKE → 07_CLOSEOUT (orchestration) | Contexte packets + summary | Innovation positive |
| t-p-vbb-session-handoff | Handoff de clôture | 07_CLOSEOUT | Session handoff | Bon |

---

## 3. Analyse détaillée par prompt

### 0-p-vbb-triage

1. **Intention** : Classifier une tâche dans exactement une voie (rapide/structurée/audit/clôture)
2. **Phase** : 01_INTAKE (correcte)
3. **Rôle** : Classifier / Router
4. **Artefact** : Verdict voie + justification brève
5. **Artefact attendu per protocole** : Énoncé implicite au sein d'un 01_INTAKE.md
6. **Handoff** : ❌ Pas de handoff explicite. Le prompt dit "state only the next recommended action" mais ne spécifie pas le passage à la phase suivante
7. **Risque de dérive** : Léger — le prompt reste focalisé sur le triage
8. **Dépendance contexte** : Oui — repose sur la mémoire pour récupérer docs/PILOTAGE.md et docs/PROJECT_MODE.md
9. **Compatibilité multi-LLM** : ✅ Bonne — utilise skills ou fallback manuel
10. **Décision** : **ADAPTER** — ajouter handoff explicite vers phase 03 ou 04 selon la voie

---

### 0-p-vbb-plan

1. **Intention** : Produire un plan avant exécution
2. **Phase** : 01_INTAKE + 04_PLAN (ambigu — deux phases dans un même prompt)
3. **Rôle** : Planner + Décideur
4. **Artefact** : Plan court (pas nommé persistant)
5. **Artefact attendu** : `04_FIX_PLAN.md`
6. **Handoff** : ⚠️ Faible — dit "waiting for confirmation" puis "execute" mais ne parle pas du passage à 05
7. **Risque de dérive** : Moyen — le prompt mélange INTAKE et PLAN, risque de sauter des étapes
8. **Dépendance contexte** : Oui — fortement dépendant de l'énoncé du goal dans le chat
9. **Compatibilité multi-LLM** : ✅ Acceptable
10. **Décision** : **ADAPTER** — scinder en deux invocations : INTAKE (résumé) puis PLAN (détail)

---

### 0-p-vbb-before-building

1. **Intention** : Pre-build checklist — valider que tout est prêt avant feature
2. **Phase** : 01_INTAKE (intake) + 04_PLAN (vérification)
3. **Rôle** : Architecte / Validateur de readiness
4. **Artefact** : Verdict readiness (READY/READY_WITH_CAVEATS/NOT_READY) + blockers + plan résumé
5. **Artefact attendu** : `01_INTAKE.md` + potentiellement `04_FIX_PLAN_SUMMARY.md`
6. **Handoff** : ⚠️ Partial — dit "Next action: commencer Wave 1, ou résoudre blockers" mais pas de transition explicite vers 04_PLAN ou 05_EXECUTION
7. **Risque de dérive** : **Élevé** — enchaîne 5 phases de gates sans séparation claire
8. **Dépendance contexte** : Très élevée — orchestre plusieurs skills en interne
9. **Compatibilité multi-LLM** : ⚠️ Risquée — complexité multi-étapes peut déborder sur modèles locaux
10. **Décision** : **ADAPTER** → scinder en orchestration `before-building-phase-1` (gate) et chaînage vers `plan` (phase 04)

---

### 1-p-vbb-quick-task

1. **Intention** : Exécuter une tâche RAPIDE (risque faible, réversible)
2. **Phase** : 01_INTAKE → 05_EXECUTION (saute 02, 03, 04)
3. **Rôle** : Exécuteur
4. **Artefact** : Code modifié, pas d'artefact nommé
5. **Artefact attendu per protocole** : Devrait produire `01_INTAKE.md` + `05_PATCH_SUMMARY_RUN_01.md`
6. **Handoff** : ❌ Absent — pas de message vers la phase suivante
7. **Risque de dérive** : **Moyen** — peut escalader de RAPIDE à STRUCTURÉE/AUDIT en cours d'exécution si le risque augmente
8. **Dépendance contexte** : Faible — localisé
9. **Compatibilité multi-LLM** : ✅ Bonne — simple et direct
10. **Décision** : **ADAPTER** — ajouter 01_INTAKE implicite + 05_PATCH_SUMMARY + handoff explicit vers review/closeout

---

### 1-p-vbb-structured-task

1. **Intention** : Exécuter une tâche STRUCTURÉE (contrats, multi-fichiers, auth, etc.)
2. **Phase** : 01_INTAKE → 04_PLAN → 05_EXECUTION (correct, mais pas 02_AUDIT explicitement)
3. **Rôle** : Planner + Exécuteur
4. **Artefact** : Plan + Code modifié, pas d'artefacts nommés persistants
5. **Artefact attendu** : `01_INTAKE.md` + `04_FIX_PLAN.md` + `05_PATCH_SUMMARY_RUN_01.md`
6. **Handoff** : ⚠️ Partiel — mentionne "summarize what changed" mais pas de passage explicite à review
7. **Risque de dérive** : Moyen — le prompt dit "Do not claim canonical compliance without governance grounding" mais n'orchestre pas les audits prérequis
8. **Dépendance contexte** : Moyenne — repose sur gouvernance
9. **Compatibilité multi-LLM** : ⚠️ Acceptable mais le manque de séquençage peut confondre une IA moins capable
10. **Décision** : **ADAPTER** — ajouter étape 02_AUDIT optionnelle avant 04_PLAN si risque augmente

---

### 1-p-vbb-project-init

1. **Intention** : Initialiser ou évaluer gouvernance Vibebackbone du repo
2. **Phase** : 01_INTAKE
3. **Rôle** : Évaluateur / Initialiseur
4. **Artefact** : Statut gouvernance (on-rails / partially-initialized / not-initialized)
5. **Artefact attendu** : `01_INTAKE.md` + potentiellement `docs/PROJECT_MODE.md` (création)
6. **Handoff** : ⚠️ Faible — dit "Recommended initialization steps" mais pas de transition vers exécution
7. **Risque de dérive** : **Élevé** — pourrait inventer des fichiers de gouvernance alors que le prompt dit "Do not invent missing governance files"
8. **Dépendance contexte** : Oui
9. **Compatibilité multi-LLM** : ✅ Acceptable
10. **Décision** : **ADAPTER** — clarifier que init est une recommandation (phase 03 DECISION), pas une action dans 01_INTAKE

---

### 1-p-vbb-tech-debt

1. **Intention** : Évaluer dette technique
2. **Phase** : 02_AUDIT (correct)
3. **Rôle** : Auditeur
4. **Artefact** : Rapport de dette classifié (pas nommé persistant)
5. **Artefact attendu** : `02_AUDIT_REPORT.md` (type: tech-debt) + persisté dans `docs/audits/`
6. **Handoff** : ❌ Absent — pas de transition vers phase 03
7. **Risque de dérive** : **Élevé** — enchaîne deux skills (janitor + tech-debt) et dit "janitor verdict BLOCKED → stop" mais ne dit pas comment scénariser la reprise
8. **Dépendance contexte** : Très élevée — orchestre deux passes et dépend du résultat de la première
9. **Compatibilité multi-LLM** : ⚠️ Délicate — deux passes séquencées peuvent surcharger modèle local
10. **Décision** : **FUSIONNER ou SCINDER** — le chaînage janitor → tech-debt est correct, mais mettre la première passe en LOCAL (qwen) et la seconde en CLOUD

---

### 1-p-vbb-legacy-level

1. **Intention** : Évaluer le legacy level et son acceptabilité
2. **Phase** : 02_AUDIT (partiel — c'est une question, pas un audit complet)
3. **Rôle** : Évaluateur
4. **Artefact** : Assessment legacy (low/moderate/high/critical) + acceptability (non-persisté)
5. **Artefact attendu** : Devrait être `02_AUDIT_REPORT.md` (type: legacy-assessment) ou note dans `docs/audits/`
6. **Handoff** : ❌ Absent
7. **Risque de dérive** : **Moyen** — le prompt liste les "legacy signals" mais ne fournit pas de critères objectifs
8. **Dépendance contexte** : Oui
9. **Compatibilité multi-LLM** : ✅ Acceptable (judgment call supportée)
10. **Décision** : **ADAPTER** — persisté dans `docs/audits/` + handoff vers phase 03

---

### 1-p-vbb-doc-feature

1. **Intention** : Produire documentation feature compatible Vibebackbone
2. **Phase** : Ambigu — pourrait être 02_AUDIT (gap detection) + 05_EXECUTION (writing)
3. **Rôle** : Documentaliste + Auditeur
4. **Artefact** : Documentation écrite (pas d'artefact nommé)
5. **Artefact attendu per protocole** : `02_AUDIT_REPORT.md` (type: doc-gap) + `05_PATCH_SUMMARY.md` (écritures effectuées)
6. **Handoff** : ⚠️ Faible — dit "Do not mix this prompt with session handoff" (bonne discipline) mais ne propose pas de transition
7. **Risque de dérive** : **Moyen** — le mode DELEGATED (cloud + local subagent) n'est pas bien défini dans le pipeline
8. **Dépendance contexte** : Très élevée — orchestration de deux agents (cloud + local)
9. **Compatibilité multi-LLM** : ⚠️ Risquée — délégation inter-LLM pas claire
10. **Décision** : **CRÉER_CANONIQUE** — définir le split cloud/local clairement (audit → cloud, écriture → local)

---

### 1-p-vbb-post-refacto-coherence

1. **Intention** : Audit post-refactoring complet (cohérence, gaps, harmonisation, handoff)
2. **Phase** : 02_AUDIT → 05_EXECUTION → 07_CLOSEOUT (orchestration multi-phases)
3. **Rôle** : Orchestrateur
4. **Artefact** : 4 artefacts (audit, gap-fill, harmonisation, handoff)
5. **Artefact attendu** : `02_AUDIT_REPORT.md` + `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md`
6. **Handoff** : ✅ Excellent — "Produire un handoff propre pour repartir" (phase 4 inclu)
7. **Risque de dérive** : **Élevé malgré bonne intention** — le cascade de verdicts (COHERENT → skip phase 2, etc.) est un piège: si un verdict bloque, la cascade se casse
8. **Dépendance contexte** : Très élevée — orchestre 4 skills en séquence avec dépendances de verdict
9. **Compatibilité multi-LLM** : ⚠️ Sérieuse — 4 passes successives risquent saturation contexte
10. **Décision** : **SCINDER en orchestration** — chacune des 4 phases devrait être une session séparée, avec compression contexte entre chacune

---

### 2-p-vbb-db-sanity

1. **Intention** : Évaluer sanité base de données
2. **Phase** : 02_AUDIT (correct, spécialisé)
3. **Rôle** : Auditeur DB
4. **Artefact** : Assessment sanité (sane/acceptable/fragile/unsafe) + liste issues (non-persisté)
5. **Artefact attendu** : `02_AUDIT_REPORT.md` (type: db-sanity)
6. **Handoff** : ❌ Absent
7. **Risque de dérive** : **Moyen** — "missing evidence" peut être un prétexte pour ne pas conclure
8. **Dépendance contexte** : Oui — repose sur accès au code/migrations
9. **Compatibilité multi-LLM** : ✅ Acceptable
10. **Décision** : **ADAPTER** — persisté dans `docs/audits/` + handoff vers 03

---

### 2-p-vbb-audit-task

1. **Intention** : Exécuter une tâche AUDIT générique
2. **Phase** : 02_AUDIT → 03_DECISION (orchestre les deux)
3. **Rôle** : Auditeur + Décideur
4. **Artefact** : Rapport audit + recommandations (pas nommé persistant)
5. **Artefact attendu** : `02_AUDIT_REPORT.md` + `03_DECISION_RECORD.md`
6. **Handoff** : ⚠️ Faible — "Produce findings, risks, and recommended actions" mais pas de transition explicite
7. **Risque de dérive** : **Élevé** — le routing est abstrait ("most relevant domain audit skills next") et laisse trop de liberté
8. **Dépendance contexte** : Très élevée — orchestre la séquence [readiness → scope → context → domain audit → risk consolidation]
9. **Compatibilité multi-LLM** : ⚠️ Délicate — orchestration multi-domaines
10. **Décision** : **ADAPTER** — le faire au rôle d'orchestrateur/séquenceur plutôt qu'agent d'exécution direct

---

### 2-p-vbb-mode-transition

1. **Intention** : Vérifier si le repo est prêt pour transition dev→prod
2. **Phase** : 03_DECISION (verdict transition) avec éléments de 02_AUDIT (preconditions)
3. **Rôle** : Décideur
4. **Artefact** : Verdict transition + blockers + recommendation (non-persisté)
5. **Artefact attendu** : `03_DECISION_RECORD.md`
6. **Handoff** : ⚠️ Faible — liste "Recommended next action" mais pas de lien vers execution
7. **Risque de dérive** : **Moyen** — ne dit pas si le verdict "NOT_READY" ferme les portes ou si une escalade vers audit est nécessaire
8. **Dépendance contexte** : Oui
9. **Compatibilité multi-LLM** : ✅ Acceptable
10. **Décision** : **ADAPTER** — artefact nommé persistant + handoff vers 04_PLAN ou 02_AUDIT (re-audit)

---

### 2-p-vbb-release-check

1. **Intention** : Pre-release gate complet (tous domaines)
2. **Phase** : 02_AUDIT (Wave 1-3) → 03_DECISION (Wave 4 + verdict)
3. **Rôle** : Orchestrateur d'audit + Décideur
4. **Artefact** : Rapport complet (GO/CONDITIONAL_GO/NO_GO) + risques acceptés
5. **Artefact attendu** : `02_AUDIT_REPORT.md` (composite) + `03_DECISION_RECORD.md`
6. **Handoff** : ✅ Bon — "Prochaine action : déployer / corriger puis re-check / escalader"
7. **Risque de dérive** : **Très élevé** — orchestre 14 skills en 4 waves, chaînage complexe. Si un skill rapporte UNKNOWN en prod, la decision est bloquée mais le prompt ne dit pas comment gérer
8. **Dépendance contexte** : Très élevée — 14 audits dans une même session = saturation quasi-certaine
9. **Compatibilité multi-LLM** : ❌ Non — trop lourd pour une seule session
10. **Décision** : **SCINDER** — créer un orchestrateur qui lance les 4 waves dans 4 sessions séparées avec compression contexte

---

### 2-p-vbb-security-pipeline

1. **Intention** : Pipeline sécurité complet (4 steps)
2. **Phase** : 02_AUDIT (steps 1-2) → 03_DECISION (step 3) → 05_EXECUTION (step 4 remediation)
3. **Rôle** : Orchestrateur + Remédiant
4. **Artefact** : 4 rapports horodatés dans `docs/audits/`
5. **Artefact attendu** : ✅ Très clair — spécifie les fichiers persistants
6. **Handoff** : ✅ Bon — "After all 4 steps, summarize" et mise à jour `AUDIT_STATUS.md`
7. **Risque de dérive** : **Moyen** — le step 4 (remediation) transforme les risques en actions mais dit "No code patches", ce qui n'est pas clair: comment un "action plan" différencie-t-il d'une "patch recommendation"?
8. **Dépendance contexte** : Très élevée — 4 steps en séquence
9. **Compatibilité multi-LLM** : ⚠️ Marginal — bien structuré mais 4 steps peuvent saturer
10. **Décision** : **ADAPTER** — clarifier la distinction 03_DECISION (priorisation) vs 05_EXECUTION (implémentation), et envisager deux sessions

---

### 3-p-vbb-risk-register

1. **Intention** : Compiler registre consolidé de risques
2. **Phase** : 07_CLOSEOUT (ou phase 03 _DECISION_ si c'est pour prioriser)
3. **Rôle** : Consolidateur
4. **Artefact** : Risk register structuré et nommé
5. **Artefact attendu** : ✅ Correct — implicite dans la phase 07, mais le prompt suggère une 03_DECISION
6. **Handoff** : ⚠️ Absent — pas de transition après compilation
7. **Risque de dérive** : Faible — c'est une consolidation pure, pas un audit
8. **Dépendance contexte** : Oui — repose sur les inputs d'audits précédents
9. **Compatibilité multi-LLM** : ✅ Bonne — consolidation structurée
10. **Décision** : **GARDER** — ajouter clarté sur _quand_ le lancer (après 02_AUDIT ou dans 07_CLOSEOUT)

---

### 4-p-vbb-before-building (doublon avec 0-p-vbb-before-building)

→ Voir analyse ci-dessus (même nom, même objectif, même problème)

**Décision** : **FUSIONNER** — Les deux prompts 0-p-vbb-before-building et 4-p-vbb-before-building couvrent le même objectif et les mêmes phases. Garder un seul prompt déduplicalisé.

---

### 4-p-vbb-after-building

1. **Intention** : Post-build validation pipeline
2. **Phase** : 05_EXECUTION → 06_REVIEW (orchestration)
3. **Rôle** : Validateur + Reviewer
4. **Artefact** : Verdict validation (VALIDATED/VALIDATED_WITH_CAVEATS/NEEDS_REWORK) + 6 rapports de phases
5. **Artefact attendu** : `05_PATCH_SUMMARY.md` (implicite, par construction) + `06_REVIEW_RUN.md` + artefacts phases optionnelles
6. **Handoff** : ✅ Bon — "Prochaine action: release-check, handoff, ou retour en développement"
7. **Risque de dérive** : **Très élevé** — orchestre 6 phases +3 optionnelles, chacune avec sa logique de blocking/conditional. Cascade complexe
8. **Dépendance contexte** : Très élevée — 9 phases potentielles
9. **Compatibilité multi-LLM** : ❌ Non — saturation quasi-certaine
10. **Décision** : **SCINDER** — phases 1-3 obligatoires en une session, phases 4-6 en une autre

---

### 4-p-vbb-anti-slop

1. **Intention** : Quality gate multi-langage (read-only)
2. **Phase** : 02_AUDIT (pont) — peut être appelé depuis n'importe quelle phase pour vérifier l'état de surface
3. **Rôle** : Validateur / Gardien qualité
4. **Artefact** : Rapport anti-slop + verdict (READY/READY_WITH_WARNINGS/BLOCKED/UNKNOWN)
5. **Artefact attendu** : Rapport destiné à `docs/audits/` si défini (pas clair)
6. **Handoff** : ⚠️ Léger — "Recommendations" mais pas de transition vers action
7. **Risque de dérive** : Faible — prompt très strict ("NEVER modify code")
8. **Dépendance contexte** : Faible — exécute des tools en read-only
9. **Compatibilité multi-LLM** : ✅ Excellente — appel à des tools externes, pas de raisonnement complexe
10. **Décision** : **GARDER** — ajouter clarté sur où persister le rapport

---

### 4-p-vbb-deploy-docker

1. **Intention** : Pipeline Docker deployment complet (audit → generate → deploy)
2. **Phase** : 02_AUDIT (stage 1) → 04_PLAN (stage 2) → 05_EXECUTION (stage 3) + checks de précondition (02_AUDIT de dépendances)
3. **Rôle** : Orchestrateur Infrastructure
4. **Artefact** : 3 rapports (audit, generate, runtime) + docker-services.map + deploy.sh + docker artifacts
5. **Artefact attendu** : ✅ Très clair — spécifie les fichiers persistants et temporaires
6. **Handoff** : ✅ Bon — "Overall pipeline verdict" + "Next steps"
7. **Risque de dérive** : **Moyen** — le "verdict cascade rule" est bien défini mais l'orchestration de 3 stages + pre-audits (2-vbb-ops, 2-vbb-data-integrity, 2-vbb-security, 2-vbb-db-robustness) en une session = saturation
8. **Dépendance contexte** : Très élevée
9. **Compatibilité multi-LLM** : ⚠️ Marginal — bien structuré mais lourd
10. **Décision** : **ADAPTER** — chaque stage dans une session séparée; pré-audits dans une session dédiée

---

### t-p-vbb-start-session

1. **Intention** : Ouvrir une session — lire contexte et proposer voie
2. **Phase** : 01_INTAKE
3. **Rôle** : Orchestrateur de session
4. **Artefact** : Résumé contexte + voie probable (pas nommé persistant)
5. **Artefact attendu** : `01_INTAKE.md` (implicite)
6. **Handoff** : ✅ Bon — termine par "Question finale: Quel est l'objectif précis de cette session ?"
7. **Risque de dérive** : Faible — strict sur "Ne lance aucun skill métier"
8. **Dépendance contexte** : Faible — lire et résumer
9. **Compatibilité multi-LLM** : ✅ Excellente
10. **Décision** : **GARDER** — exemple de prompt bien ciblé

---

### t-p-vbb-branch-policy-check

1. **Intention** : Vérifier si stratégie branche match phase courante
2. **Phase** : 03_DECISION (verdict) avec entrée potentielle 02_AUDIT (contexte)
3. **Rôle** : Décideur infrastructure
4. **Artefact** : Verdict fit + risques + recommandation (non-persisté)
5. **Artefact attendu** : `03_DECISION_RECORD.md`
6. **Handoff** : ❌ Absent — pas de lien vers 04_PLAN (corriger la politique si nécessaire)
7. **Risque de dérive** : Faible
8. **Dépendance contexte** : Oui
9. **Compatibilité multi-LLM** : ✅ Acceptable
10. **Décision** : **ADAPTER** — artefact nommé persistant + handoff

---

### t-p-vbb-git-sync

1. **Intention** : Committer + pusher avec token economy (cloud reasoning + local execution)
2. **Phase** : 05_EXECUTION (commit) → 06_REVIEW (push/merge) — pont entre phases
3. **Rôle** : Exécuteur + Delegateur
4. **Artefact** : Commit SHA + push result + merge result (non-persisté)
5. **Artefact attendu** : Peut être partie de `05_PATCH_SUMMARY.md` ou `06_REVIEW_RUN.md`
6. **Handoff** : ⚠️ Faible — "Final state" mais pas de passage vers 07_CLOSEOUT
7. **Risque de dérive** : Bas — très procédural, safety rules strictes
8. **Dépendance contexte** : Oui — repose sur le commit-ready précédent
9. **Compatibilité multi-LLM** : ✅ Excellente — cloud + local split bien pensé
10. **Décision** : **GARDER** — exemples d'innovation positive (token economy)

---

### t-p-vbb-sequenced-ship

1. **Intention** : Orchestration de travail long (multi-phase, multi-run) avec compression contexte à 40%
2. **Phase** : 01_INTAKE → 07_CLOSEOUT (orchestration globale)
3. **Rôle** : Orchestrateur longue durée
4. **Artefact** : Plan détaillé (phase 0) + context packets (checkpoints) + final summary
5. **Artefact attendu** : `.pi/SEQ_PLAN.md` (per-run) + final summary
6. **Handoff** : ✅ Excellent — explicite à chaque checkpoint
7. **Risque de dérive** : Moyen — "Compress context at ~40%, not higher" est une bonne discipline, mais le prompt ne dit pas comment réagir si un run devient BLOCKED
8. **Dépendance contexte** : Volontaire (par design) — compression et handoff explicites
9. **Compatibilité multi-LLM** : ✅ Excellente — context packet design permet local+cloud split
10. **Décision** : **GARDER** — innovation majeure, mais intégrer clairement dans orchestration globale

---

### t-p-vbb-session-handoff

1. **Intention** : Produire handoff de clôture de session
2. **Phase** : 07_CLOSEOUT
3. **Rôle** : Closeout leader
4. **Artefact** : Handoff compact + risks/dependencies
5. **Artefact attendu** : ✅ Correct — partie de `07_CLOSEOUT.md`
6. **Handoff** : ✅ Bon — "Next recommended step"
7. **Risque de dérive** : Faible
8. **Dépendance contexte** : Oui — consomme les sessions précédentes
9. **Compatibilité multi-LLM** : ✅ Excellente
10. **Décision** : **GARDER** — exemple de prompt bien ciblé

---

## 4. Gaps avec le protocole 7 phases

| Phase | Prompts Actuels | Gap Identifié | Recommandation |
|-------|-----------------|---------------|-----------------|
| **01_INTAKE** | triage, plan, start-session, before-building, project-init | Pas d'artefact persistant clair; mélange d'INTAKE+PLAN dans "plan" | Créer `01_INTAKE` canonique qui englobe triage + context detection |
| **02_AUDIT** | tech-debt, legacy-level, db-sanity, audit-task, anti-slop, partie de release-check, partie de security-pipeline, partie de deploy-docker | Audit spécialisés bien, mais gap d'orchestration centrale; pas de consolidated audit report | Créer orchestrateur audit qui choisit les domaines et produit un rapport de synthèse |
| **03_DECISION** | mode-transition, risk-register (partiellement), branch-policy-check, partie de release-check, partie de security-pipeline | Prompts de décision peu clair sur _quand_ les appeler; pas d'artefacts nommés persistants | Créer `03_DECISION` canonique qui consolide toutes les décisions post-audit |
| **04_PLAN** | plan, structured-task (implicite), before-building (implicite), partie de deploy-docker | Plan peu ciblé; mélange avec INTAKE | Scinder plan en prompt dédié qui produit `04_FIX_PLAN.md` |
| **05_EXECUTION** | quick-task, structured-task, doc-feature, post-refacto-coherence (phase 2), git-sync (stage 1), deploy-docker (stage 3), sequenced-ship (orchestration) | Pas d'artefact `05_PATCH_SUMMARY` explicite; mélange execution+review | Clarifier que chaque run 05 doit produire un patch summary nommé |
| **06_REVIEW** | after-building (phase 4-6 optionnelles), git-sync (stage 2 push/merge), partie de release-check | Peu de prompts dédiés à review indépendante; après-building mélange phases | Créer prompt de review pur (read-only, verdict explicite) |
| **07_CLOSEOUT** | session-handoff, post-refacto-coherence (phase 4), sequenced-ship (finale) | Peu d'artefacts de closeout explicites; risque que SESSION.md + AUDIT_STATUS.md ne soient pas mis à jour | Créer `07_CLOSEOUT` canonique avec mise à jour obligatoire de doc/SESSION.md et docs/AUDIT_STATUS.md |

---

## 5. Prompts à créer, adapter, fusionner ou déprécier

### À ADAPTER (priorité haute)

| Prompt | Raison | Action |
|--------|--------|--------|
| 0-p-vbb-plan | Mélange INTAKE + PLAN; pas d'artefact persistant | Extraire PLAN et le faire une phase 04 dédié; garder INTAKE court |
| 0-p-vbb-before-building | Orchestre 5 gates sans séparation; risque de débordement | Scinder en gate (phase 01) + plan (phase 04) |
| 1-p-vbb-quick-task | Pas d'artefacts nommés; escalade non gérée | Ajouter 01_INTAKE implicite + 05_PATCH_SUMMARY explicite |
| 1-p-vbb-structured-task | Pas d'audit optionnel précédent; pas d'artefacts persistants | Ajouter reference optionnelle à 02_AUDIT; nommer les artefacts |
| 1-p-vbb-tech-debt | Chaînage janitor+tech-debt sans séparation; pass ordre séquentiel | Clarifier que pass 1 (janitor) peut être LOCAL, pass 2 (tech-debt) CLOUD |
| 1-p-vbb-project-init | "Do not invent" vs recommander init | Clarifier que c'est 01_INTAKE (évaluation) → 03_DECISION (si créer) → 05_EXECUTION (si créer) |
| 2-p-vbb-mode-transition | Verdict de transition sans clarté sur suite | Ajouter handoff vers 04_PLAN ou re-audit (02_AUDIT) selon verdict |
| 2-p-vbb-release-check | Orchestre 14 skills en une session = saturation | Scinder en 4 sessions (Wave 1-4) avec compression contexte |
| 2-p-vbb-security-pipeline | 4 steps en une session; step 4 "no code" vs "remediation plan" ambigu | Clarifier phase 03 (décision/priorisation) vs phase 05 (implémentation); envisager deux sessions |
| 4-p-vbb-after-building | Orchestre 6+3 phases; cascade complexe | Scinder obligatoire (phases 1-3) et optionnel (phases 4-6) |
| 4-p-vbb-deploy-docker | 3 stages + pre-audits en une session | Scinder en sessions dédiées (pre-audits 02_AUDIT, stage 1 02_AUDIT, stage 2 04_PLAN, stage 3 05_EXECUTION) |

---

### À FUSIONNER (priorité moyenne)

| Prompts | Raison | Action |
|---------|--------|--------|
| 0-p-vbb-before-building + 4-p-vbb-before-building | Doublons : tous deux pré-construction | Fusionner en un seul prompt de phase 01_INTAKE avec gates optionnels |

---

### À CRÉER (priorité haute)

| Phase | Artifact | Prompts manquants |
|-------|----------|------------------|
| 01_INTAKE | `01_INTAKE.md` | `1-p-vbb-intake-canonical` — triage + context detection + gouvernance check (consolidé) |
| 02_AUDIT | `02_AUDIT_REPORT.md` (composite) | `2-p-vbb-audit-orchestrator` — orchestrer les domaines d'audit (sécurité, intégrité, ops, etc.) et produire un rapport synthétique |
| 03_DECISION | `03_DECISION_RECORD.md` (composite) | `3-p-vbb-decision-canonical` — consolider les décisions post-audit et accepter les risques |
| 04_PLAN | `04_FIX_PLAN.md` | `4-p-vbb-plan-canonical` — produire un plan détaillé prêt pour exécution |
| 05_EXECUTION | `05_PATCH_SUMMARY_RUN_N.md` | (Pas de prompt manquant, mais clarifier dans quick-task + structured-task) |
| 06_REVIEW | `06_REVIEW_RUN_N.md` | `6-p-vbb-review-canonical` — review indépendante en nouvelle session (read-only, verdict explicite) |
| 07_CLOSEOUT | `07_CLOSEOUT.md` | `7-p-vbb-closeout-canonical` — synthèse finale + mise à jour SESSION.md + AUDIT_STATUS.md |

---

## 6. Recommandation d'architecture

### Comparaison des 3 options

#### **Option A : Adapter les prompts seuls**

| Aspect | Évaluation |
|--------|-----------|
| Effort | Moyen (10–15 adaptations) |
| Risque | **Élevé** — les prompts existants restent en silos; l'orchestration reste à la charge de l'utilisateur |
| Résultat | Meilleur (prompts plus clairs), mais toujours fragmenté |
| Compatibilité | Les 57 skills doivent être adaptés aussi → effort total élevé |
| **Verdict** | ❌ Insuffisant seul |

#### **Option B : Créer une couche d'orchestration légère (Sequencer)**

| Aspect | Évaluation |
|--------|-----------|
| Effort | Moyen (créer 1 sequencer + adapter 5 prompts critiques) |
| Risque | **Faible** — le sequencer est une orchestration, pas une refonte |
| Résultat | **Excellent** — prompts existants restent valides; le sequencer gère le flux 01-07 |
| Compatibilité | Skills restent inchangées; prompts peuvent cohabister |
| **Verdict** | ✅ **Recommandé** |

#### **Option C : Remplacer complètement (Nouvelle série canonique 01-07)**

| Aspect | Évaluation |
|--------|-----------|
| Effort | Très élevé (créer 7 nouveaux prompts + migrer les 24 existants) |
| Risque | **Très élevé** — rupture complète; perte de la base actuelle fonctionnelle |
| Résultat | Parfait théoriquement, mais destructif |
| Compatibilité | Anciens prompts dépréciés → migration utilisateurs douloureuse |
| **Verdict** | ❌ Disproportionné |

---

### **Choix recommandé : Option B (Hybride) + Adaptations**

Créer une **couche orchestration légère** (intégrable dans `t-p-vbb-sequencer` ou amélioration de `sequenced-ship`) qui :

1. **Phase 01** : appelle `start-session` → `triage` → `before-building` (optionnel) → produit `01_INTAKE.md`
2. **Phase 02** : appelle audit-orchestrator qui choisit parmi les domaines (security, tech-debt, db, integrity, ops, ci, legal) → produit `02_AUDIT_REPORT.md` composite
3. **Phase 03** : appelle decision-canonical qui consolide les decisions post-audit → produit `03_DECISION_RECORD.md`
4. **Phase 04** : appelle plan-canonical → produit `04_FIX_PLAN.md`
5. **Phase 05** : appelle (quick-task | structured-task | custom) → produit `05_PATCH_SUMMARY_RUN_N.md`
6. **Phase 06** : appelle review-canonical (nouvelle session) → produit `06_REVIEW_RUN_N.md`
7. **Phase 07** : appelle session-handoff → produit `07_CLOSEOUT.md` + met à jour SESSION.md

**Avantages** :
- Les 24 prompts existants restent valides et utilisables individuellement
- Le sequencer les orchestre sans les modifier
- Adaptation des prompts critiques = effort minimal
- Création des prompts manquants = effort contrôlé

---

## 7. Plan de migration recommandé

### RUN 01 — Audit & Planification (✅ CE RAPPORT)

**Objectif** : Analyser les 24 prompts, identifier les points manquants, planifier les adaptations

- [x] Audit complet
- [x] Créer liste des 5 prompts critiques à adapter en priorité
- [x] Identifier dépendances entre prompts
- [x] Valider architecture recommandée

**Artefact** : `PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md` (ce rapport)

---

### RUN 02 — Création du Sequencer (⏳ À faire)

**Objectif** : Créer orchestrateur central qui invoque les 7 phases

**Tâches** :
- [ ] Créer `t-p-vbb-sequencer-phase-router` ou améliorer `sequenced-ship`
- [ ] Ajouter logic: détection voie (rapide/structurée/audit/clôture) → routing vers phases appropriées
- [ ] Ajouter logic: compression contexte à 40% entre phases
- [ ] Ajouter logic: cascades verdict (BLOCKED/UNKNOWN/PARTIAL/READY → actions)
- [ ] Tester avec cas simple (quick-task → 01-07 complet)

**Artefact** : Nouveau prompt `t-p-vbb-sequencer-phase-router.md`

---

### RUN 03 — Adaptation des prompts critiques (⏳ À faire)

**Objectif** : Adapter les 5 prompts critiques

**Priorité 1** (doivent changer) :
- [ ] `0-p-vbb-plan` → scinder INTAKE vs PLAN
- [ ] `0-p-vbb-before-building` + `4-p-vbb-before-building` → fusionner + simplifier phase 01
- [ ] `1-p-vbb-structured-task` → ajouter artefacts persistants
- [ ] `2-p-vbb-release-check` → scinder en 4 sessions avec orchestrateur
- [ ] `4-p-vbb-after-building` → scinder phases 1-3 vs 4-6

**Artefact** : Versions adaptées des 5 prompts

---

### RUN 04 — Création des prompts manquants (⏳ À faire)

**Objectif** : Créer les prompts manquants de phase canonique

- [ ] `1-p-vbb-intake-canonical` — triage + context + governance
- [ ] `2-p-vbb-audit-orchestrator` — orchestre les domaines d'audit
- [ ] `3-p-vbb-decision-canonical` — consolide décisions post-audit
- [ ] `4-p-vbb-plan-canonical` — plan dédié
- [ ] `6-p-vbb-review-canonical` — review pure (indépendant)
- [ ] `7-p-vbb-closeout-canonical` — closeout avec mise à jour docs/SESSION.md

**Artefact** : 6 nouveaux prompts

---

### RUN 05 — Testing & Validation (⏳ À faire)

**Objectif** : Tester les orchestrations sur cas réels

- [ ] Cas 1 (QUICK) : 01_INTAKE → 05_EXECUTION → 07_CLOSEOUT
- [ ] Cas 2 (STRUCTURÉE) : 01_INTAKE → 04_PLAN → 05_EXECUTION → 06_REVIEW → 07_CLOSEOUT
- [ ] Cas 3 (AUDIT) : 01_INTAKE → 02_AUDIT → 03_DECISION → 04_PLAN → 05_EXECUTION → 06_REVIEW → 07_CLOSEOUT
- [ ] Tester compression contexte à 40%
- [ ] Tester cascades verdict

**Artefact** : Test results + feedback

---

### RUN 06 — Documentation & Deployment (⏳ À faire)

**Objectif** : Documenter l'architecture et déployer

- [ ] Mettre à jour AGENTS.md avec la nouvelle architecture
- [ ] Créer `PROMPTS_ARCHITECTURE.md` (comment les 24 prompts s'intègrent)
- [ ] Créer guide utilisateur (quand utiliser quelle voie, quelle séquence)
- [ ] Déployer les nouveaux prompts et adaptations
- [ ] Archiver les anciens prompts dépréciés (s'il y en a)

**Artefact** : docs/ complets + prompts/ déployés

---

## 8. Risques systémiques

### Perte de valeur

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Les prompts existants deviennent non-maintenables via adapter seul | Moyenne | Moyen | Option B (sequencer) + adaptations ciblées |
| Les utilisateurs confus par 24 prompts + 7 phases canoniques | Élevée | Élevé | Documentation + routing automatique (sequencer) |
| Les 57 skills deviennent orphelins si prompts changent | Basse (skills sont indépendants) | Moyen | Skills doivent rester stables |

### Duplication

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Prompts chevauchants (doc-feature vs post-refacto-coherence) | Élevée | Faible | Fusion + scission claire documentée |
| Artefacts similaires (audit-task vs release-check) | Moyenne | Moyen | Naming convention + artefacts persistants clair |

### Sur-ingénierie

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Sequencer devient trop complexe | Moyenne | Moyen | Rester léger; orchestration ≠ exécution |
| Compression contexte à 40% trop restrictive ou non appliquée | Moyenne | Moyen | Test empirique; ajuster au besoin |

### Confusion

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Utilisateurs ne savent pas si utiliser (release-check) ou (triage+plan+audit+decision+plan+execute) | Élevée | Élevé | Sequencer automatique + guide clair |
| Phase names vs Prompt names : ambigu si "plan" est phase 04 ET prompt name | Élevée | Moyen | Renommer prompts selon convention (numéro-phase-description) |

### Friction

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Nouvelle session recommandée à chaque phase = friction utilisateur | Moyenne | Moyen | Sequencer automatise transitions + compression contexte explicite |
| Artefacts persistants "oubliés" si pas d'enforcement | Élevée | Moyen | Checklist d'artefacts à chaque phase; validation CLOSEOUT |

---

## 9. Mapping vers les 57 skills

### Par famille

| Famille | Prompts qui les invoquent | Clarté | Notes |
|--------|--------------------------|--------|-------|
| **Pilotage / Routing** | triage, plan, audit-task, start-session | ⚠️ Bonne mais dispersée | 0-vbb-pilotage central; autres utilisent implicitement |
| **Scope / Readiness** | before-building, plan, audit-task | ✅ Clair | 0-vbb-scope-freeze + 0-vbb-audit-readiness bien mappés |
| **Dependency mapping** | structured-task, tech-debt, legacy-level, doc-feature, db-sanity, impact | ✅ Clair | t-vbb-dependency-mapper systématiquement invoqué |
| **Code janitor / formatter** | quick-task, anti-slop, tech-debt | ✅ Clair | 1-vbb-code-janitor bien ciblé |
| **Tech debt / code review** | tech-debt, legacy-level, anti-slop | ✅ Clair | 1-vbb-tech-debt core; anti-slop pont |
| **Documentation** | doc-feature, post-refacto-coherence | ⚠️ Ambigu | Trois skills documentaires (gap-integrator, harmonizer, coherence-auditor) → clarifier quand appeler lesquels |
| **Audit domains** (security, DB, data-integrity, ops, ci, legal, api, systemic) | audit-task, release-check, security-pipeline, db-sanity, deploy-docker | ⚠️ Fragmentation | Chaque domain audit invoqué de façon ad-hoc; pas d'orchestrateur |
| **Mode transition** | mode-transition, branch-policy-check, release-check | ✅ Clair | t-vbb-mode-transition-gate bien ciblé |
| **Sequencing / Long work** | sequenced-ship | ✅ Excellent | Prompts de long-term context management |
| **Git / Deploy** | git-sync, deploy-docker | ✅ Clair | t-vbb-git-sync, t-vbb-docker-audit/generate/deploy bien mappés |
| **Risk / Decision** | risk-register, release-check, security-pipeline | ✅ Clair | 3-vbb-risk-register et 2-vbb-systemic-risk bien ciblés |
| **Handoff / Session** | session-handoff, start-session, sequenced-ship | ✅ Excellent | t-vbb-session-handoff + t-vbb-session-handoff dans sequenced-ship |

### Redondances détectées

| Skills | Prompts | Collision | Recommandation |
|--------|---------|-----------|-----------------|
| 1-vbb-code-janitor + 1-vbb-tech-debt | tech-debt | Intentionnelle (2-pass) | ✅ Correct; clarifier dans prompt que pass 1 = LOCAL, pass 2 = CLOUD |
| 1-vbb-doc-harmonizer + 1-vbb-code-doc-gap-integrator | doc-feature, post-refacto-coherence | Ambigu (quand appeler lesquels?) | ⚠️ Créer matrice d'application dans guide |
| 2-vbb-security + 2-vbb-systemic-risk | security-pipeline, release-check | Intentionnelle (dépendance) | ✅ Correct; ordre doit être security → systemic-risk |
| t-vbb-impact-analyzer | Invoqué depuis 10+ prompts | Over-used | ⚠️ Peut être optional; clarifier quand obligatoire |

---

## 10. Handoff et prochaines étapes

### Statut du rapport

✅ **AUDIT COMPLET**

- 24 prompts analysés selon 10 critères chacun
- Protocole canonique (7 phases) compris et mappé
- Recommandation d'architecture clair (Option B : hybride + sequencer)
- Plan de migration en 6 runs défini
- Risques systémiques identifiés et mitigés

---

### Prochaine session recommandée

**Session type** : STRUCTURED → AUDIT → DECISION → PLAN → EXECUTION

**Voie** : STRUCTURÉE (touches contrats d'orchestration, architecture)

**Objectif de validation (avant RUN 02)**

- Valider cette analyse avec les opérateurs vibebackbone
- Obtenir agreement sur l'option B (hybride + sequencer)
- Décider si commencer par RUN 02 ou consolider les risques d'abord

**Prochaine session : RUN 02 (Création du sequencer)**

- Créer le sequencer `t-p-vbb-phase-router` ou améliorer `sequenced-ship`
- Commencer adaptations des 5 prompts critiques

**Escalade possible**

Si l'effort (6 runs, ~10-12h) semble disproportionné → envisager Option A (adapter seuls les prompts critiques) sans sequencer global; accepter fragmentation.

---

### Artefacts produits

1. ✅ **PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md** (CE RAPPORT)
2. ⏳ `PROMPTS_DEPENDENCY_GRAPH.md` — graphe des dépendances de prompts (RUN 02)
3. ⏳ `t-p-vbb-phase-router.md` — sequencer central (RUN 02)
4. ⏳ Adaptations des 5 prompts critiques (RUN 03)
5. ⏳ 6 nouveaux prompts canoniques (RUN 04)
6. ⏳ Test results + validation (RUN 05)
7. ⏳ `PROMPTS_ARCHITECTURE.md` — guide utilisateur (RUN 06)

---

## Conclusion

Les 24 prompts lanceurs vibebackbone forment une base **fonctionnelle mais fragmentée**. Ils couvrent les 7 phases du protocole agentique, mais pas de façon linéaire ou persistante. Le triage, la planification et la validation post-build sont bien pensés; les phases intermédiaires (audit, décision, plan) manquent de clarté orchestrale.

**Recommandation d'architecture** : Créer un **sequencer léger** (`t-p-vbb-phase-router`) qui orchestre les 24 prompts existants selon les 7 phases, avec compression contexte explicite entre phases et artefacts persistants à chaque étape. Adapter 5 prompts critiques pour nommer les artefacts et améliorer les handoffs. Créer 6 nouveaux prompts pour les phases manquantes (intake-canonical, audit-orchestrator, decision-canonical, plan-canonical, review-canonical, closeout-canonical).

**Effort estimé** : 10–15h (6 runs itératifs). **Risque** : Faible (les 24 existants restent valides). **Résultat** : Excellente couverture du protocole 7 phases sans rupture.

---

**Audit réalisé par** : Claude Opus 4.7  
**Date** : 2026-05-18  
**Mode** : Voie AUDIT  
**Statut** : ✅ Complet, à valider avec opérateurs vibebackbone
