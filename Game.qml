import QtQuick 2.5

Item {
	property alias model: items.model

	Grid {
		id: grid
		columns: game_window.columns
		rows: game_window.rows
		spacing: 2

		horizontalItemAlignment: Grid.AlignHCenter
		verticalItemAlignment: Grid.AlignVCenter

		add: Transition {
			id: transition
			// move in rows from the button
			SequentialAnimation {
				PauseAnimation {
					// delay each row
					duration: transition.ViewTransition.item.row*50
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
				width: 50
				height: 50

				column: Math.floor(index % grid.columns);
				row: Math.floor(index / grid.rows);

				// init below the actual field for animation
				y: 200+row*height
			}
		}
	}
}

