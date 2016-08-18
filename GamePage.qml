import QtQuick 2.5
import QtQuick.Window 2.2
import QtQuick.Layouts 1.2

import io.thp.pyotherside 1.4

Item {
	id: root

    property alias columns: game.columns
    property alias rows: game.rows
	property int mines: 2

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

	ListModel {
        id: game_fields
    }

	function pad(num, size) {
		// pads number with leading zeros
		var s = "000000000" + num;
		return s.substr(s.length-size);
	}

	function setup() {
		py.create_game()
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

            // Import the main module and load the data
            importModule_sync("minesweeper_qml");
        }

		function create_game() {
            function init_game_fields(fields) {
                game_fields.clear();
                for(var i=0; i<fields.length; ++i) {
                    game_fields.append(fields[i]);
                }
            };

			py.call("minesweeper_qml.setup_game", [root.columns, root.rows, root.mines], init_game_fields);
		}

        function on_fields_changed(fields) {
            console.log("on_fields_changed", fields.length)
            console.assert(fields.length == game_fields.count);
            for(var i=0; i<fields.length; ++i) {
                game_fields.set(i, fields[i]);
            }
			var flags = py.call_sync("minesweeper_qml.number_of_flags")
			mines_text.num_flags = flags
        }

        function on_game_state_changed(won) {
            console.log("on_game_state_changed", won)
			game_over.won = won
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

	Stopwatch {
		id: game_time
		interval: 1000
		onTriggered: {
			time_text.time = Math.floor(passed()/1000)
		}
	}

	ColumnLayout {
		id: mainLayout

		anchors.top: parent.top
		anchors.left: parent.left
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
				id: mines_text
				property int num_flags: 0
				text: "%1/%2".arg(num_flags)
							 .arg(root.mines)
				color: num_flags > root.mines? "red" : "black"
			}
		}

		Game {
			id: game
			model: game_fields

			Layout.fillWidth: true
			Layout.fillHeight: true
			Layout.minimumWidth: game.implicitWidth
			Layout.minimumHeight: game.implicitHeight

			Rectangle {
				id: game_over

				property bool won: false

				anchors.fill: parent
				color: "grey"
				visible: false
				opacity: visible? 0.7 : 0.0

				Text {
					font.bold: true
					font.pointSize: 20.0
					anchors.centerIn: parent
					text: parent.won? "You win!" : "Game Over!"
					color: "red"
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
