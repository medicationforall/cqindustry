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
import math
from . import Ramp

class RampGreebled(Ramp):
    def __init__(self):
        super().__init__()
        # parameters
        self.segment_count:int = 20
        self.segment_x_padding:float = 2
        self.segment_y_padding:float = 3
        self.segment_depth:float = 2.5
        
        self.render_inside_outline:bool = False
        
        # shapes
        self.inside_segments:cq.Workplane|None = None
        self.inside_outline:cq.Workplane|None = None
        
    def _make_inside_outline(self):
        length = self._calculate_max_inside_length()
        
        inside_outline = cq.Workplane("XY").box(
            length,
            self.width/2,
            self._calculate_inside_height()
        )
        self.inside_outline = inside_outline.translate((0,0,-1*(self.side_inset/4)))
        
    def _add_segment(self):
        segment_height = self._calculate_inside_height() / self.segment_count
        length = self._calculate_max_inside_length()
        
        def instance_segment(loc:cq.Location) -> cq.Shape:
            # weird stuff

            segment_length = length
            
            loc_tuple = loc.toTuple()[0]
            x = loc_tuple[0]
            y = loc_tuple[1]
            
            greeble = (
                cq.Workplane("XY")
                .center(x, y)
                .box(
                    segment_length/2,
                    segment_height,
                    self.width/2
                )
            )
            
            #show_object(greeble)
            #show_object(self.inside.translate((0,0,(self.side_inset/4))).rotate((1,0,0),(0,0,0),90))
            inside = self.bp_inside.build()
            greeble = greeble.intersect(inside.translate((0,0,(self.side_inset/4))).rotate((1,0,0),(0,0,0),90))
            #show_object(greeble)
            
            minus_x_len = greeble.faces("Z").edges("<Y").vals()[0].BoundingBox().xlen #type: ignore
            plux_x_len = greeble.faces("Z").edges(">Y").vals()[0].BoundingBox().xlen #type: ignore
            
            x_len = plux_x_len
            
            if minus_x_len < x_len:
                x_len = minus_x_len
                
            s_length = x_len-self.segment_x_padding*2
            s_width = segment_height-self.segment_y_padding
            
            if segment_height<0:
                raise Exception(f"ramp segment_y_padding is too high, {self.segment_y_padding} segment height is in the negatives {s_width}")
            
            slot = cq.Workplane().center(0, y).box(
                s_length,
                s_width,
                self.segment_depth
            )
            
            if x > 0:
                slot = slot.translate((x_len/2,0,0))
            else:
                slot = slot.translate((-1*(x_len/2),0,0))
                
            slot = slot.translate((0,0,self.width/4-self.segment_depth/2))
            
            s_fillet = (s_width/2)-.01
            slot = slot.faces(">X or <X").edges(">Y or <Y").fillet(s_fillet)
            
            return slot.val() #type: ignore
        return instance_segment
    
    def _make_inside_segments(self):
        length = self._calculate_max_inside_length()
        segment_height = self._calculate_inside_height() / self.segment_count
        y_count = math.floor(self._calculate_inside_height() / segment_height)
        
        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = length/2, 
                ySpacing = segment_height,
                xCount = 2, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = self._add_segment())
            
        ).rotate((1,0,0),(0,0,0),-90).translate((0,0,-1*(self.side_inset/4)))
        self.inside_segments = result
      
    def make(self, parent=None):
        super().make(parent)
        self._make_inside_outline()
        self._make_inside_segments()
          
    def build(self):
        ramp = super().build()
        scene = cq.Workplane("XY").add(ramp)

        if self.inside_segments:
            scene = scene.cut(self.inside_segments.translate((0,self.width/2,0)))
        
        if self.render_inside_outline and self.inside_outline:
            scene = scene.add(self.inside_outline.translate((0,self.width/4,0)))
        return scene