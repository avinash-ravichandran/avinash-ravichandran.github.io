---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

<!-- Conference Papers -->
{% assign conference_papers = site.publications | where: "pub_type", "conference" | sort: "date" | reverse %}
{% if conference_papers.size > 0 %}
## Conference Papers
{% for post in conference_papers %}
  {% include archive-single.html %}
{% endfor %}
{% endif %}

<!-- Journal Papers -->
{% assign journal_papers = site.publications | where: "pub_type", "journal" | sort: "date" | reverse %}
{% if journal_papers.size > 0 %}
## Journal Papers
{% for post in journal_papers %}
  {% include archive-single.html %}
{% endfor %}
{% endif %}

<!-- Preprints -->
{% assign preprints = site.publications | where: "pub_type", "preprint" | sort: "date" | reverse %}
{% if preprints.size > 0 %}
## Preprints (arXiv)
{% for post in preprints %}
  {% include archive-single.html %}
{% endfor %}
{% endif %}

<!-- Patents -->
{% assign patents = site.publications | where: "pub_type", "patent" | sort: "date" | reverse %}
{% if patents.size > 0 %}
## Patents
{% for post in patents %}
  {% include archive-single.html %}
{% endfor %}
{% endif %}

