from kivy.uix.relativelayout import RelativeLayout
from listbuttonbehaviors import *
from kivy.app import App

class ListItemButton_(SwipeableLeft, SwipeableRight, Clickable, TouchDownAndHoldable):
	pass

class Application(RelativeLayout):

    def __init__(self, **kwargs):
        self.size_hint = (.5, .3)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        super(Application, self).__init__(**kwargs)
 
        button = ListItemButton_()
        self.add_widget(button)

class TestApp(App):
    
    def build(self):
        ''''''
        app = Application()
        return app
 
if __name__ == '__main__':
    TestApp().run()
