---
title: Distillery index
permalink: /distillery-index/
layout: single
classes: wide
---

<!-- [Jura]({{ "/distilleries/jura/" | relative_url }}) -->

{% assign sorted = site.data.producers | sort: "name" %}

{% for producer in sorted %}
  {% assign id = "" %}

  {% for pair in site.data.producers %}
    {% if pair[1].name == producer.name %}
      {% assign id = pair[0] %}
    {% endif %}
  {% endfor %}

- [{{ producer.name }}]({{ "/distilleries/" | append: id | append: "/" | relative_url }})

{% endfor %}
