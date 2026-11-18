# Security

## What this repository runs

The skill itself (`skills/masry-writing/`) is Markdown only: no hooks, scripts,
MCP servers or network access. Installing it gives an agent writing
instructions, nothing else.

The only code is the eval runner, `skills/masry-writing/evals/run.py`. It runs
only when you start it, uses the Python standard library, and calls your local
`claude` CLI.

## Reporting a vulnerability

If you find something that could harm users (a prompt-injection path in the
skill text, a problem in the eval runner, a leaked secret), please report it
privately through GitHub's
[private vulnerability reporting](https://github.com/Tayel-Ai-Labs/masry-skills/security/advisories/new)
rather than a public issue.

We aim to reply within 7 days and to fix confirmed issues in the next release.

## Supported versions

Only the latest version on `main` is supported.
