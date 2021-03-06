import tkinter as tk
from typing import Any, Dict

from services.core import Network
from services.models import SusceptibleInflectedRemoved
from services.render import Render

from ..bus import EventBusNamespace
from ..components.interactive import InteractiveRoot

__view_name__ = "SIRModel"
__view_widget__ = InteractiveRoot
__view_args__: Dict[str, Any] = {"name": __view_name__}

EventBus = EventBusNamespace.get(__view_name__, create=True)

_MODEL = None
_NETWORK = Network(30, 30)
_TRANSMISSION_RATE = 0


class SIRModelRoot(InteractiveRoot):
    def __init__(self, root: tk.Widget):
        super().__init__(root, **__view_args__)


@EventBus.subscribe("reset")
@EventBus.subscribe("init")
def modelInit(component: InteractiveRoot):
    global _MODEL, _NETWORK
    _MODEL, _NETWORK = None, Network(30, 30)
    image = Render(network=_NETWORK).export()
    component.imageView.setImage(image=image)


@EventBus.subscribe("transmission_adjust")
def transmissionAdjust(component: InteractiveRoot):
    global _TRANSMISSION_RATE, _MODEL
    _TRANSMISSION_RATE = component.adjust.transmissionRateAdjuster.get() / 100
    _MODEL = None


@EventBus.subscribe("step")
def transmissionStep(component: InteractiveRoot):
    global _MODEL, _NETWORK
    _MODEL = (
        SusceptibleInflectedRemoved(_NETWORK, transmissionRate=_TRANSMISSION_RATE)
        if _MODEL is None
        else _MODEL
    )
    try:
        _NETWORK = next(_MODEL)
    except StopIteration:
        component.buttons.imagePlayControl()
        return
    image = Render(network=_NETWORK).export()
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