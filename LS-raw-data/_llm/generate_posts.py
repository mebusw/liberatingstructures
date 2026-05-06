#!/usr/bin/env python3
import json
import re
import os

def html_to_markdown(html):
    """Convert HTML to Markdown, including handling internal links as wikilinks."""
    if not html:
        return ""

    # First, handle link conversion BEFORE tag removal
    # Internal LS links have no dots in href, external URLs have dots
    def link_to_wikilink(match):
        href = match.group(1)
        text = strip_tags(match.group(2))
        if '.' in href:
            # External URL - use markdown autolink format
            return '<' + text + '>'
        return '[[' + text + ']]'

    # Handle links with and without target="_blank"
    html = re.sub(r'<a href="([^"]*)"[^>]*target="_blank"[^>]*>(.*?)</a>', link_to_wikilink, html, flags=re.DOTALL)
    html = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', link_to_wikilink, html, flags=re.DOTALL)

    # Strip unwanted tags but preserve content for these
    html = re.sub(r'<ul[^>]*>', '', html)
    html = re.sub(r'</ul>', '', html)
    html = re.sub(r'<ol[^>]*>', '', html)
    html = re.sub(r'</ol>', '', html)

    # Convert list items to markdown (handle nested tags in content)
    html = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: '- ' + strip_tags(m.group(1)) + '\n', html, flags=re.DOTALL)

    # Convert h3 headers - extract text content from any nested tags
    def convert_h3(match):
        content = match.group(1)
        # Strip all HTML tags from content but preserve text
        content = strip_tags(content).strip()
        if content:
            return '### ' + content + '\n'
        return ''
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', convert_h3, html, flags=re.DOTALL)

    # Convert divs with br to newlines
    html = re.sub(r'<div[^>]*><br[^>]*/?></div>', '\n', html)
    html = re.sub(r'<br[^>]*/?>', '\n', html)

    # Strip remaining tags we don't need (including melo-data and other complex tags)
    for tag in ['font', 'b', 'i', 'em', 'strong', 'span', 'p', 'div', 'h1', 'h2', 'h4', 'h5', 'h6', 'style', 'melo-data']:
        html = re.sub(r'<' + tag + r'[^>]*>', '', html)
        html = re.sub(r'</' + tag + r'>', '', html)
    # Strip self-closing tags
    html = re.sub(r'<([^>]+)/>', '', html)

    # Clean up HTML entities
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&quot;', '"')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')

    # Clean up excessive newlines
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html.strip()


def strip_tags(html):
    """Strip all HTML tags but preserve content."""
    if not html:
        return ""
    # Remove tags while preserving content
    html = re.sub(r'<[^>]+>', '', html)
    # Clean up
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&quot;', '"')
    return html.strip()

def process_entry(entry):
    """Process a single entry and return the markdown content."""
    zh = entry['content'][0]  # Chinese version
    en = entry['content'][1]  # English version

    title_cn = zh['title']
    title_en = en['title']
    summary = zh['summary']
    icon_url = entry['iconURL']
    sequence = entry['sequence']
    min_dur = entry['metadata'].get('minDuration', 0)
    max_dur = entry['metadata'].get('maxDuration', min_dur)

    # Extract tags
    tags = [t['text'] for t in zh['tags']]

    # Process sections
    what_html = zh['sections'][0]['content']
    how_html = zh['sections'][1]['content']
    why_html = zh['sections'][2]['content']

    what_md = html_to_markdown(what_html)
    how_md = html_to_markdown(how_html)
    why_md = html_to_markdown(why_html)

    # Build markdown
    md = f"""---
title: {title_cn}
tags:
    - liberating-structures
    - {tags[0] if tags else ''}
---
# {title_cn}
（英文: {title_en}）

![]({icon_url})

> {summary}

**编号**：第 {sequence} 号微结构

**时长**：{min_dur}-{max_dur} 分钟

## What
{what_md}

## How
{how_md}

## Why
{why_md}
"""
    return md, title_cn

def main():
    input_file = 'structures.entries.json'
    output_dir = '_posts'

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, entry in enumerate(data):
        md, title = process_entry(entry)
        # Sanitize filename
        filename = re.sub(r'[<>:"/\\|?*]', '-', title)
        filepath = os.path.join(output_dir, f'{filename}.md')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md)

        print(f"[{i+1}/{len(data)}] Generated: {filename}.md")

if __name__ == '__main__':
    main()
