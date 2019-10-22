# -*- coding=gbk -*-
# file:www.py.py
# time:2019/9/14{10:30}
# author:Vincent

from apps.first.index import route_index
from apps.weixin.onlyone import route_onlyone
from apps.weixin.novel import route_novel

from application import app

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_onlyone, url_prefix="/weixin/onlyone")
app.register_blueprint(route_novel, url_prefix="/weixin/novel")