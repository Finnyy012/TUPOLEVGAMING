import numpy as np
from munkres import Munkres

import team
import settings


class AbsoluteDistanceTeam(team.Team):
    def __init__(
        self, 
        targets,
        n_agents,
        agent_description: dict,
        team_number: int
    ) -> None:
        super().__init__(
            targets,
            n_agents,
            agent_description,
            team_number
        )
        
        self.assign_targets()
    
    def calculate_distance(self, agent, target):
        dx = min(
            abs(agent.rot_rect.center[0] - target[0]), 
            settings.SCREEN_WIDTH - abs(agent.rot_rect.center[0] - target[0])
        )
        dy = abs(agent.rot_rect.center[1] - target[1])
        return np.sqrt(dx**2 + dy**2)
        
    def assign_targets(self) -> None:
        afstanden = np.zeros((len(self.agents), len(self.targets)))
        
        for i, agent in enumerate(self.agents):
            agent.target = None
            for j, target in enumerate(self.targets):
                afstanden[i, j] = self.calculate_distance(agent, target)

        m = Munkres()
        toewijzingen = m.compute(afstanden.tolist())

        for i, j in toewijzingen:
            self.agents[i].target = self.targets[j]

        # Print resultaten
        # for vliegtuig in self.agents:
        #     if vliegtuig.target is not None:
        #         print(f"Vliegtuig op ({vliegtuig.rot_rect.center[0]}, {vliegtuig.rot_rect.center[1]}) heeft target op ({vliegtuig.target})")
        #     else:
        #         print(f"Vliegtuig op ({vliegtuig.rot_rect.center[0]}, {vliegtuig.rot_rect.center[1]}) heeft geen target.")    

