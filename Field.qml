import QtQuick 2.0

Item {
	id: field

	property int column: 0
	property int row: 0

	Rectangle {
		anchors.fill: parent
		radius: 5
		color: "#E5E7E9"

		Text {
			anchors.centerIn: parent
			font.bold: true
            font.pixelSize: field.height*0.6
			text: hint
			visible: !mine && !flag && hint > 0
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
		color: "#909497"
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
			if (mouse.button === Qt.LeftButton)
				py.reveal_field(column, row);
			else
				py.mark_field(column, row);
		}
	}
}
