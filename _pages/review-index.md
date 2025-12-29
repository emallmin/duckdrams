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
