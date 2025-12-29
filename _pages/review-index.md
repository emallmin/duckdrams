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
    {% else %}
        missing bottle field in review {{r[0]}}
    {% endif %}

    {% if bottle %}
        {% assign producer = producers[bottle.stats.producer] %}

        {% if producer %}
            {% if producer.category %}
                {% assign cat = producer.category %}
            {% elsif producer.kind == "line" %}
                {% assign distillery = producers[producer.distillery] %}
                {% if distillery and distillery.category %}
                    {% assign cat = distillery.category %}
                {% else %}
                    review {{r[0]}} with producer {{producer}}: distillery is missing, or distillery has no category                    
                {% endif %}
            {% else %}
                review {{r[0]}}: no category in producer or no distillery to default to
            {% endif %}
            {% assign categories = categories | concat: producer.category | split: "" %}
        {% else %}
            review {{r[0]}}: producer reference not found in producers.yml
        {% endif %}       
    {% else %}
        review {{r[0]}}: bottle reference not found in bottles.yml 
    {% endif %}
 
{% endfor %}
