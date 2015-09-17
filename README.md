Trivius Player
==============

This is a cheat program for automatically playing games at the awesome quiz game website [Trivius](https://triviusgame.com)

### NOTE

Obviously... this is just a fun hacker mini-project. The fun is in discovering the possibility of cheating in the game, and not for actually getting to the top.

Cheat for fun, cheat to help others (while not hurting anyone). Don't cheat to win yourself.

Installation instructions
-------------------------

This is a 3 step process.

1.	Install the dependencies

	```
	sudo pip install virtualenv --upgrade
	git clone https://github.com/motleytech/playtrivius.git
	cd playtrivius
	virtualenv venv
	source env.sh
	pip install --upgrade pip
	pip install -r requirements.txt
	```

2.	Now, download the driver for your browser from the internet. Chrome downloads are here... `http://chromedriver.storage.googleapis.com/index.html?path=2.19/` Download this file into the playtrivius folder.

3.	Create 'logged in' profile for your Trivius player.

	In order to play the game as a non-guest, we need to login into the browser under selenium's control. You can do this by running the following...

	```
	source env.sh
	./run.sh
	```

	These commands will open the browser to the triviusgame website. Manually login into the website (not as a guest). Chrome will remember the login info in the profile folder.

	After the login, quit the browser (for osx users - quit the app, not just close the window), and stop (ctrl-c) the run.sh command. Ignore any errors that you see on the terminal when you exit.

Ready to play
-------------

Start the automatic player and watch the fun...

```
source env.sh
./run.sh
```
