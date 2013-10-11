from kivy.uix.widget import Widget
from kivy.uix.listview import ListView

class Placeholder(Widget):
    index = NumericProperty(-1)
    
class DragNDropListView(ListView):
	"""This is an altered ListView to allow Drag 'N' Drop functionality."""
    placeholder = ObjectProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        self.register_event_type("on_drag_start")
        self.register_event_type("on_drag_finish")
        self.register_event_type("on_pos_change")
        self.register_event_type("on_motion_over")
        self.register_event_type("on_motion_out")
        super(DragNDropListView, self).__init__(**kwargs)

    def on_drag_start(self, widget):
        children = self.container.children
        adapter = self.adapter
        for child in children:
            if ((type(child) is not Widget) and child.is_selected):
                adapter.deselect_item_view(child)
                return

    def on_drag_finish(self, widget):
        pass

    def on_pos_change(self, widget):
        placeholder = self.placeholder
        if not placeholder:
            self.dispatch('on_motion_over', widget)
            return
        
        children = self.container.children
        p_ix = children.index(placeholder)

        for child in children:
            if (widget.collide_widget(child) and (child is not placeholder)):
                c_ix = children.index(child)

                if ((widget.center_y <= child.top) and (widget.center_y <= placeholder.y)) or ((widget.center_y >= child.y) and (widget.center_y >= placeholder.top)):
                    children.insert(c_ix, children.pop(p_ix))

                #maybe scroll here
                return
                
    def deparent(self, widget):
        container = self.container
        placeholder = self.placeholder = Placeholder(size=widget.size,
                                                     size_hint_y=None,
                                                     index=widget.index,
                                                     ix=widget.ix,
                                                     opacity=0.0)

        container.add_widget(placeholder, container.children.index(widget))
        container.remove_widget(widget)
        widget.size_hint_x = None
        container.get_root_window().add_widget(widget)
        return

    def reparent(self, widget):
        placeholder = self.placeholder
        if not placeholder:
            self.dispatch('on_motion_out', widget)
            return

        container = self.container
        if placeholder.collide_widget(widget):
            container.remove_widget(placeholder)
            container.get_root_window().remove_widget(widget)
            container.add_widget(widget, container.children.index(placeholder))
            widget.size_hint_x = 1.
            widget.ix = placeholder.ix
            self.placeholder = None

    def on_motion_over(self, widget):
        children = self.container.children
        
        for child in children:
        	if child.collide_point(*widget.center):
        		
        		if child.state <> 'down':
        			child.state = 'down'
        			
        	else:
        		child.state = 'normal'
    
    def on_motion_out(self, widget):
        pass
