#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Config():
    def __init__(self, filename="settings.ini"):
        self.filename = filename
        self.homepath = os.path.expanduser("~")
        self.configfolder = os.path.join(self.homepath, ".studiouhr")
        self.path = os.path.join(self.configfolder, self.filename)
        self.config = ConfigParser()
        self.initialize_settings_directory()
        self.read_settings(self.path)

    def initialize_settings_directory(self):
        if not os.path.exists(self.configfolder):
            os.mkdir(self.configfolder)
            print "Created directory "+str(self.configfolder)
            self.set_defaults()
            self.write_settings(self.path)

    def write_settings(self, path):
        with open(path, 'w') as f:
            self.config.write(f)
            print "Wrote new settings to "+str(path)
            f.close()

    def read_settings(self, path):
        self.config.read(path)
        self.fullscreen = self.retrieve("Display", "fullscreen", True) == "True"
        self.textformat = self.retrieve("Digits", "textformat", "%H:%M")
        self.fontname = self.retrieve("Digits", "fontname", "Roboto Mono Thin")
        self.fontsize = int(self.retrieve("Digits", "fontsize", 20))
        self.xoffset = int(self.retrieve("Digits", "xoffset", 20))
        self.yoffset = int(self.retrieve("Digits", "yoffset", 20))
        self.displayarc = self.retrieve("Arc", "displayarc", True) == "True"
        self.arcwidth = int(self.retrieve("Arc", "arcwidth", 1))
        self.displayfivemarks = self.retrieve("Dots", "displayfivemarks", True) == "True"
        self.displayseconddots = self.retrieve("Dots", "displayseconddots", True) == "True"
        self.dotdiameter = int(self.retrieve("Dots", "dotdiameter", 50))
        self.secondmargin = int(self.retrieve("Dots", "secondmargin", 60))
        self.indicatormargin = int(self.retrieve("Dots", "indicatormargin", 15))
        self.clockinterval = float(self.retrieve("Drawscheduler", "clockinterval", 0.01))
        self.dotinterval = float(self.retrieve("Drawscheduler", "dotinterval", 0.02))
        self.arcinterval = float(self.retrieve("Drawscheduler", "arcinterval", 0.02))
        self.indicatorinterval = float(self.retrieve("Drawscheduler", "indicatorinterval", 0.02))

    def retrieve(self, configsection, configoption, default):
        """ Returns a Value from a config, if it fails returns defaults """
        try:
            return self.config.get(configsection, configoption)
        except:
            return default

    def set_defaults(self):
        # Sets the default values
        self.config.add_section("Display")
        self.config.add_section("Digits")
        self.config.add_section("Arc")
        self.config.add_section("Dots")
        self.config.add_section("Drawscheduler")
        self.config.add_section("Geo")
        self.config.set("Display", "fullscreen", True)
        self.config.set("Digits", "textformat", "%H:%M")
        self.config.set("Digits", "fontname", "Roboto Mono Thin")
        self.config.set("Digits", "fontsize", 20)
        self.config.set("Digits", "xoffset", 20)
        self.config.set("Digits", "yoffset", 20)
        self.config.set("Arc", "displayarc", True)
        self.config.set("Arc", "arcwidth", 1)
        self.config.set("Dots", "displayfivemarks", True)
        self.config.set("Dots", "displayseconddots", True)
        self.config.set("Dots", "dotdiameter", 50)
        self.config.set("Dots", "secondmargin", 60)
        self.config.set("Dots", "indicatormargin", 15)
        self.config.set("Drawscheduler", "clockinterval", 0.01)
        self.config.set("Drawscheduler", "dotinterval", 0.02)
        self.config.set("Drawscheduler", "arcinterval", 0.02)
        self.config.set("Drawscheduler", "indicatorinterval", 0.02)