"""Compute auditable word-error counts and a deterministic edit alignment."""
import argparse
import json
import re

def tokens(text):
    if not isinstance(text, str):
        raise ValueError('Text must be a string')
    return re.findall("\\w+(?:'\\w+)?", text.casefold(), flags=re.UNICODE)
