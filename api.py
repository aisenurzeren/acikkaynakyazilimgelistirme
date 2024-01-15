from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(name)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        name = request.args['name']
        age = request.args['age']
        city = request.args['city']
        new_data = pd.DataFrame({
            'name': [name],
            'age': [age],
            'city': [city]
        })
        data = pd.read_csv('users.csv')
        data = data.append(new_data, ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message': 'Record successfully added.'}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('users.csv')

        if name in data['name'].values:
            data = data[data['name'] != name]
            data.to_csv('users.csv', index=False)
            return {'message': 'Record successfully deleted.'}, 200
        else:
            return {'message': 'Record not found.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv', usecols=['city'])
        data = data.to_dict('records')
        return {'data': data}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        entry = data[data['name'] == name].to_dict('records')
        if entry:
            return {'data': entry[0]}, 200
        else:
            return {'message': 'No entry found with this name!'}, 404

api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')

if name == 'main':
    app.run(host="0.0.0.0", port=6767)
