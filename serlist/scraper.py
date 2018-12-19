# coding=utf-8

from collections import defaultdict

from lxml.html.clean import Cleaner

from serlist.selector import Selector

cleaner = Cleaner(scripts=True,
                  javascript=True,
                  comments=True,
                  style=True,
                  page_structure=False,
                  remove_unknown_tags=False,
                  safe_attrs_only=False)


class SerpScraper:
    def __init__(self, title_xpath=None, filter_no_link=True):
        self._title_xpath = title_xpath
        self._filter_no_link = filter_no_link

    def scrape(self, text):
        selector = Selector(text=cleaner.clean_html(text))
        title_nodes = self._detect_title_nodes(selector)
        if len(title_nodes) == 0:
            return []
        link_nodes, title_blocks = self._get_related_link_nodes(title_nodes)
        description_nodes = self._get_related_description_nodes(title_blocks)
        return self._pack_results(title_nodes, link_nodes, description_nodes)

    def _detect_title_nodes(self, selector):
        if self._title_xpath:
            h_list = selector.xpath(self._title_xpath)
        else:
            h_list = []
            # only considering <h2> and <h3>
            for i in (2, 3):
                h = selector.xpath('//h{}'.format(i))
                if len(h) >= len(h_list):
                    h_list = h
        return [i.root for i in h_list]

    def _get_related_link_nodes(self, title_nodes):
        link_nodes = []
        title_blocks = []
        for node in title_nodes:
            link = self._search_link_in_parents(node)
            if link is None:
                inner_links = self._search_link_in_children(node)
                if len(inner_links) > 0:
                    m = 0
                    for i in inner_links:
                        x = len(Selector(root=i).text.strip())
                        if x > m:
                            m = x
                            link = i
                title_blocks.append(node)
            else:
                title_blocks.append(link)
            link_nodes.append(link)
        return link_nodes, title_blocks

    def _search_link_in_parents(self, node):
        p = node
        while p is not None:
            if p.tag == 'a':
                return p
            p = p.getparent()

    def _search_link_in_children(self, node):
        res = []
        if node.tag == 'a':
            res.append(node)
        for c in node.getchildren():
            res += self._search_link_in_children(c)
        return res

    def _get_related_description_nodes(self, title_blocks):
        tnum = defaultdict(lambda: 0)
        for t in title_blocks:
            p = t
            while p is not None:
                tnum[p] += 1
                p = p.getparent()

        desc_nodes = []
        for t in title_blocks:
            desc = None
            p, d = t.getparent(), 1
            score = 0
            while p is not None and tnum[p] <= 1:
                for c in p.getchildren():
                    if tnum[c] == 0:
                        s = len(Selector(root=c).text.strip()) / d
                        if s > score:
                            score = s
                            desc = c
                p = p.getparent()
                d += 1
            desc_nodes.append(desc)
        return desc_nodes

    def _pack_results(self, title_nodes, link_nodes, description_nodes):
        res = []
        for i in range(0, len(title_nodes)):
            title = Selector(root=title_nodes[i]).text.strip()
            link = None
            if link_nodes[i] is not None:
                link = link_nodes[i].attrib.get('href')
                if link is not None:
                    link = link.strip()
                link_text = Selector(root=link_nodes[i]).text.strip()
                if len(link_text) < len(title):
                    title = link_text
            description = None
            if description_nodes[i] is not None:
                description = Selector(root=description_nodes[i]).text.strip()
            res.append({
                'title': title,
                'link': link,
                'description': description
            })
        if self._filter_no_link:
            res = [i for i in res if i['link'] is not None]
        return res
