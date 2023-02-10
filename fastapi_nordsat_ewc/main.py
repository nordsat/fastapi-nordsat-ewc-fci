"""
"""

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
