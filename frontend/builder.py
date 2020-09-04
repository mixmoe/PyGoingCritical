import tkinter as tk
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Type, Union

from utils.log import logger

TkComponent_T = Union[tk.Widget, tk.Misc]


@dataclass(frozen=True)
class BuilderInfo:
    child: Dict[str, "BuilderInfo"]
    widget: Type[tk.Widget]
    args: Dict[str, Any]


class Builder:
    def __init__(self, widget: Type[tk.Widget]):
        self.component: Optional[tk.Widget] = None
        self.componentTree: Dict[str, "Builder"] = {}
        self.kwargs: Dict[str, Any] = {}
        self.widget = widget

    def __getitem__(self, key: str) -> "Builder":
        return self.componentTree[key]

    def __setitem__(self, key: str, value: Union[Type[tk.Widget], "Builder"]):
        assert key not in self.componentTree
        self.componentTree[key] = (
            value
            if isinstance(value, self.__class__)
            else self.__class__(value)  # type:ignore
        )

    def __delitem__(self, key: str):
        assert key in self.componentTree
        self.componentTree.pop(key).delete()

    @property
    def data(self) -> BuilderInfo:
        return BuilderInfo(
            child={k: v.data for k, v in self.componentTree.items()},
            widget=self.widget,
            args=self.kwargs,
        )

    def toDict(self) -> Dict[str, Any]:
        return asdict(self.data)

    def setInitArgs(self, **kwargs):
        self.kwargs.update(kwargs)

    def init(self, root: TkComponent_T):
        self.component = self.widget(root, **self.kwargs)
        for k, v in self.componentTree.items():
            logger.debug(f"Initializing component {k!r} with root {root!r}.")
            v.init(root=self.component)

    def delete(self):
        if self.component:
            self.component.pack_forget()
            self.component.grid_forget()
        for child in self.componentTree.values():
            child.delete()
        self.componentTree.clear()


class _BuilderRoot:
    def __init__(self):
        self.componentTree: Dict[str, Builder] = {}
        self.root: Optional[tk.Tk] = None

    def __getitem__(self, key: str) -> Builder:
        return self.componentTree[key]

    def __setitem__(self, key: str, value: Type[tk.Widget]):
        assert key not in self.componentTree
        self.componentTree[key] = Builder(value)

    def __delitem__(self, key: str):
        assert key in self.componentTree
        self.componentTree.pop(key).delete()

    def toDict(self):
        return {
            k: (v.data if isinstance(v, Builder) else v)
            for k, v in self.componentTree.items()
        }

    def __call__(self, root: Optional[tk.Tk] = None):
        self.root = root or self.root or tk.Tk()
        for k, v in self.componentTree.items():
            logger.debug(f"Initializing component {k!r} based root.")
            v.init(self.root)
        logger.info(f"Component tree initialized: {self.toDict()!r}")
        return self


BuilderRoot = _BuilderRoot()
