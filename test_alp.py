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
from d7a.alp.operations.break_query import BreakQuery
from d7a.alp.operands.file import Data
from d7a.alp.operands.offset import Offset
from d7a.alp.operands.length import Length
from d7a.alp.operands.query import QueryOperand, QueryType, ArithQueryParams, ArithComparisonType


@scenario("alp.feature", "Using alp to return data using indirect forward")
def test_alp_indirect_forward():
    pass


@scenario("alp.feature", "Using alp to return data using direct forward")
def test_alp_direct_forward():
    pass


@scenario("alp.feature", "Using alp to return data when break query succeeds")
def test_alp_break_query():
    pass


@scenario("alp.feature", "Using alp to not return data when break query fails")
def test_alp_break_query_fail():
    pass


@scenario("alp.feature", "Node performing continuous scan will receive message encoded message larger than 255 bytes")
def test_large_packets():
    pass


@given("a default access class")
def create_default_access_class(context, default_channel_header, default_channel_index):
    context.default_access_profile = create_access_profile(default_channel_header, default_channel_index,
                                                           enable_channel_scan=False)
    context.default_access_profile_scan = create_access_profile(default_channel_header, default_channel_index,
                                                                enable_channel_scan=True)


@given("an access class different from the default one")
def create_different_access_class(context, default_channel_header, default_channel_index):
    context.access_profile = create_access_profile(default_channel_header, default_channel_index + 5,
                                                   enable_channel_scan=False)
    context.access_profile_scan = create_access_profile(default_channel_header, default_channel_index + 5,
                                                        enable_channel_scan=True)


@given("a requester, set to default access class")
def requester_default(test_device, context):
    change_access_profile(test_device,
                          context.default_access_profile_scan,
                          1)
    set_active_access_class(test_device, 0x11)
    sleep(1)  # give some time to switch AP
    return test_device

@given("on the requester, create different access class")
def requester_create_different_access_class(test_device, context):
    change_access_profile(test_device, context.access_profile_scan, 2)
    return test_device


@given("a responder, listening for foreground packets on this access class")
def responder_new(dut, context):
    change_access_profile(dut,
                          context.access_profile_scan,
                          2)
    set_active_access_class(dut, 0x21)
    sleep(1)  # give some time to switch AP
    dut.clear_unsolicited_responses_received()
    return dut


@given("a responder, listening for foreground packets on the default access class")
def responder_default(dut, context):
    change_access_profile(dut,
                          context.default_access_profile_scan,
                          1)
    set_active_access_class(dut, 0x11)
    sleep(1)  # give some time to switch AP
    dut.clear_unsolicited_responses_received()
    return dut


@given("a file on the requester, containing a predefined byte")
def file_write_requester_right(test_device):
    file_header = FileHeader(
        permissions=FilePermissions(
            executable=True,
            encrypted=False,
            user_readable=True,
            user_writable=True,
            user_executable=False,
            guest_readable=True,
            guest_executable=False,
            guest_writable=False
        ),
        properties=FileProperties(act_enabled=False, act_condition=ActionCondition.WRITE,
                                  storage_class=StorageClass.PERMANENT),
        alp_command_file_id=0x0,
        interface_file_id=0x0,
        file_size=1,
        allocated_size=1
    )
    resp = test_device.execute_command(Command.create_with_create_new_file(file_id=0x44, file_header=file_header))
    assert resp, "Create file 0x44 failed"

    resp = test_device.execute_command(Command.create_with_write_file_action(file_id=0x44, data=[0x0A]))
    assert resp, "Write file 0x44 failed"
    return test_device


@given("a file on the requester, not containing a predefined byte")
def file_write_requester_false(test_device):
    file_header = FileHeader(
        permissions=FilePermissions(
            executable=True,
            encrypted=False,
            user_readable=True,
            user_writable=True,
            user_executable=False,
            guest_readable=True,
            guest_executable=False,
            guest_writable=False
        ),
        properties=FileProperties(act_enabled=False, act_condition=ActionCondition.WRITE,
                                  storage_class=StorageClass.PERMANENT),
        alp_command_file_id=0x0,
        interface_file_id=0x0,
        file_size=1,
        allocated_size=1
    )
    resp = test_device.execute_command(Command.create_with_create_new_file(file_id=0x44, file_header=file_header))
    assert resp, "Create file 0x44 failed"

    resp = test_device.execute_command(Command.create_with_write_file_action(file_id=0x44, data=[0x00]))
    assert resp, "Write file 0x44 failed"
    return test_device


@given("an interface configuration using this access class")
def interface_conf(context):
    context.interface_conf = InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=Configuration(
            qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO, retry_mod=RetryMode.RETRY_MODE_NO),
            addressee=Addressee(
                access_class=0x21,
                id_type=IdType.NOID
            )
        )
    )


@given("an interface configuration using this default access class")
def interface_conf_default(context):
    context.interface_conf_def = InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=Configuration(
            qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO, retry_mod=RetryMode.RETRY_MODE_NO),
            addressee=Addressee(
                access_class=0x11,
                id_type=IdType.NOID
            )
        )
    )


@given("a file on the requester, containing this interface configuration")
def file_write_requester(test_device, context):
    file_header = FileHeader(
      permissions=FilePermissions(
          executable=True,
          encrypted=False,
          user_readable=True,
          user_writable=True,
          user_executable=False,
          guest_readable=True,
          guest_executable=False,
          guest_writable=False
      ),
      properties=FileProperties(act_enabled=False, act_condition=ActionCondition.WRITE,
                                storage_class=StorageClass.PERMANENT),
      alp_command_file_id=0x0,
      interface_file_id=0x0,
      file_size=13,
      allocated_size=13
    )
    resp = test_device.execute_command(Command.create_with_create_new_file(file_id=0x45, file_header=file_header))
    assert resp, "Create file 0x45 failed"

    interface_file = InterfaceConfigurationFile(interface_configuration=context.interface_conf)
    resp = test_device.execute_command(Command.create_with_write_file_action(file_id=0x45, data=list(interface_file)))
    assert resp, "Setting interface file failed"
    return test_device


@given("a command, direct forward using this interface configuration")
def direct_forward_command(context):
    context.request = Command.create_with_return_file_data_action(file_id=0x40, data=range(10),
                                                                  interface_type=context.interface_conf.interface_id,
                                                                  interface_configuration=context.interface_conf.interface_configuration)

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


@given("a command, with a break query and a forward using this default interface configuration")
def break_query_command(context):
    context.request = Command()
    context.request.add_action(
        RegularAction(
            operation=BreakQuery(
                operand=QueryOperand(
                  type=QueryType.ARITH_COMP_WITH_VALUE,
                  mask_present=False,
                  params=ArithQueryParams(comp_type=ArithComparisonType.EQUALITY, signed_data_type=False),
                  compare_length=Length(1),
                  compare_value=[0x0A],
                  file_a_offset=Offset(id=0x44, offset=Length(0))
                )
            )
        )
    )
    context.request.add_forward_action(context.interface_conf_def.interface_id, context.interface_conf_def.interface_configuration)
    context.request.add_action(
        RegularAction(
            operation=ReturnFileData(
                operand=Data(
                    data=range(10),
                    offset=Offset(id=0x40)
                )
            )
        )
    )

@given("a command, with FEC encoding longer than 255 bytes")
def long_command(context):
    context.request = Command.create_with_return_file_data_action(
        file_id=0x48,
        data=range(150),
        interface_type=context.interface_conf_def.interface_id,
        interface_configuration=context.interface_conf_def.interface_configuration
    )


@when('the requester starts a session for this command')
def push_unsolicited(test_device, context, loop_count):
    context.responses = []
    for i in range(loop_count):
        context.responses.append(test_device.execute_command(context.request, timeout_seconds=20))
        # we cannot use return value from when step as fixture apparently, so use context object


@then("the requester should not receive a response")
def requester_should_not_receive_a_response(context, loop_count):
    assert len(context.responses) == loop_count
    for i in range(loop_count):
        assert len(context.responses[i]) == 1, "Requester should not have received a response (besides the tag-response)"


@then('the responder should receive an unsolicited response')
def responder_should_receive_packet(dut, loop_count):
    if loop_count == 1:
        wait_for_unsolicited_response(dut)
    else:
        sleep(0.1 * loop_count)

    assert len(dut.get_unsolicited_responses_received()) == loop_count, \
        "DUT should have received 1 unsolicited response from test device"


@then('the responder should not receive an unsolicited response')
def responder_should_not_receive_packet(dut, loop_count):
    sleep(5)

    assert len(dut.get_unsolicited_responses_received()) == 0, \
        "Responder should not have received an unsolicited response"

