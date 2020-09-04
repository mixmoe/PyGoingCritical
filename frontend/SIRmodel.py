from .components.interactive import InteractiveRoot, AdjustLayerRoot, ButtonsLayerRoot
from .bus import EventBus
from services.render import Render
from services.core import Network
from services.models import SusceptibleInflectedRemoved

from .builder import BuilderRoot

BuilderRoot["main"]["SIRmodel"] = InteractiveRoot
BuilderRoot["main"]["SIRmodel"].setInitArgs(name="SIRmodel")

_NETWORK = Network(30, 30)
_TRANSMISSION_RATE = 0
_MODEL = None


@EventBus.subscribe("SIRmodel_init")
def modelInit(component: InteractiveRoot):
    global _MODEL
    _MODEL = None
    image = Render(network=_NETWORK).export()
    component.imageView.setImage(image=image)


@EventBus.subscribe("SIRmodel_reset")
def modelReset(component: ButtonsLayerRoot):
    rootComponent: InteractiveRoot = BuilderRoot["main"][
        "SIRmodel"
    ].component  # type:ignore
    assert rootComponent is not None
    assert modelInit is not None
    modelInit(rootComponent)


@EventBus.subscribe("SIRmodel_transmission_adjust")
def transmissionAdjust(component: AdjustLayerRoot):
    global _TRANSMISSION_RATE
    _TRANSMISSION_RATE = component.transmissionRateAdjuster.get() / 100
    rootComponent = BuilderRoot["main"]["SIRmodel"].component
    assert rootComponent is not None
    assert modelInit is not None
    modelInit(rootComponent)


@EventBus.subscribe("SIRmodel_step")
def transmissionStep(component: ButtonsLayerRoot):
    global _MODEL
    _MODEL = (
        SusceptibleInflectedRemoved(_NETWORK, transmissionRate=_TRANSMISSION_RATE)
        if _MODEL is None
        else _MODEL
    )
    try:
        calculatedNetwork = next(_MODEL)
    except StopIteration:
        component.imagePlayControl()
        return
    image = Render(network=calculatedNetwork).export()
    rootComponent: InteractiveRoot = BuilderRoot["main"][
        "SIRmodel"
    ].component  # type:ignore
    assert rootComponent is not None
    rootComponent.imageView.setImage(image=image)


@EventBus.subscribe("SIRmodel_play_control")
def playControl(component: ButtonsLayerRoot):
    def transmissionPlay():
        if component.paused:
            return
        component.imageStep()
        component.after(200, transmissionPlay)

    if component.paused:
        component.playControlButton.configure(text="暂停")
        component.playControlButton.update()
        component.paused = False
    else:
        component.playControlButton.configure(text="开始")
        component.playControlButton.update()
        component.paused = True
        return
    component.after(200, transmissionPlay)
