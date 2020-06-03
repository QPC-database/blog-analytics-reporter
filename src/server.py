from flask import Flask, jsonify, request
from flask_cors import CORS

from analytics_client import get_page_info, get_total_info
from config import config

CORS_ORIGIN = config['CORS_ORIGIN']
SERVER_HOST = config['SERVER_HOST']
SERVER_PORT = config['SERVER_PORT']

app = Flask(__name__)
CORS(app, resources={
    r'/*': {
        'origins': CORS_ORIGIN
    }
})


@app.route('/blog/analytics/total')
def get_total():
    info = get_total_info()
    return jsonify({
        'totalUniqueVisitors': info.get('ga:users'),
        'totalPageViews': info.get('ga:pageviews')
    })


@app.route('/blog/analytics/page')
def get_page():
    title = request.args.get("title")
    info = get_page_info(title)
    if info:
        return jsonify({
            'title': info.get('ga:pageTitle'),
            'pageViews': info.get('ga:pageviews')
        })
    else:
        return {}


if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT)
