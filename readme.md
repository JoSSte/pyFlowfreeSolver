# Flow free solver


## Overall Strategy
First figure out if we can solve the problem, then detect the layout and problem, and draw the solution...

1. [x] Set up game board
1. [ ] Solve pathing
   - [ ] Create layout for field
   - [ ] Connect Colours
   - [ ] Find orphans
   - [ ] Solve paths
   - [ ] Advanced pathfinding/optimisations
1. [ ] Draw solution
1. [ ] Detect playing field (only rectangles to start with)
1. [ ] Detect piece placement
1. [ ] Save screenshot
1. [ ] Get next playing field

## Board setup

### Calculating Neighbouring cells
Considering height `h` and width `w`, the rectangle will be like this:

![Conceptual bord](dimensions.svg)

So all non-edge cells (denoted `n`) have four neighbours: 
1. North (`n-w`)
1. South (`n+w`)
1. West (`n-1`)
1. East (`n+1`)

### Cells with 2 neighbours only 
The four corners that have only two neighbours are:
1. North-West (`n=1`)
1. North-East (`n=w`)
1. South-West (`n=1`)
1. South-East (`n=((h-1)*w)+1`)

### Cells on edges 
This includes the cells with only 2 neighbours twice, except for cell 1
1. Top row (`n<=w`)
1. Bottom row (`n>=(h*w)-w`)
1. First column (`n%(w+1)=0`) (doesn't match cell 1)
1. Last column (`n%w=0`)

### Calculating total number of intersections
All the vertical paths can be summed up as the number of columns minus one, multiplied by the number of rows. Similarly, the horizontal paths can be summe up as the number of rows minus one, multiplied my the number of columns. 

`t=(w-1)*h+(h-1)*w`



## Failure Conditions
Conditions that would cause a failure state, ie the game would be unsolvable.

* **Orphan unoccupied cell.** Cell where all neighbours are occupied, but the cell itself isn't.
* **Single cell kink.** Line creating a cell with only one free neighbour, all other (max 3) neighbouring cells occupied.
* **Orphaned Piece.** Pieces of the same colour on opposite sides of the line.

## Path solving tactics

### Path solving
* **Outside to inside.** Finding a piece in the outer cells, and following the border clockwise (CW) or counter-clockwise (CCW)., repeating the method on each colour pair, until solved.  
This tactic wil most likely work for simple, small boards. In case of having to snake around another this tactic will fail. May be able to be used as a trailbreaker.
* **Single cell path.** If both pieces share a single cell neighbour, so that filling out that cell will connect them. E.g. diagonals may be a more certain win, verticals or horizontals may not be.
* **Path finding algorithms** These will find the shortest path, but may not be efficient for finding the first paths in an unsolved board.
  * **A-Star.** Using the [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) algorithm for path finding.
  * **Dijkstra.** Using [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) for path finding. 

### Path certainty score
* Any path creating a failure condition with no other paths drawn should be considered unusable - negative score.
* A single cell path where there is a dead end e.g. in the corner of a board should be a high scorer.