#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Vitaly Kunitsa aka Steel
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import requests
import json
from datetime import datetime

__author__ = 'Steel'

"""Библиотека API для полного контроля и управления серверами на платформе 1Cloud.ru
Документация по API: https://1cloud.ru/api
"""

# Maximum requests per second allowed by 1cloud.ru for each request type
MAX_REQUESTS = {
    'GET': 1.5,
    'POST': 10,
    'PUT': 10,
    'DELETE': 10
}

STATUS_CODES = {
    200: 'request complete',
    401: 'not authorized',
    403: 'request denied',
    404: 'object not found',
    400: 'invalid request parameters',
    500: 'unknown error - contact 1cloud.ru support'
}

URL = 'https://api.1cloud.ru'


class OneCloudApi(object):
    """
    Модуль API 1cloud.ru для полного контроля и управления арендованными серверами

    :param api_key: Ключ API генерируется на сайте 1cloud.ru в настройках профиля. Обязательный параметр.
    :param timeout: Таймаут ожидания ответа от сервера в секундах.
    """
    api_key = None
    timeout = None
    rS = None
    last_request = None

    def __init__(self, api_key, timeout=5):
        self.api_key = api_key
        self.timeout = timeout
        self.rS = requests.Session()
        self.rS.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(api_key)
        })

    def req(self, path, method='GET', data=None):
        """
        Автоматически формирует корректный запрос к серверу
        :param path: формируется автоматически вызывающим методом
        :param method: формируется автоматически вызывающим методом
        :param data: формируется автоматически вызывающим методом
        :return: JSON объект с соответствующими запросу данными.
        В случае ошибки: {'ERROR_CODE': код ошибки, 'ERROR_MESSAGE': 'текст ошибки'}
        """
        if self.last_request is None:
            self.last_request = datetime.now()
        elif (self.last_request - datetime.now()).seconds < MAX_REQUESTS[method]:
            return {
                'ERROR_CODE': None,
                'ERROR_MESSAGE': 'Too fast for %s type requests! Try again in %s seconds.' % (
                    method, str(MAX_REQUESTS[method] - (self.last_request - datetime.now()).seconds))
            }

        r = self.rS.request(url=URL + path, method=method, data=data)
        if r.status_code != 200:
            if r.status_code in STATUS_CODES:
                return {
                    'ERROR_CODE': r.status_code,
                    'ERROR_MESSAGE': STATUS_CODES[r.status_code]
                }
            else:
                return {
                    'ERROR_CODE': None,
                    'ERROR_MESSAGE': 'Unknown error. Plain response:' + r.text
                }
        res = json.loads(r.text)
        return res

    def get_balance(self):
        """Запрос состояния счета пользователя

        :return: float значение баланса
        """
        return self.req(path='/customer/balance', method='GET')

    def get_images_list(self):
        """Образы (шаблоны) возможных систем для установки на сервер

        :return: JSON массив с характеристиками каждого образа
        """
        return self.req(path='/image', method='GET')

    def create_image(self, name, tech_name, server_id):
        """Создание шаблона на основе Вашего, уже функионирующего сервера

        :param name: string Пользовательское название шаблона
        :param tech_name: Техническое имя (что-то наподобие id)
        :param server_id: Id сервера, на основе которого будет создан шаблон
        :return: JSON массив с атрибутами шаблона
        """
        data = {
            'Name': name,
            'TechName': tech_name,
            'ServerID': server_id
        }
        return self.req(path='/image', method='POST', data=data)

    def delete_image(self, image_id):
        """Удаление шаблона

        :param image_id: Id удаляемого шаблона
        :return: None
        """
        return self.req(path='/image/{}'.format(image_id), method='DELETE')

    def get_private_networks_list(self):
        """
        Метод возвращает список всех Ваших частных сетей.
        :return: JSON объект, массив объектов, каждый элемент массива описывает атрибуты одной из сетей.
        """
        return self.req(path='/network', method='GET')

    def get_private_network_by_id(self, network_id):
        """
        Подробности об одной из Ваших частных сетей
        :param network_id: Id запрашиваемой сети
        :return: JSON объект, который будет содержать описание значений атрибутов данной частной сети.
        """
        return self.req(path='/network/{}'.format(network_id), method='GET')

    def create_private_network(self, name):
        """
        Создание новой частной сети
        :param name: Имя создаваемой сети
        :return: JSON объект, который будет содержать описание значений атрибутов данной частной сети.
        """
        data = {
            'Name': name
        }
        return self.req(path='/network/', method='POST', data=data)

    def delete_private_network(self, network_id):
        """
        Удаление частной сети
        :param network_id: Id удаляемой сети
        :return:
        """
        return self.req(path='/network/{}'.format(network_id), method='DELETE')

    def get_dc_locations(self):
        """
        Список всех доступных локаций (ЦОД), на которых возможно создать виртуальный серверю
        :return: JSON объект, с массивом объектов - атрибутов одной из доступных локаций.
        """
        return self.req(path='/dcLocation', method='GET')

    def get_servers_list(self):
        """
        Список всех Ваших заказанных серверов
        :return: JSON объект, с массивом объектов - атрибутов заказанных серверов.
        """
        return self.req(path='/server', method='GET')

    def get_server_by_id(self, server_id):
        """
        Подробности о сервере по Id
        :param server_id:
        :return:
        """
        return self.req(path='/server/{}'.format(server_id), method='GET')

    def create_server(self, name, cpu, ram, hdd, image_id, dc_location, hdd_type='SAS', is_high_performance=False):
        """
        Создание сервера
        :param name: Пользовательское название сервера, заданное при создании сервера
        :param cpu: Количество ядер процессора, выделенных на данный сервер [1...8]. Шаг увеличения значений: 1.
        :param ram: Объем ОЗУ в Мб. Linux: [512...16384], Windows: [1024...16384]
                    Шаг увеличения значений: до 1024 шаг 256, после 1024 шаг составляет 1024.
        :param hdd: Количество дискового пространства, выделенного на данный сервер (в Gb).
                    Linux: [10...250], Windows: [40...250] Шаг увеличения значений: 10.
        :param image_id: Уникальный идентификатор образа OS из get_servers_list()
        :param dc_location: Техническое наименование DC, в которой создаем сервер из get_dc_locations()
        :param hdd_type: Тип диска сервера, может быть одним из следующих значений "SAS" или "SSD"
        :param is_high_performance: True - если необходим сервер в высокопроизводительном пуле, false - в базовом пуле.
        :return: JSON объект - атрибуты созданного сервера.
        """
        data = {
            'Name': name,
            'CPU': cpu,
            'RAM': ram,
            'HDD': hdd,
            'ImageID': image_id,
            'HDDType': hdd_type,
            'isHighPerformance': is_high_performance,
            'DCLocation': dc_location
        }
        return self.req(path='/server', method='POST', data=data)

    def update_server_parameters(self, server_id, cpu, ram, hdd, hdd_type, is_high_performance):
        """
        Изменение конфигурации сервера
        :param server_id: Id сервера с изменяемой конфигурацией
        :param cpu: Количество ядер процессора, выделенных на данный сервер [1...8]. Шаг увеличения значений: 1.
        :param ram: Объем ОЗУ в Мб. Linux: [512...16384], Windows: [1024...16384]
                    Шаг увеличения значений: до 1024 шаг 256, после 1024 шаг составляет 1024.
        :param hdd: Количество дискового пространства, выделенного на данный сервер (в Gb).
                    Linux: [10...250], Windows: [40...250] Шаг увеличения значений: 10.
        :param hdd_type: Тип диска сервера, может быть одним из следующих значений "SAS" или "SSD"
        :param is_high_performance: True - если необходим сервер в высокопроизводительном пуле, false - в базовом пуле.
        :return: JSON объект - атрибуты созданного сервера.
        """
        data = {
            'CPU': cpu,
            'RAM': ram,
            'HDD': hdd,
            'HDDType': hdd_type,
            'isHighPerformance': is_high_performance
        }
        return self.req(path='/server/{}'.format(server_id), method='PUT', data=data)

    def delete_server(self, server_id):
        """
        Удаление сервера
        :param server_id:
        :return:
        """
        return self.req(path='/server/{}'.format(server_id), method='DELETE')

    def power_on_server(self, server_id):
        """
        Включить питание сервера
        :param server_id:
        :return:
        """
        data = {
            'Type': 'PowerOn'
        }
        return self.req(path='/server/{}/action'.format(server_id), method='POST', data=data)

    def power_off_server(self, server_id):
        """
        Выключить питание сервера
        :param server_id:
        :return:
        """
        data = {
            'Type': 'PowerOff'
        }
        return self.req(path='/server/{}/action'.format(server_id), method='POST', data=data)

    def shutdown_guest_os(self, server_id):
        """
        Выключение сервера средствами операционной системы. Только для ОС с усановленными VMware комонентами.
        :param server_id:
        :return:
        """
        data = {
            'Type': 'ShutDownGuestOS'
        }
        return self.req(path='/server/{}/action'.format(server_id), method='POST', data=data)

    def reboot_server(self, server_id):
        """
        Перезагрузка сервера
        :param server_id:
        :return:
        """
        data = {
            'Type': 'PowerReboot'
        }
        return self.req(path='/server/{}/action'.format(server_id), method='POST', data=data)

    def connect_server_to_network(self, server_id, network_id):
        """
        Подключить линк созданной ранее частной сети
        :param server_id:
        :param network_id:
        :return:
        """
        data = {
            'Type': 'AddNetwork',
            'NetworkID': network_id
        }
        return self.req(path='/server/{}/action'.format(server_id), method='POST', data=data)

    def disconnect_server_from_network(self, server_id, network_id):
        """
        Отключить от заданной частной сети
        :param server_id:
        :param network_id:
        :return:
        """
        data = {
            'Type': 'RemoveNetwork',
            'NetworkID': network_id
        }
        return self.req(path='/server/{}/action'.format(server_id), method='POST', data=data)
