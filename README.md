**Discontinued**

Because the use of TooGoodToGo's API for bots is seemingly not intended by the provider, I decided to stop this small project. There probably are more or less complex solutions to avoid captcha, but I don't want to go down this road. Since TooGoodToGo recently added a widget to their Android app, which refreshes the availability status every 30 minutes, the justification for a notification bot has decreased immensely. It is also likely that a future update will introduce a native notification feature.

---
---
---

[![GitHub release](https://img.shields.io/github/release/sch-mar/TooGoodToGo-Bot.svg)](https://GitHub.com/sch-mar/TooGoodToGo-Bot/releases/) [![GitHub latest commit](https://badgen.net/github/last-commit/sch-mar/TooGoodToGo-Bot)](https://GitHub.com/sch-mar/TooGoodToGo-Bot/commit/) [![GitHub issues](https://img.shields.io/github/issues/sch-mar/TooGoodToGo-Bot.svg)](https://GitHub.com/sch-mar/TooGoodToGo-Bot/issues/) [![GitHub license](https://img.shields.io/github/license/sch-mar/TooGoodToGo-Bot.svg)](https://github.com/sch-mar/TooGoodToGo-Bot/blob/master/LICENSE)

# TooGoodToGo Notification Bot

Informs users about new availabilities at their favorite stores.

## setup

Clone repository or download archive manually.

```git
# using ssh
git clone git@github.com:sch-mar/TooGoodToGo-Bot.git
```

Create a ```config/.config``` file using the following template.

```yaml
telegram:
    api_key: <your_bots_api_key>
```

Install libraries from ```.requirements```

```bash
python3 -m pip install -r .requirements
```

Run ```main.py```. Python 3.9 is required, so to make sure you can use ```python3.9```. For persistency use nohup, tmux etc.

```bash
python3 src/main.py
```
