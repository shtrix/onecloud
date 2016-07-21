# OneCloud API
API клиент для управления серверами на платформе 1Cloud.ru

# Установка
Воспользуйтесь `pip` или `easy_install`:

```bash
$ pip install --upgrade onecloud
```
or
```bash
$ easy_install --upgrade onecloud
```
# Совместимость с версиями Python:
Python 2.6 or 2.7, 3.3+ полностью поддерживаются.

# Дополнительные компоненты:
Использует всего лишь один дополнительный компонент
* [requests](https://github.com/kennethreitz/requests)

# Использование
```python
import onecloud
api = onecloud.api.OneCloud(api_key='API ключ из личного кабинета', timeout=5)
```

#Возможности:
- Актуальный баланс:
```python
 api.get_balance()
```

- Список Ваших серверов:
```python
 api.get_servers_list()
```

- Включить сервер:
```python
 api.power_on_server(self, server_id)
```

- Перезагрузить сервер:
```python
 api.reboot_server(self, server_id)
```

- Выключить сервер:
```python
api.power_off_server(self, server_id)
```

- Создать новый сервер:
```python
    api.create_server(self, name, cpu, ram, hdd, image_id, dc_location, hdd_type, is_high_performance) ...
```
- ...в выбранном ДатаЦентре
```python
api.get_dc_locations(self)
```
- ...и установить ОС из списка образов:
```python
api.get_images_list()
```

- Создать свой образ операционной системы:
```python
api.create_image(self, name, tech_name, server_id)
```

- Создать частную сеть:
```python
api.create_private_network(self, name)
```

- Список созданных сетей:
```python
api.get_private_networks_list(self)
```

- Подключить сервер к частной сети:
```python
api.connect_server_to_network(self, server_id, network_id)
```

и т.д.
более подробно:

# Документация по API
https://1cloud.ru/api
