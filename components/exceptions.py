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
class CommonException(Exception):
    """Base class for other exceptions"""

    def __init__(self, data, message):
        self.message = message
        self.data = data

    def __str__(self):
        return f'{self.data} -> {self.message}'


class ComposeInitialization(CommonException):
    """Raised when the init operation is launched before initialization of the docker engine"""
    """Exception raised for no initialization of the docker engine.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="Compose:initialize should be call before calling Compose:up"):
        super().__init__(data=data, message=message)


class UnknownBroker(CommonException):
    """Raised when the broker value is not one of the valid values"""
    """Exception raised for unknown context broker value.

    Attributes:
        data -- context broker name received
        message -- explanation of the error
    """

    def __init__(self, data, message="Unknown context broker name"):
        super().__init__(data=data, message=message)


class Unimplemented(CommonException):
    """Raised when the deployment of a broker name is not implemented"""
    """Exception raised for not implemented deployment brokers.

    Attributes:
        data -- context broker name received
        message -- explanation of the error
    """

    def __init__(self, data, message="Unimplemented deployment for this broker"):
        super().__init__(data=data, message=message)
