from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, OptionProperty, StringProperty, BooleanProperty, BoundedNumericProperty
from kivy.clock import Clock
from kivy.lang import Builder

class _OnStateClass(object):
    """ A do-nothing-class that's only used for inheriting `on_state`. """

    def __init__(self, **kwargs):
        super(_OnStateClass, self).__init__(**kwargs)
        
    def on_state(self, *args):
        pass

class Base(RelativeLayout, _OnStateClass):
    background_normal = StringProperty('atlas://data/images/defaulttheme/button')
    background_down = StringProperty('atlas://data/images/defaulttheme/button_pressed')
    state = OptionProperty('normal', options=('normal'))
    text = StringProperty('')

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        else:
            touch.grab(self)
        	touch.ud[self] = True
        	return True

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
            sup = super(Base, self).on_touch_down(touch)
            
            if not sup:
                self._press_()
            else:
                return sup

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
            self.dispatch('on_press')
        else:
            return False

    def trigger_release(self, dt):
        if self.state == 'down':
            self.dispatch('on_release')
        else:
            return False

class SwipeableLeft(Base):
    """ 
    Borrowed (with special thanks) from kovak's widget, here: https://github.com/Kovak/KivyExamples/tree/master/iOSStyle_List_Delete_Button
    """
    state = OptionProperty('normal', options=('normal', 'swiped left'))
    been_swiped_left = BooleanProperty(False)
    delta_x_left = BoundedNumericProperty(-20, max=0)

    def __init__(self, **kwargs):
        self.register_event_type('on_swiped_left_in')
        self.register_event_type('on_swiped_left_out')
        super(SwipeableLeft, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if ((value <> 'swiped left') and instance.been_swiped_left):
            instance.dispatch('on_swiped_left_in')
            instance.been_swiped_left = False

        elif value == 'swiped left':
            instance.dispatch('on_swiped_left_out')
            instance.been_swiped_left = True

        return super(SwipeableLeft, self).on_state(instance, value)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'normal':
                sup = super(Base, self).on_touch_move(touch)

                if sup:
                    return sup
                elif ((touch.dx < self.delta_x_left) and not self.been_swiped_left):
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
    delta_x_right = BoundedNumericProperty(20, min=0)

    def __init__(self, **kwargs):
        self.register_event_type('on_swiped_right_in')
        self.register_event_type('on_swiped_right_out')
        super(SwipeableRight, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if ((value <> 'swiped right') and instance.been_swiped_right):
            instance.dispatch('on_swiped_right')
            instance.been_swiped_right = False

        elif value == 'swiped right':
            instance.dispatch('on_swiped_right')
            instance.been_swiped_left = True

        return super(SwipeableRight, self).on_state(instance, value)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)
            
            if self.state == 'normal':
                sup = super(Base, self).on_touch_move(touch)
                
                if sup:
                    return sup
                elif ((touch.dx > self.delta_x_right) and not self.been_swiped_right):
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
    double_tap_time = NumericProperty(0.250)

    def __init__(self, **kwargs):
        self.register_event_type('on_double_click_in')
        self.register_event_type('on_double_click_out')
        super(DoubleClickable, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if ((value <> 'double clicked') and instance.been_double_clicked):
            instance.dispatch('on_double_click_out')
            instance.been_double_clicked = False

        elif ((value == 'double clicked')):
            instance.dispatch('on_double_click_in')
            instance.been_double_clicked = True

        return super(DoubleClickable, self).on_state(instance, value)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'normal':
            	sup = super(Base, self).on_touch_up(touch)

            	if sup:
            		return sup
            	elif (touch.is_double_tap and (touch.double_tap_time < self.double_tap_time)):
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
        self.register_event_type('on_hold_in')
        self.register_event_type('on_hold_out')
        super(TouchDownAndHoldable, self).__init__(**kwargs)

    def on_hold_down(self, dt):
        if self.state == 'down':
            self.hold_time += dt
        else:
            self.hold_time = 0.0
            return False

    def on_state(self, instance, value):
        if ((value <> 'held') and instance.been_held):
            instance.dispatch('on_hold_out')
            instance.been_held = False

        elif ((value == 'held')):
            instance.dispatch('on_hold_in')
            instance.been_held = True
        
        return super(TouchDownAndHoldable, self).on_state(instance, value)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False

        if self.state == 'normal':
            sup = super(Base, self).on_touch_down(touch)

            if not sup:
                Clock.schedule_interval(self.on_hold_down, self.hold_timeout)
            else:
                return sup
            
            if not hasattr(self, 'trigger_press'):
                self.state = 'down'

        return super(TouchDownAndHoldable, self).on_touch_down(touch)

    def on_touch_move(self, touch):  
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'down':
            	sup = super(Base, self).on_touch_move(touch)

            	if sup:
            		return sup
                elif (self.hold_time > self.hold_time_limit):
                    self.state = 'held'
                    return True

        return super(TouchDownAndHoldable, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'held':
            	sup = super(Base, self).on_touch_up(touch)
            	
            	if not sup:
            		touch.ungrab(self)
                	self.state = 'normal'
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
    
    droppable_zone_objects = ListProperty([])
    bound_zone_objects = ListProperty([])
    drag_opacity = NumericProperty(1.0)
    listview = ObjectProperty(None)
    hold_time = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.register_event_type("on_drag_start")
        self.register_event_type("on_drag_finish")
        super(DragNDroppable, self).__init__(**kwargs)

    def on_state(self, instance, value):
        container = instance.parent
        listview = instance.accordion
        
        if ((value <> 'dragged') and listview.placeholder):
        	instance.listview.reparent(instance)
            instance.dispatch('on_drag_end', instance)

        elif ((value == 'dragged') and not listview.placeholder):
            instance.dispatch('on_drag_start', instance)
            instance.listview.deparent(instance)

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

            if self.state == 'dragged':
                self.center_y = touch.y
                self.dispatch('on_pos_change')
                return True

        return super(DragNDroppable, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            assert(self in touch.ud)

            if self.state == 'dragged':
                touch.ungrab(self)
                self.state = 'normal'
                return True

        return super(DragNDroppable, self).on_touch_up(touch)

class Button_(Clickable):
    state = OptionProperty('normal', options=('down', 'normal'))
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
