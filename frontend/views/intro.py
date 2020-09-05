from ..components.intro import IntroRoot
import tkinter as tk

FirstIntro = """
# 前言
    (真心不知道怎么写)
"""

SIRIntro = """
# SIR模型
    我们首先第一个要介绍的是SIR模型,即'易感人群-感染者-免疫/死亡'(Susceptible-Inflected-Removed)
    这个模型适用于一些感染了就具有抗体,例如:水痘
    或者致死率非常高的疾病,例如:埃博拉病毒
    或者传染后无法治愈的疾病,例如:乙肝
    现在看向右边的界面,上方是'节点'组成的'网络',你可以将它看作为一个地区或者一群人
    下方有一个滑块,可以修改感染概率,即'单一节点向周围节点传播'的概率

    请你现在拖拽滑块,修改感染概率,点击开始可以多次模拟模拟感染的情况

    经过观察,当感染率只要小于100%的时候,就几乎一定存在没有被感染的人口
    所以具有这种特性的病毒只要控制传染,就一定会被遏制住
    事实上也是如此,例如埃博拉病毒由于致死率过高,导致经常只是在一个区域内爆发后便销声匿迹

    接下来让我们来看看比较复杂的模型:SIS模型
"""

SISIntro = """
# SIS模型
    我们其次要介绍一个SIS模型,即'易感人群-感染者-易感人群'(Susceptible-Inflected-Susceptible)
    这个模型的特点是感染了会恢复,然后又有可能会被再次感染
    根据近期的科学研究,新冠病毒可能属于这种类型
    比较典型的属于流感

    右边这次可以控制两个滑块,分别是'传染率'和'恢复率'
    传染率代表一个节点感染周边节点的概率
    恢复率是一个节点自行恢复的概率

    提前剧透一下,这个模型具有一个非常有意思的特点,那就是它存在一个阈值
    当感染率和恢复率达到一定程度的时候,感染者会逐渐减少直至消失
    现在拖动滑块来试一试,这个'阈值'究竟是多少呢

    可以看出,只要当感染率足够低,恢复率足够高的时候,感染就会自行消失
    这从侧面说明了我们防疫的意义所在:
    隔离和佩戴口罩可以降低感染率
    而专家和医疗团队不间断运行可以确保康复率
"""

SISPlusIntro = """
# 加强版SIS模型
    To Be Continued
"""


class FirstIntroRoot(IntroRoot):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root, content=FirstIntro)


class SIRIntroRoot(IntroRoot):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root, content=SIRIntro)


class SISIntroRoot(IntroRoot):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root, content=SISIntro)


class SISPlusIntroRoot(IntroRoot):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root, content=SISPlusIntro)