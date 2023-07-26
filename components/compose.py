#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2023 FIWARE Foundation, e.V.
#
# This file is part of IoTAgent-SDMX (RDF Turtle)
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##
from python_on_whales import DockerClient
from components.exceptions import ComposeInitialization, UnknownBroker, Unimplemented
from utils.file_utils import get_container_names_from_compose_file


class Compose:
    def __init__(self):
        self.brokers = {
            "Orion-LD": ["./composes/orionld.yml"],
            "Stellio": ["./composes/stellio.yml"],
            "Scorpio": ["./composes/scorpio.yml"]
        }

        self.container_names = {
            "Orion-LD": get_container_names_from_compose_file(self.brokers["Orion-LD"][0]),
            "Stellio": get_container_names_from_compose_file(self.brokers["Stellio"][0]),
            "Scorpio": get_container_names_from_compose_file(self.brokers["Scorpio"][0])
        }

        self.dockerEngine = None
        self.broker = None
        self.containers = list()

    def initialize(self, broker):
        try:
            self.broker = broker
            compose_files = self.brokers[broker]
        except KeyError:
            # The broker value send to the initialize process is not included in the valid values
            raise UnknownBroker(data=broker,
                                message=f'Unknown Context Broker name. Valid values: {self.brokers.keys()}')

        # At the moment Scorpio and Stellio are not implemented, therefore we raise an exception Unimplemented
        if len(compose_files) == 0:
            raise Unimplemented(data=broker)

        self.dockerEngine = DockerClient(compose_files=compose_files,
                                         compose_env_file="./composes/.env")

    def up(self):
        if self.dockerEngine is None:
            # Error, we need to call before the initialize operation to keep the broker and create the dockerEngine
            raise ComposeInitialization(data='')
        else:
            self.dockerEngine.compose.build()
            self.dockerEngine.compose.up(detach="True")

    def down(self):
        if self.dockerEngine is None:
            # Error, we need to call before the initialize operation to keep the broker and create the dockerEngine
            raise ComposeInitialization(data='')
        else:
            self.dockerEngine.compose.down(volumes="True")

    def check_health_status(self):
        """
        When a container has a HealthCheck specified, it has a health status in addition to its normal status.
        A Docker container can have three health statuses:
            - starting: This takes up to 30 seconds to run, and represents the process of the container booting up
            - healthy: The container will continue to run its Health Check at every specified interval
            - unhealthy: After a certain number of consecutive failures the container's status will be unhealthy

        :return:
        """
        if self.dockerEngine is None:
            # Error, we need to call before the initialize operation to keep the broker and create the dockerEngine
            raise ComposeInitialization(data='')
        else:
            status = self.dockerEngine.compose.ps()
            self.containers = [x.name for x in status if x.name in self.container_names[self.broker]]

            status = self.dockerEngine.container.inspect(self.containers)
            status = [{"name": x.name, "health": x.state.health.status, "status": x.state.status} for x in status]

            health_status = [x['health'] for x in status]

            if True in [ele == "unhealthy" for ele in health_status]:
                res = "unhealthy"
            elif True in [ele == "starting" for ele in health_status]:
                res = "starting"
            else:
                res = "healthy"

            response = {
                "status": res,
                "containers": status
            }

            return response
