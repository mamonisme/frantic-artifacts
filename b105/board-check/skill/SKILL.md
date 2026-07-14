---
name: frantic-board-check
description: Fetch the Frantic public board and emit a validated snapshot packet. Pure HTTP, no LLM.
runx:
  category: data
---

# Frantic Board Check

Reads the public Frantic board JSON and emits a validated snapshot with
post counts and the live API host. Used to prove a reproducible runx receipt
over a real public endpoint. No external mutation.
