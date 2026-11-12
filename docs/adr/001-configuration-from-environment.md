# ADR-001: Configuration from environment variables, validated at startup

## Status
Accepted — 2026-11-11

## Context
The agent needs secrets and parameters that change according to the environment: local
development, Docker, production. Secrets must never be committed to the repository.

## Decision
We load configuration with pydantic-settings. A `.env` file holds local values and is never
committed; a `.env.example` file listing every parameter is committed instead. Configuration
is validated at startup, and the program stops immediately if a value is missing or invalid.

## Consequences
- A configuration error appears at startup, not later in the middle of a request.
- Environment variables take precedence over the `.env` file, so any setting can be
  overridden in production without changing the code.
- `.env.example` must be updated every time a new parameter is added.