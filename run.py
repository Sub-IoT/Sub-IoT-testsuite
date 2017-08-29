import argparse
import sys
import pytest

sys.path.append('lib/pyd7a')
pytest.main(["-v", "--timeout=10"])