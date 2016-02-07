import QtQuick 2.5
import QtQuick.Window 2.2

import io.thp.pyotherside 1.4

Window {
    id: game_window
    visible: true

    width: 640
    height: 480

    property int columns: 5
    property int rows: 5

    ListModel {
        id: game_fields
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

        function reveal_field(column, row) {
            console.log("reveal_field", column, row)
            py.call("minesweeper_qml.reveal", [column, row]);
        }
    }

    Grid {
        id: grid

        anchors.fill: parent

        columns: game_window.columns
        rows: game_window.rows
        spacing: 0

        horizontalItemAlignment: Grid.AlignHCenter
        verticalItemAlignment: Grid.AlignVCenter

        property int which: 0

        Repeater {
            model: game_fields

            Loader {
                width: grid.width/grid.columns
                height: grid.height/grid.rows
                source: {
                    return "field.qml"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        var column = index % grid.columns;
                        var row = index / grid.rows;
                        py.reveal_field(Math.floor(column), Math.floor(row));
                    }
                }
            }
        }
    }
}
