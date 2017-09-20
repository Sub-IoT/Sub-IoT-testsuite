import pytest
from time import sleep
from pytest_bdd import scenario, given, when, then
from conftest import change_access_profile, create_access_profile
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.system_files.uid import UidFile
from d7a.types.ct import CT


@scenario('qos.feature', 'Using QoS with response mode No')
def test_qos_response_mode_no():
  pass


@scenario('qos.feature', 'Using QoS with response mode Any without response data')
def test_qos_response_mode_Any_without_response():
  pass

@scenario('qos.feature', 'Using QoS with response mode Any with response data')
def test_qos_response_mode_Any_with_response():
  pass


@given("a requester")
def requester(test_device, default_channel_header, default_channel_index):
  change_access_profile(test_device,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=False))
  sleep(0.2)  # give some time to switch AP
  return test_device


@given("a responder, listening for foreground packets")
def responder(dut, default_channel_header, default_channel_index):
  change_access_profile(dut,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=True))
  sleep(0.2)  # give some time to switch AP
  dut.clear_unsolicited_responses_received()
  return dut


@given("an interface configuration with QoS response mode is no")
def interface_config_no(context):
  context.interface_config = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO),
    addressee=Addressee(
      access_class=0x01,
      id_type=IdType.NBID,
      id=CT(1, 1) # assuming 1 responder here
    )
  )

@given("an interface configuration with QoS response mode is any")
def interface_config_any(context):
  context.interface_config = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_ANY),
    addressee=Addressee(
      access_class=0x01,
      id_type=IdType.NBID,
      id=CT(1, 1)  # assuming 1 responder here
    )
  )


@given("a command, forwarded to this interface, which does not require response data")
def command_without_resp(context):
  context.request = Command.create_with_return_file_data_action(
    file_id=0x40,
    data=range(10),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=context.interface_config
  )


@given("a command, forwarded to this interface, which does require response data")
def command_with_resp(context):
  context.request = Command.create_with_read_file_action_system_file(
    file=UidFile(),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=context.interface_config
  )


@when('the requester starts a session for this command')
def push_unsolicited(requester, context):
  print context.request
  context.response = requester.execute_command(context.request, timeout_seconds=10)
  # we cannot use return value from when step as fixture apparently, so use context object


@then("the requester should not receive a response")
def requester_should_not_receive_a_response(context):
  assert len(context.response) == 1, "Requester should not have received a response (besides the tag-response)"


@then("the requester should receive a response")
def requester_should_receive_a_response(context):
  assert len(context.response) == 2, "Requester should have received a response (besides the tag-response)"

@then("the requester's session should complete successfully")
def requester_session_should_complete_successfully(context):
  # the tag response command is the last one
  assert context.response[len(context.response) - 1].execution_completed, "Execution not completed"
  assert not context.response[len(context.response) - 1].completed_with_error, "Completed with error"


@then('the responder should receive an unsolicited response')
def responder_should_receive_packet(responder):
  while len(responder.get_unsolicited_responses_received()) == 0:  # endless loop, ended by pytest-timeout if needed
    pass

  assert len(responder.get_unsolicited_responses_received()) == 1, \
    "DUT should have received 1 unsolicited response from test device"
