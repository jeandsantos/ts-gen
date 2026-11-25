# Domain Docs

## Before exploring

This repository uses a single-context layout:

- Read `GLOSSARY.md` at the repository root.
- Read decisions under `docs/adr/` relevant to the area being explored.

If these paths do not exist, proceed silently. The `/domain-modeling` skill creates them lazily when terms or decisions are resolved.

## Use the glossary's vocabulary

Use glossary terms for domain concepts in issue titles, proposals, hypotheses, and test names. When a needed concept is missing, reconsider whether it belongs to the domain or note the gap for `/domain-modeling`.

## Flag ADR conflicts

If a proposal contradicts an existing ADR, identify the decision and explain why it is worth reopening rather than silently overriding it.
