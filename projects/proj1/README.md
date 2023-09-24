# A network-wide Rock-Paper-Scissors
_stage1_

## Description
Design and implement a online [Rock-Paper-Scissors](https://en.wikipedia.org/wiki/Rock_paper_scissors) game consisting one server and multiple clients. Each client is a player.

The server starts first and listens for clients. It can handle multiple clients and multiple game sessions concurrently. 

A client connects to the server, searches for players, pairs a player to start a game session, play the game until get a decided result, or quit the game, lookup history records of all game sessions. Each player can play multiple sessions in one connection.

In each execution, the server records the information below:
- date and time
- game session number and lasting time
- all players' information such as ip address, port number, player id, player game session and result
- paired players, game sessions and results (terminated or reach a decision)


## Questions
Justify your selection and answers for all the questions.

- Which server architecture will you select? 
- What communication protocol is needed? How to design it?
- Which message framing scheme will you select?
- What data structures will you use? 
- How to divide the game logic between the clients and the server?
- How to form and handle a game session?
- What information needs to be recorded and how?
- How to save the records for persistence?
- How to modularize and organize the game?
- How to handle exceptions?
- How to test the game?


Your ideas and answers to these questions form the design of the game.

## Report
- Detail the game rules, design and implementation. 
- Explain program structure and flow.
- Demonstrate all game scenarios.
- Submit the report together with the source code.


## (10%) Extra credit
The Rock-Paper-Scissors game can be extended to include multiple players (more than two) or multiple weapons (more than two). Choose one out of the two options below:
- Multiple players: 
  - the number of players $N_p≥3$ can be configured
  - how to define the winning rules?
- Multiple weapons: 
  - the number of weapons $N_w ≥ 2$ can be configured
  - the weapon beating map can be configured


# References
- [Python program to implement Rock Paper Scissor game](https://www.geeksforgeeks.org/python-program-implement-rock-paper-scissor-game/)
- [Program Your First Multiple User Network Game in Python](https://levelup.gitconnected.com/program-your-first-multiple-user-network-game-in-python-9f4cc3650de2)
  - [Online Rock Paper Scissors p.2](https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p-2)
- [Rock Paper and Scissor Game Using Tkinter](https://www.geeksforgeeks.org/rock-paper-and-scissor-game-using-tkinter/)
- Install tkinter
  ```bash
  sudo apt install python3-tk
  ```