from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, OptionProperty, StringProperty, BooleanProperty, BoundedNumericProperty
from kivy.clock import Clock
from kivy.lang import Builder

class _OnStateClass(object):
    """ A do-nothing-class that's only used for inheriting `on_state`. """
    state = OptionProperty('normal', options=('normal'))

    def __init__(self, **kwargs):
        super(_OnStateClass, self).__init__(**kwargs)
        
    def on_state(self, *args):
        pass

class Base(RelativeLayout, _OnStateClass):
    background_normal = StringProperty('atlas://data/images/defaulttheme/button')
    background_down = StringProperty('atlas://data/images/defaulttheme/button_pressed')
    text = StringProperty('')

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        else:
            touch.grab(self)
            touch.ud[self] = True
            return True

class Clickable(Base):
    Clickable_gate_open = StringProperty('down')
    Clickable_gate_close = StringProperty('normal')
    state = OptionProperty('normal', options=('normal', 'down'))
    _press_ = ObjectProperty(None)
    _release_ = ObjectProperty(None)
    press_timeout = NumericProperty(0.0625)
    relase_timeout = NumericProperty(0.15)

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        super(Clickable, self).__init__(**kwargs)

        self._press_ = Clock.create_trigger(self.trigger_press, self.press_timeout)
        self._release_ = Clock.create_trigger(self.trigger_release, self.release_timeout)

    def _do_press(self):
        self.state = self.Clickable_gate_open

    def _do_release(self):
        self.state = self.Clickable_gate_close

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False

        if self.state == self.Clickable_gate_close:
            sup = super(Base, self).on_touch_down(touch)
            
            if not sup:
                self._press_()
            else:
                return sup

        return super(Clickable, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.Clickable_gate_open:
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
        if self.state == self.Clickable_gate_close:
            self._do_press()
            self.dispatch('on_press')
        else:
            return False

    def trigger_release(self, dt):
        if self.state == self.Clickable_gate_close:
            self.dispatch('on_release')
        else:
            return False

class SwipeableLeft(Base):
    """ 
    Borrowed (with special thanks) from kovak's widget, here: https://github.com/Kovak/KivyExamples/tree/master/iOSStyle_List_Delete_Button
    """
    SwipeableLeft_gate_open = StringProperty('swiped left')
    SwipeableLeft_gate_close = StringProperty('normal')
    state = OptionProperty('normal', options=('normal', 'swiped left'))
    been_swiped_left = BooleanProperty(False)
    dx_ = BoundedNumericProperty(-20, max=0)

    def __init__(self, **kwargs):
        self.register_event_type('on_swiped_left_in')
        self.register_event_type('on_swiped_left_out')
        super(SwipeableLeft, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if ((value <> instance.SwipeableLeft_gate_open) and instance.been_swiped_left):
            instance.dispatch('on_swiped_left_in')
            instance.been_swiped_left = False

        elif value == instance.SwipeableLeft_gate_open:
            instance.dispatch('on_swiped_left_out')
            instance.been_swiped_left = True

        return super(SwipeableLeft, self).on_state(instance, value)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.SwipeableLeft_gate_close:
                sup = super(Base, self).on_touch_move(touch)

                if sup:
                    return sup
                elif ((touch.dx < self.dx_) and not self.been_swiped_left):
                    touch.ungrab(self)
                    self.state = self.SwipeableLeft_gate_open
                    return True

        return super(SwipeableLeft, self).on_touch_move(touch)

    def on_swiped_left_in(self):
        pass

    def on_swiped_left_out(self):
        pass

class SwipeableRight(Base):
    SwipeableRight_gate_open = StringProperty('swiped right')
    SwipeableRight_gate_close = StringProperty('normal')
    state = OptionProperty('normal', options=('normal', 'swiped right'))
    been_swiped_right = BooleanProperty(False)
    _dx = BoundedNumericProperty(20, min=0)

    def __init__(self, **kwargs):
        self.register_event_type('on_swiped_right_in')
        self.register_event_type('on_swiped_right_out')
        super(SwipeableRight, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if ((value <> instance.SwipeableRight_gate_open) and instance.been_swiped_right):
            instance.dispatch('on_swiped_right')
            instance.been_swiped_right = False

        elif value == instance.SwipeableRight_gate_open:
            instance.dispatch('on_swiped_right')
            instance.been_swiped_left = True

        return super(SwipeableRight, self).on_state(instance, value)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)
            
            if self.state == self.SwipeableRight_gate_close:
                sup = super(Base, self).on_touch_move(touch)
                
                if sup:
                    return sup
                elif ((touch.dx > self._dx) and not self.been_swiped_right):
                    self.state = self.SwipeableRight_gate_open
                    touch.ungrab(self)
                    return True

        return super(SwipeableRight, self).on_touch_move(touch)

    def on_swiped_right_in(self):
        pass

    def on_swiped_right_out(self):
        pass

class DoubleClickable(Base):
    DoubleClickable_gate_open = StringProperty('double clicked')
    DoubleClickable_gate_close = StringProperty('normal')
    state = OptionProperty('normal', options=('normal', 'double clicked'))
    been_double_clicked = BooleanProperty(False)
    double_tap_time = NumericProperty(0.250)

    def __init__(self, **kwargs):
        self.register_event_type('on_double_click_in')
        self.register_event_type('on_double_click_out')
        super(DoubleClickable, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if ((value <> instance.DoubleClickable_gate_open) and instance.been_double_clicked):
            instance.dispatch('on_double_click_out')
            instance.been_double_clicked = False

        elif ((value == instance.DoubleClickable_gate_open)):
            instance.dispatch('on_double_click_in')
            instance.been_double_clicked = True

        return super(DoubleClickable, self).on_state(instance, value)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.DoubleClickable_gate_close:
            	sup = super(Base, self).on_touch_up(touch)

            	if sup:
            		return sup
            	elif (touch.is_double_tap and (touch.double_tap_time < self.double_tap_time)):
                	touch.ungrab(self)
                	self.state = self.DoubleClickable_gate_open
                	return True

        return super(DoubleClickable, self).on_touch_up(touch)

    def on_double_click_in(self):
        pass

    def on_double_click_out(self):
        pass

class TouchDownAndHoldable(Base):
    TouchDownAndHoldable_gate_open = StringProperty('held')
    TouchDownAndHoldable_gate_close = StringProperty('normal')
    TouchDownAndHoldable_transient_state = StringProperty('down')
    state = OptionProperty('normal', options=('normal', 'down', 'held'))
    been_held = BooleanProperty(False)
    hold_timeout = NumericProperty(0.05)
    hold_time = NumericProperty(0.0)
    hold_time_limit = NumericProperty(0.2)
    
    def __init__(self, **kwargs):
        self.register_event_type('on_hold_in')
        self.register_event_type('on_hold_out')
        super(TouchDownAndHoldable, self).__init__(**kwargs)

    def on_hold_down(self, dt):
        if self.state == self.TouchDownAndHoldable_transient_state:
            self.hold_time += dt
        else:
            self.hold_time = 0.0
            return False

    def on_state(self, instance, value):
        if ((value <> instance.TouchDownAndHoldable_gate_open) and instance.been_held):
            instance.dispatch('on_hold_out')
            instance.been_held = False

        elif ((value == instance.TouchDownAndHoldable_gate_open)):
            instance.dispatch('on_hold_in')
            instance.been_held = True
        
        return super(TouchDownAndHoldable, self).on_state(instance, value)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False

        if self.state == self.TouchDownAndHoldable_gate_open:
            sup = super(Base, self).on_touch_down(touch)

            if not sup:
                Clock.schedule_interval(self.on_hold_down, self.hold_timeout)
            else:
                return sup
            
            if not hasattr(self, 'trigger_press'):
                self.state = self.TouchDownAndHoldable_transient_state

        return super(TouchDownAndHoldable, self).on_touch_down(touch)

    def on_touch_move(self, touch):  
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.TouchDownAndHoldable_transient_state:
            	sup = super(Base, self).on_touch_move(touch)

            	if sup:
            		return sup
                elif (self.hold_time > self.hold_time_limit):
                    self.state = self.TouchDownAndHoldable_gate_open
                    return True

        return super(TouchDownAndHoldable, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.TouchDownAndHoldable_gate_open:
            	sup = super(Base, self).on_touch_up(touch)
            	
            	if not sup:
            		touch.ungrab(self)
                	self.state = self.TouchDownAndHoldable_gate_close
                return True

    def on_hold_in(self):
        pass

    def on_hold_out(self):
        pass

class DragNDroppable(_OnStateClass):
    """
    Borrowed HEAVILY (with special thanks) from Pavel Kostelník's widget, here: https://bitbucket.org/koszta5/kivydnd/src
    To be used in conjunction with another ListButton Behavior.
    """
    DragNDroppable_gate_open = StringProperty('dragged')
    DragNDroppable_gate_close = StringProperty('dropped')
    state = OptionProperty('dropped', options=('dragged', 'dropped'))
    droppable_zone_objects = ListProperty([])
    bound_zone_objects = ListProperty([])
    drag_opacity = NumericProperty(1.0)
    been_dragged = BooleanProperty(False)
    listview = ObjectProperty(None)
    hold_time = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.register_event_type("on_drag_start")
        self.register_event_type("on_drag_finish")
        super(DragNDroppable, self).__init__(**kwargs)

    def on_state(self, instance, value):
        container = instance.parent
        listview = instance.listview
        
        if ((value <> instance.DragNDroppable_gate_open) and instance.been_dragged):
        	listview.reparent(instance)
            instance.dispatch('on_drag_end', instance)
            instance.been_dragged = False

        elif ((value == instance.DragNDroppable_gate_open) and not instance.been_dragged):
            instance.dispatch('on_drag_start', instance)
            listview.deparent(instance)
            instance.been_dragged = True

        return super(DragNDroppable, self).on_state(instance, value)            
        
    def on_drag_start(self, instance):
        pass
        #instance.opacity = self.drag_opacity
        #instance.set_bound_axis_positions()
        #instance._old_drag_pos = self.pos
        #instance._old_parent = self.parent
        #instance._old_index = self.parent.children.index(self)

    def on_drag_end(self, instance):
    	pass

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.DragNDroppable_gate_open:
                self.center_y = touch.y
                self.dispatch('on_pos_change')
                return True

        return super(DragNDroppable, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == self.DragNDroppable_gate_open:
                touch.ungrab(self)
                self.state = self.DragNDroppable_gate_close
                return True

        return super(DragNDroppable, self).on_touch_up(touch)

class Button_(Clickable):
    press_timeout = NumericProperty(0)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        else:
            return super(Button_, self).on_touch_down(touch)
        
        
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
