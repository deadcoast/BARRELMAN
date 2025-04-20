#!/usr/bin/env python3
import os

from src.lexer import BarrelmanLexer

TESTS_DIR = "./testcases"
def run_tests():
    results = {"pass": 0, "fail": 0}
    for file in os.listdir(TESTS_DIR):
        if not file.endswith(".bman"):
            continue
        path = os.path.join(TESTS_DIR, file)
        with open(path) as f:
            content = f.read()
        try:
            lexer = BarrelmanLexer(content)
            lexer.tokenize()
            if file.startswith("fail_"):
                print(f"[FAIL] {file} - should have errored")
                results["fail"] += 1
            else:
                print(f"[PASS] {file}")
                results["pass"] += 1
        except Exception as e:
            if file.startswith("fail_"):
                print(f"[PASS] {file} (expected failure)")
                results["pass"] += 1
            else:
                print(f"[FAIL] {file} - {e}")
                results["fail"] += 1
    print(f"Passed: {results['pass']} | Failed: {results['fail']}")
    exit(results["fail"])

if __name__ == "__main__":
    run_tests()
    run_tests()
