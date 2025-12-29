---
title: All reviews
permalink: /review-index/
layout: single
classes: wide
---

Test 4

{% assign reviews = site.data.reviews %}
{% assign bottles = site.data.bottles %}
{% assign producers = site.data.producers %}
{% assign bottlers = site.data.bottlers %}

<!-- Category -->


{% assign categories = "" | split: "" %}

{% for r in reviews %}
  {% assign review = r[1] %}

  {% if review.bottle %}
    {% assign bottle = bottles[review.bottle] %}
    bottle: {{ bottle}}
  {% endif %}

  {% if bottle %}
    {% assign producer = producers[bottle.stats.producer] %}
    producer: {{ producer}}
  {% endif %}

{% endfor %}
