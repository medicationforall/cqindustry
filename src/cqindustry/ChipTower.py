# going to make an orchestrator class

import cadquery as cq
from cadqueryhelper import Base
from cqindustry import ChipCan, Ring, Platform, GuardRail

class ChipTower(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length = 150
        self.width = 150
        self.height = 225

        self.stories = 2
        self.story_height = 75
        self.can_diameter_padding = 1

        self.render_can = True
        self.render_story_proxy = True
        self.render_platforms = True
        self.render_rings = True
        self.render_rail = True

        #blueprints
        self.bp_can = ChipCan()
        self.bp_ring = Ring()
        self.bp_platform = Platform()
        self.bp_rail = GuardRail()

        # shapes
        self.story_proxy = None
        self.__rings = None
        self.__rails = None

    def _make_can(self):
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

    def make(self, parent = None):
        super().make(parent)

        self._make_can()
        self.__make_story_proxy()
        self.bp_ring.make()
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

    def build(self) -> cq.Workplane:
        super().build()

        can = self.bp_can.build()
        ring = self.bp_ring.build()
        rail = self.bp_rail.build()

        scene = cq.Workplane("XY")

        if self.render_can and can:
            scene = scene.union(can)

        if self.render_story_proxy and self.story_proxy:
            stories = self.__build_story_proxies()
            scene = scene.add(stories)

        if self.render_platforms:
            platform = self.bp_platform.build()
            platforms = self.__build_platforms(platform)
            scene = scene.union(platforms)

        return scene