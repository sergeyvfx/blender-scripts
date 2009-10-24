#!BPY

#
# This script renders scene from all cameras and stores
# result to <path-of-blend-file>/render
#
# Copyright (C) 2009 Sergey I. Sharybin <g.ulairi@gmail.com>
#
# This script is covered by GNU General Public License v2 and higher
#

import Blender, os
from Blender import sys, Scene
from Blender.Scene import Render
from stat import *

path = sys.dirname(Blender.Get("filename")) + sys.dirsep + "render"

# Check existment of destination directory
if not sys.exists(path):
  os.mkdir(path)

mode = os.stat(path)[ST_MODE]

if S_ISDIR(mode):
  scene = Scene.GetCurrent()
  context = scene.getRenderingContext()

  savedDisplayMode = context.displayMode
  context.displayMode = 2

  context.setRenderPath(path)

  # Store currently active camera
  savedCamera = scene.objects.camera

  children = scene.objects
  for obj in children:
    type = obj.getType()
    if type == "Camera":
      scene.objects.camera = obj
      context.render()
      context.saveRenderedImage("/" + obj.getName())

  # Rrestore initial active camera
  scene.objects.camera = savedCamera

  context.displayMode = savedDisplayMode
