from kivy.uix.widget import Widget
from kivy.uix.listview import ListView

class Placeholder(Widget):
    index = NumericProperty(-1)
    
class DragNDropListView(ListView):
	"""This is an altered ListView to allow Drag 'N' Drop functionality."""
    placeholder = ObjectProperty(None, allownone=True)
    
    def deparent(self, widget):
        container = self.container
        placeholder = self.placeholder = Placeholder(size=widget.size,
                                                     size_hint_y=None,
                                                     index=widget.index,
                                                     opacity=0.0)

        ix = container.children.index(widget)
        container.remove_widget(widget)
        container.add_widget(placeholder, ix)
        widget.size_hint_x = None
        container.get_root_window().add_widget(widget)
        return

    def reparent(self, widget):
        placeholder = self.placeholder
        if not placeholder:
            return

        container = self.container
        if placeholder.collide_widget(widget):
            ix = container.children.index(placeholder)
            container.remove_widget(placeholder)
            container.get_root_window().remove_widget(widget)
            container.add_widget(widget, ix)
            widget.size_hint_x = 1.
            widget.index = placeholder.index
            self.placeholder = None
