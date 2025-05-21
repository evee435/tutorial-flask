#Has añadido la ruta hello como ejemplo al escribir la fábrica al principio del tutorial. Devuelve «¡Hola, mundo!», por lo que la prueba comprueba que los datos de respuesta coinciden

from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'