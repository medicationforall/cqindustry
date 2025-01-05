# Copyright 2024 James Adams
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
from . import ContainerFrame, ContainerLadder, ContainerRamp, Floor
from ..portal import Portal

class Container(Portal):
    def __init__(self):
        super().__init__()
        
        #params
        self.render_base = False
        self.render_floor:bool = True
        self.render_ladder:bool = True

        #blueprints
        self.bp_frame = ContainerFrame()
        self.bp_frame.length = 75
        self.bp_frame.width = 140
        self.bp_frame.height = 75

        self.bp_frame.top_length = 50
        self.bp_frame.base_length = 50
        self.bp_frame.base_offset = 35
        self.bp_frame.side_inset = 4
        self.bp_frame.frame_size = 7

        self.bp_frame.render_sides = True

        self.bp_ramp = ContainerRamp()
        self.bp_ramp.width = 8
        self.bp_ramp.segment_count = 10
        self.bp_ramp.segment_y_padding = 3

        self.bp_ramp.render_outside = True
        self.bp_ramp.bp_outside.padding = 5
        self.bp_ramp.bp_outside.x_translate = -10

        self.bp_hinge.rotate_deg = 0
        self.bp_hinge.ramp_bottom_margin = 0
        self.bp_hinge.tab_length = 4
        self.plate_spacer = .3

        self.bp_ladder = ContainerLadder()
        self.bp_ladder.ladder_rungs = 5
        self.bp_ladder.ladder_depth = 5
        self.bp_ladder.ladder_rung_radius = 1.5
        
        self.bp_floor = Floor()
        
    def make(self, parent=None):
        super().make(parent)
        
        self.bp_floor.length = self.bp_frame.base_length - self.bp_frame.frame_size - self.bp_frame.side_inset
        self.bp_floor.width = self.bp_frame.width
        self.bp_floor.make()

        self.bp_ladder.width = self.bp_frame.width/5
        self.bp_ladder.make(self.bp_frame)
        
    def build(self) -> cq.Workplane:
        container = super().build()

        base_z_translate = 0
        if self.render_base and self.render_base:
            base_z_translate = self.bp_base.height

        scene = (
            cq.Workplane("XY")
            .add(container.translate((0,0,-base_z_translate - self.bp_frame.height/2)))
        )
        
        if self.render_floor and self.bp_floor.floor_cut:
            floor = self.bp_floor.build()
            floor_cut = self.bp_floor.floor_cut
            floor_z = self.bp_frame.height-(self.bp_frame.frame_size*2)+self.bp_floor.height
            
            scene =(
                scene
                .cut(floor_cut.translate((0,0,-floor_z/2)))
                .union(floor.translate((0,0,-floor_z/2)))
            )

        if self.render_ladder:
            ladder_cut, ladder_rungs = self.bp_ladder.build()

            if ladder_cut:
                scene=(
                    scene
                    .cut(ladder_cut)
                    .union(ladder_rungs)
                )
        return scene