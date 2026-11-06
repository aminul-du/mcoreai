# Memory Trust Engine (MTE)

CIA Integrity gate for AI memory writes. Every write to the trusted store
passes three checks before acceptance:

1. **Provenance** — source is on the trusted-sources list.
2. **Injection** — content does not match prompt-injection / override patterns.
3. **Hash chain** — content hash chains from the previous trusted write.

Failing any check sends the record to quarantine, never to the trusted store.

## Run the 3-step proof

    python3 -m mte prove

Expected: clean memory → PASS, poisoned memory → BLOCK,
FINAL: MTE_BLOCKS_POISONED_MEMORY.

## Write a single memory

    python3 -m mte write <source> "<content>"

Exit: 0 = PASS, 1 = BLOCK.
