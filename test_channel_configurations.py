from time import sleep

import pytest

from pytest_bdd import scenario, given, when, then, parsers

from conftest import change_access_profile
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.dll.access_profile import AccessProfile
from d7a.dll.sub_profile import SubProfile
from d7a.phy.channel_header import ChannelHeader, ChannelBand, ChannelCoding, ChannelClass
from d7a.phy.subband import SubBand
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.system_files.access_profile import AccessProfileFile
from d7a.types.ct import CT
from modem.modem import Modem

# Scenario: Communication using channel 868, normal rate, channel index 0
#     Given a testdevice using an access profile based on these channel setting
#     And a DUT, using an access profile based on these channel setting and listening for foreground packets
#     When the testdevice executes a command forwarded to the D7ASP interface using this access profile
#     Then the responder should receive this command



@scenario('channel_configurations.feature',
          'Communication using 868, normal rate, channel index 0')
def test_channel_configuration():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, normal rate, channel index 270')
def test_channel_configuration_2():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, hi rate, channel index 0')
def test_channel_configuration_3():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, hi rate, channel index 270')
def test_channel_configuration_4():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, lo rate, channel index 0')
def test_channel_configuration_5():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, lo rate, channel index 279')
def test_channel_configuration_6():
  pass

@given(parsers.parse("a channel configuration using {band:Number} band, {rate} rate and channel index {index:Number}",
                     extra_types=dict(Number=int)))
def channel_configuration(band, rate, index):
  if band == 868: channel_band = ChannelBand.BAND_868
  elif band == 433: channel_band = ChannelBand.BAND_433
  elif band == 915: channel_band = ChannelBand.BAND_915
  else: raise Exception("Invalid band")

  if rate == "normal": channel_class=ChannelClass.NORMAL_RATE
  elif rate == "hi": channel_class=ChannelClass.HI_RATE
  elif rate == "lo": channel_class=ChannelClass.LO_RATE
  else: raise Exception("Invalid rate")

  return {
    "channel_header": ChannelHeader(channel_band=channel_band, channel_coding=ChannelCoding.PN9, channel_class=channel_class),
    "channel_index": index
  }


@given("a testdevice using an access profile based on this channel configuration")
def change_access_profile_test_device(test_device, channel_configuration):
  change_access_profile(test_device, channel_configuration['channel_header'], channel_configuration['channel_index'], enable_channel_scan=False)
  sleep(0.2)  # give some time to switch AP


@given("a DUT, using an access profile based on this channel configuration and listening for foreground packets")
def change_access_profile_dut(dut, channel_configuration):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                  channel_coding=ChannelCoding.PN9,
                                  channel_class=ChannelClass.NORMAL_RATE)
  change_access_profile(dut, channel_configuration['channel_header'], channel_configuration['channel_index'], enable_channel_scan=True)
  dut.clear_unsolicited_responses_received()
  sleep(0.2)  # give some time to switch AP


@when("the testdevice executes a command forwarded to the D7ASP interface using this access profile")
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

@then("the responder should receive this command on the expected channel configuration")
def validate_received(dut, channel_configuration):
  while len(dut.get_unsolicited_responses_received()) == 0:  # endless loop, ended by pytest-timeout if needed
    pass

  assert len(dut.get_unsolicited_responses_received()) == 1, \
    "DUT should have received 1 unsolicited response from test device"

  assert dut.get_unsolicited_responses_received()[0].get_d7asp_interface_status().channel_header == channel_configuration['channel_header'], \
     "Received using unexpected channel header"

  assert dut.get_unsolicited_responses_received()[0].get_d7asp_interface_status().channel_index == channel_configuration['channel_index'], \
     "Received using unexpected channel index"
