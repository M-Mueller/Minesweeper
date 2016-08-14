import QtQuick 2.0

Item {
	id: field
	anchors.fill: parent

	Rectangle {
		anchors.fill: parent
		radius: 5
		border.width: 1
		color: "transparent"

		Text {
			anchors.centerIn: parent
			font.bold: true
			text: hint
			visible: !mine && !flag
		}

		Image {
			anchors.fill: parent
			source: "mine.png"
			fillMode: Image.PreserveAspectFit
			visible: mine && !flag
		}
	}

	Rectangle {
		// covers the hint or mine
		anchors.fill: parent
		radius: 5
		border.width: 1
		color: "lightgrey"
		opacity: {
			if (revealed)
				0.0;
			else
				1.0;
		}
		Behavior on opacity {
			NumberAnimation {
				easing.type: Easing.OutQuad
			}	
		}
	}

	Image {
		// show flag on top of cover
		anchors.fill: parent
		source: "flag.png"
		fillMode: Image.PreserveAspectFit
		visible: flag
	}

	Image {
		// highlight wrong flags when revealed on game over
		anchors.fill: parent
		source: "wrong_flag.png"
		fillMode: Image.PreserveAspectFit
		visible: revealed && !mine && flag
	}

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
