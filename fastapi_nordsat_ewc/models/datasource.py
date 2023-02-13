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

from typing import Optional

import pydantic
from pydantic import BaseModel


class Datasource(BaseModel):
    data: dict = pydantic.Field(default={"": ""},
                                example={
                                    "id1": {
                                        "title": "Title",
                                        "feature_type": "NA",
                                        "resources": {
                                            "OGC:WMS": [
                                                "http://nbswms.met.no/thredds/wms_ql/NBS/S1A/2021/05/18/EW/S1A_EW_GRDM_1SDH_20210518T070428_20210518T070534_037939_047A42_65CD.nc?SERVICE=WMS&REQUEST=GetCapabilities"]
                                        }
                                    }                                                                        
                                })
    email: str = pydantic.Field(default='me@you.web', example='epiesasha@me.com')
    project: Optional[str] = pydantic.Field(default='WMS', example='Mapserver')
