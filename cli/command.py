#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2022 FIWARE Foundation, e.V.
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
"""IoTAgent RDF Turtle parser to NGSI-LD

Usage:
  agent.py [--host HOST] [--port PORT]
  agent.py [-H | --help]
  agent.py --version

Options:
  -h, --host HOST     launch the server in the corresponding host
                      [default: 127.0.0.1]
  -p, --port PORT     launch the server in the corresponding port
                      [default: 5000]

  -H, --help          show this help message and exit
  -v, --version       show version and exit

"""

from docopt import docopt
from os.path import basename
from sys import argv
from schema import Schema, And, Or, Use, SchemaError


__version__ = "0.5.0"
__author__ = "fla"


def parse_cli() -> dict:
    version = f'IoTAgent-Turtle version {__version__}'

    args = docopt(__doc__.format(proc=basename(argv[0])), version=version)

    schema = Schema(
        {
            '--help': bool,
            '--port': Or(None, And(Use(int), lambda n: 1 < n < 65535),
                         error='--port N, N should be integer 1 < N < 65535'),
            '--host': Or(None, str, error='--host HOST should be a string'),
            '--version': bool
        }
    )

    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    return args


if __name__ == '__main__':
    print(parse_cli())
