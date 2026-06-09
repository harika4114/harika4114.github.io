---
layout: home
title: Vidya Margam Blog
---

Welcome to the Vidya Margam blog, where we document the journey of building an AI-powered educational platform that makes learning accessible across language barriers.

## Latest Posts

{% for post in site.posts %}
  ### [{{ post.title }}]({{ post.url }})
  *{{ post.date | date: "%B %d, %Y" }}*
  
  {{ post.excerpt }}

{% endfor %}

## About This Project

Vidya Margam combines cutting-edge AI technologies with educational accessibility to create an intelligent learning companion that understands your language and helps you learn better.

[View the source code →](https://github.com/yourusername/vidya-margam)
