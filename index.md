---
title: "Splash Page"
layout: home
title: "DuckDrams - a whisky blog under reconstuction!"
author_profile: true
header:
  overlay_filter: "0.5"
  overlay_image: https://files.emilmallmin.com/duckdrams.png
  caption: "Photo text"
excerpt: "Bacon ipsum dolor sit amet salami ham hock ham, hamburger corned beef short ribs kielbasa biltong t-bone drumstick tri-tip tail sirloin pork chop."
intro: 
  - excerpt: 'Nullam suscipit et nam, tellus velit pellentesque at malesuada, enim eaque. Quis nulla, netus tempor in diam gravida tincidunt, *proin faucibus* voluptate felis id sollicitudin. Centered with `type="center"`'

feature_row:
  - image_path: https://files.emilmallmin.com/bar_from_afar.jpeg
    title: "Ghost Safari: Bar from afar" 
    url: /2025-11-16-ghost-safari-bar-from-afar/
  - image_path: https://files.emilmallmin.com/bar_from_afar.jpeg
    title: "Ghost Safari: Bar from afar" 
    url: /2025-11-16-ghost-safari-bar-from-afar/
  - image_path: https://files.emilmallmin.com/bar_from_afar.jpeg
    title: "Ghost Safari: Bar from afar" 
    url: /2025-11-16-ghost-safari-bar-from-afar/
---

{% include feature_row %}


This revamped version of my [old whisky blog](https://duckdrams.com) is currently under construction.

## Improvements
- Hosting set up: static GitHub Pages site with Cloudflare CDN, instead of Wordpress hosting
    - cost-free, add-free, easy to work offline, site can be generated locally
- Posts saved as markdown files: easy portability
- Underlying data structures for reviews, bottles, distillery info
    - allows automatic review index, statistics; bottle info easily scraped from whiskybase

## Todo
- ~~Review index page~~
- Other pages: categories pages, ~~post archive~~, contact, distillery list
- ~~Set up the Cloudflare CDN~~
- Enable some commenting feature (Commento?)
- Figure out how to do image gallery/tiles
- Some site styling
- Semi-manually copy over ~150 posts from the old blog...
- Transfer duckdrams.com domain (expires March)
