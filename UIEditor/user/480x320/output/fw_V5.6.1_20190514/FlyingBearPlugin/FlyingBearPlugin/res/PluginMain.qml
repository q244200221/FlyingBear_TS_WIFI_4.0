import UM 1.1 as UM 
import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Window 2.1

Window
{
    id: base

    width: 600 * screenScaleFactor
    height: 700 * screenScaleFactor
    minimumWidth: 600 * screenScaleFactor
    minimumHeight: 700 * screenScaleFactor
    title: "FlyingBear Printers Manager"
    onClosing: {manager.on_window_close();}
    
    Label {
        id: lb_ip
        objectName: "lb_ip"
        x: 13
        y: 25
        text: "IP"
        font.pointSize: 14
        font.bold: true
    }

    TextField {
        id: txt_printer_ip
        objectName: "txt_printer_ip"
        x: 39
        y: 20
        width: 122
        height: 30
        text: ""
    }

    Button {
        id: btn_connect
        objectName: "btn_connect"
        x: 167
        y: 20
        width: 70
        height: 30
        text: "Connect"
        onClicked: {manager.connect_printer();}
    }

    Button {
        id: btn_disconnect
        objectName: "btn_disconnect"
        x: 167
        y: 20
        width: 70
        height: 30
        text: "Disconnect"
        onClicked: {manager.disconnect_printer();}
    }

    Image {
        id: img_edit_printer_name
        objectName: "img_edit_printer_name"
        x: 13
        y: 65
        width: 16
        height: 16
        source: "edit.png"
        onClicked: {manager.edit_name();}
    }

    Label {
        id: lb_printer_name
        objectName: "lb_printer_name"
        x: 33
        y: 65
        text: "PrinterN"
        font.pointSize: 12
    }

    Label {
        id: lb_printer_state
        objectName: "lb_printer_state"
        x: 13
        y: 95
        text: "Not Connected"
        font.pointSize: 12
    }

    Label {
        id: lb_printer_bed
        objectName: "lb_printer_bed"
        x: 13
        y: 125
        text: "Bed: 0 / 0"
        font.pointSize: 12
    }

    Label {
        id: lb_printer_t0
        objectName: "lb_printer_t0"
        x: 13
        y: 155
        text: "T0: 0 / 0"
        font.pointSize: 12
    }

    Label {
        id: lb_printer_t1
        objectName: "lb_printer_t1"
        x: 13
        y: 185
        text: "T1: 0 / 0"
        font.pointSize: 12
    }


    Button {
        id: btn_preheat
        objectName: "btn_preheat"
        x: 13
        y: 217
        width: 80
        height: 30
        text: "Preheat"
        onClicked: {manager.send_cmd("pre_heat");}
    }

    Button {
        id: btn_cooldown
        objectName: "btn_cooldown"
        x: 99
        y: 217
        width: 80
        height: 30
        text: "Cooldown"
        onClicked: {manager.send_cmd("cool_down");}
    }

    Button {
        id: btn_sd
        objectName: "btn_sd"
        x: 185
        y: 217
        width: 80
        height: 30
        text: "SD"
        onClicked: {manager.show_sd();}
    }

    Button {
        id: btn_upload
        objectName: "btn_upload"
        x: 271
        y: 217
        width: 80
        height: 30
        text: "Upload"
        onClicked: {manager.show_upload();}
    }

    Label {
        id: lb_gcode
        objectName: "lb_gcode"
        x: 13
        y: 269
        text: "Gcode"
        font.pointSize: 14
        font.bold: true
    }

    TextField {
        id: txt_gcode
        objectName: "txt_gcode"
        x: 75
        y: 263
        width: 190
        height: 30
        text: ""
    }

    Button {
        id: btn_send
        objectName: "btn_send"
        x: 271
        y: 263
        width: 80
        height: 30
        text: "Send"
        onClicked: {manager.send_gcode();}
    }

    Label {
        id: lb_printing
        objectName: "lb_printing"
        x: 13
        y: 348
        text: "Printing"
        font.bold: true
        font.pointSize: 14
    }

    ProgressBar {
        id: pgb_progress
        objectName: "pgb_progress"
        x: 13
        y: 403
        height: 6
        value: 0.5
    }

    Label {
        id: lb_progress
        objectName: "lb_progress"
        x: 226
        y: 398
        text: "50%"
        font.pointSize: 12
    }

    Button {
        id: btn_pause
        objectName: "btn_pause"
        x: 13
        y: 426
        width: 80
        height: 30
        text: "Pause"
        onClicked: {manager.printing_task_pause();}
    }

    Button {
        id: btn_resume
        objectName: "btn_resume"
        x: 13
        y: 426
        width: 80
        height: 30
        text: "Resume"
        onClicked: {manager.printing_task_resume();}
    }

    Button {
        id: btn_stop
        objectName: "btn_stop"
        x: 99
        y: 426
        width: 80
        height: 30
        text: "Stop"
        onClicked: {manager.printing_task_stop();}
    }

    Button {
        id: btn_off
        objectName: "btn_off"
        x: 185
        y: 426
        width: 80
        height: 30
        text: "Off"
    }

    Label {
        id: lb_printing_filename
        objectName: "lb_printing_filename"
        x: 13
        y: 376
        height: 16
        text: "printing_filename.gcode"
        font.pointSize: 12
    }
}
