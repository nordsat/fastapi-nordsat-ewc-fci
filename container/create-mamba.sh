#!/bin/bash
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
