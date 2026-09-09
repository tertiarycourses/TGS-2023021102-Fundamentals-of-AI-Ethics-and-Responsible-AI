# Activity 7 — Threat-Model a Generative AI Assistant

**Course Proposal alignment:** LU2 · LO2 · K4, A2

**Goal:** Apply layered generative AI security, privacy and copyright controls (A2).

**Deliverable:** Threat model, adversarial prompt results and control architecture

**Duration:** 50 minutes

## Files

- `Prompt Pack.pdf` — approved prompts and safe-use reminders.
- `checklist.md` — submission and acceptance checklist.
- `architecture.json` — supplied mock input or working template.
- `adversarial-prompts.txt` — supplied mock input or working template.
- `security-test-results.csv` — supplied mock input or working template.
- `control-architecture.md` — supplied mock input or working template.

## Step-by-step

1. Open architecture.json and draw the users, application, model, vector store, tools and logging trust boundaries.
2. Map applicable OWASP 2025 risks and the assets each risk threatens.
3. Use only the benign attack prompts in adversarial-prompts.txt against a sandbox or tabletop scenario.
4. Record expected safe behaviour, observed behaviour and evidence without entering real secrets.
5. Design controls before, at, after and around the model; apply least privilege to every tool.
6. Add copyright/provenance checks and write a contain-investigate-recover incident runbook.

## Acceptance check

The threat model covers data, model, application and human layers; every high-risk abuse case has multiple controls and evidence.

## Safety and privacy

Use only supplied mock data. Do not enter personal, confidential, assessment or client information into a public AI system.
