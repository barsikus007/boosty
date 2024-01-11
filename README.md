<p align="center">
  <a href="https://github.com/barsikus007/boosty">
    <img src="https://raw.githubusercontent.com/barsikus007/boosty/master/logo.png" alt="BoostyPy">
  </a>
</p>

# Boosty Wrapper

[![PyPI - Version](https://img.shields.io/pypi/v/boosty.svg)](https://pypi.org/project/boosty)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/boosty.svg)](https://pypi.org/project/boosty)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage](#usage)

## Installation

```console
pip install boosty
```

## License

`boosty` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

> [!IMPORTANT]
> **!WARNING! this version of library is very unstable**
>
> **If you use it, contact maintainer to help make it stable**

## Usage

*Optional:* specify `IGNORE_MISSING_AND_EXTRA_FIELDS` environment variable to disable strict schema validation

*Optional:* fill `auth.json` file with authentication data:

```json
{
  "access_token": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
  "device_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
  "expires_at": 12345678900,
  "refresh_token": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
}
```

Example:

```python
from boosty.api import API

api = API()
response = await api.get_post("boosty", post_id="c9fb8a19-c45e-4602-9942-087c3af28c1b")
print(response.title)
# 'Добро пожаловать на борт!'
```

More examples in [examples/](https://github.com/barsikus007/boosty/blob/master/examples/) folder

### TODO for stable release

- api schema
  - add access levels logic for requests
- minimal docs
- useful properties for models
- merge reply comment with comment model
- add examples
  - render text
  - get video url
  - get comment url
- add tests
  - boosty profile
  - comments
  - replies
  - video
  - entities parsing
