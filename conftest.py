
import pytest

from d7a.alp.command import Command
from d7a.dll.access_profile import AccessProfile
from d7a.dll.sub_profile import SubProfile
from d7a.phy.channel_header import ChannelHeader, ChannelBand, ChannelCoding, ChannelClass
from d7a.phy.subband import SubBand
from d7a.system_files.access_profile import AccessProfileFile
from d7a.system_files.dll_config import DllConfigFile
from d7a.types.ct import CT
from modem.modem import Modem
from datetime import datetime
from time import sleep


def pytest_addoption(parser):
  parser.addoption("--serial-test-device", dest="serial_test_device", help="serial port for Test Device", default=None)
  parser.addoption("--serial-dut", dest="serial_dut", help="serial port for Device Under Test", default=None)
  parser.addoption("--loop", dest="loop", help="loop count", default=1, type=int)

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
def loop_count(request):
    return request.config.getoption("--loop")

@pytest.fixture(scope="session")
def test_device(serial_test_device):
    modem = Modem(serial_test_device, 115200, None)
    modem.connect()
    return modem

@pytest.fixture(scope="session")
def dut(serial_dut):
    modem = Modem(serial_dut, 115200, None)
    modem.connect()
    return modem

@pytest.fixture(scope="session")
def default_channel_header():
  return ChannelHeader(channel_band=ChannelBand.BAND_868,
                               channel_coding=ChannelCoding.FEC_PN9,
                               channel_class=ChannelClass.LO_RATE)

@pytest.fixture(scope="session")
def default_channel_index():
  return 32

@pytest.fixture
def context():
  class Context(object):
    pass

  return Context()


def create_access_profile(channel_header, channel_index, enable_channel_scan, scan_automation_period=CT.compress(0)):
  # create a simple access profile, assuming only one subprofile and one subband for now. By setting enable_channel_scan we are listening continuously on
  # the channel_index
  if enable_channel_scan:
    subband_bitmap = 0x01
  else:
    subband_bitmap = 0

  return AccessProfile(
    channel_header=channel_header,
    sub_profiles=[SubProfile(subband_bitmap=subband_bitmap, scan_automation_period=scan_automation_period), SubProfile(), SubProfile(),
                  SubProfile()],
    sub_bands=[SubBand(
      channel_index_start=channel_index,
      channel_index_end=channel_index,
      eirp=10,
      cca=86
    )] * 8
  )


def change_access_profile(modem, access_profile, specifier=0):
  resp = modem.execute_command(Command.create_with_write_file_action_system_file(
    file=AccessProfileFile(access_profile=access_profile, access_specifier=specifier)),
    timeout_seconds=30
  )
  assert resp, "Setting Access Profile failed!"

def set_active_access_class(modem, access_class):
  resp = modem.execute_command(Command.create_with_write_file_action_system_file(DllConfigFile(active_access_class=access_class)))
  assert resp, "Setting active access class failed!"

def wait_for_unsolicited_response(modem):
  start_time = datetime.now()
  timeout = False
  while len(modem.get_unsolicited_responses_received()) == 0 and not timeout:
    if (datetime.now() - start_time).total_seconds() >= 30:
      timeout = True
    else:
      sleep(0.05)

  if timeout:
    assert False, "Timed out waiting for unsolicited response"
