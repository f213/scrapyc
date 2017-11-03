# scrapyc
[![Build Status](https://travis-ci.org/f213/scrapyc.svg?branch=master)](https://travis-ci.org/f213/scrapyc)
[![codecov](https://codecov.io/gh/f213/scrapyc/branch/master/graph/badge.svg)](https://codecov.io/gh/f213/scrapyc)

Scrapyc is a command line interface and client library for a [scrapyd](https://scrapyd.readthedocs.io/en/stable/). Despite already existing
[scrapyd-client](https://github.com/scrapy/scrapyd-client) this client just works and has been well-tested.

Currently scrapyc is focused only on working with already deployed spiders. For deploying new spiders, please use the [official option](http://scrapyd.readthedocs.io/en/stable/deploy.html).


## Installation

```
pip install scrapyc
```

Both python 2 and python 3 supported.

## Usage (Cli)

```sh
scrapyc --url=http://scraper1.your.host:6800 --username=r00t --password=pass status
```

Or you can use environemnt varialbes

```sh
export SCRAPYC_URL=http://scraper1.your.host:6800
export SCARPYC_USERNAME=r00t
export SCARPYC_PASSWORD=pass

scrapyc status
```

## Usage (Lib)

```python
from scrapyc import ScrapydClient

c = ScrapydClient(url, username, password)

c.get_status()
c.schedule(project='yandex', spider='spider')
