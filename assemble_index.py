"""Assembler script to build the complete, single-file offline index.html"""

import os
import sys

# Import components from builder
from builder.css import CSS_STYLES
from builder.ch1 import CH1_DATA
from builder.ch2 import CH2_DATA
from builder.ch3 import CH3_DATA
from builder.ch4 import CH4_DATA
from builder.ch5 import CH5_DATA
from builder.ch6 import CH6_DATA
from builder.ch7 import CH7_DATA
from builder.ch8 import CH8_DATA
from builder.ch9 import CH9_DATA
from builder.interactives import INTERACTIVES_HTML
from builder.exams_glossary import EXAMS_GLOSSARY_HTML
from builder.midterm_sample import MIDTERM_SAMPLE_HTML
from builder.network_quiz import NETWORK_QUIZ_HTML
from builder.app_js import APP_JS

import re

def replace_fractions(s):
    while '\\frac' in s:
        idx = s.find('\\frac')
        open1 = s.find('{', idx)
        if open1 == -1: break
        depth = 1
        pos1 = open1 + 1
        while pos1 < len(s) and depth > 0:
            if s[pos1] == '{': depth += 1
            elif s[pos1] == '}': depth -= 1
            pos1 += 1
        if depth != 0: break
        num = s[open1+1:pos1-1]

        open2 = s.find('{', pos1)
        if open2 == -1 or s[pos1:open2].strip() != '': break
        depth = 1
        pos2 = open2 + 1
        while pos2 < len(s) and depth > 0:
            if s[pos2] == '{': depth += 1
            elif s[pos2] == '}': depth -= 1
            pos2 += 1
        if depth != 0: break
        denom = s[open2+1:pos2-1]

        num = replace_fractions(num)
        denom = replace_fractions(denom)

        replacement = f'<span class="math-frac"><span class="math-num">{num}</span><span class="math-denom">{denom}</span></span>'
        s = s[:idx] + replacement + s[pos2:]
    return s

def clean_math_str(m):
    if not m:
        return ''
    s = m
    s = s.replace('\x07pprox', '&approx;').replace('\\approx', '&approx;')
    s = re.sub(r'(?<!&a)pprox', '&approx;', s)
    s = s.replace('\x07lpha', '&alpha;').replace('\\alpha', '&alpha;')
    s = s.replace('\x08eta', '&beta;').replace('\\beta', '&beta;')
    s = s.replace('\x0crac', '\\frac')

    # Strip \left and \right FIRST before \le
    s = re.sub(r'\\left\s*([(\[|])', r'\1', s)
    s = re.sub(r'\\right\s*([)\]|])', r'\1', s)
    s = s.replace(r'\left', '').replace(r'\right', '')
    s = s.replace(r'\max', 'max').replace(r'\min', 'min')

    s = s.replace('\\times', '&times;').replace('\\cdot', '&sdot;')
    s = s.replace('\\le', '&le;').replace('\\ge', '&ge;').replace('\\ne', '&ne;')
    s = s.replace('\\in', '&isin;').replace('\\notin', '&notin;')
    s = s.replace('\\infty', '&infin;')
    s = s.replace('\\implies', '&rArr;').replace('\\to', '&rarr;').replace('\\leftarrow', '&larr;')
    s = s.replace('\\equiv', '&equiv;').replace('\\oplus', '&oplus;')
    s = s.replace('\\mu', '&mu;').replace('\\sigma', '&sigma;').replace('\\lambda', '&lambda;')
    s = s.replace('\\Delta', '&Delta;').replace('\\delta', '&delta;')
    s = s.replace('\\sum', '&sum;').replace('\\prod', '&prod;').replace('\\lim', 'lim')
    s = re.sub(r'\\mathbf\{([^}]+)\}', r'<strong>\1</strong>', s)
    s = re.sub(r'\\mathbf\s+', '', s)
    s = re.sub(r'\\mathit\{([^}]+)\}', r'<em>\1</em>', s)
    s = re.sub(r'\\text\{([^}]+)\}', r'\1', s)
    s = re.sub(r'\\pmod\{([^}]+)\}', r'(mod \1)', s)
    s = s.replace('\\bmod', 'mod')
    s = re.sub(r'\\[,;]\s*', '&nbsp;', s)
    s = s.replace('\\quad', '&emsp;').replace('\\qquad', '&emsp;&emsp;').replace('\\ ', '&nbsp;')

    # Sqrt before fractions
    s = re.sub(r'\\sqrt\{([^{}]+)\}', r'&radic;<span style="text-decoration:overline">\1</span>', s)

    # Balanced fraction replacement
    s = replace_fractions(s)

    s = re.sub(r'\\binom\{([^{}]+)\}\{([^{}]+)\}', r'<span class="math-frac"><span class="math-num">\1</span><span class="math-denom">\2</span></span>', s)

    # Subscripts & Superscripts
    s = re.sub(r'_\{([^}]+)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'_([a-zA-Z0-9]+)', r'<sub>\1</sub>', s)
    s = re.sub(r'\^\{([^}]+)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'\^([a-zA-Z0-9]+)', r'<sup>\1</sup>', s)

    return s

def clean_math(text):
    if not text:
        return text

    # First clean $$...$$ blocks
    def replace_display(match):
        inner = clean_math_str(match.group(1))
        return f'<div class="math-display">{inner}</div>'
    text = re.sub(r'\$\$([\s\S]*?)\$\$', replace_display, text)

    # Next clean $...$ inline math (avoiding currency $100 or shell $HOME)
    def replace_inline(match):
        inner = clean_math_str(match.group(1))
        return f'<span class="math-inline">{inner}</span>'
    text = re.sub(r'(?<![\\\$])\$([^\$\n]+?)\$(?!\$)', replace_inline, text)

    # Clean existing math-display and math-inline inner contents
    def clean_existing_display(match):
        inner = clean_math_str(match.group(1))
        return f'<div class="math-display">{inner}</div>'
    text = re.sub(r'<div class="math-display">([\s\S]*?)</div>', clean_existing_display, text)

    def clean_existing_inline(match):
        inner = clean_math_str(match.group(1))
        return f'<span class="math-inline">{inner}</span>'
    text = re.sub(r'<span class="math-inline">([\s\S]*?)</span>', clean_existing_inline, text)

    # Universal cleanup of any stray \text{...} in headings, callouts, or prose
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)

    return text

CHAPTERS = [CH1_DATA, CH2_DATA, CH3_DATA, CH4_DATA, CH5_DATA, CH6_DATA, CH7_DATA, CH8_DATA, CH9_DATA]

def build_sidebar():
    sidebar_html = []
    sidebar_html.append('''
    <div class="sidebar-header-row">
      <div class="sidebar-title">All 9 Chapters</div>
      <button class="sidebar-close-mobile-btn" onclick="closeSidebar()" aria-label="Close Chapters Sidebar" title="Close">✕</button>
    </div>
    ''')

    for ch in CHAPTERS:
        badge_style = f"background-color: {ch['color']};"
        is_book_exclusive = ch['num'] in [7, 9] or "BOOK EXCLUSIVE" in ch.get('title', '')
        book_badge = '<span style="background:#ffedd5; color:#c2410c; font-size:0.65rem; font-weight:700; padding:0.1rem 0.35rem; border-radius:3px; margin-left:0.35rem; border:1px solid #fdba74;">Book Only</span>' if is_book_exclusive else ''
        display_title = ch['title'].replace(' [BOOK EXCLUSIVE]', '')
        sidebar_html.append(f'''
        <div class="ch-accordion">
          <div class="ch-header" onclick="toggleChapterAccordion(this)">
            <div class="ch-header-left">
              <span class="ch-badge" style="{badge_style}">Ch {ch['num']}</span>
              <span class="ch-title-text">{display_title}{book_badge}</span>
            </div>
            <span class="arrow-icon" style="transition:transform 0.2s ease;">▶</span>
          </div>
          <div class="sec-list">
        ''')
        for sec in ch['sections']:
            sidebar_html.append(f'''
            <a class="sec-item" data-sec="{sec['id']}" onclick="navigateTo('{sec['id']}')">
              <span>{sec['num']} {sec['title']}</span>
              <span class="check-dot"></span>
            </a>
            ''')
        sidebar_html.append('''
          </div>
        </div>
        ''')
    return "\n".join(sidebar_html)

def build_dashboard():
    cards = []
    for ch in CHAPTERS:
        sec_count = len(ch['sections'])
        is_book_exclusive = ch['num'] in [7, 9] or "BOOK EXCLUSIVE" in ch.get('title', '')
        book_badge = '<span style="background:#ffedd5; color:#9a3412; font-size:0.7rem; font-weight:700; padding:0.15rem 0.45rem; border-radius:4px; border:1px solid #fdba74;">⚠️ Book Exclusive</span>' if is_book_exclusive else ''
        display_title = ch['title'].replace(' [BOOK EXCLUSIVE]', '')
        cards.append(f'''
        <div class="interactive-card" style="margin:0; cursor:pointer;" onclick="navigateTo('{ch['sections'][0]['id']}')">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
            <div style="display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;">
              <span class="ch-badge" style="background:{ch['color']}; font-size:0.8rem; padding:0.25rem 0.6rem;">Chapter {ch['num']}</span>
              {book_badge}
            </div>
            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">{sec_count} Sections</span>
          </div>
          <h3 style="font-size:1.15rem; font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">{display_title}</h3>
          <p style="font-size:0.85rem; color:var(--text-secondary); line-height:1.5; margin-bottom:1rem;">{ch['subtitle']}</p>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem; font-weight:600; color:var(--primary-text);">
            <span>Start Chapter →</span>
            <span style="color:var(--text-muted); font-weight:400;">{ch['layer']}</span>
          </div>
        </div>
        ''')

    cards_grid = "\n".join(cards)

    return f'''
    <!-- DASHBOARD HOME VIEW -->
    <section id="dashboard-section" class="content-section active">
      <div style="background:linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%); color:white; border-radius:14px; padding:2rem 2.25rem; margin-bottom:2rem; box-shadow:var(--shadow-lg);">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.75rem;">
          <span style="background:rgba(255,255,255,0.2); font-size:0.75rem; font-weight:700; padding:0.2rem 0.6rem; border-radius:20px; text-transform:uppercase;">CPCS-371 Student Companion</span>
          <span style="font-size:0.85rem; opacity:0.9;">Unofficial Peer Study Resource &bull; King Abdulaziz University</span>
        </div>
        <h2 style="font-size:2.2rem; font-weight:800; line-height:1.2; margin-bottom:0.75rem;">Computer Networking: A Top-Down Approach</h2>
        <p style="font-size:1.05rem; opacity:0.95; max-width:760px; line-height:1.6; margin-bottom:1.5rem;">
          Interactive, visual digital textbook covering <strong>all 9 chapters</strong> based on Kurose & Ross (8th Edition) and semester lecture slides. Features bit-accurate calculators, step-by-step protocol simulators, inline SVG figures, and exam problem walkthroughs.
        </p>
        <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
          <button class="btn-primary" style="background:white; color:#1e40af; font-weight:700;" onclick="navigateTo('sample-midterm')">📝 Sample Midterm Exam (Ch 1–3) →</button>
          <button class="btn-secondary" style="background:rgba(255,255,255,0.25); color:white; border-color:rgba(255,255,255,0.4); font-weight:700;" onclick="navigateTo('quiz-net')">⚡ Upcoming Quiz 2: Network Layer →</button>
          <button class="btn-secondary" style="background:rgba(255,255,255,0.15); color:white; border-color:rgba(255,255,255,0.3);" onclick="navigateTo('ch1-1')">Begin Chapter 1 →</button>
          <button class="btn-secondary" style="background:rgba(255,255,255,0.15); color:white; border-color:rgba(255,255,255,0.3);" onclick="navigateTo('calculators')">18 Calculators Hub</button>
          <button class="btn-secondary" style="background:rgba(255,255,255,0.15); color:white; border-color:rgba(255,255,255,0.3);" onclick="navigateTo('exam')">50-Question Final Exam</button>
        </div>
      </div>

      <!-- ACTIVE EXAM PREP & TARGETED QUIZZES BANNER -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.25rem; margin-bottom:2rem;">
        <!-- Card 1: Sample Midterm Exam -->
        <div class="interactive-card" style="border-top:4px solid #2563eb; cursor:pointer;" onclick="navigateTo('sample-midterm')">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span class="interactive-badge" style="background:#eff6ff; color:#1d4ed8; font-weight:700;">Chapters 1, 2 &amp; 3</span>
            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">21 Exam Problems</span>
          </div>
          <h3 style="font-size:1.25rem; font-weight:800; color:var(--text-primary); margin-bottom:0.5rem;">📝 Sample Midterm Exam</h3>
          <p style="font-size:0.875rem; color:var(--text-secondary); line-height:1.6; margin-bottom:1rem;">
            Practice with 21 high-yield questions (10 MCQs and 11 Written Problems) covering Chapters 1–3. Includes complete step-by-step collapsible solutions, calculation tables, and clear tags for slide references and student-reported book topics.
          </p>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; font-weight:700; color:var(--primary-text);">
            <span>Open Sample Midterm &rarr;</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#047857; padding:2px 8px; border-radius:4px;">100% Solved</span>
          </div>
        </div>

        <!-- Card 2: Upcoming Network Layer Quiz -->
        <div class="interactive-card" style="border-top:4px solid #10b981; cursor:pointer;" onclick="navigateTo('quiz-net')">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span class="interactive-badge" style="background:#ecfdf5; color:#047857; font-weight:700;">Chapters 4 &amp; 5 Focus</span>
            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">10 Target Questions</span>
          </div>
          <h3 style="font-size:1.25rem; font-weight:800; color:var(--text-primary); margin-bottom:0.5rem;">⚡ Upcoming Quiz 2: Network Layer</h3>
          <p style="font-size:0.875rem; color:var(--text-secondary); line-height:1.6; margin-bottom:1rem;">
            Master the 10 specific exam focus topics: Forwarding vs. Routing, Best-Effort Service, Longest Prefix Matching, Subnet Masks, DHCP DORA, IPv4/IPv6 Tunneling, SDN Control Plane, Link-State Dijkstra, Bellman-Ford Distance Vector, and RIP vs. OSPF.
          </p>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; font-weight:700; color:#047857;">
            <span>Start 10-Question Quiz &rarr;</span>
            <span style="font-size:0.75rem; background:#eff6ff; color:#1d4ed8; padding:2px 8px; border-radius:4px;">Interactive Scoring</span>
          </div>
        </div>
      </div>

      <!-- 5-Layer Stack Visual -->
      <div class="interactive-card" style="margin-bottom:2rem;">
        <div class="interactive-header">
          <div class="interactive-title">🥞 The 5-Layer Internet Protocol Stack Map</div>
          <span class="interactive-badge">Top-Down Architecture</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:0.4rem;">
          <div style="padding:0.75rem 1.25rem; border-radius:6px; background:#f5f3ff; border-left:5px solid #8b5cf6; display:flex; justify-content:space-between; align-items:center;">
            <div><strong style="color:#6d28d9;">Layer 5: Application Layer</strong> (HTTP, SMTP, DNS, P2P) — Message</div>
            <button class="btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="navigateTo('ch2-1')">Taught in Chapter 2 →</button>
          </div>
          <div style="padding:0.75rem 1.25rem; border-radius:6px; background:#eff6ff; border-left:5px solid #2563eb; display:flex; justify-content:space-between; align-items:center;">
            <div><strong style="color:#1d4ed8;">Layer 4: Transport Layer</strong> (TCP, UDP, Congestion Control) — Segment</div>
            <button class="btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="navigateTo('ch3-1')">Taught in Chapter 3 →</button>
          </div>
          <div style="padding:0.75rem 1.25rem; border-radius:6px; background:#ecfdf5; border-left:5px solid #10b981; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
            <div><strong style="color:#047857;">Layer 3: Network Layer</strong> (Data Plane &amp; Control Plane, IPv4/IPv6, Dijkstra, Bellman-Ford, OSPF) — Datagram</div>
            <button class="btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="navigateTo('ch4-1')">Taught in Chapter 4 →</button>
          </div>
          <div style="padding:0.75rem 1.25rem; border-radius:6px; background:#fffbeb; border-left:5px solid #f59e0b; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
            <div><strong style="color:#b45309;">Layer 2: Link Layer &amp; LANs</strong> (Ethernet, Switches, ARP, MAC, CRC, ALOHA) — Frame</div>
            <button class="btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="navigateTo('ch5-1')">Taught in Chapter 5 →</button>
          </div>
          <div style="padding:0.75rem 1.25rem; border-radius:6px; background:#faf5ff; border-left:5px solid #a855f7; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
            <div><strong style="color:#7e22ce;">Wireless &amp; Mobile Networks</strong> (802.11 WiFi, CDMA, Cellular 4G/5G, Mobile IP) — Radio/Mobility</div>
            <button class="btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="navigateTo('ch6-1')">Taught in Chapter 6 →</button>
          </div>
          <div style="padding:0.75rem 1.25rem; border-radius:6px; background:#fef2f2; border-left:5px solid #ef4444; display:flex; justify-content:space-between; align-items:center;">
            <div><strong style="color:#b91c1c;">Layer 1: Physical Layer</strong> (Copper, Fiber, Radio) — Bits</div>
            <button class="btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="navigateTo('ch1-2')">Taught in Chapter 1 →</button>
          </div>
        </div>
      </div>

      <!-- 9 Chapters Grid -->
      <h3 style="font-size:1.35rem; font-weight:800; margin-bottom:1rem; color:var(--text-primary);">Course Chapters Directory</h3>
      <div class="grid-3" style="gap:1rem; margin-bottom:2rem;">
        {cards_grid}
      </div>

      <!-- UNOFFICIAL EDUCATIONAL DISCLAIMER -->
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-left:4px solid var(--primary); border-radius:8px; padding:1rem 1.25rem; margin-top:2.5rem; font-size:0.82rem; color:var(--text-muted); line-height:1.6;">
        <strong>💡 Disclaimer & Educational Fair-Use Notice:</strong> This interactive visual textbook is an independent, <strong>unofficial student-created study companion</strong> developed strictly for peer education, revision, and exam preparation in CPCS-371 (Computer Networks). It is not affiliated with, endorsed by, or an official publication of King Abdulaziz University (KAU) or Pearson Education. All theoretical concepts, terminology, equations, and exercises reference <em>Computer Networking: A Top-Down Approach</em> (6th/8th Edition) by Kurose & Ross.
      </div>
    </section>

    '''

def build_chapter_sections():
    sections_html = []
    all_secs = []
    for ch in CHAPTERS:
        for s in ch['sections']:
            all_secs.append((ch, s))

    for idx, (ch, sec) in enumerate(all_secs):
        prev_sec = all_secs[idx - 1][1] if idx > 0 else None
        next_sec = all_secs[idx + 1][1] if idx < len(all_secs) - 1 else None

        # Build quiz HTML
        quiz_items = []
        if 'quiz' in sec and sec['quiz']:
            for q_idx, q in enumerate(sec['quiz']):
                opts_html = []
                for o_idx, opt in enumerate(q['opts']):
                    is_correct = (o_idx == q['ans'])
                    opts_html.append(f'''
                    <div class="quiz-opt" data-correct="{str(is_correct).lower()}" onclick="selectQuizOption(this, {str(is_correct).lower()}, '{q['exp'].replace("'", "\\'")}')">
                      <span>{chr(65 + o_idx)}.</span> {opt}
                    </div>
                    ''')
                opts_str = "\n".join(opts_html)
                quiz_items.append(f'''
                <div class="quiz-box">
                  <div class="quiz-header">
                    <span style="font-weight:700; color:var(--primary);">Self-Check Question {q_idx + 1}</span>
                    <span style="font-size:0.75rem; color:var(--text-muted);">§{sec['num']} Concept Review</span>
                  </div>
                  <div class="quiz-question">{q['q']}</div>
                  <div class="quiz-options">
                    {opts_str}
                  </div>
                  <div class="quiz-feedback"></div>
                </div>
                ''')
        quizzes_str = "\n".join(quiz_items)

        # Build Nav footer
        prev_btn = f'''<button class="btn-secondary" onclick="navigateTo('{prev_sec['id']}')">← Previous: §{prev_sec['num']} {prev_sec['title']}</button>''' if prev_sec else '<div></div>'
        next_btn = f'''<button class="btn-primary" onclick="navigateTo('{next_sec['id']}')">Next: §{next_sec['num']} {next_sec['title']} →</button>''' if next_sec else '<div></div>'

        subheading_html = f'<p class="sec-subheading">{sec["subtitle"]}</p>' if sec.get('subtitle') else ''
        sections_html.append(f'''
        <section id="{sec['id']}-section" class="content-section">
          <div class="breadcrumb">Chapter {ch['num']}: {ch['title']} &bull; Section {sec['num']}</div>
          <h2 class="sec-heading">§{sec['num']} {sec['title']}</h2>
          {subheading_html}
          
          <div class="sec-body-content">
            {clean_math(sec['content'])}
          </div>

          <!-- Section Mini-Quizzes -->
          {quizzes_str}

          <!-- Footer Navigation -->
          <div class="section-nav-footer">
            {prev_btn}
            {next_btn}
          </div>
        </section>
        ''')

    return "\n".join(sections_html)

def assemble_all():
    sidebar_content = build_sidebar()
    dashboard_content = build_dashboard()
    chapters_content = build_chapter_sections()

    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CPCS-371 Computer Networks — Interactive Visual Textbook (Kurose & Ross 8th Edition & Lecture Slides)</title>
  <style>
{CSS_STYLES}
  </style>
</head>
<body>

  <!-- TOP HEADER -->
  <header class="app-header">
    <div class="header-left">
      <!-- Mobile / iPad Sidebar Hamburger Toggle -->
      <button id="sidebar-toggle-btn" class="icon-btn sidebar-toggle-btn" onclick="toggleSidebar()" title="Toggle Chapters Sidebar" aria-label="Toggle Navigation Sidebar">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
          <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
        </svg>
      </button>

      <!-- Logo Group -->
      <div class="logo-group" onclick="navigateTo('dashboard')">
        <div class="logo-badge">CPCS 371</div>
        <div class="logo-text">
          <h1>Computer Networks</h1>
          <p>Kurose &amp; Ross 6th Ed. &bull; Unofficial Student Companion</p>
        </div>
      </div>
    </div>

    <!-- Expandable Search Dot & Bar ("Dot then Expand, Pushing Everything") -->
    <div id="search-container" class="search-container" onclick="handleSearchContainerClick(event)">
      <button id="search-dot-trigger" class="search-dot-btn" onclick="openSearch(event)" title="Search lessons (click to expand)" aria-label="Search lessons">
        <svg class="search-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
      </button>
      <input type="text" id="global-search-input" class="search-input" placeholder="Search TCP, ALOHA, DNS, BGP..." oninput="handleGlobalSearch()" onfocus="handleGlobalSearch()" autocomplete="off" aria-label="Search lessons">
      <button id="search-close-btn" class="search-close-btn" onclick="closeSearch(event)" title="Close search" aria-label="Close search">✕</button>
      <div id="search-results-dropdown" class="search-dropdown"></div>
    </div>

    <!-- Right Header Navigation (Horizontally Scrollable) -->
    <nav class="header-nav" id="header-nav" aria-label="Main Navigation">
      <span id="overall-progress-pct" class="interactive-badge" style="margin-right:0.2rem;">0% Mastered</span>
      <button class="nav-btn" data-route="dashboard" onclick="navigateTo('dashboard')">🏠 Home</button>
      <button class="nav-btn" data-route="sample-midterm" onclick="navigateTo('sample-midterm')">📝 Sample Midterm</button>
      <button class="nav-btn" data-route="quiz-net" onclick="navigateTo('quiz-net')">⚡ Quiz 2 (Net Layer)</button>
      <button class="nav-btn" data-route="dissector" onclick="navigateTo('dissector')">🔍 HTTP Dissector</button>
      <button class="nav-btn" data-route="calculators" onclick="navigateTo('calculators')">🧮 Calculators</button>
      <button class="nav-btn" data-route="simulators" onclick="navigateTo('simulators')">⚡ Simulators</button>
      <button class="nav-btn" data-route="formulas" onclick="navigateTo('formulas')">📐 Formulas</button>
      <button class="nav-btn" data-route="glossary" onclick="navigateTo('glossary')">📖 Glossary</button>
      <button class="nav-btn" data-route="flashcards" onclick="navigateTo('flashcards')">🃏 Flashcards</button>
      <button class="nav-btn" data-route="exam" onclick="navigateTo('exam')">🎯 Exam</button>
      <button class="nav-btn" data-route="checklist" onclick="navigateTo('checklist')">✅ Checklist</button>
    </nav>

    <!-- Pinned Header Actions -->
    <div class="header-actions">
      <button class="icon-btn theme-toggle-btn" onclick="toggleTheme()" title="Toggle Dark/Light Mode" aria-label="Toggle Theme">🌓</button>
    </div>
  </header>

  <!-- Sidebar Backdrop for Mobile/iPad -->
  <div id="sidebar-backdrop" class="sidebar-backdrop" onclick="closeSidebar()"></div>

  <!-- MAIN APP CONTAINER -->
  <div class="app-container">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
      {sidebar_content}
    </aside>

    <!-- MAIN READING & INTERACTIVE CONTENT -->
    <main class="main-content">
      {dashboard_content}
      {clean_math(MIDTERM_SAMPLE_HTML)}
      {clean_math(NETWORK_QUIZ_HTML)}
      {chapters_content}
      {clean_math(INTERACTIVES_HTML)}
      {clean_math(EXAMS_GLOSSARY_HTML)}
    </main>
  </div>

  <!-- SCRIPT LOGIC -->
  <script>
{APP_JS}
  </script>
</body>
</html>'''

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Successfully generated {output_path} ({len(full_html)} characters, {full_html.count(chr(10))} lines).")

if __name__ == "__main__":
    assemble_all()
