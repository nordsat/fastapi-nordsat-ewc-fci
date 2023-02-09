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

USER 1001
EXPOSE 40000

ENTRYPOINT ["/usr/bin/entrypoint.sh"]