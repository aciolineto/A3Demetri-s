from datetime import date
from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ARQUIVO = "clientes.json"

if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f:
        json.dump([], f)

def carregar_clientes():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []


def salvar_clientes(clientes):
    with open(ARQUIVO, "w") as f:
        json.dump(clientes, f, indent=4)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        modelo_carro = request.form.get("modelo_carro", "").strip()
        problema = request.form.get("problema", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        valor = request.form.get("valor", "0").strip()
        pagamento = request.form.get("pagamento", "").strip()

        clientes = carregar_clientes()

        clientes.append({
            "nome": nome,
            "telefone": telefone,
            "modelo_carro": modelo_carro,
            "problema": problema,
            "data": data,
            "horario": horario,
            "valor": valor,
            "pagamento": pagamento
        })

        salvar_clientes(clientes)

        return redirect("/listar")

    return render_template("cadastrar.html")


@app.route("/listar")
def listar():
    clientes = carregar_clientes()
    hoje = str(date.today())

    total_dia = 0
    total_geral = 0

    for cliente in clientes:
        valor = str(cliente.get("valor", "0")).replace(",", ".")

        try:
            valor_float = float(valor)
        except:
            valor_float = 0

        total_geral += valor_float

        if cliente.get("data") == hoje:
            total_dia += valor_float

    return render_template(
        "listar.html",
        clientes=clientes,
        total_dia=total_dia,
        total_geral=total_geral,
        hoje=hoje
    )


@app.route("/excluir/<int:index>", methods=["POST"])
def excluir(index):
    clientes = carregar_clientes()

    if 0 <= index < len(clientes):
        clientes.pop(index)
        salvar_clientes(clientes)

    return redirect("/listar")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
