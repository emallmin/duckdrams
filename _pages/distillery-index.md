---
title: Distillery index
permalink: /distillery-index/
layout: single
classes: wide
---

<!-- [Jura]({{ "/distilleries/jura/" | relative_url }}) -->


{% assign names = "" | split: "" %}

{% for pair in site.data.producers %}
  {% assign producer = pair[1] %}
  {% assign names = names | append: producer.name | append: "||" %}
{% endfor %}

{% assign names = names | split: "||" | sort %}

{% for name in names %}
  {% if name != "" %}
    {% assign id = "" %}
    {% for pair in site.data.producers %}
      {% if pair[1].name == name %}
        {% assign id = pair[0] %}
      {% endif %}
    {% endfor %}

 [{{ name }}]({{ "/distilleries/" | append: id | append: "/" | relative_url }}) ●

  {% endif %}
{% endfor %}
