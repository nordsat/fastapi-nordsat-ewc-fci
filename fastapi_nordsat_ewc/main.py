#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023

# Author(s):

#   Trygve Aspenes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import fastapi
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from fastapi_nordsat_ewc.views import dashboard
from fastapi_nordsat_ewc.api import endpoint

app = fastapi.FastAPI(title="NORDSAT MAPSERVER/SCRIPT",
                      description="Demo using fastapi and mapscript to server GEO COGs as OGC WMS",
                      version="0.0.1",
                      )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_PROCESSING_SECOND = 600


def configure_routing():
    app.include_router(dashboard.router)
    app.include_router(endpoint.router)

def configure():
    configure_routing()


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8999, host='localhost')
else:
    configure()
