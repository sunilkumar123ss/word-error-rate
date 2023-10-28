"""Compute auditable word-error counts and a deterministic edit alignment."""
import argparse
import json
import re

def tokens(text):
    if not isinstance(text, str):
        raise ValueError('Text must be a string')
    return re.findall("\\w+(?:'\\w+)?", text.casefold(), flags=re.UNICODE)

def evaluate(reference, hypothesis):
    (ref, hyp) = (tokens(reference), tokens(hypothesis))
    if len(ref) > 1000 or len(hyp) > 1000:
        raise ValueError('Demo limit: 1000 tokens per transcript')
    (n, m) = (len(ref), len(hyp))
    distance = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        distance[i][0] = i
    for j in range(m + 1):
        distance[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            distance[i][j] = min(distance[i - 1][j] + 1, distance[i][j - 1] + 1, distance[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]))
    (i, j) = (n, m)
    alignment = []
    counts = {'substitutions': 0, 'deletions': 0, 'insertions': 0}
    while i or j:
        if i and j and (ref[i - 1] == hyp[j - 1]) and (distance[i][j] == distance[i - 1][j - 1]):
            alignment.append({'op': 'equal', 'reference': ref[i - 1], 'hypothesis': hyp[j - 1]})
            i -= 1
            j -= 1
        elif i and j and (distance[i][j] == distance[i - 1][j - 1] + 1):
            alignment.append({'op': 'substitute', 'reference': ref[i - 1], 'hypothesis': hyp[j - 1]})
            counts['substitutions'] += 1
            i -= 1
            j -= 1
        elif i and distance[i][j] == distance[i - 1][j] + 1:
            alignment.append({'op': 'delete', 'reference': ref[i - 1], 'hypothesis': None})
            counts['deletions'] += 1
            i -= 1
        else:
            alignment.append({'op': 'insert', 'reference': None, 'hypothesis': hyp[j - 1]})
            counts['insertions'] += 1
            j -= 1
    wer = distance[n][m] / n if n else 0.0 if not m else None
    return {'reference_words': n, 'hypothesis_words': m, **counts, 'errors': distance[n][m], 'wer': wer, 'normalization': 'Unicode casefold; word tokens; punctuation ignored', 'alignment': list(reversed(alignment))}
