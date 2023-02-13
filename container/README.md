# podman build

Clone repo or use build from repo

sudo podman build /home/talonglong/fastapi-nordsat-ewc/container

Note the id; will be different from your build check with sudo podman images

sudo podman run -d -it -p 8999:8999 --name fastapi-nordsat-ewc -v /eodata/hrit_out/:/eodata/hrit_out/ -v /home/talonglong/list-of-files.json:/list-of-files.json 8638f43f7c69 /opt/conda/envs/fastapi/bin/gunicorn --worker-class uvicorn.workers.UvicornWorker --workers 10 --bind 0.0.0.0:8999 fastapi_nordsat_ewc.main:app --keep-alive 120 --log-level debug --timeout 120

The mount of the list of files file must also be adjusted.

TODO:
Build container with name
