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
from cqindustry.chip import Platform
from cadqueryhelper import Base
from . import SteelFrame

class ControlPlatform(Base):
    def __init__(self):
        super().__init__()
        self.length:float = 150
        self.width:float = 75
        self.height:float = 70
        
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
        self.bp_frame.make()
    
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