import QtQuick 2.5
import QtQuick.Window 2.2
import QtQuick.Layouts 1.2

import io.thp.pyotherside 1.4

Window {
    id: game_window
    visible: true

	property int margin: 11
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
	maximumWidth: minimumWidth
	maximumHeight: minimumHeight

    property int columns: 5
    property int rows: 5

    ListModel {
        id: game_fields
    }

	Stopwatch {
		id: game_time
		interval: 1000
		onTriggered: {
			time_text.time = Math.floor(passed()/1000)
		}
	}

	function pad(num, size) {
		// pads number with leading zeros
		var s = "000000000" + num;
		return s.substr(s.length-size);
	}

    Python {
        id: py

        onError: console.log("Python error: " + traceback)
        onReceived: console.log("Received data" + data)
        Component.onCompleted: {
            // Add the directory of this .qml file to the search path
            addImportPath(Qt.resolvedUrl('.'));

            py.setHandler("logging", function(data){
                console.log("(python) " + data)
            });

            py.setHandler("game_state_changed", on_game_state_changed);
            py.setHandler("fields_changed", on_fields_changed);

            function init_game_fields(fields) {
                game_fields.clear();
                for(var i=0; i<fields.length; ++i) {
                    game_fields.append(fields[i]);
                }
            };

            // Import the main module and load the data
            importModule("minesweeper_qml", function () {
                py.call("minesweeper_qml.setup_game", [game_window.columns, game_window.rows], init_game_fields);
            });
        }

        function on_fields_changed(fields) {
            console.log("on_fields_changed", fields.length)
            console.assert(fields.length == game_fields.count);
            for(var i=0; i<fields.length; ++i) {
                game_fields.set(i, fields[i]);
            }
        }

        function on_game_state_changed(won) {
            console.log("on_game_state_changed", won)
            game_over.visible = true
			game_time.stop()
        }

        function reveal_field(column, row) {
			game_time.start()
            console.log("reveal_field", column, row)
            py.call("minesweeper_qml.reveal", [column, row]);
        }

        function mark_field(column, row) {
			game_time.start()
            console.log("mark_field", column, row)
            py.call("minesweeper_qml.mark", [column, row]);
        }
    }

	ColumnLayout {
		id: mainLayout

		anchors.fill: parent
		anchors.margins: margin
		spacing: 5

		RowLayout {
			Layout.fillWidth: true

			Text {
				text: "Time:"
				font.bold: true
			}
			Text {
				id: time_text
				property int time: 0
				text: "00:00"
				onTimeChanged: {
					var min = Math.floor(time / 60)
					var sec = time % 60
					text = "%1:%2"
							.arg(pad(min, 2))
							.arg(pad(sec, 2))
				}
			}
			Item {
				Layout.fillWidth: true
			}
			Text {
				text: "Mines:"
				font.bold: true
			}
			Text {
				text: "0"
			}
		}

		Game {
			Layout.fillWidth: true
			Layout.fillHeight: true
			Layout.minimumWidth: childrenRect.width
			Layout.minimumHeight: childrenRect.height

			model: game_fields

			Rectangle {
				id: game_over
				anchors.fill: parent
				color: "grey"
				visible: false
				opacity: visible? 0.7 : 0.0

				Text {
					font.bold: true
					anchors.centerIn: parent
					text: "Game Over!"
					font.pointSize: 20.0
				}

				MouseArea {
					anchors.fill: parent
					acceptedButtons: Qt.AllButtons
				}

				Behavior on opacity {
					NumberAnimation {
						duration: 1000
						easing.type: Easing.OutCubic
					}
				}
			}
		}
	}
}
