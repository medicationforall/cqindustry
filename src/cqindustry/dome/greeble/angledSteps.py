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

def make_angled_step(
    length:float = 30, 
    width:float = 10, 
    height:float = 15, 
    angle:float = 36
) -> cq.Workplane:
    step_half = (
        cq.Workplane("XY")
        .box(length,width,height)
    )

    step = (
        cq.Workplane("XY")
        .add(
            step_half
            .translate((-1*(length/2),width/2,0))
            .rotate((0,0,1),(0,0,0),angle)
        )
        .add(
            step_half
            .translate((length/2,width/2,0))
        )
    )
    
    step = (
        step
        .rotate((0,0,1),(0,0,0),-1*(angle/2))
        .translate((0,-1*(length/5),0))
    )
    return step

def make_angled_steps(
        length:float = 30, 
        width:float = 10, 
        height:float = 15,
        dec:float = 5
) -> cq.Workplane:
    steps = cq.Workplane("XY")

    for i in range(3):
        step_height = height -dec*i
        step = make_angled_step(
            length,
            width,
            step_height
        )

        steps = (
            steps
            .union(
                step
                .translate((
                    0,
                    -width*i,
                    -1*(height/2)+(step_height/2))
                )
            )
        )
    return steps