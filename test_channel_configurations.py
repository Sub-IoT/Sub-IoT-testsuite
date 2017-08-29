from time import sleep

import pytest

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


def change_access_profile(modem, channel_band, channel_class, channel_coding=ChannelCoding.PN9, channel_index=0):
  access_profile = AccessProfile(
    channel_header=ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.NORMAL_RATE),
    sub_profiles=[SubProfile(subband_bitmap=0x01, scan_automation_period=CT(exp=0, mant=0)), SubProfile(), SubProfile(),
                  SubProfile()],
    sub_bands=[SubBand(
      channel_index_start=0,
      channel_index_end=0,
      eirp=10,
      cca=86  # TODO
    )]
  )

  modem.execute_command(Command.create_with_write_file_action_system_file(file=AccessProfileFile(access_profile=access_profile, access_specifier=0)))


def test_868N0(test_device, dut):
    dut.clear_unsolicited_responses_received() # TODO use pytest mechanism to do this for every test

    change_access_profile(dut, ChannelBand.BAND_868, ChannelClass.NORMAL_RATE)
    change_access_profile(test_device, ChannelBand.BAND_868, ChannelClass.NORMAL_RATE)

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

    resp = test_device.execute_command(command, timeout_seconds=10)

    while len(dut.get_unsolicited_responses_received()) == 0: # endless loop, ended by pytest-timeout if needed
      pass

    assert len(dut.get_unsolicited_responses_received()) == 1, "DUT should have received 1 unsolicited response from test device"


def test_868H0(test_device, dut):
  dut.clear_unsolicited_responses_received()  # TODO use pytest mechanism to do this for every test

  change_access_profile(dut, ChannelBand.BAND_868, ChannelClass.HI_RATE)
  change_access_profile(test_device, ChannelBand.BAND_868, ChannelClass.HI_RATE)

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

  resp = test_device.execute_command(command, timeout_seconds=10)

  while len(dut.get_unsolicited_responses_received()) == 0:  # endless loop, ended by pytest-timeout if needed
    pass

  assert len(
    dut.get_unsolicited_responses_received()) == 1, "DUT should have received 1 unsolicited response from test device"