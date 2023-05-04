# Model

Model represents the AI function. Taking in CarState, CarView, it generates an Action to drive the car.

## Action

Action is the output of Model. 

``` 
Action
    float linearAcceleration ; linear acceleration in wheel direction
    float angularVelocity ; 
```



## Model

Model class capture the data and function of AI system. Each model have its own code, and trained result data. 

During a race, a model is used in referencing mode. It loads from saved model data, generate ```Action``` in responding ```CarState``` and ```CarView```.

In training mode, a model adjusts internal data according to data from ```Car``` and ```Track```. A model saves  data for later use in referencing or training.


### Reference 

``` 
IModelReference
    bool Load() // load model data from saved file

    Action GetAction(CarState, CarView, deltaTime)
```

### Training

```
IModelTrain
    bool Load() // load model data from saved file

    bool Update(CarState, Action, UpdatedCarState) // for online training

    bool Update(RaceDataset) // for offline training

    bool Save(string folderPath) // save model data to a folder, may generate multiple files. 
```



## Model Implementation

Internal data and code logic across different models may be very different. A model may use only part of data it sees, while ignore other part.

Each model should contains a function to convert the input data into the format of internal usage. For example, it may construct a tensor, each field value extract from a input data field.

Model data saving should consider
- Easy to debug

    Write a text file, easy to read in text editor.

- Easy to load/save by other tools.
    
    Use standard format like csv, json, xml etc.

- Make it simple

    If model data structure is complex, save different part into its own file, like:
    
    - Save a matrix into csv file, can use Excel to view it.
    - Save complex data using json file.

- Robust and compatible

    Model data structure may change overtime. When design and change model data, shoule make new data not break old code, and new code not break on old data. 
    
    For row based data:
        - Do not delete an old column. Can make the old data column empty, or minimum sized valid value.
        - Add new column at end. 

    For data with named fields:
        - Add new field with new name.
        - Do not delete a field required by old code.
