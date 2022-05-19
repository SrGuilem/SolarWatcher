from sql_alchemy import banco


class ModuloModel(banco.Model):
    __tablename__ = 'modulos'

    modulo_id = banco.Column(banco.String, primary_key=True)
    corrente = banco.Column(banco.Float(precision=3))
    tensao = banco.Column(banco.Float(precision=3))
    data_registro = banco.Column(banco.String(10))
    hora = banco.Column(banco.String(5))

    def __init__(self, modulo_id, corrente, tensao, data_registro, hora):
        self.modulo_id = modulo_id
        self.corrente = corrente
        self.tensao = tensao
        self.data_registro = data_registro
        self.hora = hora

    def json(self):
        return {
            'modulo_id': self.modulo_id,
            'corrente': self.corrente,
            'tensao': self.tensao,
            'data_registro': self.data_registro,
            'hora': self.hora
        }

    @classmethod
    def find_modulo(cls, modulo_id):
        modulo = cls.query.filter_by(modulo_id=modulo_id).first()  # SELECT * FROM modulos WHERE modulo_id = modulo_id
        if modulo:
            return modulo
        return None

    def save_modulo(self):
        banco.session.add(self)
        banco.session.commit()

    def update_modulo(self, corrente, tensao, data_registro, hora):
        self.corrente = corrente
        self.tensao = tensao
        self.data_registro = data_registro
        self.hora = hora

    def delete_modulo(self):
        banco.session.delete(self)
        banco.session.commit()