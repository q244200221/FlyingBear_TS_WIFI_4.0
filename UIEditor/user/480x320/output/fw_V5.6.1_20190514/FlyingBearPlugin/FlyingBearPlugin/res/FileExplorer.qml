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
    title: "File Explorer - FlyingBear"
    onClosing: {}
    
}
