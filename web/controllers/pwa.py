from flask import Blueprint, make_response, send_from_directory, render_template

blueprint = Blueprint('pwa', __name__, url_prefix='')


@blueprint.route('/offline')
def offline():
    return render_template('offline.html')


@blueprint.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')


@blueprint.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response
