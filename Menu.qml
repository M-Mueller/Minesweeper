import QtQuick 2.0

Item {
	id: root

	width: 400
	height: 300

	property int selectedMode: -1
 
    // emitted when an item was selected
	signal selected(int columns, int rows, int mines)

	states: [
		State {
			name: "VISIBLE"
			PropertyChanges {
				target: modeList
				centerOffset: 0
			}
			PropertyChanges {
				target: titleText
				anchors.verticalCenterOffset: 0
			}
		},
		State {
			name: "HIDDEN"
			PropertyChanges {
				target: modeList
				centerOffset: -modeList.width 
			}
			PropertyChanges {
				target: titleText
				anchors.verticalCenterOffset: -titleText.height
			}
		}
	]

    property bool enableSlideAnimation: false
    transitions: [
        Transition {
            to: "*"
            ParallelAnimation {
                NumberAnimation {
                    target: titleText
                    property: "verticalCenterOffset"
					duration: 300
					easing.type: Easing.InBack
                }
                SequentialAnimation {
                    // only animate on state change and not on window resize
                    ScriptAction { script: enableSlideAnimation = true }
                    PropertyAction {
                        target: modeList
                        property: "centerOffset"
                    }
                    ScriptAction { script: enableSlideAnimation = false }
                }
            }
        }
    ]

	Rectangle {
		id: title

		anchors.top: parent.top
		anchors.left: parent.left
		anchors.right: parent.right

		height: titleText.contentHeight

		Text {
			id: titleText
			anchors.left: parent.left
			anchors.right: parent.right
			anchors.verticalCenter: parent.verticalCenter

			text: "Minesweeper"
			font.pixelSize: 40
			horizontalAlignment: Text.AlignHCenter
		}
	}
	
	ListModel {
		id: modeModel
		ListElement {
			name: "Easy"
			columns: 8
			rows: 8
			mines: 10
		}

		ListElement {
			name: "Medium"
			columns: 15
			rows: 15
			mines: 30
		}

		ListElement {
			name: "Hard"
			columns: 30
			rows: 20
			mines: 50
		}
	}

	onSelectedModeChanged: {
		var item = modeModel.get(selectedMode)
		if (selectedMode >= 0) {
			var c = item.columns
			var r = item.rows
			var m = item.mines
			root.selected(c, r, m)
		}
	}
	
	Component {
		id: modeDelegate

		Rectangle {
			anchors.horizontalCenter: parent.horizontalCenter
			anchors.horizontalCenterOffset: parent.centerOffset
			width: parent.width*0.9
			height: 50

			radius: 5
			color: "lightgrey"

			Behavior on anchors.horizontalCenterOffset {
                // items slide out of visible area starting with the selected item
                enabled: enableSlideAnimation
				SequentialAnimation {
					PauseAnimation {
						duration: {
							var delay = Math.abs(selectedMode - index)
							50*delay
						}
					}
					NumberAnimation {
						duration: 500
						easing.type: Easing.InBack
					}
				}
			}

			Text {
				y: 0
				height: parent.height/2
				anchors.left: parent.left
				anchors.right: parent.right

				font.bold: true
				text: name 
				horizontalAlignment: Text.AlignHCenter
				verticalAlignment: Text.AlignVCenter
			}

			Text {
				y: parent.height/2
				height: parent.height/2
				anchors.left: parent.left
				anchors.right: parent.right

				text: columns + "x" + rows + " (" + mines + " Mines)"
				horizontalAlignment: Text.AlignHCenter
				verticalAlignment: Text.AlignVCenter
			}
			MouseArea {
				anchors.fill: parent

				onClicked: {
					selectedMode = index
					root.state = "HIDDEN"
				}
			}
		}
	}

	Column {
		id: modeList

		property int centerOffset: 0

		anchors.top: title.bottom
		anchors.left: parent.left
		anchors.right: parent.right
		anchors.bottom: parent.bottom
		anchors.margins: 10

		spacing: 10

		Repeater {
			model: modeModel
			delegate: modeDelegate
		}
	}
}
