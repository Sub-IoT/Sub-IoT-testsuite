import pytest
from pytest_bdd import scenario, given, when, then
from d7a.alp.command import Command
from d7a.fs.file_permissions import FilePermissions
from d7a.fs.file_properties import StorageClass
from d7a.system_files.system_files import SystemFiles
from d7a.system_files.system_file_ids import SystemFileIds


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
