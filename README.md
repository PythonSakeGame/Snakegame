# snake2
This is our Version of the popular game Snake, programmed in python using the pygame module.
You play as a  snake, and your goal is to eat as much food as possible without hitting yourself or the walls. For each item you eat, you grow by one unit and gain a point.
The game has three themes - Regular Snake, Space and Sweets. A starting theme is chosen at random, and it changes every ten points reached.  
Use the arrow keys on your keyboard to control the snake´s movement. 
Your highscore is saved - try to beat it!
If you want to manually adjust the speed of the game, you can edit the code in the game loop by changing the value of time.sleep() (0.15 is the default value; please be careful when editing the code.)
Please download all files from the repository.
To run the game, you will need to install the pygame module. A quick guide on how to do this can be found here: www.pygame.org/wiki/GettingStarted
To play the game, run the code after installing pygame. A new window will open in which the game is played. 




This approach also works for installing pygame. Use it if you are having difficulty with the reccomended way of downloading
-We used PyCharm community as our IDE
-We used Python 3.9.13, but newer versions such as 3.11 will work as well.
-In PyCharm, create a new project. As an interpreter, choose System enterpreter and your installation of Python. Open the Sakegame_Base_new.py file you downloaded.
-Under "Python Packages" at the bottom of the screen, search for pygame and click install.
-Alternatively, you can use pip to install the pygame module.
The game needs to be run in a local IDE, meaning that e.g. google colab will not work.
