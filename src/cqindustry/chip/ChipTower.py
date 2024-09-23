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
from cqindustry.chip import ChipCan, Ring, Platform, GuardRail

class ChipTower(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length:float = 150
        self.width:float = 150
        self.height:float = 225

        self.stories:int = 2
        self.story_height:float = 75
        self.can_diameter_padding:float = 1

        self.render_can:bool = True
        self.ring_alternate_rotate:bool = False
        self.render_story_proxy:bool = False
        self.render_platforms:bool = True
        self.render_rings:bool = True
        self.render_rail:bool = True

        #blueprints
        self.bp_can = ChipCan()
        self.bp_ring = Ring()
        self.bp_platform = Platform()
        self.bp_rail = GuardRail()

        # shapes
        self.story_proxy = None

    def _make_can(self):
        # I could also set the height of the can to minimally meet the calculated height of the total stories
        # that may be a bad idea because the can's are not a 3d printed component and are instead externally sourced. 
        self.bp_can.height = self.height
        self.bp_can.make()

    def __make_story_proxy(self):
        self.story_proxy = cq.Workplane("XY").box(
            self.bp_can.diameter,
            self.bp_can.diameter,
            self.story_height
        )

    def _make_platform(self):
        #set minimum properties
        #intentionally trying to set what methods are protected and private
        self.bp_platform.length = self.length
        self.bp_platform.width = self.width
        self.bp_platform.cut_diameter = self.bp_can.diameter + self.can_diameter_padding
        self.bp_platform.make()

    def _make_ring(self):
        if type(self.bp_ring) is tuple: # multiple blueprints
            for blueprint in self.bp_ring: #type:ignore
                blueprint.cut_diameter = self.bp_can.diameter + self.can_diameter_padding
                blueprint.ladder_height = self.story_height - self.bp_platform.height
                blueprint.make()
        else: # single blueprint
            self.bp_ring.cut_diameter = self.bp_can.diameter + self.can_diameter_padding
            self.bp_ring.ladder_height = self.story_height - self.bp_platform.height 
            self.bp_ring.make()

    def make(self, parent = None):
        super().make(parent)

        self._make_can()
        self.__make_story_proxy()
        self._make_ring()
        
        self._make_platform()
        self.bp_rail.make()

    def __build_story_proxies(self):
        stories_outline = cq.Workplane("XY")
        #needs to take into account platform height
        z_translate = self.story_height

        for i in range(self.stories):
            stories_outline = stories_outline.add(self.story_proxy.translate((0,0,i*z_translate))) #type:ignore

        return stories_outline.translate((0,0,self.story_height/2))

    def __build_platforms(self, platform:cq.Workplane):
        platforms = cq.Workplane("XY")
 
        for i in range(self.stories):
            platforms = platforms.union(platform.translate((
                0,
                0,
                (i*self.story_height) + (self.bp_platform.height/2)
            )))

        return platforms.translate((0,0,self.story_height - self.bp_platform.height))
    
    def __build_rings(self):
        built_rings = []

        if type(self.bp_ring) is tuple: # multiple blueprints
            for blueprint in self.bp_ring: #type: ignore
                built_rings.append(blueprint.build)
        else:
            built_rings.append(self.bp_ring.build)

        # worked way easier than I thought
        rings = cq.Workplane("XY")
 
        for i in range(self.stories):
            index = i % len(built_rings)
            ring = built_rings[index]().rotate((1,0,0),(0,0,0),180)
            
            if self.ring_alternate_rotate and i % 2 == 1:
                ring = ring.rotate((0,0,1),(0,0,0), 90)

            rings = rings.union(ring.translate((0,0,(i*self.story_height))))
            if i >2:
                break
            
        rings = (
            rings
            .translate((0,0,self.story_height-self.bp_platform.height))
            .rotate((0,0,1),(0,0,0),45)
        )

        return rings

    def build(self) -> cq.Workplane:
        super().build()
        # I need to implement this yet, but that's for another time
        rail = self.bp_rail.build()
        scene = cq.Workplane("XY")

        if self.render_can:
            can = self.bp_can.build()
            scene = scene.union(can.translate((0,0,self.bp_can.height/2)))

        if self.render_story_proxy and self.story_proxy:
            stories = self.__build_story_proxies()
            scene = scene.add(stories)
            
        if self.render_platforms:
            platform = self.bp_platform.build()
            platforms = self.__build_platforms(platform)
            scene = scene.union(platforms)
            
        if self.render_rings:
            rings = self.__build_rings()
            scene = scene.union(rings)

        z_translate = -(self.height/2)
        
        if self.stories * self.story_height > self.height:
            z_translate = -((self.stories * self.story_height)/2)
            
        return scene.translate((0,0,z_translate))
    