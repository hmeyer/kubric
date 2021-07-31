#!/usr/local/bin/python3.9
# pylint disable=missing-function-docstring

import fire
import os
import re
import sys
import subprocess
from pathlib import Path

# --- python3.7 needed by suprocess 'capture output'
assert sys.version_info.major>=3 and sys.version_info.minor>=7

# --- default folders
SHAPENET_ROOT = '~/datasets/ShapeNetCore.v2'

def bash(shapenet_root=SHAPENET_ROOT):
  shapenet_root = os.path.expanduser(shapenet_root)
  command = f"""
  docker run --rm --interactive \
    --user `id -u`:`id -g` \
    --volume {shapenet_root}:/ShapeNetCore.v2 \
    --volume $PWD:/shapenet2kubric \
    kubricdockerhub/shapenet:latest \
    /bin/bash -l
  """
  _execute(command)

def parfor(module, shapenet_root=SHAPENET_ROOT, num_processes=8):
  shapenet_root = os.path.expanduser(shapenet_root)
  command = f"""
  docker run --rm --interactive \
    --user `id -u`:`id -g` \
    --volume $PWD:/shapenet2kubric \
    --volume {shapenet_root}:/ShapeNetCore.v2 \
    kubricdockerhub/shapenet:latest \
    python3.7 parfor.py \
      --functor_module {module} \
      --datadir /ShapeNetCore.v2 \
      --num_processes {num_processes}
  """
  _execute(command)

def obj2gltf(model, shapenet_root=SHAPENET_ROOT):
  shapenet_root = os.path.expanduser(shapenet_root)
  command = f"""
  docker run --rm --interactive \
    --user `id -u`:`id -g` \
    --volume $PWD:/shapenet2kubric \
    --volume {shapenet_root}:/ShapeNetCore.v2 \
    kubricdockerhub/shapenet:latest \
    python3.7 obj2gltf.py \
      --model={model}
  """
  _execute(command)

def obj2manifold(model, shapenet_root=SHAPENET_ROOT):
  shapenet_root = os.path.expanduser(shapenet_root)
  command = f"""
  docker run --rm --interactive \
    --user `id -u`:`id -g` \
    --volume $PWD:/shapenet2kubric \
    --volume {shapenet_root}:/ShapeNetCore.v2 \
    kubricdockerhub/shapenet:latest \
    python3.7 obj2manifold.py \
      --model={model}
  """
  _execute(command)

def completion():
  _execute('./launch.py -- --completion > .launch-completion')
  print('to enable completion, run "source .launch-completion"')

def _execute(command_string):
  command_string = re.sub(' +', ' ', command_string)
  command_string = command_string.replace('\n',' ')
  print(command_string)
  return subprocess.run(command_string, shell=True, check=True)

if __name__ == '__main__':
  fire.Fire()