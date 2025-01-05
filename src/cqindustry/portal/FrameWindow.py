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
from cadqueryhelper import shape
from . import Frame

class FrameWindow(Frame):
    def __init__(self):
        super().__init__()
        
        self.window_cut_width:float = 0.4
        self.window_cut_padding:float = 1
        
        self.window_key_width:float = 2
        self.window_key_padding:float = 0.8
        
        self.window_key_text:str = "Portal Key"
        self.window_key_text_size:float = 10
        self.window_key_text_height:float = 1
        
        # shapes
        self.window_cut_out:cq.Workplane|None = None
        self.window_cut_key:cq.Workplane|None = None
        
    def __make_window_cut_out(self):
        mid_offset:float = self._calculate_mid_offset()
        
        length = self.length-(self.frame_size*2) + (self.window_cut_padding*2)
        width = self.window_cut_width
        height = self.height-(self.frame_size*2) + (self.window_cut_padding*2)
        top_length = top_length = self.top_length - self.frame_size + (self.window_cut_padding*2)

        cut_out = shape.coffin(
            length,
            height,
            width,
            top_length,
            length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90).translate((0,0,0))
        
        cut_base = cq.Workplane("XY").box(length,width, self.frame_size).translate((0,0,-1*(self.height/2 -self.frame_size/2 )))
        
        cut_combined = (
            cq.Workplane("XY")
            .union(cut_out)
            .union(cut_base)
        )
        
        self.window_cut_out = cut_combined
        
    def __make_window_cut_key(self):
        mid_offset:float = self._calculate_mid_offset()
        
        length = self.length-(self.frame_size*2) + (self.window_key_padding*2)
        width = self.window_key_width
        height = self.height-(self.frame_size*2) + (self.window_key_padding*2)
        top_length = top_length = self.top_length-self.frame_size + (self.window_key_padding*2)
        base_length = base_length = self.base_length-(self.frame_size/2) + (self.window_key_padding*2)
        cut_out = shape.coffin(
            length,
            height,
            width,
            top_length,
            base_length,
            mid_offset = mid_offset
        )#.rotate((1,0,0),(0,0,0),-90)
        
        key_text = (
            cq.Workplane("XY")
            .text(
                self.window_key_text, 
                self.window_key_text_size, 
                self.window_key_text_height
            )
            .translate((0,0,width/2))
        )
        
        combined = (
            cq.Workplane()
            .union(cut_out)
            .add(key_text)
        )
        
        self.window_cut_key = combined
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_window_cut_out()
        self.__make_window_cut_key()
        
    def build(self) -> cq.Workplane:
        frame = super().build()
        
        scene = (
            cq.Workplane()
            .add(frame)
        )

        if self.window_cut_out:
            scene = scene.cut(self.window_cut_out)
        
        return scene
    
    def build_key(self) -> cq.Workplane:
        if self.window_cut_key:
            return self.window_cut_key
        else:
            raise Exception('Unable to resolve window_cut_key')