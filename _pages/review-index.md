---
title: All reviews
permalink: /review-index/
layout: single
classes: wide
---

Test

{% assign reviews = site.data.reviews %}
{% assign bottles = site.data.bottles %}
{% assign producers = site.data.producers %}
{% assign bottlers = site.data.bottlers %}

<!-- Category -->


{% assign categories = "" | split: "" %}
{% for r in reviews %}
{% assign bottle = bottles[r.bottle] %}
{% assign producer = producers[bottle.producer] %}
{% if producer.category %}
    {% assign cat = producer.category %}
{% elif producer.kind == "line" %}
    {% assign distillery = producers[producer.distillery] %}
    {% assign cat = distillery.category %}
{% else %}
    {% assign cat = "UNKNOWN CATEGORY" %}
{% endif %}
{% assign categories = categories | concat: cat %}
{% endfor %}

{% assign categories = categories | uniq | sort %}



{% for category in categories %}
  <h2> {{category}} </h2>
  <!-- -->

{% endfor %}

