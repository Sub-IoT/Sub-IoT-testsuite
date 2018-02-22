from time import sleep

from pytest_bdd import scenario, given, when, then

from conftest import change_access_profile, create_access_profile, set_active_access_class, \
  wait_for_unsolicited_response
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.phy.channel_header import ChannelClass, ChannelHeader, ChannelBand, ChannelCoding
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.types.ct import CT


@scenario('access_classes.feature',
          'Node performing background scan is accessible')
def test_bg():
  pass


@given("an access profile using <channel_class> channel class <coding> coding with one subband which has a scan automation period of <tsched>")
def access_profile(channel_class, coding, tsched, default_channel_index):
  if channel_class == "lo":
    cl = ChannelClass.LO_RATE
  elif channel_class == "normal":
    cl = ChannelClass.NORMAL_RATE
  elif channel_class == "hi":
    cl = ChannelClass.HI_RATE
  else:
    assert False

  if coding == "PN9":
    cc = ChannelCoding.PN9
  elif coding == "FEC":
    cc = ChannelCoding.FEC_PN9
  else:
    assert False

  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868, channel_coding=cc, channel_class=cl)
  return create_access_profile(channel_header, default_channel_index, enable_channel_scan=True,
                               scan_automation_period=CT.compress(int(tsched)))


@given("a testdevice using this access profile")
def change_access_profile_test_device(test_device, access_profile):
  change_access_profile(test_device, access_profile, 0)
  set_active_access_class(test_device, 0x01)
  sleep(0.2)  # give some time to switch AP



@given("a DUT, using this access profile")
def change_access_profile_dut(dut, access_profile):
  change_access_profile(dut, access_profile, 0)
  set_active_access_class(dut, 0x01)
  dut.clear_unsolicited_responses_received()
  sleep(0.2)  # give some time to switch AP


@when("the testdevice executes a command forwarded to the D7ASP interface using this access class")
def send_command(test_device):
  interface_configuration = Configuration(
      qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO),
      addressee=Addressee(
        access_class=0x01,
        id_type=IdType.NOID,
      )
    )

  command = Command.create_with_return_file_data_action(
    file_id=0x40,
    data=range(10),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_configuration
  )

  test_device.execute_command(command, timeout_seconds=10)

@then("the responder should receive this command")
def validate_received(dut):
  wait_for_unsolicited_response(dut)

  assert len(dut.get_unsolicited_responses_received()) == 1, \
    "DUT should have received 1 unsolicited response from test device"
