#Dentro de un contexto de aplicación, get_db debe devolver la misma conexión cada vez que se llame. Después del contexto, la conexión debe ser cerrada.

import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)
#El comando init-db debe llamar a la función init_db y mostrar un mensaje.

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

#Esta prueba utiliza el fixture monkeypatch de Pytest para sustituir la función init_db por otra que registre que ha sido llamada. El fixture runner se utiliza para llamar al comando init-db por su nombre.