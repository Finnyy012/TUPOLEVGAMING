import numpy as np

from agent import Agent
import settings
from munkres import Munkres


class Team:
    def __init__(self, 
                 targets,
                 n_agents,
                 agent_description: dict,
                 team_number: int
                 ) -> None:
        self.targets = targets

        self.agents = []

        start_x_coordinate = None
        start_pitch = None
        if team_number == 0:
            start_x_coordinate = 0.0
            start_pitch = 0.0
        elif team_number == 1:
            start_x_coordinate = settings.SCREEN_WIDTH - 1.0
            start_pitch = 180
        else:
            raise NotImplementedError(
                "Simulation does not support more\
                 than 2 teams at this point in time."
            )

        for i in range(n_agents):
            self.agents.append(Agent(
                settings.SCREEN_RESOLUTION,
                agent_description["SPRITE"],
                agent_description["SPRITE_TOP"],
                agent_description["MASS"],
                agent_description["ENGINE_FORCE"],
                agent_description["AGILITY"],
                agent_description["C_DRAG"],
                agent_description["C_LIFT"],
                agent_description["AOA_CRIT_LOW"],
                agent_description["AOA_CRIT_HIGH"],
                agent_description["CL0"],
                agent_description["CD_MIN"],
                agent_description["INIT_THROTTLE"],
                start_pitch,
                agent_description["INIT_V"],
                np.array((
                    start_x_coordinate, 
                    float(
                        (settings.SCREEN_HEIGHT / n_agents / 2) +
                        (settings.SCREEN_HEIGHT / n_agents * (i-1))
                    )
                )) / settings.PLANE_POS_SCALE % settings.SCREEN_RESOLUTION,
                agent_description["SIZE"]
            ))

        self.assign_targets()

    def calculate_distance(self, agent, target):
        return np.sqrt(
            (agent.rot_rect.center[0] - target[0])**2 + 
            (agent.rot_rect.center[1] - target[1])**2
        )
        
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
        for vliegtuig in self.agents:
            if vliegtuig.target is not None:
                print(f"Vliegtuig op ({vliegtuig.rot_rect.center[0]}, {vliegtuig.rot_rect.center[1]}) heeft target op ({vliegtuig.target})")
            else:
                print(f"Vliegtuig op ({vliegtuig.rot_rect.center[0]}, {vliegtuig.rot_rect.center[1]}) heeft geen target.")    

