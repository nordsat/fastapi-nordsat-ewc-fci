import sys
import rasterio
import mapscript
import traceback
import xml.dom.minidom

from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi import Request, APIRouter, Query, HTTPException

router = APIRouter()

@router.get("/request", response_class=Response)
async def generate_satpy_quicklook(full_request: Request):
    
    print("Request url scheme:", full_request.url.scheme)
    print("Request url netloc:", full_request.url.netloc)

    map_object = mapscript.mapObj()
    """"Add all needed web metadata to the generated map file."""
    map_object.web.metadata.set("wms_title", "WMS senda fastapi")
    map_object.web.metadata.set("wms_onlineresource", f"{full_request.url.scheme}://{full_request.url.netloc}/request")
    map_object.web.metadata.set("wms_srs", "EPSG:25833 EPSG:3978 EPSG:4326 EPSG:4269 EPSG:3857")
    map_object.web.metadata.set("wms_enable_request", "*")
    map_object.setProjection("AUTO")
    map_object.setSize(10000, 10000)
    map_object.units = mapscript.MS_DD
    map_object.setExtent(-90, 20, 90, 90)

    layer = mapscript.layerObj()

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
    with open('/home/trygveas/Git/fastapi-nordsat-ewc/app/list-of-files.txt') as f:
        files_from_file_list = f.readlines()
    print("files from list", files_from_file_list)
    file_names = []
    timestamps = []
    selected_file_name = None
    for l in files_from_file_list:
        file_name, timestamp, ll_x, ll_y, ur_x, ur_y = l.strip().split()
        timestamps.append(timestamp)
        file_names.append(file_name)
        if time_stamp:
            print("Need to check a time_stamp")
            if time_stamp in l:
                selected_file_name = file_name
    
    # try:
    #     print("Rasterio open")
    #     dataset = rasterio.open(f'/home/trygveas/testdata/fastapi-mapscript/natural_enh_with_night_ir_hires-20230209_084500.tif')
    #     print("Rasterio opened")
    # except rasterio.errors.RasterioIOError:
    #     exc_info = sys.exc_info()
    #     traceback.print_exception(*exc_info)
    #     return None
    # bounds = dataset.bounds
    # ll_x = bounds[0]
    # ll_y = bounds[1]
    # ur_x = bounds[2]
    # ur_y = bounds[3]  
    print(ll_x, ll_y, ur_x, ur_y)
    layer.setProjection('EPSG:3857')
    layer.status = 1
    layer.data = selected_file_name or file_names[-1]
    layer.type = mapscript.MS_LAYER_RASTER
    layer.name = 'natural_enh_with_night_ir'
    start_time = timestamps[0]
    end_time = timestamps[-1]
    layer.metadata.set("wms_title", 'Natural enhanced with night IR')
    layer.metadata.set("wms_extent", f"{ll_x} {ll_y} {ur_x} {ur_y}")
    layer.metadata.set("wms_timeextent", f'{start_time}/{end_time}/PT15M')
    layer.metadata.set("wms_default", f'{end_time}')
    # dataset.close()
    print("Complete generate layer")

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
