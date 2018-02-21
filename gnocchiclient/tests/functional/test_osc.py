# -*- encoding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from gnocchiclient.tests.functional import base


class OpenstackClentPluginTest(base.ClientTestBase):

    def test_osc_client(self):
        result = self.openstack("metric status")
        status = json.loads(result)
        self.assertGreaterEqual(3, len(status))
