#
# Copyright (c) 2017-2019 University of Antwerp, Aloxy NV.
#
# This file is part of Sub-IoT Testsuite
# (see https://github.com/Sub-IoT/Sub-IoT-testsuite).
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
import sys
import pytest

sys.path.append('lib/pyd7a')
args = ["--timeout=200", "--cucumberjson=cucumber.json", "--gherkin-terminal-reporter"]
args.extend(sys.argv[1:])
sys.exit(pytest.main(args=args))
