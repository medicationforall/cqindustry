# Copyright 2023 James Adams
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
from cadqueryhelper import Base

def make_pentagon(
        radius:float, 
        height:float, 
        z_rotate:float = 30
    )->cq.Workplane:

    hexagon = (
        cq.Workplane("XY")
        .polygon(5, radius)
        .extrude(height)
        .translate((0,0,-1 * (height/2)))
        .rotate((0,0,1), (0,0,0), z_rotate)
        #.rotate((1,0,0),(0,0,0),-58)
    )
    return hexagon

class BasePentagon(Base):
    def __init__(self):
        super().__init__()
        self.radius:float = 51
        self.height:float = 4