FROM ubuntu:22.04 AS builder

ENV MAMBA_ROOT_PREFIX=/opt/conda
ENV MAMBA_DISABLE_LOCKFILE=TRUE

RUN apt-get update && \
    apt-get install -y tar bzip2 curl && \
    apt-get autoclean

COPY environment.yaml /tmp
COPY create-mamba.sh /tmp

CMD [ "/bin/bash" ]

RUN /tmp/create-mamba.sh && \
    chgrp -R 0 /opt/conda && \
    chmod -R g=u /opt/conda

FROM ubuntu:22.04

COPY --from=builder /opt/conda /opt/conda
COPY --from=builder /usr/bin/micromamba /usr/bin/
COPY entrypoint.sh /usr/bin/
COPY ./app /app
COPY ./start.sh /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh

WORKDIR /app

ENV PYTHONPATH=/opt/conda/envs/fastapi/lib/python3.9/site-packages:$PYTHONPATH
ENV PATH=/opt/conda/envs/fastapi/bin/:$PATH
ENV LD_LIBRARY_PATH=/opt/conda/envs/fastapi/lib/:$LD_LIBRARY_PATH

EXPOSE 8999

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
#ENTRYPOINT ["/usr/bin/entrypoint.sh"]