import argparse
import sys
import pytest
#
# argparser = argparse.ArgumentParser()
# argparser.add_argument("--serial-test-device", help="serial port for Test Device",  default="/dev/ttyACM0")
# argparser.add_argument("--serial-dut", help="serial port for Device Under Test",  default="/dev/ttyACM1")
# argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
# config = argparser.parse_args()

sys.path.append('lib/pyd7a')
pytest.main()