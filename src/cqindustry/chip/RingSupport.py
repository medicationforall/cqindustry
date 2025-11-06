# Copyright 2025 James Adams
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
from . import Ring
from ..support import Segmented

class RingSupport(Ring):
    def __init__(self):
        super().__init__()

        self.bp_support:Segmented|None = Segmented()
        
    def _make_ladder(self):
        if self.bp_support:
            self.bp_support.length = self.ladder_length
            self.bp_support.width = self.ladder_width
            self.bp_support.height = self.ladder_height
            self.bp_support.make()

            ladder = self.bp_support.build()
            
            ladder = ladder.rotate((0,0,1),(0,0,0),180)
            
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