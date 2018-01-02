import argparse
import sys
import pytest

sys.path.append('lib/pyd7a')
args = ["-v", "--timeout=10", "--cucumber-json-expand", "--cucumberjson=cucumber.json", "--gherkin-terminal-reporter"]
args.extend(sys.argv[1:])
pytest.main(args=args)