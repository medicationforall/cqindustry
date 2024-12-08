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
from cqindustry.chip import Platform
from cadqueryhelper import Base
from . import SteelFrame

class ControlPlatformPrint(Base):
    def __init__(self):
        super().__init__()
        self.length:float = 150
        self.width:float = 75
        self.height:float = 70
        
        self.segment_width:float = 75
        self.segment_length:float = 75
        self.y_width:float = 5
        self.y_height:float = 10
        
        # platform blueprint init
        self.platform_bp:Platform = Platform()
        self.platform_bp.width = self.width
        self.platform_bp.height = 5
        self.platform_bp.render_center_cut = False
        self.platform_bp.render_ladders = False
        self.platform_bp.render_floor = True
        self.platform_bp.render_stripes = True
        self.platform_bp.corner_chamfer = 4
        self.platform_bp.bar_width = 10
        self.platform_bp.stripe_width = 5
        self.platform_bp.stripe_padding = .3
        
        self.bp_frame:SteelFrame = SteelFrame()
        self.bp_frame_insert:SteelFrame = SteelFrame()
        
        self.frame_insert_height:float = 1
        self.frame_insert_height_margin:float = 1
        self.frame_insert_margin:float = 0.4

        # solids
        self.platform:cq.Workplane|None = None
        
    def make(self, parent=None):
        super().make(parent)
        self.platform_bp.width = self.width
        self.platform_bp.length = self.length
        self.platform_bp.make()

        self.bp_frame.width = self.width
        self.bp_frame.length = self.length
        self.bp_frame.height = self.height
        self.bp_frame.segment_length = self.segment_length
        self.bp_frame.segment_width = self.segment_width
        self.bp_frame.y_width = self.y_width
        self.bp_frame.y_height = self.y_height
        self.bp_frame.make()
        
        self.bp_frame_insert.width = self.width + self.frame_insert_margin
        self.bp_frame_insert.length = self.length
        self.bp_frame_insert.height = self.height
        self.bp_frame_insert.segment_length = self.segment_length
        self.bp_frame_insert.segment_width = self.segment_width + self.frame_insert_margin
        self.bp_frame_insert.y_web_thickness = self.bp_frame.y_web_thickness + self.frame_insert_margin
        self.bp_frame_insert.y_width = self.y_width + self.frame_insert_margin
        self.bp_frame_insert.y_height = self.y_height + self.frame_insert_height + self.frame_insert_margin
        self.bp_frame_insert.make()
    
    def build(self):
        super().build()
        platform = self.platform_bp.build()
        frame = self.bp_frame.build()
        z_translate = (self.height/2)+(self.platform_bp.height/2)
        scene = (
            cq.Workplane("XY")
            .union(platform.translate((0,0,z_translate)))
            .union(frame)
        )
        return scene
    
    def build_print_patform(self):
        super().build()
        platform = self.platform_bp.build()
        frame = self.bp_frame.build()
        frame_insert = self.bp_frame_insert.build()
        z_translate = (self.height/2)+(self.platform_bp.height/2)
        
        scene = (
            cq.Workplane("XY")
            .union(platform.translate((0,0,z_translate)))
            .union(frame)
        )
        
        platform_cut = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.platform_bp.height)
            .translate((0,0,z_translate+self.frame_insert_height+self.frame_insert_height_margin))
        )
        
        print_frame_insert = (
            cq.Workplane("XY")
            .add(frame_insert)
            .cut(platform_cut.translate((0,0,0)))
        )
        
        frame_cut_box = cq.Workplane("XY").box(
            self.length, 
            self.width, 
            self.height
        )
    
        print_platform = (
            cq.Workplane("XY")
            .union(scene)
            .cut(frame_cut_box)
            .cut(print_frame_insert)
        )
        return print_platform
    
    def build_print_frame(self):
        super().build()
        frame = self.bp_frame.build()
        
        platform_cut = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.platform_bp.height)
            .translate((0,0,self.platform_bp.height/2+self.height/2+self.frame_insert_height))
        )
        
        print_frame = (
            cq.Workplane("XY")
            .add(frame)
            .cut(platform_cut)
        )
        
        return print_frame
    
    def build_print_frame_single(self):
        super().build()
        frame = self.bp_frame.build()
        
        platform_cut = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.platform_bp.height)
            .translate((0,0,self.platform_bp.height/2+self.height/2+self.frame_insert_height))
        )
        
        print_frame = (
            cq.Workplane("XY")
            .add(frame)
            .cut(platform_cut)
        )
        
        cut_box = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height+self.frame_insert_height)
        ).translate((0,0,self.frame_insert_height/2))
        
        single_frame = (
            cq.Workplane("XY")
            .union(print_frame)
            .cut(cut_box.translate((self.bp_frame.z_height,0,0)))
        ).translate((self.length/2-self.bp_frame.z_height/2,0,0))
        
        return single_frame.rotate((0,1,0),(0,0,0),90)
    
