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
import os


class Compose:
    def __init__(self):
        self.brokers = {
            "Orion-LD": ["./composes/orionld.yml"],
            "Stellio": [],
            "Scorpio": []
        }

        self.dockerEngine = None
        self.broker = None

    def initialize(self, broker):
        try:
            self.broker = broker
            compose_files = self.brokers[broker]
        except KeyError as e:
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

