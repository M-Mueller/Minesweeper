import QtQuick 2.0

Item {
    Rectangle {
        id: field
        anchors.fill: parent

        Text {
            id: hint_text
            anchors.centerIn: parent
            font.bold: true
            text: hint
        }

        Rectangle {
            id: mine_icon
            anchors.fill: parent
            color: "red"
            visible: mine
        }

        Rectangle {
            id: wrong_flag
            anchors.fill: parent
            color: "blue"
            visible: !mine && flag == 1
        }

        Rectangle {
            id: cover
            anchors.fill: parent
            radius: 5
            border.width: 1
            color: "lightgrey"
        }

        state: {
            if(flag == 0) {
                return "hidden";
            }
            else if(flag == 1) {
                return "marked";
            }
            else if(flag == 2) {
                return "revealed";
            }
            else {
                console.log("Unknown flag state: " + flag)
            }
        }

        states: [
            State {
                name: "hidden"
                PropertyChanges { target: cover; color: "lightgrey" }
            },
            State {
                name: "marked"
                PropertyChanges { target: cover; color: "green" }
            },
            State {
                name: "revealed"
                PropertyChanges { target: cover; visible: false }
            }
        ]

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton | Qt.RightButton
            onClicked: {
                var column = Math.floor(index % grid.columns);
                var row = Math.floor(index / grid.rows);
                if (mouse.button === Qt.LeftButton)
                    py.reveal_field(column, row);
                else
                    py.mark_field(column, row);
            }
        }
    }
}
