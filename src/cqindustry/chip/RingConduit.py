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
from cqindustry.chip import Ring
from cqterrain import tile

class RingConduit(Ring):
    def __init__(self):
        super().__init__()
        self.frame:float = 1
        self.frame_depth:float = 3
        self.pipe_count:int|None = None
        self.pipe_radius:float = 4
        self.pipe_inner_radius:float = 2
        self.segment_length:float = 6
        self.space:float = 4
        self.pipe_padding:float = 1
        
    def _make_ladder(self):

        #print("make ring conduit ladder")
        
        ladder = tile.conduit(
            length = self.ladder_height,
            width = self.ladder_length,
            height = self.ladder_width,
            frame = self.frame, 
            frame_depth = self.frame_depth, 
            pipe_count = self.pipe_count, 
            radius = self.pipe_radius, 
            inner_radius = self.pipe_inner_radius, 
            segment_length = self.segment_length, 
            space = self.space, 
            pipe_padding = self.pipe_padding 
        ).rotate((0,0,1),(0,0,0),90).rotate((1,0,0),(0,0,0),90)
        
        #ladder = cq.Workplane("XY").box(self.ladder_length, self.ladder_width, self.ladder_height)
        ladder = ladder.translate((
            0,
            self.cut_diameter/2+.6,
            self.ladder_height/2
        ))

        if self.cut_ring:
            ladder = ladder.cut(self.cut_ring)

        ladders = (
            cq.Workplane()
            .union(ladder)
            .union(ladder.rotate((0,0,1),(0,0,0),180))
        )

        self.ladders = ladders
        
    def make(self, parent = None):
        super().make()
        
    def build(self):
        #print("build ring conduit ladder")
        return super().build()