# Copyright (c) 2017 Looming
# Cura is released under the terms of the LGPLv3 or higher.

import os.path
from PyQt5.QtCore import QUrl 
from PyQt5.QtQml import QQmlComponent, QQmlContext 

from UM.Application import Application 
from UM.Extension import Extension 
from UM.Logger import Logger 
from UM.PluginRegistry import PluginRegistry 
from . import PluginMain

class FlyingBearExtension(Extension):
    def __init__(self):
        super().__init__()

        self.setMenuName("FlyingBear")
        self.addMenuItem("Manager Printers", self.showPluginMainWindow) 
        self.plugin_main = None
        Application.getInstance().mainWindowChanged.connect(self.logMessage) 

    def showPluginMainWindow(self,file_path = None):
        if not self.plugin_main: 
            self.plugin_main = PluginMain.PluginMain()
        self.plugin_main.showPluginMainWindow(file_path)

    def logMessage(self):
        pass

FlyingBearExtensionIns = FlyingBearExtension()



