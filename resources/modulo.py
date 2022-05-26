from flask_restful import Resource, reqparse
from models.modulo import ModuloModel
from flask_jwt_extended import jwt_required
import sqlite3


class Modulo(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('tensao', type=float, required=True, help="O campo 'tensao' não pode ser deixado em branco")
    argumentos.add_argument('corrente', type=float, required=True, help="O campo 'corrente' não pode ser deixado em "
                                                                        "branco")
    argumentos.add_argument('data_hora', type=str, required=True, help="O campo 'data_hora' não pode ser deixado em "
                                                                       "branco")

    def get(self):
        try:
            return {'modulos': [modulo.json() for modulo in ModuloModel.query.all()]}
        except:
            return {'message': 'Server error.'}, 500 # not found

    def post(self):
        dados = Modulo.argumentos.parse_args()
        modulo = ModuloModel(**dados)
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
