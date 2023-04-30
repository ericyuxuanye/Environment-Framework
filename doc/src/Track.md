# Track

Track define the characteristics of a racing track. It act as the physical engine. 

A track field is defined as a rectangular area consist of equal sized tiles. 

## Coordinate

When showing on screen, the upper left corner is at (0, 0). X direct from left to right. Y direct from up to low. A position in field is defined as a Point with positive value. A field of size 2000 meter wide and 500 meter height has: upper left corner (0, 0), upper right corner (0, 2000), lower left corner (500, 0), lower right corner (500, 2000).

## Field Tile
Each tile has its own tile type, which define its physical charactoristics such as the fraction ratio. Initial set of tiles include:

| Type | TypeId | FrictionRatio |
| --- | ---: | ---: |
| Road | 0 | 1 | 
| Shoulder | 1 | 3 | 
| Wall | 2 | 100 | 

A car can run well on road, slower on shoulder, and quickly stop on wall. 


## CenterTiles

To track car's progress in the race, we use number of times it complete a whole track round. 

We use the center of a track as the logical route. A set of tiles is defined as center tiles. Each center tile's center point is the marker along the route. Neighbouring center tiles along the route touch in either corner or edge. Distances between consective center tiles is either ```1``` or ```sqrt(2)```.  

Track distance is the sum of segment length along center tiles. Center tile's distance is calculated as some of distance along center route from start, divided by track distance. Other tile's distance is equal to its closest center tile's distance. If a tile has same distince to 2 different center tiles, use the smaller distance.

A car use the distince of the tile it touches. A car start race at distance 0. Finish a whole round along the track get progress of 1. If a car travel along the center tiles, its will be most efficient. 

```
Tile
    TypeId  typeId
    bool    isCenter
    float   distance    
```

## TrackField

TrackField class
```
TrackField:

    Tile Field[Width, Height];

```
Row and column index start with 0. 

A small TrackField of 5 by 11 meter consist of tile size of 1 by 1 meter, each tile is represent as {TypeId, IsCenter, discance} can be:

```
{
    "Field" : 
    {
        {{2,1,0}, {2,1,0.1}, {2,1,0.2}, {2,1,0.3}, {2,1,0.4}, {2,1,0.5}, {2,1,0.6}, {2,1,0.7}, {2,1,0.8}, {2,1,0.9}, {2,1,1}},
        {{1,1,0}, {1,1,0.1}, {1,1,0.2}, {1,1,0.3}, {1,1,0.4}, {1,1,0.5}, {1,1,0.6}, {1,1,0.7}, {1,1,0.8}, {1,1,0.9}, {1,1,1}},
        {{0,1,0}, {0,1,0.1}, {0,1,0.2}, {0,1,0.3}, {0,1,0.4}, {1,1,0.5}, {0,1,0.6}, {0,1,0.7}, {0,1,0.8}, {0,1,0.9}, {0,1,1}},
        {{0,1,0}, {0,1,0.1}, {0,1,0.2}, {0,1,0.3}, {0,1,0.4}, {1,1,0.5}, {0,1,0.6}, {0,1,0.7}, {0,1,0.8}, {0,1,0.9}, {0,1,1}},
        {{2,1,0}, {2,1,0.1}, {2,1,0.2}, {2,1,0.3}, {2,1,0.4}, {2,1,0.5}, {2,1,0.6}, {2,1,0.7}, {2,1,0.8}, {2,1,0.9}, {2,1,1}},
    }
}
```

In this track, top and bottom rows are wall. Logical route go through the 2 row, start at ```[2,0]```, end at ```[2,11]```. Track distance is 10. there is a shoulder tile on the logical route. This track only have a straight track, does not support multiple round race. 



# CarView
Car has a limited view of the track field. Depending the car's position, only a subset of the track field around the car is visible. 

```
CarView:
    Point UpperLeft;
    Tile Field[] ; a sub section of the track field 

```

We can define how far the can can see. Assume we allow a car to see two tiles from current tile on all 4 direction. When the car is on tile ```[2,3]```, the CarView is:

```
   {
    "UpperLeft" : 
        {
            X : 0,
            Y : 1,
        }
    "Field" : 
    {
        {{2,1,0.1}, {2,1,0.2}, {2,1,0.3}, {2,1,0.4}, {2,1,0.5},},
        {{1,1,0.1}, {1,1,0.2}, {1,1,0.3}, {1,1,0.4}, {1,1,0.5},},
        {{0,1,0.1}, {0,1,0.2}, {0,1,0.3}, {0,1,0.4}, {1,1,0.5},},
        {{0,1,0.1}, {0,1,0.2}, {0,1,0.3}, {0,1,0.4}, {1,1,0.5},},
        {{2,1,0.1}, {2,1,0.2}, {2,1,0.3}, {2,1,0.4}, {2,1,0.5},},
    }
} 
```


## TrackSystem 

TrackSystem provide live data in a race. 

```
TrackSystem

public :
    CarView GetCarView(CarState) 
    ; return sub section of TraveField visible to car at position of CarState.

    CarState GetNextState(CarState, Action, timeInterval)
    ; return the CarState using Action after timeInterval.

    const Shape FieldShape
    ; return (Width, Height) of whole TrackField. 
    ; could help Model if it want to build the whole TrackField.
    
private :
    ; physical engine function, should be stable. 
    CarState GetNextState(CarState, Action, timeInterval, CarConfig, TileConfig)

    TrackField trackField;
```


## Future expansion

### Noisy phyical world

We can model imperfection of a track field by adding a noise to individual tile. The noise is defined an error on a tile's fraction ratio. Noise distribution should follow standard distribution, center at 0. Most tiles do not differ much from its ideal case. 

Combination of TrackField and NoiseSet identify a race setting. 

Including noice into environment will make each race unique. It help to test AI model's robustness, as well as add some unpredictability.

A multiple round competition can be more interesting, even using same TrackField, with different NoiseSet. 


