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

import random
from numpy import arange
from typing import Callable

from .tiles import (
    plain,
    slot,
    rivet,
    vent,
    bolt_panel,
    corrugated,
    charge
)

def _resolve_value(var:tuple[float,float,float]|float|None)->float|None:
    if type(var) is tuple:
        var_choices = arange(var[0], var[1]+var[2], var[2])
        value = random.choice(var_choices)
        return float(value)
    else:
        return var #type:ignore


def stylized_panels(
        length:float = 75,
        width:float = 10,
        height:float = 2,
        count:float = (2,3,1),
        seed:str = "seed",
        rotate:tuple[float,float,float] = (-45,45,5),
        tiles:list[Callable[[float, float, float], cq.Workplane]] = [rivet,bolt_panel]
):
    
    if seed:
        random.seed(seed)
        
    spanel_count = int(_resolve_value(count))
    x_space = length/spanel_count
    s_panels = cq.Workplane("XY")
    for i in range(spanel_count):
        
        if tiles:
            #log('tiles is not null')
            tile_method = random.choice(tiles)
            tile = tile_method(x_space,width,height)
        else:
            tile = cq.Workplane("XY").box(x_space,width,height)
        rotation = _resolve_value(rotate)
        s_panels.add(tile.rotate((0,0,1),(0,0,0),rotation).translate((i*x_space,0,0)))
        
    return s_panels.translate((x_space/2-length/2,0,0))