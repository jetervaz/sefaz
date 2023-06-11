"""Useful functions for obtaining NFe information from SEFAZ by CPF."""
# -*- coding: utf-8 -*-
import base64
import gzip

from lxml import etree

from requests import Session

from settings import (
    CERTIFICATE_FILE,
    USER_CPF,
    WSDL_URL,
)

from zeep import Client
from zeep.transports import Transport


def get_client(certificate_file=CERTIFICATE_FILE, wsdl_url=WSDL_URL):
    """Return a WebService Client using the settings."""
    session = Session()
    session.verify = False
    session.cert = certificate_file
    transport = Transport(session=session)
    return Client(wsdl_url, transport=transport)


def build_xml(cpf=USER_CPF, ult_nsu=None, nsu=None):
    """Build xml for request from CPF and NSU digits."""
    xml = '<?xml version="1.0" standalone="yes"?>'\
          '<distDFeInt xmlns="http://www.portalfiscal.inf.br/nfe"'\
          ' versao="1.01">'\
          '<tpAmb>1</tpAmb>'\
          '<cUFAutor>43</cUFAutor>'\
          '<CPF>' + cpf + '</CPF>'
    if ult_nsu:
        xml += '<distNSU><ultNSU>' + ult_nsu.zfill(15) + '</ultNSU></distNSU>'
    elif nsu:
        xml += '<consNSU><NSU>' + nsu.zfill(15) + '</NSU></consNSU>'
    xml += '</distDFeInt>'
    return xml


def get_dict_from_response(response):
    """Parse XML response to dictionary."""
    r_dict = {}
    for element in response:
        tag = element.tag.split('}')[1]
        content = element.text
        if content:
            r_dict[tag] = content
        else:
            r_dict[tag] = []
            for sub_element in element:
                sub_tag = sub_element.tag.split('}')[1]
                sub_content = sub_element.text
                r_dict[tag].append({sub_tag: sub_content})
    return r_dict


def extract_nfe_docs(nfe_docs):
    """Extract gzipped and base64 encoded docs."""
    nfe_docs_extracted = []
    for doc in nfe_docs:
        # Decode base64.
        gzip_doc = base64.b64decode(doc['docZip'])
        # Extract gzip.
        xml_str = gzip.decompress(gzip_doc).decode('utf-8')
        # Build xml tree from string.
        xml_tree = etree.fromstring(xml_str)
        nfe = {}
        for element in xml_tree:
            nfe[element.tag.split('}')[1]] = element.text
        nfe_docs_extracted.append(nfe)
    return nfe_docs_extracted


def nfe_request(cpf=USER_CPF, nsu=None, ult_nsu=None):
    """Request NFe using NSU or ULT_NSU provided by user."""
    xml = build_xml(cpf=cpf, nsu=nsu, ult_nsu=ult_nsu)
    print(xml)
    client = get_client()
    result = client.service.nfeDistDFeInteresse(
        nfeDadosMsg=etree.fromstring(xml),
    )
    r_dict = get_dict_from_response(result)
    lote = r_dict.get('loteDistDFeInt')
    if lote:
        r_dict['loteDistDFeInt'] = extract_nfe_docs(lote)
    return r_dict
