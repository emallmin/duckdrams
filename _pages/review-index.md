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
    {% assign bottle = bottles[r[1].bottle] %}
    {% assign producer = producers[bottle.producer] %}
    {% if producer and producer.category %}
        {% assign cat = producer.category %}
    {% elif producer and producer.kind == "line" %}
        {% assign distillery = producers[producer.distillery] %}
        {% assign cat = distillery.category %}
    {% else %}
        {% assign cat = "UNKNOWN CATEGORY" %}
    {% endif %}
    {{ cat }}
    
{% endfor %}