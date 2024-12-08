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
import math
from cqterrain.stairs import IndustrialStairs as Stairs
from cqterrain import tile
from cadqueryhelper import Base, wave

class StairLift(Base):
    def __init__(
            self,
            length:float = 150,
            width:float = 75,
            height:float = 75,
            overlook_tile_size:float = 10,
            walkway_tile_size:float = 27,
            tile_height:float = 2,
            stair_count:int = 9,
            stair_chamfer:float|None = None
        ):
        super().__init__()
        # parameters
        self.length:float = length
        self.width:float = width
        self.height:float = height
        
        self.overlook_tile_size:float = overlook_tile_size
        self.walkway_tile_size:float = walkway_tile_size
        self.tile_height:float = tile_height
        
        self.face_cut_width:float = 4
        self.face_cut_padding:float = 3
        self.wave_function = wave.square #wave.triangle wave.sine
        self.wave_segment_length:float = 5
        
        # Blueprints
        self.bp_stairs = Stairs(
            stair_count=stair_count, 
            stair_chamfer=stair_chamfer
        )
        
        #parts
        self.stairs = None
        self.overlook = None
        self.walkway = None
        self.wall_cut = None
        
    def __make_stairs(self):
        stair_length:float = self.length/2
        stair_width:float = self.width/2
        
        self.bp_stairs.length = stair_length
        self.bp_stairs.width = stair_width
        self.bp_stairs.height = self.height
        self.bp_stairs.make()
        
    def _make_tile(self, tile_size):
        result = tile.slot_diagonal(
            tile_size = tile_size,
            height = self.tile_height,
            slot_width = 2,
            slot_height = self.tile_height,
            slot_length_padding = 7,
            slot_width_padding = 2,
            slot_width_padding_modifier = .25
        )
        return result
    
    def _make_floor_tiles(self, length, width, tile_size, padding = 2):
        floor_tile = self._make_tile(tile_size)
        def add_tile(loc:cq.Location)->cq.Shape:
            return floor_tile.val().located(loc)#type:ignore
        
        padded_tile_size = tile_size+2
        x_count = math.floor((length) / padded_tile_size)
        y_count = math.floor((width) / padded_tile_size)
        
        floor_tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = padded_tile_size, 
                ySpacing = padded_tile_size,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_tile)
        )
        
        outline = cq.Workplane("XY").box(
            x_count*padded_tile_size+padding*1+1, 
            y_count*padded_tile_size+padding*1, 
            self.tile_height
        )
        return floor_tiles, outline
    
    def _calculate_panel_height(self):
        return self.height - self.tile_height - self.face_cut_padding*2
    
    def __make_overlook(self):
        floor_tiles, outline = self._make_floor_tiles(
            self.length/2, 
            self.width/2, 
            self.overlook_tile_size
        )
        
        overlook = cq.Workplane("XY").box(
            self.length/2,
            self.width/2,
            self.height
        )
        
        overlook = overlook.faces("<Z").shell(-self.face_cut_width-1)

        
        # --- face cuts
        panel_y_length = self.length/2 - self.face_cut_padding*2
        panel_height = self._calculate_panel_height()
        
        face_y_cut = cq.Workplane("XY").box(
            panel_y_length,
            self.face_cut_width,
            panel_height
        )
        
        face_x_cut = cq.Workplane("XY").box(
            self.face_cut_width,
            self.width/2 - self.face_cut_padding,
            panel_height
        )
        
        cut_face_y_tranlslate = self.width/4-self.face_cut_width/2
        cut_face_z_translate = self.tile_height/2
        
        side_cut_face_x_translate = self.length/4 - self.face_cut_width/2
        side_cut_face_y_translate = self.face_cut_padding/2
        overlook = (
            overlook
            .cut(outline.translate((0,0,self.height/2 - self.tile_height/2)))
            .union(floor_tiles.translate((0,0,self.height/2 - self.tile_height/2)))
            .cut(face_y_cut.translate((0,-cut_face_y_tranlslate,-cut_face_z_translate)))
            .cut(face_x_cut.translate((-side_cut_face_x_translate,side_cut_face_y_translate,-cut_face_z_translate)))
        )
        
        # --- wave paneling
        wave_panel_y = self.wave_function(
            length = panel_y_length,
            width = self.face_cut_width-1,
            height = panel_height,
            segment_length = self.wave_segment_length,
            inner_width = .5
        ).rotate((1,0,0),(0,0,0),180)
        
        
        overlook = (
            overlook
            .union(wave_panel_y.translate((0,-cut_face_y_tranlslate+1,-cut_face_z_translate)))
        )
        
        self.overlook = overlook
        
    def __make_walkway(self):
        floor_tiles, outline = self._make_floor_tiles(
            self.length, 
            self.width/2,
            self.walkway_tile_size
        )
        walkway = cq.Workplane("XY").box(
            self.length,
            self.width/2,
            self.height
        )
        
        #shell
        walkway = walkway.faces("<Z").shell(-self.face_cut_width-1)
        
        panel_height = self._calculate_panel_height()
        
        face_y_cut = cq.Workplane("XY").box(
            self.length - self.face_cut_padding*2,
            self.face_cut_width,
            panel_height 
        )
        
        face_x_cut = cq.Workplane("XY").box(
            self.face_cut_width,
            self.width/2 - self.face_cut_padding,
            panel_height
        )
        
        face_x_cut_2 = cq.Workplane("XY").box(
            self.face_cut_width,
            self.width/2 - self.face_cut_padding*2,
            self.height - self.tile_height - self.face_cut_padding*2
        )
        
        side_cut_face_x_translate = self.length/2 - self.face_cut_width/2
        side_cut_face_y_translate = self.face_cut_padding/2
        
        walkway = (
            walkway
            .cut(outline.translate((0,0,self.height/2 - self.tile_height/2)))
            .union(floor_tiles.translate((0,0,self.height/2 - self.tile_height/2)))
            .cut(face_y_cut.translate((0,self.width/4-self.face_cut_width/2,- self.tile_height/2)))
            .cut(face_x_cut.translate((-side_cut_face_x_translate, -side_cut_face_y_translate,- self.tile_height/2)))
            .cut(face_x_cut_2.translate((side_cut_face_x_translate, 0,- self.tile_height/2)))
        )
        
        # --- wave panels
        wave_panel_y = self.wave_function(
            length = self.length - self.face_cut_padding*2,
            width = self.face_cut_width-1,
            height = panel_height,
            segment_length = self.wave_segment_length,
            inner_width = .5
        )
        
        walkway = walkway.union(wave_panel_y.translate((0,self.width/4-self.face_cut_width/2-1,- self.tile_height/2)))
        
        self.walkway = walkway
        
    def __make_wall_cut(self):
        wall_cut = (
            cq.Workplane("XY")
            .box((self.length/2)-(self.face_cut_width+1)*2,self.width-(self.face_cut_width+1)*2,self.height-(self.face_cut_width))
        ).translate((-1*(self.length/4),0,-1*(self.face_cut_width-1)))
        self.wall_cut = wall_cut
        
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_stairs()
        self.__make_overlook()
        self.__make_walkway()
        self.__make_wall_cut()
        
    def build(self):
        super().build()
        
        
        scene = cq.Workplane("XY")

        if self.walkway:
            scene = (
                scene
                .union(self.walkway.translate((0,self.width/4,0)))
            )

        if self.overlook:
            scene = (
                scene
                .union(self.overlook.translate((-self.length/4,-self.width/4,0)))
            )

        if self.bp_stairs:
            self.stairs = self.bp_stairs.build()
            scene = (
                scene
                .union(self.stairs.translate((self.bp_stairs.length/2,-1*(self.bp_stairs.width/2),0)))
            )

        if self.wall_cut:
            scene = (
                scene
                .cut(self.wall_cut)
            )

        panel_height = self._calculate_panel_height()
        wave_panel_x = self.wave_function(
            length = self.width - self.face_cut_padding*2,
            width = self.face_cut_width-1,
            height = panel_height,
            segment_length = self.wave_segment_length,
            inner_width = .5
        ).rotate((1,0,0),(0,0,0),180).rotate((0,0,1),(0,0,0),90)
        
        side_cut_face_x_translate = self.length/2 - self.face_cut_width
        #side_cut_face_y_translate = self.face_cut_padding/2
        
        scene = scene.add(wave_panel_x.translate((
            -side_cut_face_x_translate-1,
            0,
            -1*(self.tile_height/2)
        )))
        
        #return self.walkway
        return scene