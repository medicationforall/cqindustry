import cadquery as cq
from cadqueryhelper import Base

class Container(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 126
        self.width:float = 114
        self.height:float = 65
        
        self.top_length:float = 111
        self.top_width:float = 93
        self.top_fillet:float = 8
        self.side_fillet:float = 9
        
        self.material_width:float = 1
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.body:cq.Workplane|None = None
        self.shell:cq.Workplane|None = None
        
    def make_outline(self):
        length_inset = (self.length - self.top_length)/2
        width_inset = (self.width - self.top_width) /2
        body = (
            cq.Workplane("XY" )
            .wedge(
                self.length,
                self.height,
                self.width,
                length_inset, #length
                width_inset, # width
                self.length - length_inset,
                self.width - width_inset
            ).rotate((1,0,0),(0,0,0),-90)
        )
        
        body_faces = body.faces()[0].edges()[1,3].fillet(self.side_fillet)
        body_faces = body_faces.faces()[6].edges()[1,3].fillet(self.side_fillet)
        
        body = body_faces.faces("Z").fillet(self.top_fillet)
        
        #show_object(body)
        self.outline = body.translate((0,0,self.height/2))
        
    def make_body(self):
        length_inset = (self.length - self.top_length)/2
        width_inset = (self.width - self.top_width) /2
        body = (
            cq.Workplane("XY" )
            .wedge(
                self.length,
                self.height,
                self.width,
                length_inset, #length
                width_inset, # width
                self.length - length_inset,
                self.width - width_inset
            ).rotate((1,0,0),(0,0,0),-90)
        )
        
        body_faces = body.faces()[0].edges()[1,3].fillet(self.side_fillet)
        body_faces = body_faces.faces()[6].edges()[1,3].fillet(self.side_fillet)
        
        body = body_faces.faces("Z").fillet(self.top_fillet)
        
        #show_object(body)
        self.body = body.translate((0,0,self.height/2))
        
    def make_shell(self):
        length = self.length - self.material_width*2
        width = self.width - self.material_width*2
        height = self.height - self.material_width*1
        top_length = self.top_length - self.material_width*2
        top_width = self.top_width - self.material_width*2
        
        length_inset = (length - top_length)/2
        width_inset = (width - top_width) /2
        
        shell = (
            cq.Workplane("XY" )
            .wedge(
                length,
                height,
                width,
                length_inset, #length
                width_inset, # width
                length - length_inset,
                width - width_inset
            ).rotate((1,0,0),(0,0,0),-90)
        )
        
        shell_faces = shell.faces()[0].edges()[1,3].fillet(self.side_fillet)
        shell_faces = shell_faces.faces()[6].edges()[1,3].fillet(self.side_fillet)
        
        shell = shell_faces.faces("Z").fillet(self.top_fillet)
        
        self.shell = shell.translate((0,0,height/2))
        
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_body()
        self.make_shell()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
            
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.body:
            part = part.add(self.body)
            
        if self.shell:
            part = part.cut(self.shell)
        
        return part