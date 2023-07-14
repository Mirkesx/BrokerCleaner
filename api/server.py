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

from fastapi import FastAPI, Request, Response, status
from uvicorn import run
from datetime import datetime
from secure import Server, ContentSecurityPolicy, StrictTransportSecurity, \
    ReferrerPolicy, PermissionsPolicy, CacheControl, Secure
from logging import getLogger
from api.custom_logging import CustomizeLogger
from components.compose import Compose
from components.exceptions import ComposeInitialization, UnknownBroker, Unimplemented
from cli.command import __version__

initial_uptime = datetime.now()
logger = getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title='BrokerCleaner Management', debug=False)
    app.logger = CustomizeLogger.make_logger()

    return app


application = create_app()
composeEngine = Compose()


@application.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    server = Server().set("Secure")

    csp = (
        ContentSecurityPolicy().default_src("'none'")
                               .base_uri("'self'")
                               .connect_src("'self'" "api.spam.com")
                               .frame_src("'none'")
                               .img_src("'self'", "static.spam.com")
    )

    hsts = StrictTransportSecurity().include_subdomains().preload().max_age(2592000)

    referrer = ReferrerPolicy().no_referrer()

    permissions_value = (
        PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()
    )

    cache_value = CacheControl().must_revalidate()

    secure_headers = Secure(
        server=server,
        csp=csp,
        hsts=hsts,
        referrer=referrer,
        permissions=permissions_value,
        cache=cache_value,
    )

    secure_headers.framework.fastapi(response)

    return response


@application.get("/version", status_code=status.HTTP_200_OK)
def getversion(request: Request):
    request.app.logger.info("Request version information")
    data = {
        "doc": "...",
        "git_hash": "nogitversion",
        "version": __version__,
        "release_date": "no released",
        "uptime": get_uptime()
    }

    return data


@application.post("/init", status_code=status.HTTP_201_CREATED)
async def init(request: Request, response: Response):
    request.app.logger.info(f'Request init a Context Broker')

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = await request.json()
        broker = json["broker"]

        # Send the information to the docker management classes
        try:
            composeEngine.initialize(broker=broker)
            await composeEngine.up()

            resp = {'message': f'Deploying the Context Broker: {broker}'}
            response.status_code = status.HTTP_201_CREATED
            request.app.logger.info(f'POST /init 201 Created Request, Deploying {broker}')

        except ComposeInitialization as e:
            resp = {'message': f'The docker engine was not initialized'}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            request.app.logger.error(f'POST /init 500 Internal Server Error: {e.message}')
        except UnknownBroker as e:
            resp = {'message': f'Unexpected name for the Context Broker. Valid values: {composeEngine.brokers.keys()}'}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            request.app.logger.error(f'POST /init 500 Internal Server Error: {e.message}')
        except Unimplemented as e:
            resp = {'message': f'The deployment of {broker} is not implemented'}
            response.status_code = status.HTTP_501_NOT_IMPLEMENTED
            request.app.logger.error(f'POST /init 501 Internal Server Error: {e.message}')

    else:
        resp = {'message': 'Allowed Content-Type is only application/json'}
        response.status_code = status.HTTP_400_BAD_REQUEST
        request.app.logger.error(f'POST /init 400 Bad Request')

    return resp


@application.post("/clean", status_code=status.HTTP_200_OK)
async def clean(request: Request, response: Response):
    request.app.logger.info(f'Request clean a Context Broker')

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = await request.json()
        broker = json["broker"]

        # Send the information to the docker management classes
        composeEngine.initialize(broker=broker)
        composeEngine.down()

        resp = {'message': f'Cleaning the Context Broker: {json["broker"]}'}
        response.status_code = status.HTTP_200_OK
        request.app.logger.info(f'POST /clean 200 Created Request, Deploying {json["broker"]}')
    else:
        resp = {'message': 'Allowed Content-Type is only application/json'}
        response.status_code = status.HTTP_400_BAD_REQUEST
        request.app.logger.error(f'POST /clean 400 Bad Request')

    return resp


def get_uptime():
    now = datetime.now()
    delta = now - initial_uptime

    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)


def launch(app: str = "server:application", host: str = "127.0.0.1", port: int = 5000):
    run(app=app, host=host, port=port, log_level="info", reload=True, server_header=False)
