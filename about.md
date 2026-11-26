---
layout: page
title: About
permalink: /about/
---

Backend developer with special interest in software design, architecture and system modelling. Trying to stay in a continuous learning mindset. I enjoy refactoring, clean code, the DDD philosophy and the TDD approach.

I write about two things. The first is software: architecture, distributed systems, observability, backend services in Go or Python. The second is learning: how talent develops, what deliberate practice can do, which books and philosophers changed my thinking.

## Elsewhere

{% for link in site.data.elsewhere %}
- [{{ link.name }}]({{ link.url }})
{%- endfor %}
