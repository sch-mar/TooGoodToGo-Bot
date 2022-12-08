[![GitHub release](https://img.shields.io/github/release/sch-mar/TooGoodToGo-Bot.svg)](https://GitHub.com/sch-mar/TooGoodToGo-Bot/releases/) [![GitHub latest commit](https://badgen.net/github/last-commit/sch-mar/TooGoodToGo-Bot)](https://GitHub.com/sch-mar/TooGoodToGo-Bot/commit/) [![GitHub issues](https://img.shields.io/github/issues/sch-mar/TooGoodToGo-Bot.svg)](https://GitHub.com/sch-mar/TooGoodToGo-Bot/issues/) [![GitHub license](https://img.shields.io/github/license/sch-mar/TooGoodToGo-Bot.svg)](https://github.com/sch-mar/TooGoodToGo-Bot/blob/master/LICENSE)

# TooGoodToGo Notification Bot

Informs users about new availabilities at their favorite stores.

## setup

Clone repository or download archive manually.

```git
# using ssh
git clone git@github.com:sch-mar/TooGoodToGo-Bot.git
```

Create a ```/config/.config``` file using the following template.

```yaml
telegram:
    api_key: <your_bots_api_key>
```

Install libraries from ```.requirements```

```bash
python3 -m pip install -r .requirements
```

Run ```python3 /src/main.py```. To ensure persistency use nohup, tmux etc.
