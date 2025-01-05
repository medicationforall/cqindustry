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
from cadqueryhelper import Base
from . import PortalBase, Frame, FrameWindow, Ramp, PortalHinge, EnergyInsert

class Portal(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.render_base:bool = True
        self.render_hinges:bool = True
        
        self.hinge_segments:int = 3
        self.plate_spacer = 1.2
        
        # blueprints
        self.bp_base = PortalBase()
        self.bp_frame:Frame|FrameWindow = Frame()
        self.bp_ramp = Ramp()
        self.bp_hinge:PortalHinge|None = PortalHinge()
        self.bp_iris:EnergyInsert|None = None
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_base.make()
        self.bp_frame.make()
        self.bp_ramp.make(self.bp_frame)
        
        if self.bp_hinge:
            self.bp_hinge.length = self.bp_frame.base_length - self.bp_frame.side_inset
            self.bp_hinge.segments = self.hinge_segments
            self.bp_hinge.plate_spacer = self.plate_spacer
            self.bp_hinge.make(self.bp_ramp)

        if self.bp_iris:
            window_padding = 0
            if self.bp_frame is FrameWindow and self.bp_frame.window_cut_padding:
                window_padding = self.bp_frame.window_cut_padding
            top_length = self.bp_frame.top_length - (self.bp_frame.frame_size) + (window_padding*2)
            length = self.bp_frame.length-(self.bp_frame.frame_size*2) + (window_padding*2)
            height = self.bp_frame.height-(self.bp_frame.frame_size) + (window_padding*2)
            self.bp_iris.top_length = top_length
            self.bp_iris.length = length
            self.bp_iris.height = height
            self.bp_iris.base_offset = self.bp_frame.base_offset
            self.bp_iris.base_height = self.bp_frame.frame_size

            if self.bp_frame is FrameWindow and self.bp_frame.window_cut_width:
                self.bp_iris.width = self.bp_frame.window_cut_width
            self.bp_iris.make()
        
    def build_hinges(self) -> cq.Workplane:
        if self.bp_hinge:
            base_z_translate = 0
            if self.render_base and self.render_base:
                base_z_translate = self.bp_base.height

            portal_hinge = self.bp_hinge.build()
            hinge_y = self.bp_frame.width/2 + self.bp_hinge.radius + self.bp_hinge.plate_spacer
            hinge_z = base_z_translate + self.bp_hinge.radius
            
            hinges = (
                cq.Workplane("XY")
                .add(
                    portal_hinge
                    .rotate((0,0,1),(0,0,0),180)
                    .translate((0,hinge_y,hinge_z))
                )
                .add(
                    portal_hinge
                    .translate((0,-hinge_y,hinge_z))
                )
            )        
            return hinges
        else:
            raise Exception('Unable to resolve bp_hinge instance')

    def build_frame(self):
        base_z_translate = 0
        if self.render_base and self.render_base:
            base_z_translate = self.bp_base.height

        frame = self.bp_frame.build()
        frame = frame.translate((0,0,self.bp_frame.height/2 + base_z_translate))

        if self.render_hinges and self.bp_hinge:   
            hinges = self.build_hinges()
            frame = frame.union(hinges)

        return frame
    
    def build_iris(self):
        base_z_translate = 0
        if self.render_base and self.render_base:
            base_z_translate = self.bp_base.height

        if self.bp_iris:
            return self.bp_iris.build().translate((0,0,base_z_translate))
        else:
            raise Exception("Unable to resolve bp_iris instance")
        
    def build(self) -> cq.Workplane:
        super().build()

        base_z_translate = 0
        if self.render_base and self.render_base:
            base_z_translate = self.bp_base.height
        
        frame = self.build_frame()
        scene = cq.Workplane("XY").union(frame)
        
        if self.render_base and self.bp_base:
            portal_base  = self.bp_base.build()
            scene = scene.union(portal_base.translate((0,0,base_z_translate/2)))

        if self.bp_iris:
            scene.add(self.build_iris())

        return scene
    
    def build_cutaway(self):
        model = self.build()

        base_z_translate = 0
        if self.render_base and self.render_base:
            base_z_translate = self.bp_base.height

        cut = cq.Workplane("XY").box(
            self.bp_frame.length, 
            self.bp_frame.width + self.bp_frame.height*2+20, 
            self.bp_frame.height+base_z_translate
        )

        scene = (
            cq.Workplane("XY")
            .union(model)
            .cut(cut.translate((self.bp_frame.length/2,0,(self.bp_frame.height+base_z_translate)/2)))
        )

        return scene