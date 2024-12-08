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
from . import Cradle, StairLift, ControlPlatform, SpoolCladding
from cadqueryhelper import Base
from cqterrain.spool import Spool
from cqterrain.walkway import Walkway
from cqterrain import Ladder


class PowerStation(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.p_spool:dict = {}
        self.p_spool['height'] = 60
        self.p_spool['radius'] = 97.5
        self.p_spool['wall_width'] =4
        self.p_spool['cut_radius'] = 36.5
        
        self.p_cradle:dict = {}
        self.p_cradle['height'] = self.p_spool['radius'] - self.p_spool['cut_radius']+2
        self.p_cradle['angle'] = 45
        
        self.p_stairs:dict = {}
        self.ladder_raise:float = 25
        self.ladder_increase:float = 10
        self.render_stairs:bool = True
        self.render_control:bool = True
        self.render_spool:bool = True
        self.render_walkway:bool = True
        self.render_cradle:bool = True
        self.render_cladding:bool = True
        self.render_ladder:bool = True

        #self.p_cladding = {}
        
        # blueprints
        self.bp_spool:Spool = Spool(**self.p_spool)
        self.bp_cradle:Cradle = Cradle(**self.p_cradle)
        self.bp_walk:Walkway = Walkway()

        self.bp_stairs:StairLift = StairLift(**self.p_stairs)
        self.bp_control:ControlPlatform = ControlPlatform()
        self.bp_cladding:SpoolCladding = SpoolCladding()
        self.bp_ladder:Ladder = Ladder()
        self.bp_ladder.height=self.bp_spool.radius + self.ladder_increase
        
    def make(self, parent = None):
        super().make(parent)
        if self.render_spool: 
            self.bp_spool.make(self)

        if self.render_cradle:
            self.bp_cradle.make(self.bp_spool)

        if self.render_cladding:
            self.bp_cladding.make(self.bp_spool)

        if self.render_ladder:
            self.bp_ladder.make()

        if self.render_stairs:
            self.bp_stairs.make(self)

        if self.render_control:
            self.bp_control.make(self)

        if self.render_walkway:
            self.bp_walk.make()

        
    def build(self):
        super().build()
        building = cq.Workplane("XY")

        if self.render_spool:
            spool = (
                self.bp_spool.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            )
            building = building.add(spool.translate((0,0,2)))
        
        if self.render_cladding:
            cladding = (
                self.bp_cladding.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            )
            building = building.add(cladding.translate((0,0,2)))
            
        if self.render_ladder:
            ladder = self.bp_ladder.build()
            ladder_x_translate = self.bp_spool.cut_radius + self.bp_ladder.length/2
            ladder_y_translate = self.bp_spool.height/2 + self.bp_ladder.width/2
            ladder_z_translate = self.bp_spool.radius+1 + self.ladder_raise
            building = building.add(ladder.translate((ladder_x_translate,ladder_y_translate,ladder_z_translate)))
            building = building.add(ladder.translate((-ladder_x_translate,-ladder_y_translate,ladder_z_translate)))

        if self.render_cradle:
            cradle = self.bp_cradle.build()
            building = building.union(cradle.translate((0,0,self.bp_cradle.height/2)))
            
        if self.render_stairs:
            stairs = self.bp_stairs.build()
            building = building.add(stairs.translate((0,-75,self.bp_stairs.height/2)))

        if self.render_control:
            controlPlatform = self.bp_control.build()
            building = building.add(controlPlatform.translate((0,75,self.bp_control.height/2)))

        if self.render_walkway:
            walk_z_translate = (self.bp_walk.height /2)+self.bp_cradle.height +10
            walkway = self.bp_walk.build().rotate((0,0,1),(0,0,0), 90)
            building = building.add(walkway.translate((0,0,walk_z_translate)))
        
        return building
    
    def build_assembly(self) -> cq.Assembly:
        super().build()
        assembly = cq.Assembly()

        if self.render_spool:
            spool = (
                self.bp_spool.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            ).translate((0,0,2))
            assembly.add(spool, color=cq.Color(0,0,1), name="spool")

        if self.render_cladding:
            cladding = (
                self.bp_cladding.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            ).translate((0,0,2))
            assembly.add(cladding, color=cq.Color(0,1,0), name="cladding")

        if self.render_ladder:
            ladder = self.bp_ladder.build()
            ladder_x_translate = self.bp_spool.cut_radius + self.bp_ladder.length/2
            ladder_y_translate = self.bp_spool.height/2 + self.bp_ladder.width/2
            ladder_z_translate = self.bp_spool.radius+1 + self.ladder_raise
            ladder1 = ladder.translate((ladder_x_translate,ladder_y_translate,ladder_z_translate))
            ladder2 = ladder.translate((-ladder_x_translate,-ladder_y_translate,ladder_z_translate))

            assembly.add(ladder1, color=cq.Color(1,0,0), name="ladder_one")
            assembly.add(ladder2, color=cq.Color(1,0,0), name="ladder_two")

        if self.render_cradle:
            cradle = self.bp_cradle.build().translate((0,0,self.bp_cradle.height/2))
            assembly.add(cradle, color=cq.Color(1,1,0), name="cradle")

        if self.render_stairs:
            stairs = self.bp_stairs.build().translate((0,-75,self.bp_stairs.height/2))
            assembly.add(stairs, color=cq.Color(1,0,1), name="stairs")

        if self.render_control:
            controlPlatform = self.bp_control.build().translate((0,75,self.bp_control.height/2))
            assembly.add(controlPlatform, color=cq.Color(0,1,1), name="controlPlatform")

        if self.render_walkway:
            walk_z_translate = (self.bp_walk.height /2)+self.bp_cradle.height +10
            walkway = self.bp_walk.build().rotate((0,0,1),(0,0,0), 90).translate((0,0,walk_z_translate))
            assembly.add(walkway, color=cq.Color(1,1,1), name="walkway")

        return assembly

    
    def build_cladding(self):
        building = cq.Workplane("XY")
        if self.render_cladding:
            cladding = (
                self.bp_cladding.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            )
            building = building.add(cladding.translate((0,0,2)))

        if self.render_cradle:
            cradle = self.bp_cradle.build()
            building = building.cut(cradle.translate((0,0,self.bp_cradle.height/2)))

        return building