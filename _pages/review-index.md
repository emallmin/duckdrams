---
title: All reviews
permalink: /review-index/
layout: single
classes: wide
---

{% assign reviews = site.data.reviews %}
{% assign producers = site.data.producers %}


<!-- comment -->
{% assign categories = "" | split: "" %}
{% for r in reviews %}
  {% assign p = producers[r[1].stats.producer] %}
  {% if p and p.category %}
    {% unless categories contains p.category %}
      {% assign categories = categories | push: p.category %}
    {% endunless %}
  {% endif %}
{% endfor %}
{% assign categories = categories | sort %}

{% for category in categories %}
  <h2>{{ category }}</h2>
    
<!-- Collect classes within this category -->

  {% assign classes = "" | split: "" %}
  {% for r in reviews %}
    {% assign p = producers[r[1].stats.producer] %}
    {% if p and p.category == category and p.class %}
      {% unless classes contains p.class %}
        {% assign classes = classes | push: p.class %}
      {% endunless %}
    {% endif %}
  {% endfor %}
  {% assign classes = classes | sort %}

  {% for class in classes %}
    <h3>{{ class }}</h3>

    <--! Collect regions within this class -->
    {% assign regions = "" | split: "" %}
    {% for r in reviews %}
      {% assign p = producers[r[1].stats.producer] %}
      {% if p and p.category == category and p.class == class and p.region %}
        {% unless regions contains p.region %}
          {% assign regions = regions | push: p.region %}
        {% endunless %}
      {% endif %}
    {% endfor %}
    {% assign regions = regions | sort %}

    {% for region in regions %}
      <h4>{{ region }}</h4>
      <ul>

      {% for r in reviews %}
        {% assign review = r[1] %}
        {% assign p = producers[review.stats.producer] %}
        {% if p
              and p.category == category
              and p.class == class
              and p.region == region %}

          <li>
            {{ p.name }}
            {% if review.stats.age %}
              {{ review.stats.age }}yo
            {% else %}
              NAS
            {% endif %}
            — {{ review.stats.abv }}%
          </li>

        {% endif %}
      {% endfor %}

      </ul>
    {% endfor %}
  {% endfor %}
{% endfor %}
