"""Add localized labelstock guidance to the existing guide and product pages."""

from html import escape

from design_update import replace_once
from editorial_copy import COPY


def link(url, label):
    return f'<a href="{escape(url)}">{escape(label)}</a>'


def questions_section(section_id, title, questions, action=''):
    items = ''.join(
        f'<details><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>'
        for question, answer in questions
    )
    return (
        f'<section class="questions procurement-questions" id="{section_id}">'
        f'<h2>{escape(title)}</h2>{items}{action}</section>'
    )


def add_editorial_guides(dist, groups, languages, canonical_path):
    reviewed = []
    for index, language in enumerate(languages):
        copy = COPY[language]

        def url(group):
            return canonical_path(groups[group][index])

        def insert(group, pattern, content):
            filename = groups[group][index]
            page = dist / filename
            html = page.read_text(encoding='utf-8')
            page.write_text(replace_once(pattern, lambda match: content + match[0], html), encoding='utf-8')
            reviewed.append(filename)

        label, construction, selection = copy['label']
        summary = (
            '<section class="record-callout" id="labelstock-basics">'
            f'<h2>{escape(label)}</h2><p>{escape(construction)}</p>'
            f'<p>{escape(selection)}</p></section>'
        )
        purchase = '<p class="section-intro">' + link(url('request') + '?mode=quote', copy['quote']) + '</p>'
        references = '<div class="toc">' + link(url('woodfree') + '#coat-weight', copy['trial']) + link(url('printing'), copy['printing']) + '</div>'
        technical = questions_section('industry-guides', copy['guide'], copy['topics'], references + purchase)
        guide_link = '<p class="section-intro">' + link(url('guide') + '#industry-guides', copy['guide']) + '</p>'
        insert('guide', r'<section id="adhesives">', summary)
        insert('guide', r'<p class="updated">', technical)
        insert('home', r'<section id="materials">', guide_link)

        pet_quote = '<p class="section-intro">' + link(url('request') + '?material=pet&mode=quote', copy['quote']) + '</p>'
        pet_faq = questions_section('pet-order-faq', copy['pet'], copy['questions'], pet_quote)
        insert('pet', r'<p class="updated">', pet_faq)

        question, answer = copy['thermal']
        thermal = (
            '<section class="record-callout" id="thermal-bpa">'
            f'<h2>{escape(question)}</h2><p>{escape(answer)}</p></section>'
        )
        insert('thermal', r'<p class="updated">', thermal)

    return set(reviewed)
