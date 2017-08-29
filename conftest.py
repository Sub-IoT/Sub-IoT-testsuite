import pytest

def pytest_addoption(parser):
  parser.addoption("--serial-test-device", help="serial port for Test Device",  default="/dev/ttyACM0")
  parser.addoption("--serial-dut", help="serial port for Device Under Test",  default="/dev/ttyACM1")

@pytest.fixture(scope="session")
def serial_test_device(request):
    return request.config.getoption("--serial-test-device")

@pytest.fixture(scope="session")
def serial_dut(request):
    return request.config.getoption("--serial-dut")