import QtQuick 2.5

Item {
	property alias interval: _timer.interval
	property alias running: _timer.running
	signal triggered()

	property Timer _timer
	property double _start_time: -1
	property double _stop_time: -1

	Timer {
		id: _timer
		onTriggered: parent.triggered()
		repeat: true
	}

	function start() {
		if (!_timer.running) {
			_start_time = Date.now()
			_stop_time = -1
			_timer.start()
		}
	}

	function stop() {
		if (_timer.running) {
			_stop_time = Date.now()
			_timer.stop()
		}
	}
	
	function passed() {
		if (_start_time >= 0) {
			if (_stop_time >= 0) 
				return _stop_time - _start_time
			else
				return Date.now() - _start_time
		} else {
			return 0;
		}
	}
}
