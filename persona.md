# Dataset & Use Case

## Dataset
OpenParlData.ch — a harmonized REST API aggregating parliamentary affairs, persons, votings, and related data from over 74 Swiss national, cantonal, and municipal parliaments.

## User Persona: Swiss Startup Founder
A founder of a Swiss startup or scaleup (e.g. in fintech, healthtech, or cleantech) who is growing fast enough that regulation has started to matter, but does not yet have a dedicated government relations budget or team.

## Problem
Swiss parliamentary data is fragmented across dozens of parliaments published in incompatible formats. A founder who wants to engage with policymakers has no way to systematically identify which politicians are active on topics relevant to their business or let alone understand their commission memberships, declared interests, or cross-parliament activity.

## Why They Need a Pipeline
Political engagement is time-sensitive. Affairs move through parliaments on a regular session schedule. Without a structured, up-to-date data pipeline, a founder either misses relevant legislative developments entirely or spends hours manually researching politicians across cantonal and federal websites.

## How They Use the Processed Data
The pipeline produces a unified politician relevance profile: for a given startup topic (e.g. "Digitalisierung", "Fintech", "Künstliche Intelligenz"), the founder can identify which politicians across all Swiss parliaments have filed related affairs, how recently and how often, which commissions they sit on, and whether they have declared interests aligned with the startup ecosystem. This gives founders a prioritized, evidence-based shortlist of policymakers to contact — without needing a lobbyist.

## Transformation Rationale
The raw API data requires significant enrichment before it is useful to this persona. Affairs must be tagged by startup-relevant topic, politicians must be scored by activity and recency, commission memberships must be joined to signal institutional influence, and declared interests must be cross-referenced to identify allies. None of this structure exists in the raw data — it is produced entirely by the transformation layer.
