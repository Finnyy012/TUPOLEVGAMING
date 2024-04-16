import numpy as np

import settings
from absolute_distance_team import AbsoluteDistanceTeam
from agent import Agent


class EnergyBiddingTeam(AbsoluteDistanceTeam):
    def __init__(
            self,
            targets: np.array,
            n_agents: int,
            agent_description: dict,
            team_number: int
    ) -> None:
        super().__init__(
            targets,
            n_agents,
            agent_description,
            team_number
        )

    def _calculate_distance(
        self,
        agent: Agent,
        target: np.ndarray
    ) -> float:
        """
        Approximates the energy required for displacement to `target`

        :param target: (np.ndarray) target vector
        :return: (Tuple[float, int])
        - approximation of required energy
        """
        E_min = float("inf")
        offset = np.array([settings.SCREEN_WIDTH, 0])
        i_min = 0

        for i in [-1, 0, 1]:
            target_relative = target - agent.rot_rect.center + i * offset

            # height energy: Eh = mgh
            Eh = (agent.mass * 9.81 * -target_relative[1])

            # rotational energy:
            # Er = |Ek1 - Ek2|, where Ek = 1/2 mv^2
            # Er = m/2 * |(v1)^2 - (v2)^2|
            Er = agent.mass / 2 * np.linalg.norm(
                agent.v ** 2 - (
                    target_relative / np.linalg.norm(
                        target_relative
                    ) * np.linalg.norm(
                        agent.v
                    )
                ) ** 2
            )

            # kinetic energy loss to drag (approximate): Ed = Fd * s
            Ed = np.linalg.norm(agent.f_drag) * np.linalg.norm(target_relative)

            if Eh + Er + Ed < E_min:
                E_min = (Eh + Er + Ed)
                i_min = i

        return E_min
