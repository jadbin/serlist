=======
SERList
=======

.. image:: https://travis-ci.org/jadbin/serlist.svg?branch=master
    :target: https://travis-ci.org/jadbin/serlist

.. image:: https://coveralls.io/repos/github/jadbin/serlist/badge.svg?branch=master
    :target: https://coveralls.io/github/jadbin/serlist?branch=master

.. image:: https://img.shields.io/badge/license-Apache 2-blue.svg
    :target: https://github.com/jadbin/serlist/blob/master/LICENSE

Overview
========

SERList is used to scrap the information from a search engine results page including:

- title
- link
- description

Now, SERList can well deal with the results from these search engines without setting anything (e.g. XPath):

- Google_
- Yahoo_
- Bing_
- Yandex_
- Baidu_
- Sogou_
- `360 Search`_

Installation
============

Install using pip::

    pip install serlist

Basic Usage
===========

.. code-block:: python

    from serlist import SerpScraper

    SerpScraper().scrap(text)

The variable ``text`` is the text of a search engine results page.

Documentation
=============

https://serlist.readthedocs.io/

.. _Google: https://www.google.com/
.. _Yahoo: https://www.yahoo.com/
.. _Bing: https://www.bing.com/
.. _Yandex: https://www.yandex.com/
.. _Baidu: https://www.baidu.com/
.. _Sogou: https://www.sogou.com/
.. _`360 Search`: https://www.so.com/
