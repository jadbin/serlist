# coding=utf-8

from lxml import etree


class Selector:
    def __init__(self, text=None, root=None):
        if text is not None:
            if not isinstance(text, str):
                raise TypeError("'text' argument must be str")
            root = etree.fromstring(text, parser=etree.HTMLParser())
        elif root is None:
            raise ValueError("Needs either text or root argument")
        self.root = root

    def xpath(self, xpath, **kwargs):
        kwargs.setdefault('smart_strings', False)
        res = self.root.xpath(xpath, **kwargs)
        if not isinstance(res, list):
            res = [res]
        return SelectorList([self.__class__(root=i) for i in res])

    @property
    def string(self):
        try:
            return etree.tostring(self.root, encoding="unicode", method='html', with_tail=False)
        except TypeError:
            return str(self.root)

    @property
    def text(self):
        try:
            return etree.tostring(self.root, encoding="unicode", method="text", with_tail=False)
        except TypeError:
            return str(self.root)


class SelectorList(list):
    def __getitem__(self, item):
        obj = super().__getitem__(item)
        return self.__class__(obj) if isinstance(item, slice) else obj

    def xpath(self, xpath, **kwargs):
        res = self.__class__()
        for i in self:
            res += i.xpath(xpath, **kwargs)
        return res

    @property
    def string(self):
        return [i.string for i in self]

    @property
    def text(self):
        return [i.text for i in self]
