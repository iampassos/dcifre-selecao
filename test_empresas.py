from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
import main

url = "http://localhost:8000/api"


mock_empresas = [{
    "id": 1,
    "nome": "Empresa Teste",
    "cnpj": "12345678901234",
    "endereco": "Recife",
    "email": "empresa_teste@gmail.com",
    "telefone": "81900000000"
}, {
    "id": 2,
    "nome": "Empresa Teste 2",
    "cnpj": "43210987654321",
    "endereco": "Olinda",
    "email": "empresa_teste_2@gmail.com",
    "telefone": "819000001111"
}]

payload = {
    "nome": "Empresa Teste",
    "cnpj": "12345678901234",
    "endereco": "Recife",
    "email": "empresa_teste@gmail.com",
    "telefone": "81900000000"
}


@pytest.fixture
def client():
    return TestClient(main.app)


def test_create_empresa(client):
    with patch("empresas.add_empresa") as mock:
        mock.return_value = mock_empresas[0]

        response = client.post(f"{url}/empresas", json=payload)

        assert response.status_code == 201

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        for key, value in data["data"].items():
            if key != "id":
                assert data["data"][key] == payload[key]


def test_get_empresas(client):
    with patch("empresas.list_empresas") as mock:
        mock.return_value = mock_empresas

        response = client.get(f"{url}/empresas/")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data
        assert len(data["data"]) == 2


def test_get_empresa(client):
    with patch("empresas.list_empresa_by_cnpj") as mock:
        mock.return_value = mock_empresas[0]

        response = client.get(f"{url}/empresas/{payload["cnpj"]}")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        for key, value in data["data"].items():
            if key != "id":
                assert data["data"][key] == payload[key]


mock_empresa_update = {
    "id": 1,
    "cnpj": "12345678901234",
    "nome": "Empresa Teste Novo",
    "endereco": "Recife Novo",
    "email": "empresa_teste_novo@gmail.com",
    "telefone": "61900000001"
}


def test_update_empresa(client):
    with patch("empresas.update_empresa") as mock:
        mock.return_value = mock_empresa_update

        novo_payload = {
            "nome": "Empresa Teste Novo",
            "endereco": "Recife Novo",
            "email": "empresa_teste_novo@gmail.com",
            "telefone": "61900000001"
        }

        response = client.patch(
            f"{url}/empresas/{payload["cnpj"]}", json=novo_payload)

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        for key, value in data["data"].items():
            if key != "id" and key != "cnpj":
                assert data["data"][key] == novo_payload[key]

        with patch("empresas.list_empresa_by_cnpj") as mock2:
            mock2.return_value = mock_empresa_update

            new_response = client.get(f"{url}/empresas/{payload["cnpj"]}")
            data = new_response.json()

            for key, value in data["data"].items():
                if key != "id" and key != "cnpj":
                    assert data["data"][key] == novo_payload[key]


def test_delete_empresa(client):
    with patch("empresas.delete_empresa_by_cnpj") as mock:
        mock.return_value = None

        response = client.delete(f"{url}/empresas/{payload["cnpj"]}")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data
        assert data["data"] is None
