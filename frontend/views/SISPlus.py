import tkinter as tk
from typing import Any, Dict

from services.core import Network
from services.models import SusceptibleInflectedSusceptible
from services.render import DensityRender

from ..bus import EventBusNamespace
from ..components.interactive import InteractiveRoot

__view_name__ = "SISModelPlus"
__view_widget__ = InteractiveRoot
__view_args__: Dict[str, Any] = {
    "name": __view_name__,
    "enableRecovery": True,
    "enableDensity": True,
}

EventBus = EventBusNamespace.get(__view_name__, create=True)

_DENSITY_ENABLED = True
_MODEL = None
_NETWORK = Network(30, 30)
_RECOVERY_RATE = 0
_TRANSMISSION_RATE = 0


class SISModelPlusRoot(InteractiveRoot):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root, **__view_args__)


@EventBus.subscribe("reset")
@EventBus.subscribe("init")
def modelInit(component: InteractiveRoot):
    global _MODEL, _NETWORK
    _MODEL, _NETWORK = None, Network(30, 30)
    if _DENSITY_ENABLED:
        _NETWORK.makeDensityDistribution((10, 10), radius=10)
        _NETWORK.makeDensityDistribution((25, 25), radius=7)
    image = DensityRender(network=_NETWORK).export()
    component.imageView.setImage(image=image)


@EventBus.subscribe("transmission_adjust")
def transmissionAdjust(component: InteractiveRoot):
    global _TRANSMISSION_RATE, _MODEL
    _TRANSMISSION_RATE = component.adjust.transmissionRateAdjuster.get() / 100
    _MODEL = None


@EventBus.subscribe("recovery_adjust")
def recoveryAdjust(component: InteractiveRoot):
    global _RECOVERY_RATE, _MODEL
    _RECOVERY_RATE = component.adjust.recoveryRateAdjuster.get() / 100
    _MODEL = None


@EventBus.subscribe("density_switch")
def densitySwitch(component: InteractiveRoot):
    global _DENSITY_ENABLED
    _DENSITY_ENABLED = component.adjust.densityEnabled.get()
    modelInit(component)


@EventBus.subscribe("step")
def transmissionStep(component: InteractiveRoot):
    global _MODEL, _NETWORK
    _MODEL = (
        SusceptibleInflectedSusceptible(
            _NETWORK,
            transmissionRate=_TRANSMISSION_RATE,
            recoveryRate=_RECOVERY_RATE,
            useDensity=_DENSITY_ENABLED,
        )
        if _MODEL is None
        else _MODEL
    )
    try:
        _NETWORK = next(_MODEL)
    except StopIteration:
        component.buttons.imagePlayControl()
        return
    image = DensityRender(network=_NETWORK).export()
    component.imageView.setImage(image=image)


@EventBus.subscribe("play_control")
def playControl(component: InteractiveRoot):
    def transmissionPlay():
        if component.buttons.paused:
            return
        component.buttons.imageStep()
        component.after(200, transmissionPlay)

    if component.buttons.paused:
        component.buttons.playControlButton.configure(text="暂停")
        component.buttons.playControlButton.update()
        component.buttons.paused = False
    else:
        component.buttons.playControlButton.configure(text="开始")
        component.buttons.playControlButton.update()
        component.buttons.paused = True
        return
    component.after(200, transmissionPlay)