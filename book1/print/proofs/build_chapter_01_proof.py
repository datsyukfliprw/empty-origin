#!/usr/bin/env python3
"""Build the Chapter 1 proof from the same production layout as the full book."""
from pathlib import Path
import subprocess
import sys

if __name__ == '__main__':
    production = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(production/'build_print_interior.py')], check=True)
    subprocess.run([sys.executable, str(production/'validate_print_interior.py')], check=True)
    print(production/'proofs/EMPTY_ORIGIN_CHAPTER_01_LAYOUT_PROOF.pdf')
