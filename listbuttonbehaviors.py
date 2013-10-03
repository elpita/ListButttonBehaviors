from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, OptionProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.lang import Builder

class Base(RelativeLayout):
    background_normal = StringProperty('atlas://data/images/defaulttheme/button')
    background_down = StringProperty('atlas://data/images/defaulttheme/button_pressed')
    text = StringProperty('')
    state = OptionProperty('normal', options=('normal'))

    def on_touch_down(self, touch):
        touch.grab(self)
        touch.ud[self] = True
        return True

    def on_state(self, *args):
        pass

class Clickable(Base):
    state = OptionProperty('normal', options=('normal', 'down'))    
    _press_ = ObjectProperty(None)
    _release_ = ObjectProperty(None)
    press_timeout = NumericProperty(0.0625)
    relase_timeout = NumericProperty(0.15)

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self._press_ = Clock.create_trigger(self.trigger_press, self.press_timeout)
        self._release_ = Clock.create_trigger(self.trigger_release, self.release_timeout)
        super(Clickable, self).__init__(**kwargs)

    def _do_press(self):
        self.state = 'down'

    def _do_release(self):
        self.state = 'normal'

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False

        if self.state == 'normal':
            super(Base, self).on_touch_down(touch)
            self._press_()

        return super(Clickable, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'down':
                self._do_release()
                super(Base, self).on_touch_up(touch)
                touch.ungrab(self)
                self._release_()

        return super(Clickable, self).on_touch_up(touch)

    def on_press(self):
        pass

    def on_release(self):
        pass

    def trigger_press(self, dt):
        if self.state == 'normal':
            self._do_press()
            return self.dispatch('on_press_callback')
        else:
            return False

    def trigger_release(self, dt):
        if self.state == 'down':
            return self.dispatch('on_release')
        else:
            return False
        
class SwipeableLeft(Base):    
    state = OptionProperty('normal', options=('normal', 'swiped left'))
    been_swiped_left = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SwipeableLeft, self).__init__(**kwargs)
        self.register_event_type('on_swiped_left_in')
        self.register_event_type('on_swiped_left_out')
    
    def on_state(self, instance, value):
        if ((value <> 'swiped left') and instance.been_swiped_left):
            instance.dispatch('on_swiped_left_in')
            instance.been_swiped_left = False

        elif value == 'swiped left':
            instance.dispatch('on_swiped_left_out')
            instance.been_swiped_left = True

        return super(SwipeableLeft, self).on_state(instance, value)

    def on_touch_down(self, touch):
        if self.state == 'swiped left':
            super(Base, self).on_touch_down(touch)

            if not self.been_swiped_left:
                self.state = 'normal'
            return True

        else:
            return super(SwipeableLeft, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        
        if touch.grab_current is self:
            assert(self in touch.ud)
            super(Base, self).on_touch_move(touch)

            if ((touch.dx < -20) and not self.been_swiped_left):
                touch.ungrab(self)
                self.state = 'swiped left'
                return True

        return super(SwipeableLeft, self).on_touch_move(touch)

    def on_swiped_left_in(self):
        pass

    def on_swiped_left_out(self):
        pass

class SwipeableRight(Base):
    state = OptionProperty('normal', options=('normal', 'swiped right'))
    been_swiped_right = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SwipeableRight, self).__init__(**kwargs)
        self.register_event_type('on_swiped_right_in')
        self.register_event_type('on_swiped_right_out')

    def on_state(self, instance, value):
        if ((value <> 'swiped right') and instance.been_swiped_right):
            instance.dispatch('on_swiped_right')

        elif value == 'swiped right':
            instance.dispatch('on_swiped_right')

        return super(SwipeableRight, self).on_state(instance, value)

    def on_touch_down(self, touch):
        if self.state == 'swiped right':
            super(Base, self).on_touch_down(touch)

            if not self.been_swiped_left:
                self.state = 'normal'
            return True

        else:
            return super(SwipeableRight, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        if touch.grab_current is self:
            assert(self in touch.ud)
            super(Base, self).on_touch_move(touch)

            if ((touch.dx > 20) and not self.been_swiped_right):
                self.state = 'swiped right'
                touch.ungrab(self)
                return True

        return super(SwipeableRight, self).on_touch_move(touch)

    def on_swiped_right_in(self):
        pass

    def on_swiped_right_out(self):
        pass

class DoubleClickable(Base):
    state = OptionProperty('normal', options=('normal', 'double clicked'))
    been_double_clicked = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(DoubleClickable, self).__init__(**kwargs)
        self.register_event_type('on_double_click_in')
        self.register_event_type('on_double_click_out')

    def on_state(self, instance, value):
        if ((value <> 'double clicked') and instance.been_double_clicked):
            instance.dispatch('on_double_click_out')

        elif ((value == 'double clicked')):
            instance.dispatch('on_double_click_in')
        
        return super(DoubleClickable, self).on_state(instance, value)
    
    def on_touch_down(self, touch):            

        if self.state == 'double clicked':
            super(Base, self).on_touch_down(touch)

            if not self.been_double_clicked:
                self.state = 'normal'

            return True

        else:
            return super(DoubleClickable, self).on_touch_down(touch)
        
    def on_touch_up(self, touch):

        if touch.grab_current is self:
            assert(self in touch.ud)
            super(Base, self).on_touch_up(touch)

            if (touch.is_double_tap and (touch.double_tap_time < .250)):
                touch.ungrab(self)
                self.state = 'double clicked'

                return True
            
        return super(DoubleClickable, self).on_touch_up(touch)

    def on_double_click_in(self):
        pass

    def on_double_click_out(self):
        pass

class TouchDownAndHoldable(Base):
    state = OptionProperty('normal', options=('normal', 'down', 'held'))
    been_held = BooleanProperty(False)
    hold_timeout = NumericProperty(0.05)
    hold_time = NumericProperty(0.0)
    hold_time_limit = NumericProperty(0.2)
    
    def __init__(self, **kwargs):
        super(TouchDownAndHoldable, self).__init__(**kwargs)
        self.register_event_type('on_hold_in')
        self.register_event_type('on_hold_out')

    def on_hold_down(self, dt):
        if self.state == 'down':
            self.hold_time += dt
        else:
            self.hold_time = 0.0
            return False

    def on_state(self, instance, value):
        if ((value <> 'held') and instance.been_held):
            instance.dispatch('on_hold_out')

        elif ((value == 'held')):
            instance.dispatch('on_hold_in')
        
        return super(TouchDownAndHoldable, self).on_state(instance, value)

    def on_touch_down(self, touch):
        if self.state == 'normal':
            Clock.schedule_interval(self.on_hold_down, self.hold_timeout)

            return super(TouchDownAndHoldable, self).on_touch_down(touch)

    def on_touch_move(self, touch):  
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'normal':
                self.state = 'down'

            if self.state == 'down':
                if (self.hold_time > self.hold_time_limit):
                    self.state = 'held'
                    return True

        return super(TouchDownAndHoldable, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.state = 'normal'
            return True

    def on_hold_in(self):
        pass

    def on_hold_out(self):
        pass

class DragNDroppable(object):
    droppable_zone_objects = ListProperty([])
    bound_zone_objects = ListProperty([])
    drag_opacity = NumericProperty(1.0)
    drop_func = ObjectProperty(None)
    drop_args = ListProperty([])
    hold_time = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(DragNDroppable, self).__init__(**kwargs)
        
        self.register_event_type("on_drag_start")
        #self.register_event_type("on_being_dragged")
        #self.register_event_type("on_drag_finish")
        self.register_event_type("on_pos_change")
        #self.register_event_type("on_motion_over")
        #self.register_event_type("on_motion_out")

    def on_state(self, instance, value):
        container = instance.parent
        listview = instance.accordion
        
        if ((value <> 'held') and listview.placeholder):
            self.reparent(instance)

        elif ((value == 'held') and not listview.placeholder):
            instance.opacity = self.drag_opacity
            self.dispatch('on_drag_start', instance)
            #instance.set_bound_axis_positions()
            #instance._old_drag_pos = self.pos
            #instance._old_parent = self.parent
            #instance._old_index = self.parent.children.index(self)
            
            self.deparent(instance, container)

        #return super(DragNDroppable, self).on_state(instance, value)            
        
    def on_drag_start(self, instance):
        container = instance.accordion.container
        for child in container.children:
            if ((type(child) is not Widget) and child.is_selected):
                accordion.adapter.deselect_item_view(child)

    def on_touch_down(self, touch):
        #super(Base, self).on_touch_down(touch)
        if self.state == 'normal':
            self.state = 'down'

        if self.state == 'down':
            Clock.schedule_interval(self.on_hold_down, .05)
            if self.hold_time >= 0.2:
                print 'held'
                # detect if the touch is short - has time and end (if not dispatch drag)
                self.state = "dragged"
                return True

        return super(DragNDroppable, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        #super(Base, self).on_touch_move(touch)
        
        if touch.grab_current is self:
            assert(self in touch.ud)
            #touch.apply_transform_2d(self.to_local)
            if self.state == 'held':
                self.center_y = touch.y
                self.dispatch('on_pos_change')
                return True

        return super(DragNDroppable, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        #super(Base, self).on_touch_up(touch)

        if touch.grab_current is self:
            assert(self in touch.ud)
            if self.state == 'held':
                touch.ungrab(self)
                self.state = 'normal'
                return True

        return super(DragNDroppable, self).on_touch_up(touch)
                
    def deparent(self, widget, container):
        #accordion = widget.accordion
        listview = widget.accordion
        listview.placeholder = Placeholder(size=widget.size,
                                           size_hint_y=None,
                                           index=widget.index,
                                           opacity=0.0)

        ix = container.children.index(widget)
        container.remove_widget(widget)
        container.add_widget(listview.placeholder, ix)
        widget.size_hint_x = None
        container.get_root_window().add_widget(widget)
        return

    def reparent(self, widget):
        listview = widget.accordion
        container = listview.container
        placeholder = listview.placeholder
        
        if self.collide_widget(placeholder):
            ix = container.children.index(placeholder)
            container.remove_widget(placeholder)
            container.get_root_window().remove_widget(widget)
            container.add_widget(widget, ix)
            widget.size_hint_x = 1.
            widget.index = placeholder.index
            listview.placeholder = None
            return
            
    def on_pos_change(self, *args):
        #accordion = self.accordion
        listview = self.accordion
        placeholder = listview.placeholder
        if not placeholder:
            return
        
        container = listview.container.children
        _ix = container.index(placeholder)

        for item in container:
            if self.collide_widget(item):

                if item is placeholder:
                    continue

                ix = container.index(item)
                if ((self.center_y <= item.top) and (self.center_y <= placeholder.y)) or ((self.center_y >= item.y) and (self.center_y >= placeholder.top)):
                    container.insert(ix, container.pop(_ix))

                    '''if placeholder.index > item.index:
                        item.index += 1
                    elif placeholder.index < item.index:
                        item.index -= 1'''

                #maybe scroll here
                return

class Button_(Clickable):
    state = OptionProperty('normal', options=('down', 'normal'))
    press_timeout = NumericProperty(0)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        else:
            return super(Button_, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self not in touch.ud:
            return False

        else:
            return super(Button_, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self not in touch.ud:
            return False

        else:
            return super(Button_, self).on_touch_up(touch)
        
        
Builder.load_string("""
#:import BoxLayout kivy.uix.boxlayout

<Base>:
    layout: layout_id
    label: label_id
    state_image: self.background_down if self.state == 'down' else self.background_normal
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            size: self.size
        BorderImage:
            source: self.state_image
            size: self.size

    BoxLayout
        id: layout_id
        orientation: 'horizontal'
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: .75, .75
        Label:
            id: label_id
            text: root.text
            shorten: True

""")
