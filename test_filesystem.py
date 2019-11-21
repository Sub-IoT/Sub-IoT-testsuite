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
from pytest_bdd import scenario, given, when, then
from d7a.alp.command import Command
from d7a.alp.regular_action import RegularAction
from d7a.fs.file_header import FileHeader
from d7a.fs.file_permissions import FilePermissions
from d7a.fs.file_properties import StorageClass, ActionCondition, FileProperties
from d7a.system_files.system_files import SystemFiles
from d7a.system_files.system_file_ids import SystemFileIds


@scenario('filesystem.feature', 'Creating a user file')
def test_filesystem_create_user_file():
  pass

@when('creating a user file')
def create_userfile(serial_modem, context):
  context.file_header = FileHeader(
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
    alp_command_file_id=0x41,
    interface_file_id=0x42,
    file_size=1,
    allocated_size=1
  )

  serial_modem.execute_command(Command.create_with_create_new_file(file_id=0x40, file_header=context.file_header))

@then('the new file should be accessible')
def user_file_accessible(serial_modem):
  resp = serial_modem.execute_command(Command.create_with_read_file_action(file_id=0x40, length=1))
  assert(len(resp[0].actions) == 1)
  assert(type(resp[0].actions[0]) == RegularAction)
  assert(resp[0].actions[0].operand.offset.id ==0x40)

@then('the new file header should be as expected')
def user_file_header_correct(serial_modem, context):
  resp = serial_modem.execute_command(Command.create_with_read_file_header(file_id=0x40))
  assert(len(resp[0].actions) == 1)
  header = resp[0].actions[0].operand.file_header
  assert (header == context.file_header)

@scenario('filesystem.feature', 'System file is defined, having the correct header and the file data be parsed')
def test_filesystem_systemfiles():
  pass

@given("a serial modem")
def serial_modem(test_device):
  return test_device

@when('reading system file <system_file> header and data')
def read_system_file(serial_modem, system_file, context):
  context.received_system_file = serial_modem.execute_command(
    Command.create_with_read_file_action_system_file(SystemFiles.files[SystemFileIds(int(system_file))]))[0]
  assert (len(context.received_system_file.actions) == 1)
  context.received_system_file_header = serial_modem.execute_command(
    Command.create_with_read_file_header(int(system_file)))[0]
  assert (len(context.received_system_file_header.actions) == 1)

@then("the data should be parseable according to system file <system_file>")
def data_parseable(context, system_file):
  assert(context.received_system_file.actions[0].operation.systemfile_type == SystemFiles.files[SystemFileIds(int(system_file))])

def parse_permissions(perm_str):
  assert(len(perm_str) == 6)
  ur = uw = ux = gr = gw = gx = False
  if perm_str[0] == 'r': ur = True
  if perm_str[1] == 'w': uw = True
  if perm_str[2] == 'x': ux = True
  if perm_str[3] == 'r': gr = True
  if perm_str[4] == 'w': gr = True
  if perm_str[5] == 'x': gx = True
  return FilePermissions(encrypted=False, executeable=False, user_readable=ur,
                         user_writeable=uw, user_executeable=ux,
                         guest_readable=gr, guest_writeable=gw,
                         guest_executeable=gx)


@then("the file permissions of <system_file> should equal <permissions>")
def check_perm(context, system_file, permissions):
  perm = parse_permissions(permissions)
  header = context.received_system_file_header.actions[0].operand.file_header
  assert(header.permissions == perm)

@then("the properties of <system_file> should be as expected")
def check_prop(context, system_file):
  assert (context.received_system_file_header.actions[0].operand.file_id == int(system_file))
  header = context.received_system_file_header.actions[0].operand.file_header
  file_size = SystemFiles.files[SystemFileIds(int(system_file))].length
  assert(header.file_size == file_size)
  assert(header.allocated_size == file_size)
  assert(header.alp_command_file_id == 0xFF)
  assert (header.interface_file_id == 0xFF)
  assert(header.properties.act_enabled == False)
  assert(header.properties.storage_class == StorageClass.PERMANENT)

@then("there should be no reboots")
def check_reboots(dut, test_device):
  assert len(dut.get_rebooted_received()) == 0, "dut device got rebooted"
  assert len(test_device.get_rebooted_received()) == 0, "test device got rebooted"
