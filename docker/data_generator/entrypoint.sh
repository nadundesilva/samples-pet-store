#!/bin/bash
# Copyright (c) 2021, Deep Net. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set +e

echo "{\"message\": \"Waiting for dependency ${PET_STORE_API_TCP_ADDRESS}\"}"
dockerize -wait ${PET_STORE_API_TCP_ADDRESS} --timeout 1m &> /dev/null
if [[ "${?}" != "0" ]]; then
    echo "{\"message\": \"Waiting for dependency ${PET_STORE_API_TCP_ADDRESS} timed out\"}"
    exit 1
else
    echo "{\"message\": \"Dependency ${PET_STORE_API_TCP_ADDRESS} ready\"}"
fi

set -eo pipefail

python -c 'from data_generator.main import generate_data; generate_data();'
