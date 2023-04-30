# Summary

Define key components in car racing system that will support interaction between Car, Model, Track. UI, Traing and Competition system will build above them.
- [Track](track\index.md) define the characteristics of a racing track. It act as the physical engine. Given a car's current status will provide:
    - CarView: what the car can see of the track environment.
    - Given Model's output, what is the car's status at delta time from now. 
- [Car](car\index.md) represent data unique to a car. At beginning, all cars can be same except its identity.
   - Static data - like size, friction ratio(static, sliding, rotation), maximum (linear, angular) velocity and acceleration. 
    - Runtime data - location (X, Y), velocity (V_x, V_y), Angle, etc.
- [Model](model\index.md) represent to AI function, which take the car's data, CarView, generate an Action to drive the car.  
- [Run](run\index.md) system drive the interaction between Car, Model and Track, generate a race dataset.
- [Training](traing\index.md) system will drive model training.
    - Online: call model to adjust at every interaction between Car, Model and Track.
    - Offline: call model to adjust with a completed race dataset.
- [UI](ui\index.md) visualize a race:
    - Offline mode: based on saved race dataset. It can support pause, fast forward, at different speed, frame by frame etc.
    - online mode: interact with car, model and track in realtime, collect data at each interaction, and update UI. Support to save a race dataset, enable to playback later in offline mode.
- [Competition](competition\index.md):
    - A game is defined a run with specific combination of one or multiple car (with its model), and a track. 
    - A game data contains race data for each car, generate result such as each car's time, position, score, ranking point etc.
    - Select which set of cars will play at each game.
    - decide which car to advance and final standing.


