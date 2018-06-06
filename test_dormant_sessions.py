import pytest
from time import sleep
from pytest_bdd import scenario, given, when, then
from conftest import change_access_profile, create_access_profile, wait_for_unsolicited_response, \
  set_active_access_class
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.system_files.uid import UidFile
from d7a.types.ct import CT



@scenario('dormant_sessions.feature', 'Registering a dormant session for a requester which does unicast requests')
def test_dormant_unicast():
  pass


@given("a requester, which does not scan")
def requester(test_device, default_channel_header, default_channel_index):
  change_access_profile(test_device,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=False),
                        specifier=0)
  change_access_profile(test_device,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=True),
                        specifier=1)
  set_active_access_class(test_device, 0x01)
  sleep(0.2)  # give some time to switch AP
  return test_device


@given("a responder, continuously listening for foreground packets")
def responder(dut, default_channel_header, default_channel_index):
  change_access_profile(dut,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=False),
                        specifier=0)
  change_access_profile(dut,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=True),
                        specifier=1)
  set_active_access_class(dut, 0x11)
  sleep(0.2)  # give some time to switch AP
  dut.clear_unsolicited_responses_received()
  return dut

@given("a dormant session registered at the responder for the UID of the requester")
def dormant_session(test_device, responder, context):
  interface_config = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_ANY),
    addressee=Addressee(
      access_class=0x01,
      id_type=IdType.UID,
      id=int(test_device.uid, 16)
    ),
    dorm_to=CT.compress(10000)
  )

  context.dormant_request = Command.create_with_return_file_data_action(
    file_id=0x41,
    data=[0],
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_config,
  )

  context.dormant_session_tag_id = context.dormant_request.tag_id
  responder.execute_command_async(context.dormant_request)


@when("the requester starts a unicast session to the responder")
def send_unicast(requester, dut, context):
  interface_config = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
    addressee=Addressee(
      access_class=0x11,
      id_type=IdType.UID,
      id=int(dut.uid, 16)
    ),
  )

  request = Command.create_with_return_file_data_action(
    file_id=0x40,
    data=[0],
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_config
  )

  context.requester_response = requester.execute_command(request, timeout_seconds=10)

@then("the requester's session should complete successfully")
def requester_session_should_complete_successfully(context):
  # the tag response command is the last one
  assert context.requester_response[-1].execution_completed, "Execution not completed"
  assert not context.requester_response[-1].completed_with_error, "Completed with error"


@then('the responder should receive an unsolicited response')
def responder_should_receive_packet(responder):
  wait_for_unsolicited_response(responder)

  assert len(responder.get_unsolicited_responses_received()) == 1, \
    "DUT should have received 1 unsolicited response from test device"

  responder.clear_unsolicited_responses_received()
  print "clear_unsolicited_responses_received"


@then('the requester should receive the dormant session')
def requester_should_receive_dormant_session(requester):
  wait_for_unsolicited_response(requester)

  assert len(requester.get_unsolicited_responses_received()) == 1, \
    "test should have received 1 unsolicited response from DUT"

@then("the responders's dormant session should complete successfully")
def dormant_session_should_complete(context, responder):
  wait_for_unsolicited_response(responder)

  resp = responder.get_unsolicited_responses_received()
  assert resp[-1].execution_completed, "Execution not completed"
  assert not resp[-1].completed_with_error, "Completed with error"
  assert resp[-1].tag_id == context.dormant_session_tag_id, "Tag ID does not match dormant session tag ID"

