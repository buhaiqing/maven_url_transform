#coding=utf-8
from __future__ import unicode_literals

import pytest
from app import parse
def test1():
    s = '| 1.1.1 | [rumba-rik-client-1.1.1.zip|http://maven.qianfan123.com/repository/maven-releases/com/hd123/rumba/remoteinvoker/rumba-rik-client/1.1.1/rumba-rik-client-1.1.1.zip]'
    r=parse(s)
    assert r