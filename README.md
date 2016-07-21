# OneCloud API
API клиент для управления серверами на платформе [https://1Cloud.ru](https://1cloud.ru/ref/17308)

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
from onecloud import api
a = api.OneCloud(api_key='API ключ из личного кабинета', timeout=5)
```

#Возможности:
- Актуальный баланс:
```python
 a.get_balance()
```

- Список Ваших серверов:
```python
 a.get_servers_list()
```

- Включить сервер:
```python
 a.power_on_server(self, server_id)
```

- Перезагрузить сервер:
```python
 a.reboot_server(self, server_id)
```

- Выключить сервер:
```python
a.power_off_server(self, server_id)
```

- Создать новый сервер:
```python
    a.create_server(self, name, cpu, ram, hdd, image_id, dc_location, hdd_type, is_high_performance) ...
```
- ...в выбранном ДатаЦентре
```python
a.get_dc_locations(self)
```
- ...и установить ОС из списка образов:
```python
a.get_images_list()
```

- Создать свой образ операционной системы:
```python
a.create_image(self, name, tech_name, server_id)
```

- Создать частную сеть:
```python
a.create_private_network(self, name)
```

- Список созданных сетей:
```python
a.get_private_networks_list(self)
```

- Подключить сервер к частной сети:
```python
a.connect_server_to_network(self, server_id, network_id)
```

и т.д.
более подробно:

# Документация по API
https://1cloud.ru/api
