import numpy as np

from agent import Agent
import settings


class Team:
    """
    Base class for team.
    Only implements constructor and empty bidding method to override.

    + targets (list[tuple[float, float]]) all targets xy coords
    + agents (list[Agent]) list with all existing agents for team
    """
    def __init__(
        self, 
        targets: list[tuple[float, float]],
        n_agents: int,
        agent_description: dict,
        team_number: int
    ) -> None:
        """
        Constructor for Team.

        :param targets: (list[tuple[float, float]]) 
        all targets xy coords
        :param n_agents: (int) number of agents to construct
        :param agent_description: (dict) a dict used for creating agents
        must contain at minimum the following keys:
        - SPRITE
        - SPRITE_TOP
        - MASS
        - ENGINE_FORCE
        - AGILITY
        - C_DRAG
        - C_LIFT
        - AOA_CRIT_LOW
        - AOA_CRIT_HIGH
        - CL0
        - CD_MIN
        - INIT_THROTTLE
        - INIT_V
        :param team_number: (int) number of team, 
        1 starts on the left, 2 starts on the right (facing left)
        """
        self.targets = targets

        self.agents = []
        if team_number not in [0,1]:
            raise NotImplementedError(
                "Simulation does not support more\
                 than 2 teams at this point in time."
            )

        for i in range(n_agents):
            if team_number == 0:
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
                    0.0, # Start pitch
                    agent_description["INIT_V"],
                    np.array((
                        0.0, # start x
                        float(
                            (settings.SCREEN_HEIGHT / n_agents / 2) +
                            (settings.SCREEN_HEIGHT / n_agents * (i-1))
                        )
                    )) / settings.PLANE_POS_SCALE % settings.SCREEN_RESOLUTION,
                    agent_description["SIZE"]
                ))
            if team_number == 1:
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
                    180, # start pitch
                    -np.array(agent_description["INIT_V"]),
                    np.array((
                        settings.SCREEN_WIDTH - 1.0, # start x
                        float(
                            (settings.SCREEN_HEIGHT / n_agents / 2) +
                            (settings.SCREEN_HEIGHT / n_agents * (i-1))
                        )
                    )) / settings.PLANE_POS_SCALE % settings.SCREEN_RESOLUTION,
                    agent_description["SIZE"]
                ))


    def assign_targets(self) -> None:
        """
        Bidding function for team. 
        This function should be implemented in child classes.
        The function should do the following:
        - Have all agents bid for a target
        - Assign each agent a target if possible
          based on the bidding results
        """
        pass