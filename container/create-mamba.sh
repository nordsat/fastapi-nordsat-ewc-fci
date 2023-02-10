#!/bin/bash

mkdir /opt/conda
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /usr/bin/ --strip-components=1 bin/micromamba
/usr/bin/micromamba shell init -s bash --prefix=/opt/conda
source /root/.bashrc
mv /root/.bashrc /opt/conda/.bashrc
#micromamba activate
micromamba create -y -f /tmp/environment.yaml
/opt/conda/envs/fastapi/bin/pip cache purge
micromamba remove -y --force git pip
micromamba clean -a -y
#### mv /root/.bashrc /opt/conda/.bashrc
