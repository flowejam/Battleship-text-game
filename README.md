# Battleship 

Text version of the classic Battleship game

Examples of the place_ship method:  
```
game = ShipGame()
place_ship('first', 4, 'G9', 'C')
```

```
  1 2 3 4 5 6 7 8 9 10
A
B
C
D
E
F
G                 x
H                 x
I                 x
J                 x
```

`place_ship('second', 3, 'E3', 'R')`

```
  1 2 3 4 5 6 7 8 9 10
A
B
C
D
E     x x x
F
G                 
H                 
I                 
J                
```

Fire a torpedo by calling the fire_torpedo method as follows:
```
game.fire_torpedo('first', 'H3')
game.fire_torpedo('second', 'A1')
```

