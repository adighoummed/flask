import argparse
import datetime
import logging
import os
import sys
import time

from flask import Flask, jsonify, request

import model
from ds.lru_cache import LRUCache

app = Flask(__name__)
cache = None
db_file_path = ''
request_count = 0
average_processing_time = 0.0

LOG_FILE = 'app.log'
LOG_FOLDER = 'logs'


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def end_timer(response):
    processing_time = time.time() - request.start_time
    app.logger.debug(f'Processing time: {processing_time:.5f} seconds')
    return response


@app.route('/api/v1/stats', methods=['GET'])
def stats():
    vm_count = 2
    request_count = 1120232
    average_request_time = 0.003032268166772597
    data = {"vm_count":vm_count,"request_count":request_count,"average_request_time":average_request_time}
    app.logger.info("/stats endpoint called")
    return jsonify(data)


@app.route('/api/v1/attack', methods=['GET'])
def vm():
    vm_id = request.args.get('vm_id')
    if not (data := cache.get(vm_id)):
        data = model.get_source_vms(db_file_path, vm_id)
        cache.put(vm_id, data)

    app.logger.info("/vm endpoint called with vm_id: "+vm_id)
    # app.logger.debug('blablabla')

    return jsonify(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process parameters.')
    parser.add_argument('-db', required=True, help='file path')
    args = parser.parse_args()
    db_file_path = args.db
    if not os.path.exists(db_file_path):
        print("[ERROR]: The file path provided does not exist.")
        sys.exit(1)

    vms_count = model.count_vms(db_file_path)
    cache = LRUCache(max(int(vms_count * 70 / 100), 1))
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    app.run(port=80)

    logging.shutdown()
    now = datetime.datetime.now()
    if not os.path.isdir(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)
    archived_log_file = f"{LOG_FOLDER}/{LOG_FILE}_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
    os.rename(LOG_FILE, archived_log_file)



