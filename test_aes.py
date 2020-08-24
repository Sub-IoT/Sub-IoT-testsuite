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
from pytest_bdd import scenario, given, when, then, parsers
from conftest import change_access_profile, create_access_profile, wait_for_unsolicited_response, \
  set_active_access_class
from random import SystemRandom
from d7a.alp.command import Command
from d7a.alp.regular_action import RegularAction
from d7a.fs.file_header import FileHeader
from d7a.fs.file_permissions import FilePermissions
from d7a.fs.file_properties import FileProperties, ActionCondition, StorageClass
from d7a.sp.configuration import Configuration
from d7a.system_files.interface_configuration import InterfaceConfigurationFile
from d7a.system_files.security_key import SecurityKeyFile
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


@scenario("aes.feature", "Send and receive an unencrypted message")
def test_aes_none():
    pass


@scenario("aes.feature", "Send and receive an encrypted message using aes ctr with same keys")
def test_aes_ctr():
    pass


@scenario("aes.feature", "Send and not receive an encrypted message using aes ctr with different keys")
def test_aes_ctr_fail():
    pass


@scenario("aes.feature", "Send and receive an encrypted message using aes cbc with same keys")
def test_aes_cbc():
    pass


@scenario("aes.feature", "Send and not receive an encrypted message using aes cbc with different keys")
def test_aes_cbc_fail():
    pass


@scenario("aes.feature", "Send and receive an encrypted message using aes ccm with same keys")
def test_aes_ccm():
    pass


@scenario("aes.feature", "Send and not receive an encrypted message using aes ccm with different keys")
def test_aes_ccm_fail():
    pass


@given("a default access class")
def create_default_access_class(context, default_channel_header, default_channel_index):
    context.default_access_profile = create_access_profile(default_channel_header, default_channel_index,
                                                           enable_channel_scan=False)
    context.default_access_profile_scan = create_access_profile(default_channel_header, default_channel_index,
                                                                enable_channel_scan=True)

@given("a requester, set to default access class")
def requester_default(test_device, context):
    change_access_profile(test_device,
                          context.default_access_profile,
                          1)
    change_access_profile(test_device,
                          context.default_access_profile_scan,
                          2)
    set_active_access_class(test_device, 0x11)
    sleep(1)  # give some time to switch AP
    return test_device


@given("a responder, listening for foreground packets on the default access class")
def responder_new(dut, context):
    change_access_profile(dut,
                          context.default_access_profile_scan,
                          2)
    set_active_access_class(dut, 0x21)
    sleep(1)  # give some time to switch AP
    dut.clear_unsolicited_responses_received()
    return dut


@given("a key, randomly generated")
def generate_key(context):
    context.key = SystemRandom().randint(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)


@given("a key, different from the other one")
def generate_different_key(context):
    context.dif_key = context.key
    while context.dif_key == context.key:
        context.dif_key = SystemRandom().randint(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)


@given("the generated key written to the requester")
def write_key_requester(context, test_device):
    command = Command.create_with_write_file_action_system_file(SecurityKeyFile(key=context.key))
    test_device.execute_command(command)


@given("the generated key also written to the responder")
def write_key_responder(context, dut):
    command = Command.create_with_write_file_action_system_file(SecurityKeyFile(key=context.key))
    dut.execute_command(command)


@given("the different key written to the responder")
def write_dif_key_responder(context, dut):
    command = Command.create_with_write_file_action_system_file(SecurityKeyFile(key=context.dif_key))
    dut.execute_command(command)


@given(parsers.parse("an interface configuration using the default scan access class and using {Nls_Method}"))
def interface_conf_default(context, Nls_Method):
    if Nls_Method == "no encryption": Nls_Method = NlsMethod.NONE
    elif Nls_Method == "AES CTR": Nls_Method = NlsMethod.AES_CTR
    elif Nls_Method == "AES CBC": Nls_Method = NlsMethod.AES_CBC_MAC_128
    elif Nls_Method == "AES CCM": Nls_Method = NlsMethod.AES_CCM_128

    context.interface_conf = InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=Configuration(
            qos=QoS(resp_mod=ResponseMode.RESP_MODE_PREFERRED, retry_mod=RetryMode.RETRY_MODE_NO),
            addressee=Addressee(
                access_class=0x21,
                id_type=IdType.NBID,
                nls_method=Nls_Method,
                id=CT.compress(2)
            )
        )
    )


@given("a command, direct forward using this interface configuration")
def direct_forward_command(context):
    context.request = Command.create_with_return_file_data_action(file_id=0x40, data=range(10),
                                                                  interface_type=context.interface_conf.interface_id,
                                                                  interface_configuration=context.interface_conf.interface_configuration)


@when('the requester starts a session for this command')
def push_unsolicited(test_device, context, loop_count):
    context.responses = []
    for i in range(loop_count):
        context.responses.append(test_device.execute_command(context.request, timeout_seconds=20))
        # we cannot use return value from when step as fixture apparently, so use context object


@then('the requester s session should complete successfully')
def check_success(context, loop_count):
    for i in range(loop_count):
        answ = context.responses[i][len(context.responses[i]) - 1]
        assert answ.execution_completed and not answ.completed_with_error, "the session did not complete {} {}".format(answ.execution_completed, answ.completed_with_error)


@then('the requester s session should not complete successfully')
def check_success(context, loop_count):
    for i in range(loop_count):
        answ = context.responses[i][len(context.responses[i]) - 1]
        assert answ.execution_completed and answ.completed_with_error, "the session did complete successfully {} {}".format(answ.execution_completed, answ.completed_with_error)


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

