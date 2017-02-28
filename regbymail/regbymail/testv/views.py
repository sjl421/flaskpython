from flask import render_template, Blueprint, send_file, make_response
from regbymail.ldebug import log


testv_blueprint = Blueprint('testv', __name__)

@testv_blueprint.route('/mainindex')
def mainindex():
    try:
        log.log('Enter testv.mainindex')
        return render_template('testv/showchart.html', chartid=1)
    except:
        log.log_exception()

@testv_blueprint.route('/showchart/<chartid>')
def showchart(chartid):
    log.log('entert showchart')
    log.log('charid is {}'.format(chartid))
    import numpy as np
    import matplotlib.pyplot as plt
    from io import BytesIO
    log.log('Enter testv blueprint')
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (0, 32, 34, 20, 25)
    menStd =(5, 8, 4, 1, 2)
    womenStd=(1, 0, 1, 3, 3)
    ind = np.arange(N)
    width = 0.35
    log.log('get all paras')
    p1 = plt.bar(ind, menMeans, width, color='green', yerr=menStd)
    p2 = plt.bar(ind, womenMeans, width, color='red', bottom=menMeans, yerr=womenStd)

    plt.ylabel('Task Progress')
    plt.title('Task progress group by item')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 80, 10))
    plt.legend((p1[0], p2[0]), ('Finished', 'UnFinished'))
    log.log('try to save to image')

    img = BytesIO()
    log.log('new image instance')
    plt.savefig(img, format='png')
    img.seek(0)
    log.log('save ok...')
    log.log('before send image')
    return send_file(img, mimetype='image/png')
