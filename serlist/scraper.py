# coding=utf-8

from serlist.selector import Selector


class SerpScraper:
    def __init__(self, filter_no_link=True):
        self._filter_no_link = filter_no_link

    def scrap(self, text):
        selector = Selector(text=text)
        title_nodes = self._select_title_nodes(selector)
        if len(title_nodes) == 0:
            return []
        link_nodes = self._get_related_link_nodes(title_nodes)
        return self._pack_results(title_nodes, link_nodes)

    def _select_title_nodes(self, selector):
        h_list = []
        # only considering <h2> and <h3>
        for i in (2, 3):
            h = selector.xpath('//h{}'.format(i))
            if len(h) >= len(h_list):
                h_list = h
        return [i.root for i in h_list]

    def _get_related_link_nodes(self, title_nodes):
        link_nodes = []
        for node in title_nodes:
            link = self._search_link_in_parents(node)
            if link is None:
                link = self._search_link_in_sons(node)
            link_nodes.append(link)
        return link_nodes

    def _search_link_in_parents(self, node):
        p = node
        while True:
            p = p.getparent()
            if p is None:
                break
            if p.tag == 'a':
                return p

    def _search_link_in_sons(self, node):
        if node.tag == 'a':
            return node
        for c in node.getchildren():
            res = self._search_link_in_sons(c)
            if res is not None:
                return res

    def _pack_results(self, title_nodes, link_nodes):
        res = []
        for i in range(0, len(title_nodes)):
            title = Selector(root=title_nodes[i]).text.strip()
            link = None
            if link_nodes[i] is not None:
                link = link_nodes[i].attrib.get('href')
                if link is not None:
                    link = link.strip()
            res.append({
                'title': title,
                'link': link
            })
        if self._filter_no_link:
            res = [i for i in res if i['link'] is not None]
        return res
