---
title: Distillery index
permalink: /distillery-index/
layout: single
classes: wide
---

<!-- [Jura]({{ "/distilleries/jura/" | relative_url }}) -->


{% capture json %}
[
{% for pair in site.data.producers %}
  {% assign id = pair[0] %}
  {% assign producer = pair[1] %}
  {"id":"{{ id }}","name":"{{ producer.name }}"}{% unless forloop.last %},{% endunless %}
{% endfor %}
]
{% endcapture %}

{% assign list = json | from_json %}
{% assign sorted = list | sort: "name" %}

{% for p in sorted %}
- [{{ p.name }}]({{ "/distilleries/" | append: p.id | append: "/" | relative_url }})
{% endfor %}
