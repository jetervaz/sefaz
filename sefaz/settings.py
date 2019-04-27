"""General settings."""
import os

WSDL_URL = 'https://www1.nfe.fazenda.gov.br/'\
           'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx?wsdl'
CERTIFICATE_FILE = os.getenv('USER_PEM_CERTIFICATE')
USER_CPF = os.getenv('USER_CPF_DIGITS')
