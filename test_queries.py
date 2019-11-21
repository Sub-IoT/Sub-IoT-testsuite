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
from time import sleep

import struct

import pytest
from pytest_bdd import scenario, given, when, then

from conftest import change_access_profile, create_access_profile, set_active_access_class
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.file import DataRequest
from d7a.alp.operands.length import Length
from d7a.alp.operands.offset import Offset
from d7a.alp.operands.query import QueryOperand, QueryType, ArithQueryParams, ArithComparisonType
from d7a.alp.operations.break_query import BreakQuery
from d7a.alp.operations.requests import ReadFileData
from d7a.alp.regular_action import RegularAction
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.types.ct import CT


@scenario('queries.feature',
          'When predicate of Break Query action fails all subsequent actions are dropped')
def test_break_query_fails():
  pass


@given("a command containing a Break Query action, which results in a fail, and a Read action")
def query_cmd_fail(context):
  cmd = Command()
  # we assume comparing the UID file to 0 results in a fail
  cmd.add_action(
    RegularAction(
      operation=BreakQuery(
        operand=QueryOperand(
          type=QueryType.ARITH_COMP_WITH_VALUE,
          mask_present=False,
          params=ArithQueryParams(comp_type=ArithComparisonType.EQUALITY, signed_data_type=False),
          compare_length=Length(8),
          compare_value=[0, 0, 0, 0, 0, 0, 0, 0],
          file_a_offset=Offset(id=0, offset=Length(0))
        )
      )
    )
  )
  cmd.add_action(
    RegularAction(
      operation=ReadFileData(
        operand=DataRequest(
          offset=Offset(id=0, offset=Length(0)),
          length=8
        )
      )
    )
  )

  context.query_cmd = cmd


@when("the testdevice executes the command")
def send_command(test_device, context):
  context.response = test_device.execute_command(context.query_cmd, timeout_seconds=10)


@then("the command executes successfully")
def executes_successfully(context):
  assert len(context.response) == 1, "expected one response"
  assert context.response[0].execution_completed, "execution should be completed"
  assert not context.response[0].completed_with_error, "the command should execute without error"

@then("the Read action does not return a result")
def does_not_return_result(context):
  assert len(context.response) == 1, "expected one response"
  assert len(context.response[0].actions) == 0, "expected no return file action"


@scenario('queries.feature',
          'When predicate of Break Query action succeeds all subsequent actions are executed')
def test_break_query_succeeds():
  pass

@given("a command containing a Break Query action, which results in a success, and a Read action")
def query_cmd_success(test_device, context):
  cmd = Command()

  # comparing the UID file to the UID results in a success
  cmd.add_action(
    RegularAction(
      operation=BreakQuery(
        operand=QueryOperand(
          type=QueryType.ARITH_COMP_WITH_VALUE,
          mask_present=False,
          params=ArithQueryParams(comp_type=ArithComparisonType.EQUALITY, signed_data_type=False),
          compare_length=Length(8),
          compare_value=[ord(b) for b in struct.pack(">Q", int(test_device.uid, 16))],
          file_a_offset=Offset(id=0, offset=Length(0))
        )
      )
    )
  )
  cmd.add_action(
    RegularAction(
      operation=ReadFileData(
        operand=DataRequest(
          offset=Offset(id=0, offset=Length(0)),
          length=8
        )
      )
    )
  )

  context.query_cmd = cmd

@then("the Read action does return a result")
def does_return_result(context):
  assert len(context.response) == 1, "expected one response"
  assert len(context.response[0].actions) == 1, "expected a return file action"


def get_arithm_comp_to_uid_cmd(value, comp_type):
  # we compare the UID file to value using the comp_type comparator
  cmd = Command()

  cmd.add_action(
    RegularAction(
      operation=BreakQuery(
        operand=QueryOperand(
          type=QueryType.ARITH_COMP_WITH_VALUE,
          mask_present=False,
          params=ArithQueryParams(comp_type=comp_type, signed_data_type=False),
          compare_length=Length(8),
          compare_value=[ord(b) for b in struct.pack(">Q", value)],
          file_a_offset=Offset(id=0, offset=Length(0))
        )
      )
    )
  )
  cmd.add_action(
    RegularAction(
      operation=ReadFileData(
        operand=DataRequest(
          offset=Offset(id=0, offset=Length(0)),
          length=8
        )
      )
    )
  )

  return cmd


@scenario('queries.feature',
          'Validate correct execution of queries with arithmetic comparison',
          example_converters=dict(comp_type=str, value_comparison=str, result_count=str))
def test_comp_generic(comp_type, value_comparison):
  pass


@given("a command containing a query with a <comp_type> comparison comparing a known value with a value which is <value_comparison>, and a Read action")
def query_cmd_generic(context, test_device, comp_type, value_comparison):
  # we compare the UID file to UID, or UID - 1 or UID + 1, depending on value_comparisor
  if comp_type == ">":
    c = ArithComparisonType.GREATER_THAN
  elif comp_type == ">=":
    c = ArithComparisonType.GREATER_THAN_OR_EQUAL_TO
  elif comp_type == "<":
    c = ArithComparisonType.LESS_THAN
  elif comp_type == "<=":
    c = ArithComparisonType.LESS_THAN_OR_EQUAL_TO
  elif comp_type == "==":
    c = ArithComparisonType.EQUALITY
  elif comp_type == "!=":
    c = ArithComparisonType.INEQUALITY
  else:
    assert False

  if value_comparison == "bigger":
    v = 1
  elif value_comparison == "equal":
    v = 0
  elif value_comparison == "smaller":
    v = -1
  else:
    assert False

  context.query_cmd = get_arithm_comp_to_uid_cmd(int(test_device.uid, 16) + v, c)

@then("the Read action does return <result_count> results")
def return_result(context, result_count):
  assert len(context.response) == 1, "expected one response"
  assert len(context.response[0].actions) == int(result_count), "expected {} return file action".format(result_count)

@then("there should be no reboots")
def check_reboots(dut, test_device):
  assert len(dut.get_rebooted_received()) == 0, "dut device got rebooted"
  assert len(test_device.get_rebooted_received()) == 0, "test device got rebooted"