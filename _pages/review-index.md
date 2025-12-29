---
title: All reviews
permalink: /review-index/
layout: single
classes: wide
---

Test 2

{% assign reviews = site.data.reviews %}
{% assign bottles = site.data.bottles %}
{% assign producers = site.data.producers %}
{% assign bottlers = site.data.bottlers %}

<!-- Category -->


{% assign categories = "" | split: "" %}

{% for r in reviews %}
    {{ r }}
    {% assign bottle = bottles[r.bottle] %}
    {% if bottle %}
        {{ bottle }}
    {% else %} 
        missing bottle
    {% endif %}
{% endfor %}