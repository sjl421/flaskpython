from flask import render_template, Blueprint
from regbymail.ldebug import log

testv_blueprint = Blueprint('testv', __name__)

@testv_blueprint.route('/mainindex')
def mainindex():
    try:
        render_template('base.html')
    except:
        log.log_exception()
