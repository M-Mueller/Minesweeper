import QtQuick 2.5
import QtQuick.Window 2.2

Window {
    id: root
	
	property int columns: 0
	property int rows: 0
	property int mines: 0
	property int margins: 12

	visible: true
	minimumWidth: {
		var w = 0
		if (loader.item) 
			w = loader.item.implicitWidth + 2*margins
		return Math.max(w, 400)
	}
	minimumHeight: {
		var h = 0 
		if (loader.item)
			h = loader.item.implicitHeight + 2*margins
		return Math.max(h, 250)
	}

	Menu {
		anchors.fill: parent
		onSelected: {
			root.columns = columns
			root.rows = rows
			root.mines = mines
			loader.source = "GamePage.qml"
		}
	}

	SequentialAnimation {
		id: loaderAnimation
		PauseAnimation {
			duration: 600
		}
		ScriptAction {
			script: {
				loader.item.setup()
				loader.item.visible = true
			}
		}
	}

	Loader {
		id: loader
		anchors.margins: margins
		anchors.fill: parent

		onLoaded: {
			item.visible = false
			item.columns = root.columns
			item.rows = root.rows
			item.mines = root.mines
			loaderAnimation.start()
		}
	}
}
