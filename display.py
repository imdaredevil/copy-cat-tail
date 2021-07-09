import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="HeaderBar Demo")
        self.set_default_size(600, 500)
        self.set_border_width(0)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_opacity(0.8)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Copy Cat\'s Tail"
        self.set_titlebar(hb)
        # the scrolledwindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(2)      
        # there is always the scrollbar (otherwise: AUTOMATIC - only if needed
        # - or NEVER)
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(
            Gtk.Arrow(arrow_type=Gtk.ArrowType.LEFT, shadow_type=Gtk.ShadowType.NONE)
        )
        box.add(button)
        button = Gtk.Button()
        button.add(
            Gtk.Arrow(arrow_type=Gtk.ArrowType.RIGHT, shadow_type=Gtk.ShadowType.NONE)
        )
        box.add(button)

        hb.pack_start(box)
        self.label = Gtk.Label(label='Temporary one ' * 1000)
        self.label.set_line_wrap(True)
        self.label.set_max_width_chars(150)
        scrolled_window.add_with_viewport(self.label)
        self.add(scrolled_window)
        self.connect("key-release-event",self.exit_window)
        self.connect("key-press-event", self.change_clip)

    def exit_window(self, widget, event):
        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
        if shift and event.keyval == Gdk.KEY_Shift_R:
            self.destroy()
            Gtk.main_quit()
    
    def change_clip(self, widget, event):
        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))
        shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
        if shift and event.keyval == Gdk.KEY_Right:
            print("right")
        if shift and event.keyval == Gdk.KEY_Left:
            print("left")

win = HeaderBarWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()