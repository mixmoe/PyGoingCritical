from random import random
from typing import Iterator, Optional, Set, Tuple

from .core import Network, Status
from utils.log import logger
from utils.misc import TimeIt


@TimeIt
def SusceptibleInflectedRemoved(
    network: Network, *, transmissionRate: float = 1.0
) -> Iterator[Network]:
    assert transmissionRate <= 1.0
    logger.info(
        f"New SIR spread model built with transmissionRate={transmissionRate:.3%}."
    )
    network = network.deepcopy()
    network.center.status = Status.INFLECTED
    calculateStep = 0
    while True:
        inflectNodes = {(i.x, i.y) for i in network.all if i.status == Status.INFLECTED}
        nearbyNodes: Set[Tuple[int, int]] = set()
        if not inflectNodes:
            break
        for position in inflectNodes:
            network.get(*position).status = Status.REMOVED
            nearbyNodes.update({(i.x, i.y) for i in network.nearby(*position)})
        for position in nearbyNodes:
            node = network.get(*position)
            if node.status != Status.SUSCEPTIBLE:
                continue
            if random() <= transmissionRate:
                node.status = Status.INFLECTED
        calculateStep += 1
        yield network.deepcopy()
    logger.info(f"SIR model calculate finished in {calculateStep} steps.")


@TimeIt
def SusceptibleInflectedSusceptible(
    network: Network,
    *,
    transmissionRate: float = 1.0,
    recoveryRate: Optional[float] = None,
    useDensity: bool = False,
) -> Iterator[Network]:
    recoveryRate = transmissionRate if recoveryRate is None else recoveryRate
    assert transmissionRate <= 1.0
    assert recoveryRate <= 1.0
    logger.info(
        "New SIS spread model built with "
        f"transmissionRate={transmissionRate:.3%}, "
        f"recoveryRate={recoveryRate:.3%}, "
        f"useDensity={useDensity}."
    )
    network = network.deepcopy()
    network.center.status = Status.INFLECTED
    calculateStep = 0
    while True:
        inflectNodes = {(i.x, i.y) for i in network.all if i.status == Status.INFLECTED}
        nearbyNodes: Set[Tuple[int, int]] = set()
        if not inflectNodes:
            break
        for position in inflectNodes:
            node = network.get(*position)
            node.status = (
                Status.SUSCEPTIBLE if random() <= recoveryRate else Status.INFLECTED
            )
            nearbyNodes.update({(i.x, i.y) for i in network.nearby(node=node)})
        for position in nearbyNodes:
            node = network.get(*position)
            if node.status != Status.SUSCEPTIBLE:
                continue
            if random() <= (
                (transmissionRate + (1 - transmissionRate) * (node.density - 1))
                if useDensity
                else transmissionRate
            ):
                node.status = Status.INFLECTED
        calculateStep += 1
        yield network.deepcopy()
    logger.info(f"SIS model calculate finished in {calculateStep} steps.")