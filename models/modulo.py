from sql_alchemy import banco


class ModuloModel(banco.Model):
    __tablename__ = 'modulos'
    modulo_id = banco.Column(banco.Integer(), primary_key=True)
    corrente = banco.Column(banco.String(15))
    tensao = banco.Column(banco.String(15))
    data_hora = banco.Column(banco.String(20))

    def __init__(self, corrente, tensao, data_hora):
        self.corrente = corrente
        self.tensao = tensao
        self.data_hora = data_hora

    def json(self):
        return {
            'corrente': self.corrente,
            'tensao': self.tensao,
            'data_hora': self.data_hora
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

    def update_modulo(self, corrente, tensao, data_hora):
        self.corrente = corrente
        self.tensao = tensao
        self.data_hora = data_hora

    def delete_modulo(self):
        banco.session.delete(self)
        banco.session.commit()