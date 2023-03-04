import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from tinydb import Query, TinyDB


@dataclass
class Registrador:
    nomeuser: str # Por qual nome deseja ser chamado
    user_ident: int # Numero de usuário no telegram
    data: str # Data em que foi realizado o registro
    rep_dep: str # Se acessor, representa qual deputado
    is_writable: bool # Posso escrever algo
    tipo: Literal['acessor', 'deputado'] = 'deputado' # Classificação

    def as_dict(self):
        return asdict(self)

def inserir_dado(usuario, user_ident, data, rep_dep, is_wrritable, types):

    db_path = Path(__file__).parent / 'deputados.db'

    r1 = Registrador(usuario, user_ident, data, rep_dep, is_wrritable, types)

    db = TinyDB(db_path, indent=4)
    index1 = db.insert(r1.as_dict())

    return index1

def editar_dado(key_s, valor_act, user_idds):
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    Loc = Query()
    db.update({key_s: valor_act}, Loc.user_ident == user_idds)



def todo_banco():
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    return db.all()

def remover_elm(nomeuser):
    Loc = Query()
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    return(db.remove(Loc.nometelegram == nomeuser))


def limpar_banco():
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    db.truncate()

def buscar_id_user(id_tuser):
    Loc = Query()
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    return db.get(Loc.user_ident == id_tuser)

if __name__ == '__main__':
    ...
    limpar_banco()
    # inserir_dado("Joao Gomes", 123456, "14/03/2023", "", False, 'deputado')
    # user = buscar_id_user(123456)
    # print(user["data"])