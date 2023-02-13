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

import base64
import fastapi
from typing import List
from fastapi_nordsat_ewc.models.datasource import Datasource
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import Query
import json

templates = Jinja2Templates(directory='/app/templates')
router = fastapi.APIRouter()

# placeholder to fill an a template (html+js viewer or mapfile etc.) 
@router.get("/dashboard", name='dashboard', response_model=Datasource)
async def get_dashboard(request: Request,
                        data: str = Query(None,
                                                 title="dict of data",
                                                 description="dict of data and meta informations")):
    decode_data = base64.urlsafe_b64decode(data)
    #input_data = json.dumps(json.loads(decode_data), indent=4, sort_keys=True) 
    #print(input_data)
    