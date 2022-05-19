from flask_restful import Resource, reqparse
from models.modulo import ModuloModel
from flask_jwt_extended import jwt_required
import sqlite3


# path /modulos?data_min=20/05/2022&data_max=22/05/2022
path_params = reqparse.RequestParser()
path_params.add_argument('corrente_min', type=float)
path_params.add_argument('corrente_max', type=float)
path_params.add_argument('tensao_min', type=float)
path_params.add_argument('tensao_max', type=float)
path_params.add_argument('data_registro', type=str)
path_params.add_argument('hora', type=str)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Modulos(Resource):
    def get(self):
        return {'modulos': [modulo.json() for modulo in ModuloModel.query.all()]}


class Modulo(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('tensao', type=float, required=True, help="O campo 'tensao' não pode ser deixado em branco")
    argumentos.add_argument('corrente', type=float, required=True, help="O campo 'corrente' não pode ser deixado em "
                                                                        "branco")
    argumentos.add_argument('data_registro', type=str, required=True, help="O campo 'data_registro' não pode ser deixado em branco")
    argumentos.add_argument('hora', type=str, required=True, help="O campo 'data' não pode ser deixado em branco")

    @jwt_required()
    def get(self, modulo_id):
        modulo = ModuloModel.find_modulo(modulo_id)
        if modulo:
            return modulo.json()
        return {'message': 'Modulo não encontrado.'}, 404  # not found

    @jwt_required()
    def post(self, modulo_id):
        if ModuloModel.find_modulo(modulo_id):
            return {"message": "O módulo de ID '{}' já existe.".format(modulo_id)}, 400  # Bad Request
        dados = Modulo.argumentos.parse_args()
        modulo = ModuloModel(modulo_id, **dados)
        try:
            modulo.save_modulo()
        except:
            return {'message': 'Um erro interno ocrreu ao tentar salvar o módulo'}, 500  # Internal Server Error
        return modulo.json()

    @jwt_required()
    def put(self, modulo_id):
        dados = Modulo.argumentos.parse_args()
        modulo_encontrado = ModuloModel.find_modulo(modulo_id)
        if modulo_encontrado:
            modulo_encontrado.update_modulo(**dados)
            modulo_encontrado.save_modulo()
            return modulo_encontrado.json(), 200  # atualizado
        modulo = ModuloModel(modulo_id, **dados)
        try:
            modulo.save_modulo()
        except:
            return {'message': 'Um erro interno ocorreu ao tentar salvar o módulo'}, 500  # Internal Server Error
        return modulo.json(), 201  # criado

    @jwt_required()
    def delete(self, modulo_id):
        modulo = ModuloModel.find_modulo(modulo_id)
        if modulo:
            try:
                modulo.delete_modulo()
            except:
                return {'message': 'Um erro ocorreu ao tentar deletar o módulo'}, 500
            return {'message': 'Módulo deletado.'}
        return {'message': 'Módulo não encontrado'}, 404
