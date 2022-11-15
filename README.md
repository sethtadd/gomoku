# Gomoku

This project includes a graphical (pygame) gomoku game as well as a brute-force engine. Only use the brute force engine for 3x3 tic-tac-toe games; anything larger will take forever.

My goal is to create a [MCTS](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) with [UCT](https://www.chessprogramming.org/UCT) engine that utilizes neural networks to direct search/evaluation of the game's state space. The [AlphaZero](https://arxiv.org/pdf/1712.01815.pdf) paper is a good reference for this, as well as [this article](https://nikcheerla.github.io/deeplearningschool/2018/01/01/AlphaZero-Explained/) which demonstrates some implementation of the algorithm.

## TODO
- put BoardGUI and player **classes on separate processes**
  - being on different threads (current implementation) seems to make the GUI start up slowly due to the player classes using all resources (python GIL)
  - BoardGUI should be run on the main process and GameController on child process with each player on another child process off of GameController's process
- **implement ML algorithm** to play tic-tac-toe, then move on to 8x8 gomoku then full 15x15 gomoku
- **convert static functions** in Board into inner functions since they're only called from within another function
- **take advantage of Gomoku symmetries**: consider making the hash for a gomoku board rotation/reflection invariant
  - for a given board, calculate all 8 relfections/rotations, hash each one, order the hashes in increasing order, then take the minimum hash
  - the next thing to do would be to also store the transformation **FROM** the transformed board associated with the minimum hash **TO** the actual board so that when pushing a move it can be transformed correctly to be placed on the actual board in the intended position
