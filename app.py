from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

# Pasta para salvar os contratos gerados
CONTRATOS_DIR = "contratos"
os.makedirs(CONTRATOS_DIR, exist_ok=True)

# Rota principal (formulário)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para gerar o contrato e retornar o PDF
@app.route('/gerar', methods=['POST'])
def gerar_contrato():
    # Dados do formulário
    nome_locador = request.form.get('nome_locador')
    nome_locatario = request.form.get('nome_locatario')
    endereco_imovel = request.form.get('endereco_imovel')
    valor_aluguel = request.form.get('valor_aluguel')
    prazo = request.form.get('prazo')
    data_assinatura = request.form.get('data_assinatura')

    # Modelo do contrato
    contrato_texto = f"""
    CONTRATO DE LOCAÇÃO

    LOCADOR: {nome_locador}
    LOCATÁRIO: {nome_locatario}
    IMÓVEL: {endereco_imovel}
    VALOR DO ALUGUEL: R$ {valor_aluguel}

    PRAZO: {prazo} meses.

    Data de assinatura: {data_assinatura}
    """

    # Gerar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for linha in contrato_texto.split("\n"):
        pdf.cell(0, 10, linha, ln=True)

    # Caminho do arquivo PDF
    arquivo_pdf = os.path.join(CONTRATOS_DIR, f"contrato_{nome_locatario.replace(' ', '_')}.pdf")
    pdf.output(arquivo_pdf)

    # Retornar o PDF para download
    return send_file(arquivo_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
