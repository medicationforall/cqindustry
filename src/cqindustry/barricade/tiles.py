# Copyright 2026 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cadquery as cq
from cqterrain import tile, greeble
 

def plain(length,width,height) -> cq.Workplane:
    #log('plain')
    return cq.Workplane("XY").box(length,width,height)

def slot(length,width,height) -> cq.Workplane:
    #hardcoding padding
    #log('slot')
    return tile.slot(length,width,height,0)

def rivet(length,width,height) -> cq.Workplane:
    #hardcoding padding
    #log('rivet')
    return tile.rivet(length,width,height,0)
    #return tile.rivet(length,width,height,0)

def vent(length,width,height) -> cq.Workplane:
    #log('vent')
    return greeble.vent(width,length).rotate((0,0,1),(0,0,0),90)

def bolt_panel(length,width,height) -> cq.Workplane:
    #log('bolt panel')
    return tile.bolt_panel(length,width)

def corrugated(length,width,height) -> cq.Workplane:
    #log('****corrugated')
    return tile.corrugated(
        length, 
        width, 
        height,
        segment_length = 3,
        inner_width = 0.5
    )

def charge(length,width,height) -> cq.Workplane:
    #log('charge')
    if width == 5:
        width = 5
        padding = 0
    else:
        padding = 1.5

    return tile.charge(
        length = length, 
        width = width, 
        height = 3,
        line_width = 1.5,
        line_depth = 1,
        corner_chamfer = 2,
        edge_chamfer = 1,
        padding = padding
    )