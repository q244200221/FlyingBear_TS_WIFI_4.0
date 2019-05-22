# Copyright (c) 2017 Looming
# Cura is released under the terms of the LGPLv3 or higher.

from . import FlyingBearOutputDevice
from . import FlyingBearExtension
from . import FlyingBearStage


def getMetaData():
    return {
        "stage": {
            "name":  "FlyingBear",
            "weight": 99
        }
    }


def register(app):
    FlyingBearStage.FlyingBearStageIns = FlyingBearStage.FlyingBearStage(app)
    return {
        "output_device": FlyingBearOutputDevice.FlyingBearOutputDevicePlugin(),
        # "extension": FlyingBearExtension.FlyingBearExtensionIns,
        "stage": FlyingBearStage.FlyingBearStageIns
        }
