import json
import os
from datetime import date, datetime

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from data2.datamanager import *

TOKEN = '6120299498:AAF10CfoQzpsDWnuoQd5NeyqreZoStO4JwM'


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


@csrf_exempt
def teleg(requests):
    if requests.method == 'POST':
        json_list = json.loads(requests.body)
        print(json_list)
        # print(json_list)
        if("message" in json_list.keys()):
            id_chatt = json_list["message"]["chat"]["id"]
            # É um comando
            if("entities" in json_list['message'].keys()):
                # Se o comando for help
                if json_list['message']['text'] == '/help':
                    editar_dado("rep_dep", "Dinossauro", json_list["message"]["chat"]["id"])
                # Se o comando for start
                elif json_list['message']['text'] == '/start':
                    if not(buscar_id_user(id_chatt)):
                        inserir_dado("", id_chatt, form_data(json_list["message"]["date"]), "", False, "deputado")
                        usuer = buscar_id_user(id_chatt)
                    usuer = buscar_id_user(id_chatt)
                    print("Meu usuario")
                    print(usuer)
                    inicial("Selecione a opção", id_chatt)
            else:
            # É uma mensagem
                # REALIZAR CADASTRO
                usuer = buscar_id_user(id_chatt)
                print(usuer)
                if json_list['message']['text'] == '✅ CADASTRAR':
                    send_menu("Qual cargo o senhor ocupa", id_chatt)
                # REALIZAR EDIÇÃO
                elif json_list['message']['text'] == '✏ EDITAR':
                    send_message("Vou editar seus dados", id_chatt)
                elif json_list['message']['text'] == '🗑 DELETAR':
                    send_message("Vou deletar seus dados", id_chatt)
                elif usuer["is_writable"] == True:
                    editar_dado("nomeuser", json_list['message']['text'], json_list["message"]["chat"]["id"])
                    editar_dado("is_writable", False, json_list["message"]["chat"]["id"])

                    # i_files = os.getcwd()
                    # i_file = os.path.join(i_files,'telegram', 'img', 'mao.png')
                else:
                    send_message("Desculpe não entendi seu comando", id_chatt)
            

        # É um callback
        elif("callback_query" in json_list.keys()):
            id_chatt = json_list["callback_query"]["message"]["chat"]["id"]
            escolha = json_list["callback_query"]["data"]
            # É um deputado
            if json_list["callback_query"]["data"] == 'D':
                editar_dado("tipo", "deputado", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Olá Senhor Deputado", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Por qual nome o senhor gostaria de ser chamado?", json_list["callback_query"]["message"]["chat"]["id"])
                editar_dado("is_writable", True, json_list["callback_query"]["message"]["chat"]["id"])

            # É um acessor
            if json_list["callback_query"]["data"] == 'A':
                editar_dado("tipo", "acessor", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Olá Senhor Acessor", json_list["callback_query"]["message"]["chat"]["id"])
                send_message("Por qual nome o senhor gostaria de ser chamado?", json_list["callback_query"]["message"]["chat"]["id"])
                editar_dado("is_writable", True, json_list["callback_query"]["message"]["chat"]["id"])






    return HttpResponse("OK")

