import abc

from utils.Utils import appendAttr


class BaseInfo(metaclass=abc.ABCMeta):
    # 反射获取所有str属性，并且设置对应的不同命名方式的值。
    def appendSelfAttr(self):
        for attrs in dir(self):
            if not attrs.startswith("__"):
                strAttr = getattr(self, attrs)
                if isinstance(strAttr, str):
                    appendAttr(self, attrs, strAttr)
                #     如果是属性那么直接追加不同命名方式的属性

                elif isinstance(strAttr, BaseInfo):
                    m = getattr(strAttr, "appendSelfAttr")
                    m()
                #     如果是BaseInfo的类型，调用appendSelfAttr()

                elif isinstance(strAttr, list):
                    for dd in strAttr:
                        if isinstance(dd, BaseInfo):
                            m = getattr(dd, "appendSelfAttr")
                            m()
                            # list类型判断是否是BseInfo，再调用

