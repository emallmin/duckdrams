---
title: Distillery index
permalink: /distillery-index/
layout: single
classes: wide
---

<!-- [Jura]({{ "/distilleries/jura/" | relative_url }}) -->

{% assign producers = site.data.producers | sort: "name" %}

{% for p in producers %}
  {% assign id = p[0] %}
  {% assign producer = p[1] %}
  - [{{ producer.name }}]({{ "/distilleries/" | append: id | append: "/" | relative_url }})
{% endfor %}
