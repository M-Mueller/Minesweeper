import QtQuick 2.5

Item {
	id: root

	implicitWidth: grid.implicitWidth
	implicitHeight: grid.implicitHeight

	property alias model: items.model
	property alias columns: grid.columns
	property alias rows: grid.rows

	property int fieldSize: {
		if (columns > 10 || rows > 10)
			25
		else
			50
	}	

	Grid {
		id: grid
		spacing: 2

		horizontalItemAlignment: Grid.AlignHCenter
		verticalItemAlignment: Grid.AlignVCenter

		add: Transition {
			id: transition
			// slide in rows from the bottom
			SequentialAnimation {
				PauseAnimation {
					// delay each row
					duration: transition.ViewTransition.item.row*20
				}
				NumberAnimation {
					properties: "y"
					duration: 500
					easing.type: Easing.OutQuint
					easing.amplitude: 0.8
				}
			}
		}

		Repeater {
			id: items
		
			Field {
				width: root.fieldSize
				height: root.fieldSize

				column: Math.floor(index % grid.columns);
				row: Math.floor(index / grid.columns);

				// init below the actual field for nice transition
				y: grid.implicitHeight+row*height
			}
		}
	}
}

