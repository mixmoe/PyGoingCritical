from services.core import Network
from services.models import SusceptibleInflectedSusceptible
from services.render import Render

from .builder import BuilderRoot
from .bus import EventBus
from .components.interactive import AdjustLayerRoot, ButtonsLayerRoot, InteractiveRoot

BuilderRoot["main"]["SISmodel"] = InteractiveRoot
BuilderRoot["main"]["SISmodel"].setInitArgs(name="SISmodel", enableRecovery=True)

_NETWORK = Network(30, 30)
_TRANSMISSION_RATE = 0
_RECOVERY_RATE = 0
_MODEL = None


@EventBus.subscribe("SISmodel_init")
def modelInit(component: InteractiveRoot):
    global _MODEL
    _MODEL = None
    image = Render(network=_NETWORK).export()
    component.imageView.setImage(image=image)


@EventBus.subscribe("SISmodel_reset")
def modelReset(component: ButtonsLayerRoot):
    rootComponent: InteractiveRoot = BuilderRoot["main"][
        "SISmodel"
    ].component  # type:ignore
    assert rootComponent is not None
    assert modelInit is not None
    modelInit(rootComponent)


@EventBus.subscribe("SISmodel_transmission_adjust")
def transmissionAdjust(component: AdjustLayerRoot):
    global _TRANSMISSION_RATE
    _TRANSMISSION_RATE = component.transmissionRateAdjuster.get() / 100
    rootComponent = BuilderRoot["main"]["SISmodel"].component
    assert rootComponent is not None
    assert modelInit is not None
    modelInit(rootComponent)


@EventBus.subscribe("SISmodel_recovery_adjust")
def recoveryAdjust(component: AdjustLayerRoot):
    global _RECOVERY_RATE
    _RECOVERY_RATE = component.recoveryRateAdjuster.get() / 100
    rootComponent = BuilderRoot["main"]["SISmodel"].component
    assert rootComponent is not None
    assert modelInit is not None
    modelInit(rootComponent)


@EventBus.subscribe("SISmodel_step")
def transmissionStep(component: ButtonsLayerRoot):
    global _MODEL
    _MODEL = (
        SusceptibleInflectedSusceptible(
            _NETWORK, transmissionRate=_TRANSMISSION_RATE, recoveryRate=_RECOVERY_RATE
        )
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
        "SISmodel"
    ].component  # type:ignore
    assert rootComponent is not None
    rootComponent.imageView.setImage(image=image)


@EventBus.subscribe("SISmodel_play_control")
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
