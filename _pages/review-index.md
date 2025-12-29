---
title: All reviews
permalink: /review-index/
layout: single
classes: wide
---

{% assign reviews = site.data.reviews %}
{% assign bottles = site.data.bottles %}
{% assign producers = site.data.producers %}


{% assign categories = "" | split: "" %}
{% for r in reviews %}
    {% assign bottle = bottles.r.bottle %}
    {% if bottle.category %}
        {% assign categories = categories | concat bottle.category | split: "" %}
    {% elsif bottle.kind == "line"%}
        {{hej}}
    {% endif %}
{% endfor %}


{% for category in categories %}
  <h2> {{category}} </h2>
{% endfor %}
