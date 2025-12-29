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

    r: {{ r | inspect }}<br>
    bottle key: {{ r[1].bottle }}<br>
    bottle: {{ bottle | inspect }}<br>
    producer: {{ producer | inspect }}<br>
    <hr>

    
{% endfor %}