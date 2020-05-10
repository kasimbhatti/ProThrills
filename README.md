# ProThrills
Hackathon project

Download all 4 files, and then run the client file.

This game is a 3D version of Connect 4. It has been created completely in python, using an OpenGL wrapper for graphics control. The game allows a row and column number to be inputted (controls described in terminal when game runs), which will place the counter in the lowest layer which does not already have a counter in that row/column position. The aim of the game is no different form a normal Connect  game, except now, the game allows for Connect 4s to be made in 3 dimensions, making for significantly more interesting gameplay.

We chose to use Python for a veriety of reasons, the main one being that the graphics programmer had already worked with OpenGL before in Python, and the other reasoning being that Python is very easy to create code in and debug. This meant that many errors that would have occured due to small mistakes were easy to spot. Considering this game included many complicated problems to solve to allow for Connect 4s in 3D, making the debugging process as easy as possible was key in allowing us to finish the program in time for the deadline. If we had more time, then using the Python version as a base to work on, a more versatile version of the game could be made in a more suited language for OpenGL, such as C++.

We solved the problem of syncing data together by writing out own server which would run the game entirely on the host's side, whilst allowing the data to come from each client. This meant that as long as there was a way to prevent a client from inputting data whilst it was the other client's turn to input data, there was no data to 'sync', as all of it was processed on the same computer.

This game automatically connects you to another player who also runs the client file. These 2 players do not have to be on the same wifi or on the same machine. A player can join you from anywhere in the world. We think this is a great way to enhance gameplay, by virtually connecting you to someone else in the world, you are increasing the size of your community.

This game was intended to bring all th efun of a family connect 4 game, and virtually extend the range of players which can play with you. You could also get help with moves from your family and local community, in order to connect with them too.

This game was intended to bring fun to those that play it, so we hope that you do!
