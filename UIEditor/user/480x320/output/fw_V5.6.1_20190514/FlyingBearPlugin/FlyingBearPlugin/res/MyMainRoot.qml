// Copyright (c) 2019 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.0 as UM
import Cura 1.0 as Cura

Rectangle
{
    anchors.fill: parent

    Label {
        id: jz_ts
        objectName: "JZ-TS"
        x: 13
        y: 25
        text: "Loading..."
    }  
}