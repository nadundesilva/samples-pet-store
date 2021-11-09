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

IFS=',' read -r -a dependencies <<< "${WAIT_FOR}"
for dependency in "${dependencies[@]}"
do
   echo "{\"message\": \"Waiting for dependency ${dependency}\"}"
   dockerize -wait "${dependency}" --timeout 1m &> /dev/null
   if [[ "${?}" != "0" ]]; then
      echo "{\"message\": \"Waiting for dependency ${dependency} timed out\"}"
      exit 1
   else
      echo "{\"message\": \"Dependency ${dependency} ready\"}"
   fi
done

set -eo pipefail

uvicorn ${PET_STORE_PACKAGE}.main:app \
   --host 0.0.0.0 \
   --port 8080 \
   --header server:pet-store-server \
   --no-use-colors
