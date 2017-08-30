import pytest

from modem.modem import Modem


def pytest_addoption(parser):
  parser.addoption("--serial-test-device", dest="serial_test_device", help="serial port for Test Device", default=None)
  parser.addoption("--serial-dut", dest="serial_dut", help="serial port for Device Under Test", default=None)

@pytest.fixture(scope="session")
def serial_test_device(request):
    dev = request.config.getoption("--serial-test-device")
    if dev is None:
      raise Exception("A serial port for the test device is required")

    return dev

@pytest.fixture(scope="session")
def serial_dut(request):
    dev = request.config.getoption("--serial-dut")
    if dev is None:
      raise Exception("A serial port for the DUT is required")

    return dev

@pytest.fixture(scope="session")
def test_device(serial_test_device):
    return Modem(serial_test_device, 115200, None)

@pytest.fixture(scope="session")
def dut(serial_dut):
    return Modem(serial_dut, 115200, None)
