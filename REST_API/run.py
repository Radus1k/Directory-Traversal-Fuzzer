#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask import Flask, g,jsonify
import markdown
from pathlib import Path
import os
import shelve
import sqlite3
import json

app = Flask(__name__)

api = Api(app)

DATABASE = 'fuzzing_small.sqlite'


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """Present some documentation"""

    # Open the README file

    dir_bro = os.path.dirname(app.root_path)
    with open('intro.txt', 'r') as markdown_file:

        # Read the content of the file

        content = markdown_file.read()
        return markdown.markdown(content)

@app.route('/json2')
def json_page():
     with app.app_context():
            cursor = get_db().cursor()
            sqlite_select_query = """SELECT * from Stats"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            dictionary = list()


            for row in records:
                dictionary_index = {
                    'id': row[0],
                    'host': row[1],
                    'fuzzed_url': row[2],
                    'status': row[3],
                    'result_length': row[4],
                    }

            dictionary.append(dictionary_index)
            cursor.close()
            json_dump = json.dumps(dictionary, sort_keys=True)  
            json_out = "```json" + '\n' +  json_dump + '\n' +  '```'
            return markdown.markdown(json_out)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class DataList(Resource):

    def get(self):
        with app.app_context():
            cursor = get_db().cursor()
            sqlite_select_query = """SELECT * from Stats"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            dictionary = list()
            json_string = str()
            json_str_list = list()


            for row in records:
                dictionary_index = {
                    'id': row[0],
                    'host': row[1],
                    'fuzzed_url': row[2],
                    'status': row[3],
                    'result_length': row[4]
                    }
                #json_string = "{\n    \"Id\": " + row[0] + ",\n    \"Host\": " + row[1] + ",\n\"    Fuzzed_Url\": " +  row[2] + ",\n\"    Status\": " + row[3] + ",\n\"    result_length\": " + row[4] + '\n}'
                dictionary.append(dictionary_index)
                #json_str_list.append(json_string)

            cursor.close()
            #json_dump = json.dumps(dictionary, sort_keys=True)
            return jsonify(dictionary)
            #return {'Database': json_dump}, 200


class jsonExample(Resource):

    def get(self):
        json_list = []
        with open('json.txt', 'r') as json_file:
            json_list = list(json_file)
            return markdown.markdown(json_list)
            #return markdown.markdown(content)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/hello')            


api.add_resource(DataList, '/devices')

api.add_resource(jsonExample, '/json.html')


app.run(host='0.0.0.0', port=80, debug=True)


            