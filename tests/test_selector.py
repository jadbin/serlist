# coding=utf-8

import pytest

from serlist.selector import Selector


def test_selector_list():
    html = """<li>a</li><div><ul><li>b</li><li>c</li></ul></div><ul><li>d</li></ul>"""
    s = Selector(html)
    assert s.xpath("//li/text()")[0].text == "a"
    assert s.xpath("//li/text()")[-1].text == "d"
    assert s.xpath("//div").xpath(".//li").text[0] == "b"
    assert s.xpath("//div").xpath(".//li").text[-1] == "c"


def test_attribute_selection():
    html = """<a href="http://example.com/" target=_blank>"""
    s = Selector(html)
    assert s.xpath('//a')[0].xpath('@href')[0].text == 'http://example.com/'
    assert s.xpath("//a/@href")[0].text == "http://example.com/"
    assert s.xpath("//a/@target")[0].text == "_blank"


def test_text_selection():
    html = """<div><p>expression: <var>x</var>+<var>y</var>=<var>z</var></p></div>"""
    s = Selector(html)
    assert s.xpath("//var/text()")[0].text == "x"
    assert s.xpath("//var")[0].text == "x"
    assert s.xpath("//var[last()]").text == ["z"]
    assert s.xpath("//var/text()").text == ["x", "y", "z"]
    assert s.xpath("//var").text == ["x", "y", "z"]
    assert s.xpath("//p")[0].text == "expression: x+y=z"


def test_diff_between_string_and_text():
    html = """<div><p>expression: <var>x</var>+<var>y</var>=<var>z</var></p></div>"""
    s = Selector(html)
    assert s.xpath("//var")[0].text == "x"
    assert s.xpath("//var")[0].string == "<var>x</var>"
    assert s.xpath("//var").text == ["x", "y", "z"]
    assert s.xpath("//var").string == ["<var>x</var>", "<var>y</var>", "<var>z</var>"]


def test_node_selection():
    html = """<p></p><p class='primary'>primary</p><p class="minor gray">minor</p>"""
    s = Selector(html)
    primary = s.xpath("//p[@class='primary']")
    assert len(primary) == 1 and primary[0].text == 'primary'
    minor = s.xpath("//p[@class='minor']")
    assert len(minor) == 0
    minor = s.xpath("//p[@class='gray minor']")
    assert len(minor) == 0
    minor = s.xpath("//p[@class='minor gray']")
    assert len(minor) == 1 and minor[0].text == 'minor'
    minor = s.xpath("//p[contains(@class, 'minor')]")
    assert len(minor) == 1 and minor[0].text == 'minor'


def test_wrong_arguments():
    html = b"<html></html>"
    with pytest.raises(TypeError):
        Selector(html)
    with pytest.raises(ValueError):
        Selector()


def test_node_context():
    html = "<p>header</p><div><p>text</p></div>"
    s = Selector(html)
    assert s.xpath("/p") == []
    assert s.xpath("//p") != []
    assert s.xpath("/html/body/p") != []
    assert s.xpath("//p")[0].text == "header"
    assert s.xpath("//div").xpath("//p")[0].text == "header"
    assert s.xpath("//div").xpath(".//p")[0].text == "text"
    assert s.xpath("//div").xpath("./p")[0].text == "text"
