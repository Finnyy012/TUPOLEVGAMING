import numpy as np
from munkres import Munkres

from team import Team
from agent import Agent

import settings


class TwoTargetsTeam(Team):
    """
    Team class that bids using the absolute distance of 
    the path to two different targets.

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
        Constructor for TwoTargetsTeam.
        Creates member variables using super Team class.
        Assigns starting targets to agents

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
        super().__init__(
            targets,
            n_agents,
            agent_description,
            team_number
        )
        
        self.assign_targets()
    
    def _calculate_distance(
        self, 
        startpoint: tuple[float, float], 
        target: tuple[float, float]
    )-> float:
        """
        Calculate absolute distance between startpoint and target.
        It also wraps around the doughnut that is our world.

        :param startpoint: (tuple[float, float]) current starting 
        point to analyse.
        :param target: (tuple[float, float]) current target to measure.

        :return: (float) absolute distance to `target` 
        from `startpoint`.
        """
        dx = min(
                abs(target[0] - startpoint[0]), 
                settings.SCREEN_WIDTH - abs(target[0] - startpoint[0])
            )
        dy = abs(target[1] - startpoint[1])
        return np.sqrt(dx**2 + dy**2)
        

    def _calculate_path(
            self, 
            target : tuple[float, float], 
            agent : Agent, 
            targets :list[tuple[float, float]]
        ) -> float:
        """
        This function bets on a target by calculating the shortest 
        distance between the agent and two targets.

        :param target: target to be bet on (target.Target)
        :param agent: agent that bets on the target (agent.Agent)
        :param targets: list of targets (list[target.Target])

        :return: the shortest distance between the agent 
        and two targets.
        """
        distance_dict = {}
        agent_pos = agent.rot_rect.center 
        agent_to_target_distance = self._calculate_distance(agent_pos, target)
        if len(targets) == 1:
            return agent_to_target_distance
        # When there are no targets there is no need 
        # to calculate a distance
        if len(targets) == 0:
            return 0

        for target2 in targets:
            if target[0] != target2[0] or target[1] != target2[1]:
                distance = self._calculate_distance(target, target2)
                total_distance = agent_to_target_distance + distance 
                distance_dict[total_distance] = (target, target2)
        return min(distance_dict.keys())

    def assign_targets(self) -> None:
        """
        Bidding function for team. 
        This function uses the absolute distance from an agent 
        to a target to another target to bid for one. 
        """
        distances = np.zeros((len(self.agents), len(self.targets)))
        if len(self.targets) == 0:
            return
        # calculate distances for bidding for agents.
        for i, agent in enumerate(self.agents):
            agent.target = None
            for j, target in enumerate(self.targets):
                distances[i, j] = self._calculate_path(target, agent, self.targets)

        # calculate targets
        mukres = Munkres()
        assigned_info = mukres.compute(distances.tolist())

        # assign targets
        for i, j in assigned_info:
            self.agents[i].target = self.targets[j]
