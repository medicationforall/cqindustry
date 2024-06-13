import cadquery as cq
from cadqueryhelper import Base
import math

class GuardRail(Base):
    def __init__(self):
        #just guessing here will verify
        super().__init__()
        self.length:float = 75
        self.width:float = 3
        self.height:float = 25
        self.corner_chamfer:float = 5
        self.frame_padding:float = 4
        
        self.render_posts:bool = True
        self.post_length:float = 3
        self.post_width:float = 3
        self.post_spacing:float = 20
        
        self.render_clamps:bool = True
        self.clamp_length:float = 6
        self.clamp_width:float = 6
        self.clamp_height:float = 6
        self.clamp_padding:float = 2
        self.clamp_spacing:float = 30
        self.clamp_cut_width:float = 1
        self.clamp_cut_height:float = 3
        self.clamp_cut_z_translate:float = 0.5
        self.clamp_y_translate:float = -1
        
        # parts
        self.guard_rail:cq.Workplane|None = None
        self.rail_posts:cq.Workplane|None = None
        self.clamps:cq.Workplane|None = None
        
    def __make_rail(
            self, 
            length, 
            width, 
            height, 
            corner_chamfer=None
        ):
        rail = cq.Workplane("XY").box(
            length,
            width, 
            height
        )
        
        if corner_chamfer:
            if corner_chamfer < height/2 and corner_chamfer < length/2:
                rail = (
                    rail
                    .faces("Z or -Z")
                    .edges("Y")
                    .chamfer(corner_chamfer)
                )
            else:
                raise Exception(f"Rail Corner chamfer {corner_chamfer} is not less than length {length/2} or height {height/2}")
        return rail

    def __make_rail_frame(self):
        rail_outer = self.__make_rail(
            self.length, 
            self.width, 
            self.height, 
            self.corner_chamfer
        )
    
        rail_inner = self.__make_rail(
            self.length-self.frame_padding, 
            self.width, 
            self.height-self.frame_padding, 
            self.corner_chamfer
        )
        
        rail_frame = (
            cq.Workplane("XY")
            .add(rail_outer)
            .cut(rail_inner)
        )
        return rail_frame
    
    def _make_post(
            self,
            loc:cq.Location
        ) -> cq.Shape:
        post = cq.Workplane("XY").box(
            self.post_length,
            self.post_width,
            self.height
        )

        return post.val().located(loc) #type:ignore
    
    def __make_posts(self):
        post_count = math.floor(self.length / self.post_spacing)
        
        posts = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.post_spacing, 
                ySpacing = 1,
                xCount = post_count, 
                yCount= 1, 
                center = True)
            .eachpoint(callback = self._make_post)
        )
        
        self.posts = posts
        
    def _make_clamp(
            self,
            loc: cq.Location
        ) -> cq.Shape:
        clamp = cq.Workplane("XY").box(
            self.clamp_length,
            self.clamp_width,
            self.clamp_height
        )
        
        clamp_cut = cq.Workplane("XY").box(
            self.clamp_length,
            self.clamp_width-self.clamp_cut_width,
            self.clamp_height-self.clamp_cut_height
        ).translate((0,self.clamp_cut_width/2,-1*self.clamp_cut_z_translate))
        
        clamp_combined = clamp.cut(clamp_cut).translate((0,self.clamp_y_translate,0))

        return clamp_combined.val().located(loc) #type: ignore
        
    def __make_clamps(self):
        clamp_count = math.floor(self.length / self.clamp_spacing)
        
        clamps = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.clamp_spacing, 
                ySpacing = 1,
                xCount = clamp_count, 
                yCount= 1, 
                center = True)
            .eachpoint(callback = self._make_clamp)
        )
        
        self.clamps = clamps
        
    def make(self, parent = None):
        super().make(parent)
        rail = self.__make_rail_frame()
        self.guard_rail = rail
        
        if self.render_posts:
            self.__make_posts()
            
        if self.render_clamps:
            self.__make_clamps()
        
    def build(self) -> cq.Workplane:
        super().build()
        
        scene = (
            cq.Workplane("XY")
            .union(self.guard_rail)
        )
        
        if self.render_posts and self.posts:
            scene = scene.union(self.posts)
            
        if self.render_clamps and self.clamps:
            clamps_z_translate = self.height/2+self.clamp_height/2-self.frame_padding/2
            scene = scene.union(self.clamps.translate((
                0,
                0,
                -1*clamps_z_translate
            )))
            
        return scene