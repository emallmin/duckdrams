---
title: Distillery index
permalink: /distillery-index/
layout: single
classes: wide
---

<!-- [Jura]({{ "/distilleries/jura/" | relative_url }}) -->


<h2> Producer </h2>
<div>
{% assign names = "" %}
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
    <a href="{{ "/distilleries/" | append: id | append: "/" | relative_url }}">
      {{ name }}
    </a> ●
  {% endif %}
{% endfor %}
</div>

<h2> Bottler </h2>
<div>
{% assign names = "" %}
{% for pair in site.data.bottlers %}
  {% assign bottler = pair[1] %}
  {% assign names = names | append: bottler.name | append: "||" %}
{% endfor %}
{% assign names = names | split: "||" | sort %}
{% for name in names %}
  {% if name != "" %}
    {% assign id = "" %}
    {% for pair in site.data.bottlers %}
      {% if pair[1].name == name %}
        {% assign id = pair[0] %}
      {% endif %}
    {% endfor %}
    <a href="{{ "/distilleries/" | append: id | append: "/" | relative_url }}">
      {{ name }}
    </a> ●
  {% endif %}
{% endfor %}
</div>

