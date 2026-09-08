# Word Error Rate Aligner

**Demo/starter · Python standard library only.**

Compute word-level substitution, deletion and insertion counts with a reproducible edit alignment.

All bundled fixtures are synthetic and contain no customer data or secrets.

## Run

Use Python 3.9 or later (validated with Python 3.9.6). No installation or network access is needed. From this project directory:

```sh
python3 main.py
python3 main.py --reference "turn on the light" --hypothesis "turn off light"
python3 -m unittest -v
```

The default CLI executes a deterministic working demo. Invalid input exits with a readable error and nonzero status.

## Behavior

Inputs are reference and hypothesis strings. Unicode casefolding and word tokenization ignore punctuation. WER is errors divided by reference length and can exceed 1. A nonempty hypothesis against an empty reference yields null WER; both empty yields 0. Ties prefer equality, substitution, deletion, then insertion during backtrace.

## Limits and optional provider boundary

Normalization changes the score. This implementation uses O(n × m) time and memory with a 1,000-token limit per transcript. Built-in examples are synthetic; there is no benchmark dataset or claimed product accuracy.

Supply human reference text and externally generated ASR hypotheses. The evaluator compares strings and performs no inference.

## Tests

`test_main.py` checks fixed expected results, edge cases and invalid inputs with `unittest`. These tests validate the local implementation, not real-world speech accuracy or production readiness. Run `python3 verify.py` to repeat this repository’s checks.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
