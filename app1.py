# coding=utf-8
from __future__ import unicode_literals

import copy
from functools import wraps

from flask import request, flash, Flask, Response, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, SelectField, SelectMultipleField, RadioField

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.secret_key = '05ec288956b56cf53af7f2e02a2799e6'
bootstrap = Bootstrap(app)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'hd123'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def parse(content):
    """
    如何发现对应内容，返回不为空；没发现，返回空
    :param content:
    :return:
    """
    import re
    data = re.findall(r'(http://hdm2repo/nexus/service(.*)+)[\]|\|]', content)
    return data


def parse_old_maven_url(url):
    """
    从原始的url地址分析出对应的maven坐标信息
    Example output :
        { u'a': u'rumba-commons-mini',
          u'c': u'bin',
          u'e': u'zip',
          u'g': u'com.hd123.rumba.commons',
          u'v': u'1.21.0'}
    :param url: old url
    :return: dict
    """
    import urlparse
    result = urlparse.urlparse(url)
    result = result.query.split('&')
    odict = dict()
    for i, value in enumerate(result):
        k, v = value.split('=')
        odict[k] = v

    return odict


def build_new_url(options):
    url = 'http://maven.qianfan123.com/repository/hdm2repo/'
    url += options['g'].replace('.', '/')
    url = url + '/' + options['a']
    url = url + '/' + options['v']
    if 'c' in options:
        url = url + '/' + "{}-{}-{}.{}".format(options['a'], options['v'], options['c'], options['e'])
    else:
        url = url + '/' + "{}-{}.{}".format(options['a'], options['v'], options['e'])
    return url


class IndexForm(FlaskForm):
    source = StringField("条件一")
    target = SelectField("Language", choices=[("all", 'ALL'), ("1", 'English'), ('2', 'Chinese')])
    btnSubmit = SubmitField("转换")
    btnClear = SubmitField("重置")


columns = [
    {
        "field": "name",  # which is the field's name of data key
        "title": "name",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "age",
        "title": "age",
        "sortable": True,
    }
]


@app.route('/index', methods=['GET', "POST"])
def index():
    form = IndexForm()
    return render_template("index.html", form=form)


@app.route('/', methods=['GET', "POST"])
# @requires_auth
def home():
    # flash category : info,danger,success
    # flash("欢迎回来", 'info')
    _form = IndexForm()
    data = []
    if _form.validate_on_submit():
        if _form.btnSubmit.data:
            data = [
                {"name": 'buhaiqing', "age": 39},
                {"name": 'user1', "age": 39},
                {"name": 'user2', "age": 39},
                {"name": 'user3', "age": 39},
                {"name": 'user4', "age": 39},
                {"name": 'user5', "age": 39},
                {"name": 'grade', "age": 36},
                {"name": 'ada', "age": 36},
            ]

        if _form.btnClear.data:
            data = []
            _form.source.data = ""

    return render_template("app1.html", form=_form, columns=columns, data=data, total_page=10, content=[
        {'id': 1, 'notify_type': "邮件", 'notify_name': "卜海清", 'notify_number': 6211, 'status': True}
    ])


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5055)
