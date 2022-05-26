import requests
from flask_restful import Resource, reqparse
from models.modulo import ModuloModel
from flask_jwt_extended import jwt_required
import sqlite3
import csv
import pandas as pd
import numpy as np
import xlsxwriter


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
            return {'message': 'Server error.'}, 500  # not found

    def post(self):
        dados = Modulo.argumentos.parse_args()
        modulo = ModuloModel(**dados)
        try:
            modulo.save_modulo()
        except:
            return {'message': 'Um erro interno ocrreu ao tentar salvar o módulo'}, 500  # Internal Server Error
        return modulo.json()


class ModuloExcel(Resource):
    def get(self):
        """
        Open a file to write the data
        Connects to the database
        Creates a cursor object to address the table results individually

        :return: Created ok message
        """
        header = ['id', 'Corrente', 'Tensão', 'Data e Hora']

        with open('/home/sr-guilem/PycharmProjects/projetoSolarWatcher/medicoes.csv', 'w') as write_file:
            writer = csv.writer(write_file)
            writer.writerow(header)
            conn = sqlite3.connect('/home/sr-guilem/PycharmProjects/projetoSolarWatcher/banco.db')
            cursor = conn.cursor()
            for row in cursor.execute('SELECT * FROM modulos'):
                writer.writerow(row)

        read_file = pd.read_csv(r'/home/sr-guilem/PycharmProjects/projetoSolarWatcher/medicoes.csv')
        read_file.to_excel(r'/home/sr-guilem/PycharmProjects/projetoSolarWatcher/medicoes.xlsx', index=False)

        df = pd.read_excel('/home/sr-guilem/PycharmProjects/projetoSolarWatcher/medicoes.xlsx', 'Sheet1')
        print(df)

        pic = df.plot.line(title='Medições', x='Data e Hora', y=['Tensão', 'Corrente'], figsize=(15, 5), grid=True,
                           legend=True, color={'Tensão': 'red', 'Corrente': 'blue'})
        pic = pic.get_figure()
        pic.savefig('grph.jpg')

        afk = '/home/sr-guilem/PycharmProjects/projetoSolarWatcher/medicoes.xlsx'
        workbook = xlsxwriter.Workbook(afk)
        sheet = workbook.add_worksheet()
        sheet.insert_image('G3', 'grph.jpg')

        for i, col_name in enumerate(df.columns):
            sheet.write(0, i, col_name)
            sheet.write_column(1, i, df[col_name])

        workbook.close()

        return {'message': 'Documento criado com sucesso'}

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
