# Flow free solver


## Overall Strategy
1. [ ] Detect playing field (only rectangles to start with)
1. [ ] Set up coordinate system
1. [ ] Detect piece placement
1. [ ] Solve pathing
   - [ ] Create layout for field
   - [ ] Connect Colours
   - [ ] Find orphans
   - [ ] Solve paths
   - [ ] Advanced pathfinding/optimisations
1. [ ] Draw solution
1. [ ] Save screenshot
1. [ ] Get next playing field


## Calculating Neighbouring cells
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

## Calculating total number of intersections
All the vertical paths can be summed up as the number of columns minus one, multiplied by the number of rows. Similarly, the horizontal paths can be summe up as the number of rows minus one, multiplied my the number of columns. 

`t=(w-1)*h+(h-1)*w`