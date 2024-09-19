# -*- coding: utf-8 -*-
import re
from burp import IBurpExtender, IHttpListener

def validate_cpf(cpf):
    unformatted_cpf = re.sub(r'\D', '', cpf)
    if unformatted_cpf == unformatted_cpf[0] * 11:
        return False
    sum_ = sum(int(unformatted_cpf[i]) * (10 - i) for i in range(9))
    digit1 = 11 - (sum_ % 11)
    digit1 = 0 if digit1 >= 10 else digit1
    sum_ = sum(int(unformatted_cpf[i]) * (11 - i) for i in range(10))
    digit2 = 11 - (sum_ % 11)
    digit2 = 0 if digit2 >= 10 else digit2
    return unformatted_cpf[-2:] == "{}{}".format(digit1, digit2)

def extract_dates(body_str):
    date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    return date_pattern.findall(body_str)

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("PII Scanner")
        callbacks.registerHttpListener(self)
        print("Meu PIIScannerDoCP5, Installation OK!")

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            request_info = self._helpers.analyzeRequest(messageInfo)
            body = messageInfo.getResponse()[request_info.getBodyOffset():]
            body_str = self._helpers.bytesToString(body)

            # Padrão para números de telefone: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
            phone_pattern = re.compile(r'\(\d{2}\) \d{5}-\d{4}|\(\d{2}\) \d{4}-\d{4}')
            phone_matches = phone_pattern.findall(body_str)

            # Formata os números de telefone para o padrão (XX) XXXX-XXXX
            formatted_phone_matches = [phone for phone in phone_matches]

            # Extraindo CPF
            cpf_pattern = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
            possible_cpf = cpf_pattern.findall(body_str)
            possible_cpf = list(set(possible_cpf))  # Remove duplicatas
            cpf_ok = [cpf for cpf in possible_cpf if validate_cpf(cpf)]

            # Padrão para números de cartão de crédito
            cc_pattern = re.compile(r'\b\d{4} \d{4} \d{4} \d{4}\b')
            cc_matches = cc_pattern.findall(body_str)

            # Padrão para CNPJ: 12.345.678/0001-00
            cnpj_pattern = re.compile(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b')
            cnpj_matches = cnpj_pattern.findall(body_str)

            # Padrão para RG: 417245683 (apenas números)
            rg_pattern = re.compile(r'\b\d{7,9}\b')
            rg_matches = rg_pattern.findall(body_str)

            # Extraindo datas
            date_matches = extract_dates(body_str)

            # Exibe apenas as informações válidas
            if formatted_phone_matches:
                for phone in formatted_phone_matches:
                    print("Numero de Celular: %s" % phone)
            if cpf_ok:
                for cpf in cpf_ok:
                    print("CPF: %s" % cpf) 
            if cc_matches:
                for cc in cc_matches:
                    print("Numero de cartao de Credito: %s" % cc)
            if cnpj_matches:
                for cnpj in cnpj_matches:
                    print("CNPJ: %s" % cnpj)
            if rg_matches:
                for rg in rg_matches:
                    print("RG: %s" % rg)
            if date_matches:
                for date in date_matches:
                    print("Data no formato (DD/MM/YYYY): %s" % date)

