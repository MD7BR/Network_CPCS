"""Formulas Sheet, Glossary, Flashcards, and Final Comprehensive Exam"""

EXAMS_GLOSSARY_HTML = """
<!-- ========================================== -->
<!-- FORMULA SHEET (PRINTABLE)                  -->
<!-- ========================================== -->
<section id="formulas-section" class="content-section">
  <div class="breadcrumb">Reference &bull; Formula Sheet (Printable)</div>
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
    <div>
      <h2 class="sec-heading">Networking Complete Formula Sheet</h2>
      <p class="sec-subheading">Comprehensive reference of every equation, algorithm, and worked rule from Chapters 1 to 9.</p>
    </div>
    <button class="btn-secondary" onclick="window.print()">🖨️ Print Formula Sheet</button>
  </div>

  <div class="interactive-card">
    <h3 style="color:var(--primary-text); margin-bottom:0.75rem;">Chapter 1: Network Core & Performance</h3>
    <table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700; width:30%;">Total Nodal Delay</td><td style="padding:6px; font-family:monospace;">d_nodal = d_proc + d_queue + d_trans + d_prop</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Transmission Delay</td><td style="padding:6px; font-family:monospace;">d_trans = L / R (L in bits, R in bps)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Propagation Delay</td><td style="padding:6px; font-family:monospace;">d_prop = d / s (d in meters, s ≈ 2×10^8 m/s)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Traffic Intensity</td><td style="padding:6px; font-family:monospace;">I = (L · a) / R (Loss occurs when I > 1)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Bandwidth-Delay Product</td><td style="padding:6px; font-family:monospace;">BDP = R × d_prop (Volume of the link in bits)</td></tr>
      <tr><td style="padding:6px; font-weight:700;">Pipelined Store-and-Forward</td><td style="padding:6px; font-family:monospace;">Total Delay = (N + P - 1) × (L / R) (P packets, N links)</td></tr>
    </table>
  </div>

  <div class="interactive-card" style="margin-top:1.5rem;">
    <h3 style="color:var(--purple-text); margin-bottom:0.75rem;">Chapter 2: Application Layer</h3>
    <table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700; width:30%;">Non-Persistent HTTP Time</td><td style="padding:6px; font-family:monospace;">2 RTT + Transmission Time per object</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Persistent Pipelined HTTP</td><td style="padding:6px; font-family:monospace;">1 RTT for handshake + 1 RTT total for all referenced objects</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Web Cache Average Delay</td><td style="padding:6px; font-family:monospace;">T_avg = (h × D_LAN) + ((1 - h) × D_Internet) (h = hit ratio)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Client-Server File Distribution</td><td style="padding:6px; font-family:monospace;">D_CS ≥ max( N·F / u_s , F / d_min )</td></tr>
      <tr><td style="padding:6px; font-weight:700;">P2P File Distribution</td><td style="padding:6px; font-family:monospace;">D_P2P ≥ max( F / u_s , F / d_min , N·F / (u_s + Σ u_i) )</td></tr>
    </table>
  </div>

  <div class="interactive-card" style="margin-top:1.5rem;">
    <h3 style="color:var(--primary-text); margin-bottom:0.75rem;">Chapter 3: Transport Layer</h3>
    <table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700; width:30%;">Stop-and-Wait Utilization</td><td style="padding:6px; font-family:monospace;">U_sender = (L / R) / (RTT + L / R)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Pipelined Utilization (Window N)</td><td style="padding:6px; font-family:monospace;">U_sender = [ N × (L / R) ] / (RTT + L / R)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Selective Repeat Window Rule</td><td style="padding:6px; font-family:monospace;">Window Size W ≤ 2^(k - 1) (where k = sequence number bits)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">TCP EstimatedRTT (EWMA)</td><td style="padding:6px; font-family:monospace;">EstimatedRTT = (1 - α)·EstimatedRTT + α·SampleRTT (α = 0.125)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">TCP DevRTT (Variance)</td><td style="padding:6px; font-family:monospace;">DevRTT = (1 - β)·DevRTT + β·|SampleRTT - EstimatedRTT| (β = 0.25)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">TCP TimeoutInterval</td><td style="padding:6px; font-family:monospace;">TimeoutInterval = EstimatedRTT + 4 × DevRTT</td></tr>
      <tr><td style="padding:6px; font-weight:700;">TCP Steady-State Throughput</td><td style="padding:6px; font-family:monospace;">Throughput ≈ (1.22 × MSS) / (RTT × √L) (L = loss rate)</td></tr>
    </table>
  </div>

  <div class="interactive-card" style="margin-top:1.5rem;">
    <h3 style="color:var(--accent-text); margin-bottom:0.75rem;">Chapters 4 & 5: Network & Link Layers</h3>
    <table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700; width:30%;">IPv4 Usable Hosts (/x)</td><td style="padding:6px; font-family:monospace;">Usable Hosts = 2^(32 - x) - 2</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">IPv4 Fragment Offset</td><td style="padding:6px; font-family:monospace;">Offset = (Byte Offset in original data) / 8</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Bellman-Ford DV Equation</td><td style="padding:6px; font-family:monospace;">d_x(y) = min_v { c(x,v) + d_v(y) }</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Slotted ALOHA Max Efficiency</td><td style="padding:6px; font-family:monospace;">1 / e ≈ 0.368 (36.8%)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Pure ALOHA Max Efficiency</td><td style="padding:6px; font-family:monospace;">1 / (2e) ≈ 0.184 (18.4%)</td></tr>
      <tr><td style="padding:6px; font-weight:700;">CSMA/CD Backoff Delay</td><td style="padding:6px; font-family:monospace;">Wait K × 512 bit times (where K ∈ {0, 1, ..., 2^n - 1})</td></tr>
    </table>
  </div>

  <div class="interactive-card" style="margin-top:1.5rem;">
    <h3 style="color:var(--danger-text); margin-bottom:0.75rem;">Chapters 6, 7 & 8: Wireless, Multimedia & Security</h3>
    <table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700; width:30%;">CDMA Inner Product Decoding</td><td style="padding:6px; font-family:monospace;">d_i = (1 / M) × (Z · C_i)</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Token Bucket Max Burst</td><td style="padding:6px; font-family:monospace;">Max Bits in Time t = b + r · t</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">Weighted Fair Queuing Rate</td><td style="padding:6px; font-family:monospace;">Guaranteed Rate = R × [ w_i / Σ w_j ]</td></tr>
      <tr style="border-bottom:1px solid var(--border);"><td style="padding:6px; font-weight:700;">RSA Modulus & Totient</td><td style="padding:6px; font-family:monospace;">n = p · q , z = (p - 1)(q - 1)</td></tr>
      <tr><td style="padding:6px; font-weight:700;">RSA Encrypt / Decrypt</td><td style="padding:6px; font-family:monospace;">c = m^e mod n , m = c^d mod n</td></tr>
    </table>
  </div>
</section>

<!-- ========================================== -->
<!-- GLOSSARY SECTION                           -->
<!-- ========================================== -->
<section id="glossary-section" class="content-section">
  <div class="breadcrumb">Reference &bull; Networking Terms Glossary</div>
  <h2 class="sec-heading">A-Z Networking Glossary</h2>
  <p class="sec-subheading">Authoritative definitions extracted directly from Kurose & Ross 6th Edition.</p>

  <div style="margin-bottom:1.5rem;">
    <input type="text" id="glossary-filter" class="search-input" placeholder="Type to filter glossary terms..." onkeyup="filterGlossary()">
  </div>

  <div id="glossary-list" class="grid-2">
    <!-- Items generated dynamically or static fallback -->
  </div>
</section>

<!-- ========================================== -->
<!-- FLASHCARDS SECTION                         -->
<!-- ========================================== -->
<section id="flashcards-section" class="content-section">
  <div class="breadcrumb">Study Tools &bull; Interactive Flashcards</div>
  <h2 class="sec-heading">Mastery Flashcard Deck</h2>
  <p class="sec-subheading">Active recall cards covering all 9 chapters. Click card to flip; spacebar or arrows to navigate.</p>

  <div style="display:flex; justify-content:center; gap:0.5rem; margin-bottom:1rem; flex-wrap:wrap;">
    <button class="nav-btn active" onclick="filterFlashcards('all', this)">All Chapters</button>
    <button class="nav-btn" onclick="filterFlashcards('ch1', this)">Ch 1</button>
    <button class="nav-btn" onclick="filterFlashcards('ch2', this)">Ch 2</button>
    <button class="nav-btn" onclick="filterFlashcards('ch3', this)">Ch 3</button>
    <button class="nav-btn" onclick="filterFlashcards('ch4', this)">Ch 4</button>
    <button class="nav-btn" onclick="filterFlashcards('ch5', this)">Ch 5</button>
    <button class="nav-btn" onclick="filterFlashcards('ch6', this)">Ch 6</button>
    <button class="nav-btn" onclick="filterFlashcards('ch7', this)">Ch 7</button>
    <button class="nav-btn" onclick="filterFlashcards('ch8', this)">Ch 8</button>
    <button class="nav-btn" onclick="filterFlashcards('ch9', this)">Ch 9</button>
  </div>

  <div class="flip-card" onclick="flipActiveCard()">
    <div id="active-flashcard-inner" class="flip-card-inner">
      <div class="flip-card-front">
        <span id="fc-category" class="interactive-badge" style="margin-bottom:1rem;">Chapter 1</span>
        <h3 id="fc-front-text" style="font-size:1.35rem; font-weight:700;">Store-and-Forward Transmission</h3>
        <p style="font-size:0.75rem; color:var(--text-muted); margin-top:1.5rem;">(Click to reveal definition)</p>
      </div>
      <div class="flip-card-back">
        <h4 style="font-size:1rem; font-weight:700; margin-bottom:0.75rem; color:var(--primary-text);">Definition & Rule:</h4>
        <p id="fc-back-text" style="font-size:0.95rem; line-height:1.6;">
          The switch must receive the entire packet before it can begin to transmit the first bit of the packet onto the outbound link.
        </p>
      </div>
    </div>
  </div>

  <div style="display:flex; justify-content:center; align-items:center; gap:1rem; margin-top:1rem;">
    <button class="btn-secondary" onclick="prevFlashcard()">← Previous</button>
    <span id="fc-progress" style="font-size:0.875rem; font-weight:600; color:var(--text-secondary);">1 / 50</span>
    <button class="btn-primary" onclick="nextFlashcard()">Next →</button>
  </div>
</section>

<!-- ========================================== -->
<!-- COMPREHENSIVE FINAL EXAM                   -->
<!-- ========================================== -->
<section id="exam-section" class="content-section">
  <div class="breadcrumb">Assessment &bull; Comprehensive Final Exam</div>
  <h2 class="sec-heading">CPCS-371 Comprehensive Final Exam</h2>
  <p class="sec-subheading">50 randomized, timed multiple-choice and scenario questions across all 9 chapters.</p>

  <div id="exam-welcome-card" class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">🎯 Exam Instructions & Settings</div>
    </div>
    <ul style="margin:1rem 0 1.5rem 1.5rem; font-size:0.9rem; line-height:1.7;">
      <li>50 Questions covering all network layers (Ch 1 to Ch 9).</li>
      <li>Instant grading, time tracking, and section review citations.</li>
      <li>Built according to the instructor's exam philosophy: <em>understand, don't just memorize!</em></li>
    </ul>
    <button class="btn-primary" onclick="startFinalExam()">Start Final Exam Now</button>
  </div>

  <div id="exam-active-card" class="interactive-card" style="display:none;">
    <div class="interactive-header">
      <div class="interactive-title" id="exam-q-title">Question 1 of 50</div>
      <span id="exam-timer" class="interactive-badge" style="background:#fef2f2; color:#b91c1c;">⏱ 60:00</span>
    </div>
    <p id="exam-q-text" style="font-size:1.05rem; font-weight:600; margin:1rem 0;"></p>
    <div id="exam-q-options" class="quiz-options"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.5rem;">
      <button class="btn-secondary" onclick="prevExamQuestion()">← Previous</button>
      <button id="exam-submit-btn" class="btn-primary" onclick="nextExamQuestion()">Next Question →</button>
    </div>
  </div>

  <div id="exam-results-card" class="interactive-card" style="display:none;">
    <div class="interactive-header">
      <div class="interactive-title">📊 Final Exam Results</div>
    </div>
    <div id="exam-score-display" style="text-align:center; padding:1.5rem 0;">
      <div id="exam-score-circle" style="font-size:3rem; font-weight:800; color:var(--primary);">0%</div>
      <p id="exam-score-msg" style="font-size:1.1rem; font-weight:600; margin-top:0.5rem;"></p>
    </div>
    <div id="exam-review-list" style="margin-top:1.5rem;"></div>
  </div>
</section>

<!-- ========================================== -->
<!-- STUDY GUIDE CHECKLIST SECTION              -->
<!-- ========================================== -->
<section id="checklist-section" class="content-section">
  <div class="breadcrumb">Study Guide &bull; 'I Can...' Objectives Checklist</div>
  <h2 class="sec-heading">'I Can...' Mastery Checklist</h2>
  <p class="sec-subheading">Aligned with the KAU CPCS-371 Midterm Study Guide (Ch 1–3) and derived full-course objectives (Ch 4–9). Ticks are saved to your browser.</p>

  <div id="checklist-container" class="interactive-card">
    <!-- Populated by JavaScript -->
  </div>
</section>
"""
