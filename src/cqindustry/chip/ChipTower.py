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
        #print('make rings')
        if type(self.bp_ring) is tuple: # multiple blueprints
            #print("dealing ith multiple blueprints")
            for blueprint in self.bp_ring: #type:ignore
                #print('calling make for rung blueprint')
                blueprint.cut_diameter = self.bp_can.diameter + self.can_diameter_padding
                blueprint.ladder_height = self.story_height - self.bp_platform.height
                blueprint.make()
            #print('exited multiple blueprints loop')
        else: # single blueprint
            #print("dealing with single blueprint")
            self.bp_ring.cut_diameter = self.bp_can.diameter + self.can_diameter_padding
            self.bp_ring.ladder_height = self.story_height - self.bp_platform.height 
            self.bp_ring.make()
            #print("exited single blueprints")


    def make(self, parent = None):
        super().make(parent)

        self._make_can()
        self.__make_story_proxy()
        #print("_make_ring")
        self._make_ring()
        
        #print("_make_platform")
        self._make_platform()

        #print("bp_rail.make")
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
            #print("multiple ring blueprints")
            for blueprint in self.bp_ring: #type: ignore
                #print("append ring blueprints")
                built_rings.append(blueprint.build)
        else:
            #print("sibgle ring blueprints")
            built_rings.append(self.bp_ring.build)

        # worked way easier than I thought
        rings = cq.Workplane("XY")
 
        for i in range(self.stories):
            #print('build ring template')
            index = i % len(built_rings)
            #print(f'invoke ring {index}')
            ring = built_rings[index]().rotate((1,0,0),(0,0,0),180)
            #print(f'invokeed ring {index}')
            
            if self.ring_alternate_rotate and i % 2 == 1:
                ring = ring.rotate((0,0,1),(0,0,0), 90)

            rings = rings.union(ring.translate((0,0,(i*self.story_height))))
            if i >2:
                break

        #print('rings have been made')
            
        rings = (
            rings
            .translate((0,0,self.story_height-self.bp_platform.height))
            .rotate((0,0,1),(0,0,0),45)
        )

        #print('rings have been placed')

        return rings

    def build(self) -> cq.Workplane:
        super().build()
        # I need to implement this yet, but that's for another time
        rail = self.bp_rail.build()
        scene = cq.Workplane("XY")

        #print("I made it bo build")

        #print("render_can")
        if self.render_can:
            can = self.bp_can.build()
            scene = scene.union(can.translate((0,0,self.bp_can.height/2)))

        print("render_story_proxy")
        if self.render_story_proxy and self.story_proxy:
            stories = self.__build_story_proxies()
            scene = scene.add(stories)

        #print("render_platforms")    
        if self.render_platforms:
            platform = self.bp_platform.build()
            platforms = self.__build_platforms(platform)
            scene = scene.union(platforms)
            
        #print("render_rings")      
        if self.render_rings:
            rings = self.__build_rings()
            #print("union rings") 
            # this is a mean little bug.. this should be a union but in cadquery 25.2 it breaks with ring types.
            # The union operation works when run in the debugger but not from the command line proper, implies a race / threading issue that's eating an error.
            scene = scene.add(rings)

        z_translate = -(self.height/2)
        
        #print("stories") 
        if self.stories * self.story_height > self.height:
            z_translate = -((self.stories * self.story_height)/2)
            
        return scene.translate((0,0,z_translate))
    