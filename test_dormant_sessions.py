import pytest
from time import sleep
from pytest_bdd import scenario, given, when, then
from conftest import change_access_profile, create_access_profile, wait_for_unsolicited_response, \
  set_active_access_class
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.phy.channel_header import ChannelClass
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.system_files.uid import UidFile
from d7a.types.ct import CT



@scenario('dormant_sessions.feature', 'Dormant session succeeds for a requester which does unicast requests')
def test_dormant_unicast():
  pass

@scenario('dormant_sessions.feature', 'Dormant session fails for a requester which does broadcast requests')
def test_dormant_broadcast():
  pass

@scenario('dormant_sessions.feature', 'Dormant session times out as expected and fails when no response')
def test_dormant_timeout_with_response():
  pass

@scenario('dormant_sessions.feature', 'Dormant session times out as expected and succeeds on response')
def test_dormant_timeout_without_response():
  pass

def get_channel_class(channel_class_string):
  if channel_class_string == "lo":
    return ChannelClass.LO_RATE
  elif channel_class_string == "normal":
    return ChannelClass.NORMAL_RATE
  elif channel_class_string == "hi":
    return ChannelClass.HI_RATE
  else:
    assert False

@given("an access profile using <channel_class> which does not scan")
def ap1(channel_class, default_channel_header, default_channel_index):
  channel_header = default_channel_header
  channel_header.channel_class = get_channel_class(channel_class)
  return create_access_profile(channel_header, default_channel_index, enable_channel_scan=False)

@given("an access profile using <channel_class> which does scan continuously")
def ap2(channel_class, default_channel_header, default_channel_index):
  channel_header = default_channel_header
  channel_header.channel_class = get_channel_class(channel_class)
  return create_access_profile(channel_header, default_channel_index, enable_channel_scan=True)


@given("a requester, using the first AP")
def requester(test_device, ap1, ap2):
  change_access_profile(test_device, ap1, specifier=0)
  change_access_profile(test_device, ap2, specifier=1)
  set_active_access_class(test_device, 0x01)
  sleep(0.5)  # give some time to switch AP
  test_device.clear_unsolicited_responses_received()
  return test_device


@given("a requester, which scans continuously")
def requester_scanning(test_device, default_channel_header, default_channel_index):
  change_access_profile(test_device,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=True),
                        specifier=0)
  change_access_profile(test_device,
                        create_access_profile(default_channel_header, default_channel_index, enable_channel_scan=True),
                        specifier=1)
  set_active_access_class(test_device, 0x01)
  sleep(0.2)  # give some time to switch AP
  test_device.clear_unsolicited_responses_received()
  return test_device

@given("a responder, using the second AP")
def responder(dut, ap1, ap2):
  change_access_profile(dut, ap1, specifier=0)
  change_access_profile(dut, ap2, specifier=1)
  set_active_access_class(dut, 0x11)
  sleep(0.5)  # give some time to switch AP
  dut.clear_unsolicited_responses_received()
  return dut

@given("a dormant session registered at the responder for the UID of the requester")
def dormant_session(test_device, responder, context):
  context.timeout_seconds = 10
  interface_config = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_ANY),
    addressee=Addressee(
      access_class=0x01,
      id_type=IdType.UID,
      id=int(test_device.uid, 16)
    ),
    dorm_to=CT.compress(context.timeout_seconds)
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

@when("the requester starts a broadcast session to the responder")
def send_unicast(requester, dut, context):
  interface_config = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
    addressee=Addressee(
      access_class=0x11,
      id_type=IdType.NOID
    ),
  )

  request = Command.create_with_return_file_data_action(
    file_id=0x40,
    data=[0],
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_config
  )

  context.requester_response = requester.execute_command(request, timeout_seconds=10)


@when("waiting for the dormant session to time out")
def waiting_for_dormant_timeout(context, responder):
  assert len(responder.get_unsolicited_responses_received()) == 0
  sleep(context.timeout_seconds * 1.2) # make sure we sleep long enough

@then("the requester's session should complete successfully")
def requester_session_should_complete_successfully(context):
  # the tag response command is the last one
  assert context.requester_response[-1].execution_completed, "Execution not completed"
  assert not context.requester_response[-1].completed_with_error, "Completed with error"


@then('the responder should receive an unsolicited response')
def responder_should_receive_packet(responder):
  wait_for_unsolicited_response(responder)

  for resp in responder.get_unsolicited_responses_received():
    print("resp {}".format(resp))

  assert len(responder.get_unsolicited_responses_received()) >= 1, \
    "DUT should have received 1 unsolicited response from test device"


@then('the requester should receive the dormant session')
def requester_should_receive_dormant_session(requester):
  wait_for_unsolicited_response(requester)

  assert len(requester.get_unsolicited_responses_received()) == 1, \
    "test should have received 1 unsolicited response from DUT"


@then('the requester should not receive the dormant session')
def requester_should_not_receive_dormant_session(requester):
  sleep(15)

  assert len(requester.get_unsolicited_responses_received()) == 0, \
    "requester should have received no dormant session from responder"

@then("the responders's dormant session should complete successfully")
def dormant_session_should_complete(context, responder):
  session_completed = False
  while not session_completed:
    for resp in responder.get_unsolicited_responses_received():
      if resp.tag_id == context.dormant_session_tag_id and resp.execution_completed:
        assert not resp.completed_with_error, "Execution should be completed without error"
        session_completed = True

    sleep(0.1)

@then("the responders's dormant session should not complete successfully")
def dormant_session_should_not_complete(context, responder):
  session_completed = False
  while not session_completed:
    for resp in responder.get_unsolicited_responses_received():
      if resp.tag_id == context.dormant_session_tag_id and resp.execution_completed:
        assert resp.completed_with_error, "Execution should be completed with error"
        session_completed = True

    sleep(0.1)

