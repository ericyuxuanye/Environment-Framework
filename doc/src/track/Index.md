# Track

Track define the characteristics of a racing track. It act as the physical engine. 

A track field is defined as a rectangular area consist of equal sized tiles. Each tile has its own tile type, which define its physical charactoristics such as the static, slide, rotation fraction ratio. Initial set of tiles include:

| Type | TypeId | Static | Slide | Rotation |
| --- | ---: | ---: |---: | ---: |
| Road | 0 | 5 | 3 | 1 |
| Shoulder | 1 | 10 | 6 | 2 |
| Wall | 2 | 100 | 100 | 100 |


TrackField class
```
TrackField:

    Tile Field[Width, Height];

```
Row and column index start with 0. 

A small TrackField of 5 by 10 meter consist of tile size of 1 by 1 meter can be:

```
{
    "Field" : 
    {
        {2, 2, 2, 2, 2, 2, 2, 2, 2, 2},
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
        {1, 0, 0, 0, 0, 1, 0, 0, 0, 1},
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
        {2, 2, 2, 2, 2, 2, 2, 2, 2, 2},
    }
}
```
In this track, top and bottom rows are wall. A road is in row 2 with shoulder on all sides. There is also a tile of should at middle of the road. 

A car can run well on road, slower on shoulder, and quickly stop on wall. 

Car has a limited view of the racing track. Depending the car's current position, only a subset of the racing track's data around the car is visible. 

```
CarView:
    Point UpLeft;
    Tile Field[] ; a sub section of entire track field 

```

We can define how far the can can see. If we allow a car to see 2 tiles from current tile on all 4 direction, and the car is on tile ```[2,3]```, then the CarView value should be

```
   {
    "UpLeft" : 
        {
            X : 0,
            Y : 1,
        }
    "Field" : 
    {
        {2, 2, 2, 2, 2},
        {1, 1, 1, 1, 1},
        {0, 0, 0, 0, 1},
        {1, 1, 1, 1, 1},
        {2, 2, 2, 2, 2},
    }
} 
```




Track system class
```
TrackSystem

public :
    CarView GetCarView(CarState) 
    ; return sub section of TraveField visible to car at position of CarState.

    CarState GetNextState(CarState, Action, timeInterval)
    ; return the CarState using Action after timeInterval.

    Shape GetFieldShape()
    ; return (Width, Height) of whole TrackField. 
    ; could help Model if it want to build the whole TrackField.
    

private :
    ; physical engine function, should be stable. 
    CarState GetNextState(CarState, Action, timeInterval, CarConfig, TileConfig)

```
