import numpy as np
from munkres import Munkres

from team import Team
from agent import Agent
import settings


class AbsoluteDistanceTeam(Team):
    """
    Team class that bids using the absolute distance to the targets.

    + targets (list[tuple[float, float]]) all targets xy coords
    + agents (list[Agent]) list with all existing agents for team
    """
    def __init__(
        self, 
        targets: np.ndarray,
        n_agents: int,
        agent_description: dict,
        team_number: int
    ) -> None:
        """
        Constructor for AbsoluteDistanceTeam.
        Creates member variables using super Team class.
        Assigns starting targets to agents

        :param targets: (np.array)
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
        super().__init__(
            targets,
            n_agents,
            agent_description,
            team_number
        )
        
        self.assign_targets()
    
    def _calculate_distance(
        self, 
        agent: Agent, 
        target: np.array
    )-> float:
        """
        Calculate absolute distance between agent and target.
        It also wraps around the doughnut that is our world.

        :param agent: (Agent) current agent to analyse.
        :param target: (np.array) current target to measure.

        :return: (float) absolute distance to `target` from `agent`.
        """
        dx = min(
            abs(agent.rot_rect.center[0] - target[0]),
            settings.SCREEN_WIDTH - abs(agent.rot_rect.center[0] - target[0])
        )
        dy = abs(agent.rot_rect.center[1] - target[1])
        return np.sqrt(dx**2 + dy**2)
        
    def assign_targets(self) -> None:
        """
        Bidding function for team. 
        This function uses the absolute distance from an agent to a target
        to bid for one. 

        if there are no targets, the function returns.
        """
        distances = np.zeros((len(self.agents), len(self.targets)))
        if len(self.targets) == 0:
            return
        # calculate distances for bidding for agents.
        for i, agent in enumerate(self.agents):
            agent.target = None
            for j, target in enumerate(self.targets):
                distances[i, j] = self._calculate_distance(agent, target)

        # calculate targets
        mukres = Munkres()
        assigned_info = mukres.compute(distances.tolist())

        # assign targets
        for i, j in assigned_info:
            self.agents[i].target = self.targets[j]

    def __str__(self) -> str:
        """
        Print out class data using this method in the format of:

        Absolute Distance Team:
            Contains `n` agents.
            Currently thinks there are `n` targets.
            Score: `n`.
        """
        return f"Absolute Distance {super().__str__()}"
