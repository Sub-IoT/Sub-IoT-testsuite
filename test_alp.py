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
import pytest
from time import sleep
from pytest_bdd import scenario, given, when, then
from conftest import change_access_profile, create_access_profile, wait_for_unsolicited_response, \
  set_active_access_class
from d7a.alp.command import Command
from d7a.alp.regular_action import RegularAction
from d7a.fs.file_header import FileHeader
from d7a.fs.file_permissions import FilePermissions
from d7a.fs.file_properties import FileProperties, ActionCondition, StorageClass
from d7a.sp.configuration import Configuration
from d7a.system_files.interface_configuration import InterfaceConfigurationFile
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.sp.qos import QoS, ResponseMode, RetryMode
from d7a.d7anp.addressee import Addressee, IdType, NlsMethod
from d7a.types.ct import CT
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operands.file import Data
from d7a.alp.operands.offset import Offset


@scenario("alp.feature", "Using alp to read data using indirect forward")
def test_alp_indirect_forward():
    pass


@given("an access class different from the default one")
def create_different_access_class(context, default_channel_header, default_channel_index):
    context.access_profile = create_access_profile(default_channel_header, default_channel_index + 5,
                                                   enable_channel_scan=False)
    context.access_profile_scan = create_access_profile(default_channel_header, default_channel_index + 5,
                                                        enable_channel_scan=True)


@given("a requester, set to default access class but with different access class created")
def requester(test_device, default_channel_header, default_channel_index, context):
    change_access_profile(test_device,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=False),
                        1)
    change_access_profile(test_device,
                        context.access_profile,
                        2)
    set_active_access_class(test_device, 0x11)
    sleep(1)  # give some time to switch AP
    return test_device


@given("a responder, listening for foreground packets on this access class")
def responder(dut, context):
    change_access_profile(dut,
                          context.access_profile_scan,
                          2)
    set_active_access_class(dut, 0x21)
    sleep(1)  # give some time to switch AP
    dut.clear_unsolicited_responses_received()
    return dut


@given("an interface configuration using this access class")
def interface_conf(context):
    context.interface_conf = InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=Configuration(
            qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO),
            addressee=Addressee(
                access_class=0x21,
                id_type=IdType.NBID,
                id=CT(1, 1)  # assuming 1 responder here
            )
        )
    )


@given("a file on the requester, containing this interface configuration")
def file_write_requester(requester, context):
    file_header = FileHeader(
      permissions=FilePermissions(
          executeable=True,
          encrypted=False,
          user_readable=True,
          user_writeable=True,
          user_executeable=False,
          guest_readable=True,
          guest_executeable=False,
          guest_writeable=False
      ),
      properties=FileProperties(act_enabled=False, act_condition=ActionCondition.WRITE,
                                storage_class=StorageClass.PERMANENT),
      alp_command_file_id=0x0,
      interface_file_id=0x0,
      file_size=13,
      allocated_size=13
    )
    resp = requester.execute_command(Command.create_with_create_new_file(file_id=0x45, file_header=file_header))
    assert resp, "Create file 0x45 failed"

    interface_file = InterfaceConfigurationFile(interface_configuration=context.interface_conf)
    resp = requester.execute_command(Command.create_with_write_file_action(file_id=0x45, data=list(interface_file)))
    assert resp, "Setting interface file failed"
    return requester


@given("a command, indirect forwarded to this file")
def indirect_forward_to_file(context):
    context.request = Command()
    context.request.add_indirect_forward_action(interface_file_id=0x45, overload=False, overload_configuration=None)
    context.request.add_action(
        RegularAction(
            operation=ReturnFileData(
                operand=Data(
                    offset=Offset(id=0x40),
                    data=range(10)
                )
            )
        )
    )


@when('the requester starts a session for this command')
def push_unsolicited(requester, context, loop_count):
    context.responses = []
    for i in range(loop_count):
        print context.request
        context.responses.append(requester.execute_command(context.request, timeout_seconds=20))
        # we cannot use return value from when step as fixture apparently, so use context object


@then("the requester should not receive a response")
def requester_should_not_receive_a_response(context, loop_count):
    assert len(context.responses) == loop_count
    for i in range(loop_count):
        assert len(context.responses[i]) == 1, "Requester should not have received a response (besides the tag-response)"


@then('the responder should receive an unsolicited response')
def responder_should_receive_packet(responder, loop_count):
    if loop_count == 1:
        wait_for_unsolicited_response(responder)
    else:
        sleep(0.1 * loop_count)

    assert len(responder.get_unsolicited_responses_received()) == loop_count, \
        "DUT should have received 1 unsolicited response from test device"

