from direct.showbase.ShowBase import ShowBase, DirectObject
from view.AxisTripod import AxisTripod


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.terrain = loader.loadModel('models/environment')
        self.terrain.reparentTo(render)

        self._tripod = AxisTripod(self)
        # make sure the tripod model follows the orientation of the terrain
        self._tripod.model.set_compass(self.terrain)


app = MyApp()
app.run()