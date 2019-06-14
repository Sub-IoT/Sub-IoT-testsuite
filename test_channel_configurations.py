#
# Copyright (c) 2017-2019 University of Antwerp, Aloxy NV.
#
# This file is part of OSS-7 Testsuite
# (see https://github.com/MOSAIC-LoPoW/oss7-testsuite).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from time import sleep

from pytest_bdd import scenario, given, when, then, parsers

from conftest import change_access_profile, create_access_profile, wait_for_unsolicited_response, \
  set_active_access_class
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.phy.channel_header import ChannelHeader, ChannelBand, ChannelCoding, ChannelClass
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS


@scenario('channel_configurations.feature',
          'Communication using 868, normal rate class, channel index 0')
def test_channel_configuration():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, normal rate class, channel index 270')
def test_channel_configuration_2():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, hi rate class, channel index 0')
def test_channel_configuration_3():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, hi rate class, channel index 270')
def test_channel_configuration_4():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, lo rate class, channel index 0')
def test_channel_configuration_5():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, lo rate class, channel index 279')
def test_channel_configuration_6():
  pass


@scenario('channel_configurations.feature',
          'Communication using 433, normal rate class, channel index 0')
def test_channel_configuration_7():
  pass


@scenario('channel_configurations.feature',
          'Communication using 915, normal rate class, channel index 0')
def test_channel_configuration_8():
  pass


@scenario('channel_configurations.feature',
          'Communication using 868, lora class, channel index 0')
def test_channel_configuration_9():
  pass

@given(parsers.parse("a channel configuration using {band:Number} band, {channel_class} class and channel index {index:Number}",
                     extra_types=dict(Number=int)))
def channel_configuration(band, channel_class, index):
  if band == 868: channel_band = ChannelBand.BAND_868
  elif band == 433: channel_band = ChannelBand.BAND_433
  elif band == 915: channel_band = ChannelBand.BAND_915
  else: raise Exception("Invalid band")

  if channel_class == "normal rate": channel_class = ChannelClass.NORMAL_RATE
  elif channel_class == "hi rate": channel_class = ChannelClass.HI_RATE
  elif channel_class == "lo rate": channel_class = ChannelClass.LO_RATE
  elif channel_class == "lora": channel_class = ChannelClass.LORA
  else: raise Exception("Invalid rate")

  return {
    "channel_header": ChannelHeader(channel_band=channel_band, channel_coding=ChannelCoding.PN9, channel_class=channel_class),
    "channel_index": index
  }


@given("a testdevice using an access profile based on this channel configuration")
def change_access_profile_test_device(test_device, channel_configuration):
  change_access_profile(test_device,
                        create_access_profile(channel_configuration['channel_header'], channel_configuration['channel_index'], enable_channel_scan=False))
  set_active_access_class(test_device, 0x01)
  sleep(2)  # give some time to switch AP


@given("a DUT, using an access profile based on this channel configuration and listening for foreground packets")
def change_access_profile_dut(dut, channel_configuration):
  change_access_profile(dut,
                        create_access_profile(channel_configuration['channel_header'], channel_configuration['channel_index'], enable_channel_scan=True))
  set_active_access_class(dut, 0x01)
  dut.clear_unsolicited_responses_received()
  sleep(2)  # give some time to switch AP


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
  wait_for_unsolicited_response(dut)

  assert len(dut.get_unsolicited_responses_received()) == 1, \
    "DUT should have received 1 unsolicited response from test device"

  assert dut.get_unsolicited_responses_received()[0].get_d7asp_interface_status().channel_id.channel_header == channel_configuration['channel_header'], \
     "Received using unexpected channel header"

  assert dut.get_unsolicited_responses_received()[0].get_d7asp_interface_status().channel_id.channel_index == channel_configuration['channel_index'], \
     "Received using unexpected channel index"
