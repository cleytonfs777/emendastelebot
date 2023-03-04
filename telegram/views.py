import json
import os
import re
from datetime import date, datetime

import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from data2.datamanager import *
from data.dep_estadual import deputados_estaduais as dep_e
from data.dep_federal import deputados_federais as dep_f

from .models import Registrador

load_dotenv()

TOKEN = os.getenv('TOKEN')

def inserir_dado(usuario="", user_id="", data='', rep_dep="", is_writable="",locale_is="", tipo=""):
    aposta = Registrador(nomeuser=usuario,user_ident=user_id, data=data, rep_dep=rep_dep, is_writable=is_writable,locale_is=locale_is,tipo=tipo)
    aposta.save()

def todo_banco():
    r = serializers.serialize("json", Registrador.objects.all())
    rest = json.loads(r)
    return rest

def buscar_id_user(idd_user):
    r = serializers.serialize("json", Registrador.objects.filter(user_ident=idd_user))
    rest = json.loads(r)
    if len(rest) == 0:
        return rest
    else:
        return rest[0]["fields"]

def edit_data(alvo, novo_valor, idd_user):

    registro = Registrador.objects.get(user_ident=idd_user)
    if alvo == 'nomeuser':
        registro.nomeuser = novo_valor
    elif alvo == 'user_id':
        registro.user_ident = novo_valor
    elif alvo == 'data':
        registro.data = novo_valor
    elif alvo == 'rep_dep':
        registro.rep_dep = novo_valor
    elif alvo == 'is_writable':
        registro.is_writable = novo_valor
    elif alvo == 'locale_is':
        registro.locale_is = novo_valor
    elif alvo == 'tipo':
        registro.tipo = novo_valor
    registro.save()

def remover_elm(idd_user):
    registro = Registrador.objects.get(user_ident=idd_user).delete()
    return registro

#---------------------------------#------------------------------#----------------------------#

def form_data(timestam):    
    datas = date.fromtimestamp(timestam)
    dataFormatada = datas.strftime('%d/%m/%Y')
    return dataFormatada

def get_message(text, chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    # print("Resultado do meu Chat33333333333333")
    # print(response.content)

def send_message(text, chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)

def send_message_ACESS(dep_cat, chat_id):
    text = f'Informe o numero que representa o {dep_cat} o senhor acessora\n'
    if dep_cat == "Federal":
        for dep in dep_f:
            text += f'{dep["id"]}. {dep["nome"]}\n'
    if dep_cat == "Estadual":
        for dep in dep_e:
            text += f'{dep["id"]}. {dep["nome"]}\n'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)

    
    # print(response.content)

def send_image(file_path, chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    data = {'chat_id': chat_id, }
    files = {'photo': open(file_path, 'rb')}
    response = requests.post(url, data=data, files=files)
    # print(response.content)

def inicial(text, chat_id):
    menu_init = {
            "keyboard": [
                [
                    {"text": "✅ CADASTRAR"},
                    {"text": "👁‍🗨 CONSULTAR"},
                ],[
                    {"text": "✏ EDITAR"},
                    {"text": "🗑 DELETAR"},
                ]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    butt = json.dumps(menu_init)
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': butt}
    response = requests.post(url, data=data)
    # print(response.content)

def send_menu(text, chat_id):
    botoes = {
            "inline_keyboard": [
                [
                    {"text": "DEPUTADO", "callback_data": "D"},
                    {"text": "ACESSOR", "callback_data": "A"}
                ]
            ]
        }
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    butt = json.dumps(botoes)
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': butt}
    response = requests.post(url, data=data)
    # print(response.content)

def send_menu_dep1(text, chat_id):
    botoes = {
            "inline_keyboard": [
                [
                    {"text": "FEDERAL", "callback_data": "FE"},
                    {"text": "ESTADUAL", "callback_data": "ES"}
                ]
            ]
        }
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    butt = json.dumps(botoes)
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': butt}
    response = requests.post(url, data=data)
    # print(response.content)

#Pergunta se é acessor de Deputado Estadual ou Federal
def choose_dep_acess(text, chat_id):

    botoes = {
            "inline_keyboard": [
                [
                    {"text": "FEDERAL", "callback_data": "ACFE"},
                    {"text": "ESTADUAL", "callback_data": "ACES"}
                ]
            ]
        }
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    butt = json.dumps(botoes)
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': butt}
    response = requests.post(url, data=data)
    # print(response.content)

def catch_dep( est, id):
    id = int(id)
    if est == 'Estadual':
        for dep in dep_e:
            print(dep['id'] == id)
            print(f"{type(dep['id'])} == {type(id)}")
            if dep['id'] == id:
                return dep['nome']
    elif est == 'Federal':
        for dep in dep_f:
            print(dep['id'] == id)
            print(f"{type(dep['id'])} == {type(id)}")
            if dep['id'] == id:
                return dep['nome']

@csrf_exempt
def teleg(requests):
    if requests.method == 'POST':
        json_list = json.loads(requests.body)
        # print(json_list)
        if("message" in json_list.keys()):
            id_chatt = json_list["message"]["chat"]["id"]
            # É um comando
            if("entities" in json_list['message'].keys()):
                # Se o comando for help
                if json_list['message']['text'] == '/help':
                    edit_data("nome", "Dinossauro", id_chatt)
                    edit_data("is_writable", "", id_chatt)
                # Se o comando for start
                elif json_list['message']['text'] == '/start':
                    if not(buscar_id_user(id_chatt)):
                        inserir_dado(user_id=id_chatt, data=form_data(json_list["message"]["date"]))
                        usuer = buscar_id_user(id_chatt)
                    usuer = buscar_id_user(id_chatt)

                    inicial("Selecione a opção", id_chatt)
            else:
            # É uma mensagem
                # REALIZAR CADASTRO
                usuer = buscar_id_user(id_chatt)
                print(usuer)
                if len(usuer) == 0:
                    send_message("Você deve enviar o comando /start para iniciar o cadastro", id_chatt)
                elif json_list['message']['text'] == '✅ CADASTRAR':
                    edit_data("is_writable", "", id_chatt)
                    send_menu("Qual cargo o senhor ocupa", id_chatt)
                # REALIZAR EDIÇÃO
                elif json_list['message']['text'] == '✏ EDITAR':
                    edit_data("is_writable", "", id_chatt)
                    send_message("Vou editar seus dados", id_chatt)
                elif json_list['message']['text'] == '👁‍🗨 CONSULTAR':
                    edit_data("is_writable", "", id_chatt)
                    send_message("Vou editar seus dados", id_chatt)
                elif json_list['message']['text'] == '🗑 DELETAR':
                    edit_data("is_writable", "", id_chatt)
                    send_message("Vou deletar seus dados", id_chatt)
                elif usuer["is_writable"] == "nomeuser":
                    edit_data("nomeuser", json_list['message']['text'], json_list["message"]["chat"]["id"])
                    edit_data("is_writable", "", json_list["message"]["chat"]["id"])
                    nome_d = buscar_id_user(json_list["message"]["chat"]["id"])
                    if nome_d['tipo'] == 'Deputado':
                        send_message(f'Seja Bem Vindo Sr {nome_d["tipo"]} {nome_d["locale_is"]} {nome_d["nomeuser"]}', nome_d["user_ident"])

                    if nome_d['tipo'] == 'Acessor':
                        send_message(f'Seja Bem Vindo Sr {nome_d["tipo"]} {nome_d["nomeuser"]}', nome_d["user_ident"])
                        choose_dep_acess("Qual categoria de deputado o senhor acessora", nome_d["user_ident"])
                        

                elif usuer["is_writable"] == "rep_dep":
                    tip_dep = usuer["locale_is"] 
                    tip_num = 77 if tip_dep == 'Estadual' else 52 if tip_dep == 'Federal' else None
                    rest = re.findall(r'\d+',json_list['message']['text'])
                    if len(rest) == 0:
                        send_message("Por favor. Digite um numero válido", usuer["user_ident"])
                    elif int(rest[0]) < 0 or int(rest[0]) > tip_num:
                        send_message("Por favor. Digite um numero válido", usuer["user_ident"])
                    else:
                        dept = catch_dep(usuer["locale_is"],int(rest[0]))
                        edit_data("rep_dep", dept, json_list["message"]["chat"]["id"])
                        edit_data("is_writable", "", json_list["message"]["chat"]["id"])
                        usuer = buscar_id_user(json_list["message"]["chat"]["id"])
                        send_message(f"Obrigado senhor acessor do Deputado {usuer['locale_is']} {usuer['rep_dep']} ", usuer["user_ident"])
                        send_message("Cadastro concluído com sucesso 😃", usuer["user_ident"])
                        send_message("Aguarde a mensagem de aprovação do administrador para receber todas as atualizações", usuer["user_ident"])
                    print(usuer)
                    # i_files = os.getcwd()
                    # i_file = os.path.join(i_files,'telegram', 'img', 'mao.png')
                else:
                    send_message("Desculpe não entendi seu comando", id_chatt)
            

        # É um callback
        elif("callback_query" in json_list.keys()):
            id_chatt = json_list["callback_query"]["message"]["chat"]["id"]
            escolha = json_list["callback_query"]["data"]
            usuer = buscar_id_user(id_chatt)

            # É um deputado
            if json_list["callback_query"]["data"] == 'FE':
                print("Tipo de User")
                print(usuer['tipo'])
                if(usuer['tipo']=="Acessor"):
                    send_message("O Senor não está cadastrado como deputado. Por gentileza realizar a correção clicando na opção EDITAR", json_list["callback_query"]["message"]["chat"]["id"])
                else:
                    send_message("Obrigado pela confirmação Senhor Deputado", json_list["callback_query"]["message"]["chat"]["id"])
                    edit_data("locale_is", "Federal", json_list["callback_query"]["message"]["chat"]["id"])
                    send_message("Por qual nome o senhor gostaria de ser chamado?", json_list["callback_query"]["message"]["chat"]["id"])
                    edit_data("is_writable", "nomeuser", json_list["callback_query"]["message"]["chat"]["id"])
            
            elif json_list["callback_query"]["data"] == 'ES':
                send_message("Obrigado pela confirmação Senhor Deputado", json_list["callback_query"]["message"]["chat"]["id"])
                edit_data("locale_is", "Estadual", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Por qual nome o senhor gostaria de ser chamado?", json_list["callback_query"]["message"]["chat"]["id"])
                edit_data("is_writable", "nomeuser", json_list["callback_query"]["message"]["chat"]["id"])

            elif json_list["callback_query"]["data"] == 'D':
                edit_data("tipo", "Deputado", json_list["callback_query"]["message"]["chat"]["id"])
                send_menu_dep1("Por favor no informe a que categoria o Senhor pertence", json_list["callback_query"]["message"]["chat"]["id"])

            # É um acessor
            elif json_list["callback_query"]["data"] == 'A':
                edit_data("tipo", "Acessor", json_list["callback_query"]["message"]["chat"]["id"])
                edit_data("locale_is", "", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Olá Senhor Acessor", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Por qual nome o senhor gostaria de ser chamado?", json_list["callback_query"]["message"]["chat"]["id"])
                edit_data("is_writable", "nomeuser", json_list["callback_query"]["message"]["chat"]["id"])

            elif json_list["callback_query"]["data"] == 'ACFE':
                edit_data("locale_is", "Federal", json_list["callback_query"]["message"]["chat"]["id"])
                edit_data("is_writable", "rep_dep", json_list["callback_query"]["message"]["chat"]["id"])
                send_message_ACESS("Federal", json_list["callback_query"]["message"]["chat"]["id"])
            elif json_list["callback_query"]["data"] == 'ACES':
                edit_data("locale_is", "Estadual", json_list["callback_query"]["message"]["chat"]["id"])
                edit_data("is_writable", "rep_dep", json_list["callback_query"]["message"]["chat"]["id"])
                send_message_ACESS("Estadual", json_list["callback_query"]["message"]["chat"]["id"])

    return HttpResponse("OK")

