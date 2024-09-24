<p align="center">
  <a href="https://github.com/barsikus007/boosty">
    <img src="https://raw.githubusercontent.com/barsikus007/boosty/master/logo.svg" alt="BoostyPy" height="250px">
  </a>
</p>

# Обертка для Boosty

[![PyPI - Version](https://img.shields.io/pypi/v/boosty.svg)](https://pypi.org/project/boosty)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/boosty.svg)](https://pypi.org/project/boosty)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

-----

**[English description](https://github.com/barsikus007/boosty/blob/master/README.md)**

**Содержание**

- [Установка](#установка)
- [Лицензия](#лицензия)
- [Использование](#использование)

## Установка

```console
pip install boosty
```

## Лицензия

`boosty` распространяется на условиях лицензии [MIT](https://spdx.org/licenses/MIT.html).

> [!IMPORTANT]
> **!ВНИМАНИЕ! эта версия библиотеки очень нестабильна (в новых версиях возможны радикальные изменения в API и зависимостях)**
>
> **Если вы используете ее, свяжитесь с мейнтейнером, чтобы помочь сделать ее стабильной**

## Использование

*Необязательно:* укажите переменную среды `IGNORE_MISSING_AND_EXTRA_FIELDS` чтобы отключить строгую проверку схемы

*Необязательно:* заполните файл `auth.json` данными аутентификации (или используйте [браузерную аутентификацию](https://github.com/barsikus007/boosty/blob/master/examples/browser_auth.py) чтобы их создать):

```json
{
  "access_token": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
  "device_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
  "expires_at": 12345678900,
  "refresh_token": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
}
```

Пример:

```python
from boosty.api import API

api = API()
response = await api.get_post("boosty", post_id="c9fb8a19-c45e-4602-9942-087c3af28c1b")
print(response.title)
# 'Добро пожаловать на борт!'
```

Больше примеров в папке [examples/](https://github.com/barsikus007/boosty/tree/master/examples/)
