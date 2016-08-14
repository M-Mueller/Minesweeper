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

		Repeater {
			id: items
		
			Loader {
				width: 50
				height: 50
				source: {
					return "Field.qml"
				}
			}
		}
	}
}

