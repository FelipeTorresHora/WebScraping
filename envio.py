import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
import os
from dotenv import load_dotenv
from logger_config import setup_logger
from constants import SMTP_SERVER, SMTP_PORT

load_dotenv()
logger = setup_logger(__name__)

def enviar_email(destinatario, assunto, corpo, anexo=None):
    """
    Envia um e-mail com ou sem anexo.
    
    :param destinatario: E-mail do destinatário
    :param assunto: Assunto do e-mail
    :param corpo: Corpo do e-mail em texto simples
    :param anexo: Caminho do arquivo anexo (opcional)
    :return: True se o envio for bem-sucedido, False caso contrário
    """
    # Configurações do servidor SMTP (exemplo com Gmail)
    smtp_server = SMTP_SERVER
    smtp_port = SMTP_PORT
    remetente = os.getenv("SENDER_EMAIL")
    senha = os.getenv("Senha_Email")

    # Validar variáveis de ambiente
    if not remetente:
        raise ValueError("SENDER_EMAIL não configurado no .env")
    if not senha:
        raise ValueError("Senha_Email não configurada no .env")

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))  # Use 'html' se o corpo for em HTML

    # Anexar arquivo, se fornecido
    if anexo:
        try:
            with open(anexo, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(anexo))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(anexo)}"'
                msg.attach(part)
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {anexo}")
            raise FileNotFoundError(f"Arquivo não encontrado: {anexo}")
        except IOError as e:
            logger.error(f"Erro ao ler arquivo {anexo}: {e}")
            raise IOError(f"Erro ao ler arquivo {anexo}: {e}")

    # Conectar ao servidor SMTP e enviar
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia conexão segura
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        logger.info(f"E-mail enviado com sucesso para {destinatario}")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {str(e)}")
        return False

def gerar_pdf_relatorio(filtros, resultados, nome_arquivo='relatorio.pdf'):
    """
    Gera um relatório em PDF com filtros e resultados.
    
    :param filtros: Dicionário com os filtros aplicados
    :param resultados: DataFrame com os resultados (ex.: dados de FIIs)
    :param nome_arquivo: Nome do arquivo PDF gerado
    :return: Caminho do arquivo PDF gerado
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.cell(200, 10, txt="Relatório Personalizado", ln=True, align='C')

    # Filtros aplicados
    pdf.cell(200, 10, txt="Filtros Aplicados:", ln=True)
    for chave, valor in filtros.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)

    # Resultados
    pdf.cell(200, 10, txt="Resultados:", ln=True)
    for index, row in resultados.iterrows():
        linha = f"{row['código']} - Cotação: R$ {row['cotação']:.2f}"
        pdf.cell(200, 10, txt=linha, ln=True)

    # Salvar o PDF
    pdf.output(nome_arquivo)
    return nome_arquivo