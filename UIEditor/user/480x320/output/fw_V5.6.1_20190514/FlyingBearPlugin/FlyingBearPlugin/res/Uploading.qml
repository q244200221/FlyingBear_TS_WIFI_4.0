import UM 1.1 as UM 
import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Window 2.1

UM.Dialog
{
    id: base

    width: 600 * screenScaleFactor
    height: 300 * screenScaleFactor
    minimumWidth: 600 * screenScaleFactor
    minimumHeight: 300 * screenScaleFactor
    title: "Uploading"
    onClosing: {manager.on_uploading_window_close();}

    Label {
        id: lb_uploading_filename
        objectName: "lb_uploading_filename"
        x: 25
        y: 24
        height: 16
        text: "printing_filename.gcode"
        font.pointSize: 12
    }

    ProgressBar {
        id: pgb_progress
        objectName: "pgb_progress"
        x: 25
        y: 54
        width: 400
        height: 6
        value: 0
    }

    Button {
        id: btn_cancel
        objectName: "btn_cancel"
        x: 190
        y: 172
        width: 80
        height: 30
        text: "Cancel"
        onClicked: {manager.cancel_upload();}
    }

    Label {
        id: lb_speed
        objectName: "lb_speed"
        x: 25
        y: 70
        height: 16
        text: "Speed:"
        font.pointSize: 12
    }

    Label {
        id: lb_remain_time
        objectName: "lb_remain_time"
        x: 25
        y: 96
        text: "Remain Time: "
        horizontalAlignment: Text.AlignRight
        font.pointSize: 12
    }

    CheckBox {
        id: ck_auto_start_print
        objectName: "ck_auto_start_print"
        x: 25
        y: 123
        text: "Start printing as soon as the transfer is complete"
    }
}
