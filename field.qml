import QtQuick 2.0

Item {
    Rectangle {
        id: field
        anchors.fill: parent
        color: "white"
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
                console.log("Unknown flag state: "+flag)
            }
        }

        states: [
            State {
                name: "hidden"
                PropertyChanges { target: field; color: "white" }
                PropertyChanges { target: hint_text; text: "" }
            },
            State {
                name: "marked"
                PropertyChanges { target: field; color: "green" }
                PropertyChanges { target: hint_text; text: "" }
            },
            State {
                name: "revealed"
                PropertyChanges { target: field; color: "red" }
                PropertyChanges { target: hint_text; text: hint }
            }
        ]

        Text {
            id: hint_text
            anchors.centerIn: parent
            text: ""
        }
    }
}
