#
# Copyright (c) 2017-2019 University of Antwerp, Aloxy NV.
#
# This file is part of Sub-IoT Testsuite
# (see https://github.com/Sub-IoT/Sub-IoT-testsuite).
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
from conftest import change_access_profile, create_access_profile, set_active_access_class

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.phy.channel_header import ChannelClass, ChannelHeader, ChannelBand, ChannelCoding
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.system_files.uid import UidFile
from d7a.types.ct import CT


@scenario('access_classes.feature',
          'Node performing background scan is accessible')
def test_bg():
  pass

@scenario('access_classes.feature',
          'Node performing background scan is accessible, using UID')
def test_bg_uid():
  pass

@scenario('access_classes.feature',
          'Node performing background scan is not accessible, when using wrong UID')
def test_bg_wrong_uid():
  pass

@given(parsers.parse("an access profile using {channel_class} channel class {coding} coding with one subband which has a scan automation period of {tsched}"), target_fixture="access_profile")
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
  sleep(2)  # give some time to switch AP



@given("a DUT, using this access profile")
def change_access_profile_dut(dut, access_profile):
  change_access_profile(dut, access_profile, 0)
  set_active_access_class(dut, 0x01)
  dut.clear_unsolicited_responses_received()
  sleep(2)  # give some time to switch AP


@when("the testdevice executes a query (in a loop), forwarded to the D7ASP interface using this access class")
def send_command(test_device, context, loop_count):
  interface_configuration = Configuration(
      qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
      addressee=Addressee(
        access_class=0x01,
        id_type=IdType.NBID,
        id=CT.compress(2)
      )
    )

  command = Command.create_with_read_file_action_system_file(
    file=UidFile(),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_configuration
  )

  context.succeeded = 0
  for i in range(loop_count):
    responses = test_device.execute_command(command, timeout_seconds=10)
    sleep(1)
    for resp in responses:
      if resp.execution_completed and not resp.completed_with_error:
          context.succeeded = context.succeeded + 1


@when("the testdevice executes a query (in a loop), forwarded to the D7ASP interface using this access class for a specific UID")
def send_command_uid(test_device, context, loop_count, dut):
  interface_configuration = Configuration(
      qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
      addressee=Addressee(
        access_class=0x01,
        id_type=IdType.UID,
        id=int(dut.uid, 16)
      )
    )

  command = Command.create_with_read_file_action_system_file(
    file=UidFile(),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_configuration
  )

  context.succeeded = 0
  for i in range(loop_count):
    responses = test_device.execute_command(command, timeout_seconds=10)
    sleep(2)
    for resp in responses:
      if resp.execution_completed and not resp.completed_with_error:
          context.succeeded = context.succeeded + 1


@when("the testdevice executes a query (in a loop), forwarded to the D7ASP interface using this access class for a specific (wrong) UID")
def send_command_uid(test_device, context, loop_count, dut):
  interface_configuration = Configuration(
      qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
      addressee=Addressee(
        access_class=0x01,
        id_type=IdType.UID,
        id=123 # wrong!
      )
    )

  command = Command.create_with_read_file_action_system_file(
    file=UidFile(),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_configuration
  )

  context.succeeded = 0
  for i in range(loop_count):
    responses = test_device.execute_command(command, timeout_seconds=10)
    sleep(1)
    for resp in responses:
      if resp.execution_completed and not resp.completed_with_error:
          context.succeeded = context.succeeded + 1


@then("the requester should receive the responses")
def validate_received(context, loop_count):
  assert context.succeeded == loop_count, \
    "the requester should received the responses"


@then("the requester should not receive the responses")
def validate_received(context, loop_count):
  assert context.succeeded == 0, \
    "the requester should not have received the responses"
