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

import os
import sys
import json
import mapscript
import traceback
import xml.dom.minidom
from datetime import datetime
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi import Request, APIRouter, Query, HTTPException

router = APIRouter()

def _generate_layer(layer_name, layer_data, start_time, end_time, layer):
    """Generate a layer based on the metadata from geotiff."""

    try:
        layer.setProjection(layer_data['proj4'])
    except KeyError:
        try:
            layer.setProjection(layer_data['crs'])
        except KeyError:
            layer.setProjection('init=epsg:3857')
    layer.status = 1
    layer.data = f"{layer_data['uri']}"
    layer.type = mapscript.MS_LAYER_RASTER
    layer.name = layer_name
    layer.metadata.set("wms_title", layer_name)
    layer.metadata.set("wms_extent", f"{layer_data['area_extent'][0]} {layer_data['area_extent'][1]} {layer_data['area_extent'][2]} {layer_data['area_extent'][3]}")
    layer.metadata.set("wms_timeextent", f'{start_time:%Y-%m-%dT%H:%M:%S}Z/{end_time:%Y-%m-%dT%H:%M:%S}Z/PT15M')
    layer.metadata.set("wms_default", f'{end_time:%Y-%m-%dT%H:%M:%S}Z')
    print(f"Complete generate layer: ", layer_name)

@router.get("/request", response_class=Response)
async def generate_map_config_and_respond(full_request: Request):
    """
    Based on a dynamical updated a json file list generate correct request reply.
    For GetCapability request generete all layers available with full time range for each layer.
    The reply will be xml.
    For GetMap requests generate only the requested layer at the requested time.
    The reply will we a png image
    """
    print("Request url scheme:", full_request.url.scheme)
    print("Request url netloc:", full_request.url.netloc)
    netloc = os.environ.get("NETLOC_ADDRESS", full_request.url.netloc)
    scheme = os.environ.get("NETLOC_SCHEME", full_request.url.scheme)
    print("Using scheme:", scheme)
    print("Using netloc:", netloc)
    map_object = mapscript.mapObj()
    """"Add all needed web metadata to the generated map file."""
    map_object.web.metadata.set("wms_title", "WMS fastapi")
    map_object.web.metadata.set("wms_onlineresource", f"{scheme}://{netloc}/request")
    map_object.web.metadata.set("wms_srs", "EPSG:25833 EPSG:3978 EPSG:4326 EPSG:4269 EPSG:3857")
    map_object.web.metadata.set("wms_enable_request", "*")
    map_object.setSize(10000, 10000)
    map_object.units = mapscript.MS_DD
    map_object.setExtent(-90, 20, 90, 90)
    try:
        map_object.setProjection("init=epsg:3857")
    except Exception:
        map_object.setConfigOption('PROJ_LIB', '/opt/conda/envs/fastapi/share/proj/')
        map_object.applyConfigOptions()
        map_object.setProjection("init=epsg:3857")

    ows_req = mapscript.OWSRequest()
    ows_req.type = mapscript.MS_GET_REQUEST
    try:
        ows_req.loadParamsFromURL(str(full_request.query_params))
    except mapscript.MapServerError:
        ows_req = mapscript.OWSRequest()
        ows_req.type = mapscript.MS_GET_REQUEST
        pass
    if not full_request.query_params or (ows_req.NumParams == 1 and 'satpy_products' in full_request.query_params):
        print("Query params are empty or only contains satpy-product query parameter. Force getcapabilities")
        ows_req.setParameter("SERVICE", "WMS")
        ows_req.setParameter("VERSION", "1.3.0")
        ows_req.setParameter("REQUEST", "GetCapabilities")
    else:
        print("ALL query params: ", str(full_request.query_params))

    time_stamp = ows_req.getValueByName('TIME')

    files_from_file_list = []
    try:
        with open('/list-of-files.json') as json_file:
            files_from_file_list = json.load(json_file)
    except FileNotFoundError:
        with open('/home/trygveas/Git/fastapi-nordsat-ewc/fastapi_nordsat_ewc/list-of-files.json') as json_file:
            files_from_file_list = json.load(json_file)
    parsed_list = {}
    for l in files_from_file_list:
        if l['layer'] not in parsed_list:
            parsed_list[l['layer']] = []
        _to_append = {}
        if 'proj4' in l:
            _to_append = {'uri': l['uri'],
                          'start_time': l['start_time'],
                          'area_extent': l['area_extent'],
                          'proj4': l['proj4']}
        elif 'crs' in l:
            _to_append = {'uri': l['uri'],
                          'start_time': l['start_time'],
                          'area_extent': l['area_extent'],
                          'crs': l['crs']}
        else:
            _to_append = {'uri': l['uri'],
                          'start_time': l['start_time'],
                          'area_extent': l['area_extent']}
        parsed_list[l['layer']].append(_to_append)
    for layer_name in parsed_list:
        layer_data_sorted = sorted(parsed_list[layer_name], key=lambda d: d['start_time'])
        selected_element = None
        if time_stamp:
            print("Need to check a time_stamp")
            for element in layer_data_sorted:
                if time_stamp in element['start_time']:
                    selected_element = element
                    break
        if not selected_element:
            selected_element = layer_data_sorted[-1]
        start_time = datetime.strptime(layer_data_sorted[0]['start_time'], "%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime(layer_data_sorted[-1]['start_time'], "%Y-%m-%dT%H:%M:%SZ")
        layer = mapscript.layerObj()
        _generate_layer(layer_name, selected_element, start_time, end_time, layer)
        layer_no = map_object.insertLayer(layer)

    map_object.save(f'./satpy-products-testets.map')

    print("NumParams", ows_req.NumParams)
    print("TYPE", ows_req.type)
    if ows_req.getValueByName('REQUEST') != 'GetCapabilities':
        mapscript.msIO_installStdoutToBuffer()
        map_object.OWSDispatch( ows_req )
        content_type = mapscript.msIO_stripStdoutBufferContentType()
        result = mapscript.msIO_getStdoutBufferBytes()
    else:
        mapscript.msIO_installStdoutToBuffer()
        dispatch_status = map_object.OWSDispatch(ows_req)
        if dispatch_status != mapscript.MS_SUCCESS:
            print("DISPATCH status", dispatch_status)
        content_type = mapscript.msIO_stripStdoutBufferContentType()
        mapscript.msIO_stripStdoutBufferContentHeaders()
        _result = mapscript.msIO_getStdoutBufferBytes()

        if content_type == 'application/vnd.ogc.wms_xml; charset=UTF-8':
            content_type = 'text/xml'
        dom = xml.dom.minidom.parseString(_result)
        result = dom.toprettyxml(indent="", newl="")
    return Response(result, media_type=content_type)
