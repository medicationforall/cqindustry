import cadquery as cq
from cqterrain import Ladder
from cqterrain import tile

class Conduit(Ladder):
    def __init__(self):
        super().__init__()
        self.frame:float = 1
        self.frame_depth:float = 3
        self.pipe_count:int = 2
        self.pipe_radius:float = 4
        self.pipe_inner_radius:float = 2
        self.segment_length:float = 6
        self.space:float = 4
        self.pipe_padding:float = 1

        #shapes
        self.conduit:cq.Workplane|None = None

    def _make_ladder(self):
        #print("make ring conduit ladder")
        ladder = tile.conduit(
            length = self.height,
            width = self.length,
            height = self.width,
            frame = self.frame, 
            frame_depth = self.frame_depth, 
            pipe_count = self.pipe_count, 
            radius = self.pipe_radius, 
            inner_radius = self.pipe_inner_radius, 
            segment_length = self.segment_length, 
            space = self.space, 
            pipe_padding = self.pipe_padding 
        ).rotate((0,0,1),(0,0,0),90).rotate((1,0,0),(0,0,0),-90)
        
        #print('position the ladder')
        self.conduit = ladder
        #ladder = ladder.translate((
        #    0,
            #self.cut_diameter/2+.6,
        #    self.ladder_height/2
        #))

    def make(self, parent=None):
        self.parent = parent
        self.make_called = True
        #super().make(parent)
        self.outline = cq.Workplane("XY").box(
            self.length, 
            self.width, 
            self.height
        )
        self._make_ladder()
        #self.__make_rails()
        #self.__make_rung()
        #self.__make_rungs()

    def build(self) -> cq.Workplane:
        if self.make_called == False:
            raise Exception('Make has not been called')
        #super().build()
        combined = cq.Workplane("XY")
        combined = combined.union(self.conduit)
        #.union(self.side_rails[0])
        #.union(self.side_rails[1])
        #.union(self.rungs)
        #)

        return combined