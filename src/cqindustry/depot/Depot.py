import cadquery as cq
from cadqueryhelper import Base
import math
from . import Container
from cqterrain import greeble
from cqterrain.Ladder import Ladder
from cqterrain.window import ShutterWindow
from cqterrain.greeble import FanIndustrial
from cqterrain.door import DoorDouble
from cqterrain.door import DoorSingle
from cqterrain.door import Frame
from cqterrain.roof import angle
from cadqueryhelper.shape import triangle_right


def _make_rung(length, width, height):
    rung = cq.Workplane("XY").box(length+1.5, width ,height)
    rung = rung.edges("X").fillet(.909999)
    return rung

def _make_side_rail(width, height, rail_width):
    rail = (cq.Workplane("XY")
            .box( height, rail_width, width)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((1,0,0),(0,0,0),90)
            )
    rail = rail.faces("<Y").edges("X").fillet(3)
    return rail

#------------------

class Depot(Base):
    def __init__(self):
        super().__init__()
        #parameters
        #self.length:float = 30
        #self.width:float = 25
        #self.height:float = 60
        
        self.bp_body = Container()
        self.bp_fan = FanIndustrial()
        
        self.bp_ladder = Ladder()
        self.bp_ladder.make_rung = _make_rung
        self.bp_ladder.make_side_rail = _make_side_rail
        
        self.bp_window = ShutterWindow()
        
        self.bp_double_door = DoorDouble()
        self.bp_connector = Frame()
        
        self.bp_single_door = DoorSingle()
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.vent:cq.Workplane|None = None
        
    def calculate_width_angle(self):
        height = self.bp_body.height
        length = (self.bp_body.width - self.bp_body.top_width)/2
        r_angle = 360 - 90 - angle(length,height)
        
        return r_angle
    
    def calculate_length_angle(self):
        height = self.bp_body.height
        length = (self.bp_body.length - self.bp_body.top_length)/2
        r_angle = 360 - 90 - angle(length,height)
        
        return r_angle
    
    def make_fan(self):
        bp_fan = self.bp_fan
        bp_fan.height = 12
        bp_fan.diameter = 25
        bp_fan.fan_cylinder_diameter = 7
        bp_fan.blade_count = 6
        bp_fan.shift_rotate = 0
        bp_fan.blade_width = 2
        bp_fan.blade_rotate = 30
        self.bp_fan.make()
        
    def make_ladder(self):
        height = self.bp_body.height
        length = (self.bp_body.width - self.bp_body.top_width)/2
        hyp = math.hypot(length, height)
        
        bp_ladder = self.bp_ladder
        bp_ladder.height = hyp - self.bp_body.top_fillet
        bp_ladder.length = 20
        bp_ladder.make()
        
    def make_window(self):
        bp_window = self.bp_window
        bp_window.height = 30
        bp_window.pane_count = 2
        bp_window.frame_width = 3
        bp_window.louver_count = 7
        bp_window.louver_rotate = 16
        
        self.bp_window.make()
        
    def make_double_door(self):
        bp_door = self.bp_double_door
        bp_door.length = 55
        bp_door.width = 4
        bp_door.height = 55
        bp_door.window_length = 8
        bp_door.window_height = 12
        bp_door.window_z_translate = 38
        bp_door.door_width = 1.5
        bp_door.make()
        
    def make_double_connector(self):
        self.bp_connector.length = 55+2
        self.bp_connector.width = 8
        self.bp_connector.frame_width = 4
        self.bp_connector.height = 55 + 1
        self.bp_connector.make()
        
    def make_single_door(self):
        bp_door = self.bp_single_door
        bp_door.length = 30
        bp_door.height = 45
        bp_door.make()
        
    def make_vent(self):
        tall_vent = greeble.vent(
            length = 40,
            width = 15,
            height = 2,
            segment_length = 2,
            inner_width = 1,
            frame_width = 3.5,
            chamfer = 2
        )
        
        self.vent = tall_vent
        
    def make(self):
        super().make()
        self.bp_body.make()
        
        self.make_fan()
        self.make_ladder()
        self.make_window()
        self.make_double_door()
        
        self.make_double_connector()
        self.make_single_door()
        self.make_vent()
        
    def build_fan(self):
        part = cq.Workplane("XY")
        
        if self.bp_fan:
            fan = self.bp_fan.build()
            z_translate = self.bp_body.height
            x_translate = self.bp_body.top_length/2 - self.bp_body.top_fillet - self.bp_fan.diameter/2
            y_translate = self.bp_fan.diameter/2
            part = (
                part
                .add(fan.translate((-x_translate,y_translate,z_translate)))
                .add(fan.translate((-x_translate,-y_translate,z_translate)))
            )
        
        return part
        
    def build_ladder(self):
        part = cq.Workplane("XY")
        if self.bp_ladder:
            
            height = self.bp_body.height
            length = (self.bp_body.width - self.bp_body.top_width)/2
            r_angle = self.calculate_width_angle()
            #log(f'{self.bp_body.width=}, {self.bp_body.top_width=}, {length=}, {height}, {r_angle=}')
            
            ladder = (
                self.bp_ladder.build()
                .rotate((1,0,0),(0,0,0),-r_angle)
                .translate((0,length/2,self.bp_ladder.height/2))
            )
            
            ex_triangle = triangle_right(
                length = length, 
                width = height, 
                height= 5
            ).rotate((1,0,0),(0,0,0),-90).rotate((0,0,1),(0,0,0),-90).translate((-5/2,0,0))
            #part = part.add(ex_triangle.translate((0,self.bp_body.width/2-length,0)))

            #log(r_angle)
            x_translate = self.bp_body.length/5
            y_translate = self.bp_body.width/2-length + self.bp_ladder.width/2+.5
            part = part.add(ladder.translate((x_translate,y_translate,0)))
            
        return part
    
    def build_window(self):
        part = cq.Workplane("XY")
        if self.bp_window:
            r_angle = self.calculate_width_angle()-180
            length = (self.bp_body.width - self.bp_body.top_width)/2
            
            shutter_window = self.bp_window.build().rotate((1,0,0),(0,0,0),r_angle)
            
            part = part.add(shutter_window.translate((
                0,
                -self.bp_body.width/2+length/2,
                self.bp_body.height/2
            )))
            
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_body:
            body = self.bp_body.build()
            part = part.add(body)
            
        if self.bp_fan:
            fan = self.build_fan()
            part = part.add(fan)
        
        if self.bp_ladder:
            ladder = self.build_ladder()
            part = part.add(ladder)
            
        if self.bp_window:
            window = self.build_window()
            part = part.add(window)
            
        if self.bp_double_door:
            double_door = self.bp_double_door.build().rotate((0,0,1),(0,0,0),90)
            part = part.add(double_door.translate((
                self.bp_body.length/2 +self.bp_double_door.width/2,
                0,
                0
            )))
            
        if self.bp_connector:
            connector = (
                self.bp_connector
                .build()
                .rotate((0,0,1),(0,0,0),90)
            ).translate((self.bp_body.length/2-self.bp_connector.width/2,0,0))
            
            frame_cut = (
                self.bp_connector.frame_cut
                .rotate((0,0,1),(0,0,0),90)
            ).translate((self.bp_body.length/2-self.bp_connector.width/2,0,self.bp_connector.height/2))
            
            body_outline = self.bp_body.build_outline()
            
            #show_object(body_outline)
            connector = connector.cut(body_outline)
            
            part = (
                part
                .add(connector)
                .cut(frame_cut)
            )
            
        if self.bp_single_door:
            r_angle = self.calculate_width_angle()-180
            x_translate = self.bp_body.length/5
            y_translate = self.bp_body.width/2
            z_translate = 0#self.bp_single_door.height/2
            
            #log(f'{r_angle=}')
            single_door = (
                self.bp_single_door.build()
                .translate((0,0,z_translate))
                .rotate((1,0,0),(0,0,0),r_angle)
                .rotate((0,0,1),(0,0,0),180)
            )
            

            part = part.add(single_door.translate((-x_translate,y_translate,0)))
            
        if self.vent:
            r_angle = self.calculate_length_angle()-180
            #log(f'{r_angle=}')
            
            vent = (
                self.vent
                .rotate((0,1,0),(0,0,0),-90)
                .translate((0,0,self.bp_body.height/2))
                .rotate((0,1,0),(0,0,0),r_angle)
                .rotate((0,0,1),(0,0,0),180)
            ).translate((-self.bp_body.length/2,0,))#,))
            
            
            y_translate = self.bp_body.width /6
            part = (
                part
                .add(vent.translate((0,y_translate,0)))
                .add(vent.translate((0,-y_translate,0)))
            )
        
        return part
    
    def build_plate(self):
        part = cq.Workplane("XY")
        
        if self.bp_fan:
            fan = self.bp_fan.build()
            part = (
                part
                .add(fan)
                .add(fan.translate((0,30,0)))
            )
            
        if self.bp_ladder:
            ladder = self.bp_ladder.build().rotate((1,0,0),(0,0,0),90)
            part = part.add(ladder.translate((-25,15,self.bp_ladder.width/2)))
            
        if self.bp_window:
            window = self.bp_window.build().rotate((1,0,0),(0,0,0),90)
            part = part.add(window.translate((40,0,self.bp_window.width/2)))
            
        if self.bp_double_door:
            double_door = self.bp_double_door.build().rotate((1,0,0),(0,0,0),90)
            part = part.add(double_door.translate((0,-75,self.bp_double_door.width/2)))
            
        if self.bp_connector:
            connector = (
                self.bp_connector
                .build()
                .rotate((0,0,1),(0,0,0),90)
            ).translate((self.bp_body.length/2-self.bp_connector.width/2,0,0))
            
            frame_cut = (
                self.bp_connector.frame_cut
                .rotate((0,0,1),(0,0,0),90)
            ).translate((self.bp_body.length/2-self.bp_connector.width/2,0,self.bp_connector.height/2))
            
            body_outline = self.bp_body.build_outline()
            
            #show_object(body_outline)
            connector = (
                connector
                .cut(body_outline)
                .translate((-(self.bp_body.length/2-self.bp_connector.width/2),0,-self.bp_connector.height/2))
                .rotate((0,1,0),(0,0,0),-90)
                .translate((0,0,self.bp_connector.width/2))
            )
            
            part = (
                part
                .add(connector.translate((58,0,0)))
            )
            
        if self.bp_single_door:
            single_door = (
                self.bp_single_door.build()
                #.translate((0,0,z_translate))
                #.rotate((1,0,0),(0,0,0),r_angle)
                .rotate((1,0,0),(0,0,0),90)
            )
            
            part = (
                part
                .add(
                    single_door
                    .rotate((0,0,1),(0,0,0),90)
                    .translate((20,50,self.bp_single_door.width/2))
                    
                )
            )
            
        if self.vent:
            #r_angle = self.calculate_length_angle()-180
            #log(f'{r_angle=}')
            
            vent = (
                self.vent
                #.rotate((0,1,0),(0,0,0),-90)
                #.translate((0,0,self.bp_body.height/2))
                #.rotate((0,1,0),(0,0,0),r_angle)
                #.rotate((0,0,1),(0,0,0),180)
            )#.translate((-self.bp_body.length/2,0,))#,))
            
            
            #y_translate = self.bp_body.width /6
            part = (
                part
                .add(vent.translate((50,-40,2/2)))
                .add(vent.translate((50,-60,2/2)))
                #.add(vent.translate((0,-y_translate,0)))
            )
                
        return part