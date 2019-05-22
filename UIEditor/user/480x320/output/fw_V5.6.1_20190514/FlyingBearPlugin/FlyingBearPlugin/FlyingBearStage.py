# Copyright (c) 2017 Looming
# Cura is released under the terms of the LGPLv3 or higher.

import os.path
from PyQt5.QtCore import QUrl, QTimer 
from PyQt5.QtQml import QQmlComponent, QQmlContext 

from UM.Application import Application 
from UM.Extension import Extension
from UM.Logger import Logger 
from UM.PluginRegistry import PluginRegistry 
from . import PluginMain

from UM.Qt.QtApplication import QtApplication
from cura.Stages.CuraStage import CuraStage

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from UM.View.View import View

from cura.CuraApplication import CuraApplication

FlyingBearStageIns = None

class FlyingBearStage(CuraStage): 
    def __init__(self, application: QtApplication, parent = None) -> None:
        super().__init__(parent)
        self._application = application
        self._application.engineCreatedSignal.connect(self._engineCreated)
        self._previously_active_view = None  # type: Optional[View]

        self.plugin_main = None
        self.jz_root = None
        self.plugin_ui_item = None
        self.timer = None
        self.upload_file_name = None


    def onStageSelected(self) -> None:
        self._previously_active_view = self._application.getController().getActiveView()
        self.delay_run()

    def delay_run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.init_jz_plugin)
        self.timer.start(100)

    def init_jz_plugin(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

        if self._previously_active_view is not None:
            if self.jz_root is None:
                self.find_jz_root_item()
                if self.jz_root:
                    self.plugin_main = PluginMain.PluginMain()
                    qml_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res", "MyMain.qml")
                    self.plugin_ui_item = Application.getInstance().createQmlComponent(qml_file_path, {"manager": self.plugin_main})
                    self.plugin_ui_item.setParentItem(self.jz_root)
                    self.plugin_main.init_stage(self.plugin_ui_item,self.upload_file_name)
                    self.upload_file_name = None
                    self.jz_root.update()

    def find_jz_root_item(self):
        app = CuraApplication.getInstance()
        main_window = app.getMainWindow()
        root_item = main_window.contentItem()
        self.find_child_names(root_item)
        
    def find_child_names(self,item):
        if self.jz_root:
            return
        t = item.property("objectName")
        if t == "JZ-TS":
            item.setProperty("text","")
            self.jz_root = item.parentItem()
            return

        for child in item.childItems():
            self.find_child_names(child)


    def onStageDeselected(self) -> None:
        if self._previously_active_view is not None:
            self._application.getController().setActiveView(self._previously_active_view.getPluginId())
        self._previously_active_view = None

        if self.plugin_main:
            self.plugin_main.deleteLater()
        self.plugin_main = None
        self.jz_root = None
        self.plugin_ui_item = None


    def _engineCreated(self) -> None:
        plugin_path = self._application.getPluginRegistry().getPluginPath(self.getPluginId())
        if plugin_path is not None:
            menu_component_path = os.path.join(plugin_path, "res", "MyMenu.qml")
            main_component_path = os.path.join(plugin_path, "res", "MyMainRoot.qml")
            self.addDisplayComponent("menu", menu_component_path)
            self.addDisplayComponent("main", main_component_path)

    def setUploadFileName(self, upload_file_name):
        self.upload_file_name = upload_file_name



