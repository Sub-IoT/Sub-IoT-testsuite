from time import sleep

import pytest

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.types.ct import CT
from modem.modem import Modem

def test_push_unsolicited_response(test_device, dut):
    dut.clear_unsolicited_responses_received() # TODO use pytest mechanism to do this for every test

    interface_configuration = Configuration(
        qos=QoS(resp_mod=ResponseMode.RESP_MODE_ANY),
        addressee=Addressee(
            access_class=0x01,
            id_type=IdType.NBID,
            id=CT(exp=0, mant=1)  # we expect one responder
        )
    )

    command = Command.create_with_return_file_data_action(
      file_id=0x40,
      data=range(10),
      interface_type=InterfaceType.D7ASP,
      interface_configuration=interface_configuration
    )

    resp = test_device.execute_command(command, timeout_seconds=10)
    assert len(resp) == 2, "No response from DUT received" # 1 for response from DUT + 1 tagresponse on flush completed

    while len(dut.get_unsolicited_responses_received()) == 0: # endless loop, ended by pytest-timeout if needed
      pass

    assert len(dut.get_unsolicited_responses_received()) == 1, "DUT should have received 1 unsolicited response from test device"