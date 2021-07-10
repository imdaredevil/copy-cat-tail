#!/usr/bin/python3

import gi
import glob
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import subprocess
import os

CONFIG_DIR = '{0}/.copy-cat-tail/config'.format(os.environ.get('HOME'))
CONFIG = {}

def get_config():
    config = open('{0}/config'.format(CONFIG_DIR), 'r')
    configList = [row.split('=') for row in config.readlines()]
    configDict = {row[0]: row[1][1:-1] for row in configList}
    return configDict

def get_file_data():
    numFiles = len(glob.glob('{0}/copies/clip*.txt'.format(CONFIG['WORKING_DIR'])))
    currentIdxFile = open('{0}/currentIdx.txt'.format(CONFIG['WORKING_DIR']), 'r')
    currentIdx = int(currentIdxFile.read())
    return numFiles,currentIdx


class HeaderBarWindow(Gtk.Window):
    def __init__(self, numFiles, currentIdx):
        super().__init__(title="HeaderBar Demo")
        # setting window properties
        self.set_default_size(500, 400)
        self.set_border_width(0)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_opacity(0.8)

        # setting the files and contents
        self.numFiles = numFiles
        self.currentIdx = currentIdx

        # composing the header
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Copy Cat\'s Tail"
        self.set_titlebar(hb)

        # adding child components to header
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        button = Gtk.Button()
        button.add(
            Gtk.Arrow(arrow_type=Gtk.ArrowType.LEFT, shadow_type=Gtk.ShadowType.NONE)
        )
        button.connect('clicked', self.move_next)
        box.add(button)
        self.numLabel = Gtk.Label()
        box.add(self.numLabel)
        button = Gtk.Button()
        button.add(
            Gtk.Arrow(arrow_type=Gtk.ArrowType.RIGHT, shadow_type=Gtk.ShadowType.NONE)
        )
        button.connect('clicked', self.move_prev)
        box.add(button)
        hb.pack_start(box)

        # setting scroll window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(2)      
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        
        # adding label to scroll window
        self.label = Gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_max_width_chars(150)
        scrolled_window.add(self.label)
        self.connect("key-release-event",self.exit_window)
        self.connect("key-press-event", self.change_clip)

        # adding scroll window to window
        self.add(scrolled_window)

        # setting values
        self.set_display_text()

    def exit_window(self, widget, event):
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and event.keyval == Gdk.KEY_Control_R:
            self.destroy()
            subprocess.run("echo -n \"{0}\" | xclip -i -selection clipboard".format(self.label.get_text()), shell=True)
            Gtk.main_quit()
    
    def change_clip(self, widget, event):
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and event.keyval == Gdk.KEY_Right:
            self.move_prev(widget)
        if ctrl and event.keyval == Gdk.KEY_Left:
            self.move_next(widget)

    def move_next(self, widget):
        if self.currentIdx < self.numFiles - 1:
                self.currentIdx += 1
        self.set_display_text()
    
    def move_prev(self, widget):
        if self.currentIdx > 0:
                self.currentIdx -= 1
        self.set_display_text()
    
    def set_display_text(self):
        global CONFIG
        currentFile = open('{0}/copies/clip{1}.txt'.format(CONFIG['WORKING_DIR'], self.currentIdx))
        self.label.set_text(currentFile.read())
        self.numLabel.set_text('{0} / {1}'.format(self.numFiles - self.currentIdx, self.numFiles))
    
CONFIG = get_config()
numFiles, currentIdx = get_file_data() 
win = HeaderBarWindow(numFiles, currentIdx)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()