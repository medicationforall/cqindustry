import cadquery as cq
from cadqueryhelper import Base
from cqterrain.wall import BaseWall
from . import CorridorWall

class CorridorWallGreebled(Base):
    def __init__(self):
        #parameters        
        self.length:float = 75
        self.width:float = 12
        self.height:float = 75
        self.window_y_translate:float = 4
        
        #blueprints
        self.bp_wall:BaseWall = CorridorWall()
        self.bp_window:Base|None = None
        
    def make_wall(self):
        if self.bp_wall:
            length = self.length
            width = self.width
            height = self.height
            
            self.bp_wall.length = length
            self.bp_wall.width = width
            self.bp_wall.height = height
            self.bp_wall.make()
            
    def make_window(self):
        if self.bp_window:
            self.bp_window.make()
        
    def make(self):
        super().make()
        self.make_wall()
        self.make_window()
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_wall:
            wall = self.bp_wall.build()
            part = part.add(wall)
            
        if self.bp_window:
            window  = self.bp_window.build()
            cut_window = self.bp_window.build_outline()
            
            y_translate = self.window_y_translate
            part = part.cut(cut_window.translate((0,y_translate,0)))
            part = part.add(window.translate((0,y_translate,0)))
            
        return part