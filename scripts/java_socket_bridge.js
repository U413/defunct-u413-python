// Global variables
var java_socket_bridge_ready_flag = false;

// Applet reports it is ready to use
function java_socket_bridge_ready(){
	java_socket_bridge_ready_flag = true;
}

// Connect to a given url and port
function socket_connect(url, port){
	if(java_socket_bridge_ready_flag){
		return get_java_socket_bridge().connect(url, port);
	}
	else{
		on_socket_error("Applet not yet loaded. Make sure you have java applets enabled on your browser. Select 'Run this time' on the yellow bar above if you are using Chrome.");
	}
}

// Disconnect
function socket_disconnect(){
	if(java_socket_bridge_ready_flag){
		return get_java_socket_bridge().disconnect();
	}
	else{
		on_socket_error("Applet not yet loaded. Make sure you have java applets enabled on your browser. Select 'Run this time' on the yellow bar above if you are using Chrome.");
	}
}

// Write something to the socket
function socket_send(message){
	if(java_socket_bridge_ready_flag){
		return get_java_socket_bridge().send(message);
	}
	else{
		on_socket_error("Applet not yet loaded. Make sure you have java applets enabled on your browser. Select 'Run this time' on the yellow bar above if you are using Chrome.");
	}
}

// Get something from the socket
function on_socket_get(message){}

// Report an error
function on_socket_error(message){
	alert(message);
}

// Get the applet object
function get_java_socket_bridge(){
	return document.getElementById('JavaSocketBridge');
}