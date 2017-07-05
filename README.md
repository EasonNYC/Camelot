
Camelot is 5-DOF Robotic Manipulator that plays a board game themed after the sentient computer HAL from "2001: A Space Odyssey" | Author: Eason Smith Eason@EasonRobotics.com 

This project remains the cumilative work of two graduate level semester projects, completed two years apart while the author was attending NYU Tandon School of Engineering.

[![Video of AI and VREP simulation footage for Camelot by Eason Smith](http://www.youtube.com/watch?v=uc2t7ujrt4c&t=6s)](http://www.youtube.com/watch?v=uc2t7ujrt4c&t=6s "Artificial Intelligence and Robot ARM Demo for Camelot board game")

Academic Description:

**CS4613 - Artificial Intelligence (Spring 2015):**  The semester long project assignment consisted of writing an AI agent for implementation of an abreviated
version of the board game of "Camelot" https://en.wikipedia.org/wiki/Camelot_(board_game) in the language of the students choice.
All game code for this assignment was written entirely in python by the author, including game logic, the GUI interactive elements,
and AI agent. While a GUI was required, it was not graded. For fun, the author themed the game after the malicious sentient computer "HAL" from the 1968 film "2001: A Space Odyssey." 
Submission guidelines included a research paper, all code and graphical elements, as well as a live demonstration of playing the game against the AI demonstrating the scope of it's search functionality.  

Artificial Intelligence overview:
  1. Search: Minimax using Alpha-Beta Pruning, Iterative Deepening, Local move ordering  
  2. Static Evaluation: Goal found, Piece Count, Closest Piece to Goal, Average Closeness  

**EL5223 - Sensor Based Robotics (Spring 2017):** The semester assignment was to apply lessons learned in class into a non-trivial robotics research project of the students choice
using the VREP robotic simulation software environment and its associated APIs. With permission from the instructor, the original Artificial Intelligence
class final project was used as a basis and a 5-DOF robotic ARM and 3D gameboard environment were created in a VREP scene. The original game code 
was updated to control the robotic manipulator. The manipulator can move 3D models of the pieces on a game board sitting on a tabletop in the VREP simulation enviroment.
New features include robotic task and 3D waypoint generation after a move has been decided. The arm will move pieces for both players. 
Submission guidelines included a research paper, all code, vrep scene and graphical elements, as well as a live demonstration of the Robotic manipulator moving pieces and playing the game.


**How to play:**
Gameplay is similar to checkers, but with the added element of the two respective center goal tiles added at the upper and lower ends of the board. Players alternate moving one piece per turn. Players may move any of their own pieces by one unit to  a free square in any direction ("plain move"). They may also jump ("Cantor") a friendly adjacent piece, moving to the free space on the friendly piece's opposite side. A "capture" move is performed by jumping over
an enemy piece that is adjacent to the players tile (similar to checkers), and removing the opposing piece from the board. The official rules were modified for this class to reduce the original search space and also to simplify it down into a viable semester-long project.

There are two ways to win.
1. Capture all of the other sides pieces by jumping over them.
2. Move one of your own pieces into the opposing sides goal while defending your own.


AUTHORS NOTE: This project and its elements are strictly not intended for redistribution of any kind, commercial or otherwise. This repo is maintained by the author for academic and reference purposes only.
Camelot game and VREP manipulator created and programmed by Eason Smith | Eason@EasonRobotics.com All other works are copyright of their respective owners.


 **Other credits:**
 1. Camelot (board game) was created by Parker Brothers  
 2. 2001: A Space Odyssey novel by Arthur C Clark  
 3. The 1968 film of the same name is directed and produced by Stanley Kubrick  
 3. Game board and Game Piece graphical elements are from https://en.wikipedia.org/wiki/Camelot_(board_game)  
 4. Uses sound clips from: www.wavsource.com/movies/2001.htm and http://sounds.stoutman.com/sounds.php?Category=HAL%209000



