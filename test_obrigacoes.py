from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
import main

url = "http://localhost:8000/api"

mock_obrigacao = {
    "nome": "IMPOSTO",
    "periodicidade": "ANUAL",
    "id": 1,
    "empresa_id": 1
}

mock_obrigacoes_empresa = {
    "id": 1,
    "nome": "Empresa Teste",
    "cnpj": "12345678901234",
    "endereco": "Recife",
    "email": "empresa_teste@gmail.com",
    "telefone": "81900000000",
    "obrigacoes": mock_obrigacao
}


@pytest.fixture
def client():
    return TestClient(main.app)


def test_create_obrigacao(client):
    with patch("obrigacoes.add_obrigacao_by_cnpj") as mock:
        mock.return_value = mock_obrigacao

        payload = {
            "nome": "IMPOSTO",
            "periodicidade": "ANUAL"
        }

        response = client.post(
            f"{url}/obrigacoes/{mock_obrigacoes_empresa["cnpj"]}", json=payload)

        assert response.status_code == 201

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        for key, value in data["data"].items():
            if key != "id" and key != "empresa_id":
                assert data["data"][key] == payload[key]


def test_get_obrigacoes_empresa(client):
    with patch("obrigacoes.list_obrigacoes_by_cnpj") as mock:
        mock.return_value = mock_obrigacoes_empresa

        response = client.get(f"{url}/empresas/")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data
        assert len(data["data"]) == 2


def test_get_obrigacao(client):
    with patch("obrigacoes.list_obrigacao") as mock:
        mock.return_value = mock_obrigacao

        response = client.get(
            f"{url}/obrigacoes/{mock_obrigacoes_empresa["cnpj"]}/{mock_obrigacao["id"]}")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        for key, value in data["data"].items():
            if key != "id":
                assert data["data"][key] == mock_obrigacao[key]


mock_obrigacao_update = {
    "nome": "IMPOSTO NOVO",
    "periodicidade": "TRIMESTRAL",
    "id": 1,
    "empresa_id": 1
}


def test_update_obrigacao(client):
    with patch("obrigacoes.update_obrigacao") as mock:
        mock.return_value = mock_obrigacao_update

        novo_payload = {
            "nome": "IMPOSTO NOVO",
            "periodicidade": "TRIMESTRAL"
        }

        response = client.patch(
            f"{url}/obrigacoes/{mock_obrigacoes_empresa["cnpj"]}", json=novo_payload)

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        for key, value in data["data"].items():
            if key != "id" and key != "empresa_id":
                assert data["data"][key] == novo_payload[key]

        with patch("obrigacoes.list_obrigacao") as mock2:
            mock2.return_value = mock_obrigacao_update

            new_response = client.get(
                f"{url}/obrigacoes/{mock_obrigacoes_empresa["cnpj"]}/{mock_obrigacao["id"]}")
            data = new_response.json()

            for key, value in data["data"].items():
                if key != "id" and key != "empresa_id":
                    assert data["data"][key] == novo_payload[key]


def test_delete_obrigacao(client):
    with patch("obrigacoes.delete_obrigacao_by_id") as mock:
        mock.return_value = None

        response = client.delete(
            f"{url}/obrigacoes/{mock_obrigacoes_empresa["cnpj"]}")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "data" in data
        assert data["data"] is None
