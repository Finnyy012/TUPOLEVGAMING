import numpy as np
from munkres import Munkres


class Team:
    def __init__(self, 
                 targets,
                 agents
                 ) -> None:
        self.targets = targets
        self.aircrafts = agents
        
        self.assign_targets()

    def calculate_distance(self, aircraft, target):
        return np.sqrt(
            (aircraft.rot_rect.center[0] - target.coords[0])**2 + 
            (aircraft.rot_rect.center[1] - target.coords[1])**2
        )
        
    def assign_targets(self) -> None:
        afstanden = np.zeros((len(self.aircrafts), len(self.targets)))
        
        for i, aircraft in enumerate(self.aircrafts):
            aircraft.target = None
            for j, target in enumerate(self.targets):
                afstanden[i, j] = self.calculate_distance(aircraft, target)

        m = Munkres()
        toewijzingen = m.compute(afstanden.tolist())

        for i, j in toewijzingen:
            self.aircrafts[i].target = self.targets[j].coords

        # Print resultaten
        for vliegtuig in self.aircrafts:
            if vliegtuig.target is not None:
                print(f"Vliegtuig op ({vliegtuig.rot_rect.center[0]}, {vliegtuig.rot_rect.center[1]}) heeft target op ({vliegtuig.target})")
            else:
                print(f"Vliegtuig op ({vliegtuig.rot_rect.center[0]}, {vliegtuig.rot_rect.center[1]}) heeft geen target.")    

    # def update(self) -> None:
    #     for aircraft in self.add_aircrafts:
    #         if aircraft.target == None:
    #             self.assign_targets()
    #             break