# RemoveMeFrom Telegram [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com)

A curated list of awesome Telegram channels, bots, chat's services, etc. related with addmeto-chat

- - -

# Chatlanians

Всё просто:

* Админы - школьники,
* Бобук - Бог,
* Николаич - православие и отвага,
* Фронтендеры - геи,
* Тян - не нужны,
* Валера - бета тестер айоси,
* Табакеров - филиал ада,
* Рома - пьющий китаец :)

- - -

# CONTENT

{% for category in categories %}
- [{{ category }}](#{{ category | replace(" ", "-") | lower() }})
  {% for tagname in categories[category] %}
  - [{{ tagname }}](#{{ tagname | replace(" ", "-") | lower() }})
  {% endfor %}
{% endfor %}

- - -

# Awesome List

{% for category in categories %}
## {{ category }}
{% for tagname in categories[category] %}
### {{ tagname }}
{% for entry in categories[category][tagname] %}
* [{{ entry.title }}]({{ entry.url }}) - {{ entry.subscribers }} subscribers

    {{ entry.description }}
{% endfor %}{% endfor %}{% endfor %}

- - -

# Other Awesome Lists

List of lists.

- - -

# Contributing

Your contributions are always welcome! Please take a look at the [contribution guidelines](https://goo.gl) first.

I will keep some pull requests open if I'm not sure whether those libraries are awesome, you could [vote for them](https://goo.gl) by adding :+1: to them. Pull requests will be merged when their votes reach **20**.
