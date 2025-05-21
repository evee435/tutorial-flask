#La vista register debería ser mostrada con éxito en GET. En POST con datos de formulario válidos, debería redirigir a la URL de acceso y los datos del usuario deberían estar en la base de datos. Los datos no válidos deberían mostrar mensajes de error.

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

#client.get() realiza una petición GET y devuelve el objeto Response devuelto por Flask. Del mismo modo, client.post() realiza una petición POST, convirtiendo el dictado data en datos del formulario.

#headers tendrá una cabecera Location con la URL de acceso cuando la vista de registro redirija a la vista de acceso.

#data contiene el cuerpo de la respuesta en forma de bytes. Si esperas que un determinado valor se renderice en la página, comprueba que está en data. Los bytes deben ser comparados con bytes. Si quieres comparar texto, utiliza get_data(as_text=True) en su lugar.

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
#El uso de client en un bloque with permite acceder a variables de contexto como session después de que se devuelva la respuesta. Normalmente, acceder a session fuera de una petición daría un error.

#Probar logout es lo contrario de login. session no debe contener user_id después de cerrar la sesión

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session