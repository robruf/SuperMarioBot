SuperMarioBot -- 0.1

This is a plugin-based IRC bot. If you want to add a cool functionality to the bot, you can do it by writing a little script and placing it in the plugins/ folder.

A plugin needs to have two functions in order to work: control() and main(array). Control() simply checks if the plugin needs to be executed; main(array) contains the plugin's functionalities itself.

main(arg) gets a list of three elements as a arg: the socket on which it operates, the channel name and the data received.


See examples in plugins/ for a better understanding.


Usage:	

	@mariobot !load plugin_name

	@mariobot !command

	@mariobot !unload plugin_name


