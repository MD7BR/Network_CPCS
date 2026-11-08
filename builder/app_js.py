"""Client-side JavaScript Application Code (Vanilla ES6+)"""

APP_JS = r"""
// ==========================================
// CORE STATE & LOCALSTORAGE
// ==========================================
let currentRoute = 'dashboard';
let completedSections = new Set(JSON.parse(localStorage.getItem('cpcs371_completed_sections') || '[]'));
let completedChecklist = new Set(JSON.parse(localStorage.getItem('cpcs371_checklist') || '[]'));
let activeFlashcardIdx = 0;
let filteredFlashcards = [];
let examState = {
  active: false,
  qIndex: 0,
  userAnswers: {},
  timeRemaining: 3600,
  timerInterval: null
};

// ==========================================
// THEME MANAGEMENT
// ==========================================
function initTheme() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (saved === 'dark' || (!saved && prefersDark)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// ==========================================
// ROUTER & NAVIGATION
// ==========================================
function navigateTo(route) {
  window.location.hash = route;
}

function handleRoute() {
  const hash = window.location.hash.replace('#', '') || 'dashboard';
  currentRoute = hash;

  // Hide all sections
  document.querySelectorAll('.content-section').forEach(el => el.classList.remove('active'));

  // Update header nav buttons
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const activeNavBtn = document.querySelector(`.nav-btn[data-route="${hash}"]`);
  if (activeNavBtn) activeNavBtn.classList.add('active');

  // Deactivate sidebar items
  document.querySelectorAll('.sec-item').forEach(el => el.classList.remove('active'));

  if (hash === 'dashboard') {
    const dash = document.getElementById('dashboard-section');
    if (dash) dash.classList.add('active');
  } else if (hash === 'dissector') {
    const diss = document.getElementById('dissector-section');
    if (diss) diss.classList.add('active');
  } else if (hash === 'calculators') {
    const calc = document.getElementById('calculators-section');
    if (calc) calc.classList.add('active');
  } else if (hash === 'simulators') {
    const sim = document.getElementById('simulators-section');
    if (sim) sim.classList.add('active');
  } else if (hash === 'formulas') {
    const form = document.getElementById('formulas-section');
    if (form) form.classList.add('active');
  } else if (hash === 'glossary') {
    const gloss = document.getElementById('glossary-section');
    if (gloss) gloss.classList.add('active');
  } else if (hash === 'flashcards') {
    const fc = document.getElementById('flashcards-section');
    if (fc) fc.classList.add('active');
  } else if (hash === 'exam') {
    const exam = document.getElementById('exam-section');
    if (exam) exam.classList.add('active');
  } else if (hash === 'checklist') {
    const chk = document.getElementById('checklist-section');
    if (chk) chk.classList.add('active');
  } else {
    // Standard section like ch1-1
    const secEl = document.getElementById(hash + '-section');
    if (secEl) {
      secEl.classList.add('active');
      // Highlight sidebar
      const sideItem = document.querySelector(`.sec-item[data-sec="${hash}"]`);
      if (sideItem) {
        sideItem.classList.add('active');
        const parentAcc = sideItem.closest('.ch-accordion');
        if (parentAcc) parentAcc.classList.add('open');
      }
    } else {
      // Fallback
      const dash = document.getElementById('dashboard-section');
      if (dash) dash.classList.add('active');
    }
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
  updateProgressUI();
  if (typeof initSectionInteractives === 'function') initSectionInteractives();
}

window.addEventListener('hashchange', handleRoute);

// Toggle Sidebar Accordion
function toggleChapterAccordion(header) {
  const acc = header.closest('.ch-accordion');
  acc.classList.toggle('open');
}

// Toggle Solution Box
function toggleSolution(id) {
  const el = document.getElementById(id);
  if (el) {
    el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
  }
}

// ==========================================
// QUIZ ENGINE
// ==========================================
function selectQuizOption(btn, isCorrect, expText) {
  const parent = btn.closest('.quiz-box');
  const allOpts = parent.querySelectorAll('.quiz-opt');
  allOpts.forEach(o => {
    o.style.pointerEvents = 'none';
    if (o.dataset.correct === 'true') o.classList.add('correct');
  });

  if (isCorrect) {
    btn.classList.add('correct');
  } else {
    btn.classList.add('wrong');
  }

  const feedback = parent.querySelector('.quiz-feedback');
  if (feedback) {
    feedback.innerHTML = `<strong>${isCorrect ? '✅ Correct!' : '❌ Incorrect.'}</strong> ${expText}`;
    feedback.style.background = isCorrect ? 'var(--accent-light)' : 'var(--danger-light)';
    feedback.style.color = isCorrect ? 'var(--accent-text)' : 'var(--danger-text)';
    feedback.classList.add('show');
  }

  // Mark section as completed if all quizzes in section answered
  const sectionEl = btn.closest('.content-section');
  if (sectionEl) {
    const secId = sectionEl.id.replace('-section', '');
    completedSections.add(secId);
    localStorage.setItem('cpcs371_completed_sections', JSON.stringify(Array.from(completedSections)));
    updateProgressUI();
  }
}

function updateProgressUI() {
  const totalSections = document.querySelectorAll('.sec-item').length || 45;
  const doneCount = completedSections.size;
  const pct = Math.min(100, Math.round((doneCount / totalSections) * 100));

  const pctBadge = document.getElementById('overall-progress-pct');
  if (pctBadge) pctBadge.innerText = `${pct}% Mastered`;

  // Update checkmarks in sidebar
  document.querySelectorAll('.sec-item').forEach(item => {
    const sec = item.dataset.sec;
    if (completedSections.has(sec)) {
      item.classList.add('completed');
    }
  });
}

// ==========================================
// HTTP MESSAGE DISSECTOR DETAILS
// ==========================================
const DISSECTOR_DATA = {
  'req-line': {
    title: 'HTTP Request Line: GET /somedir/page.html HTTP/1.1',
    desc: 'The request line has three fields: (1) Method: GET (fetches an object; others are POST, HEAD, PUT, DELETE); (2) URL Path: /somedir/page.html (path of the requested resource on server); (3) Protocol Version: HTTP/1.1 (the client speaks HTTP version 1.1). Exam Note: HTTP is case-sensitive for methods and paths.'
  },
  'req-host': {
    title: 'Host Header: Host: www.someschool.edu',
    desc: 'Mandatory in HTTP/1.1! Required for virtual hosting (shared web hosting), where multiple websites with different domain names run on the same physical server and share the same public IP address. Without the Host header, the server cannot know which virtual web site the client wants!'
  },
  'req-conn': {
    title: 'Connection Header: Connection: keep-alive',
    desc: 'Specifies whether the client wants a persistent or non-persistent connection. In HTTP/1.1, connections are persistent by default (keep-alive), allowing multiple objects to be requested over the same TCP connection without repeated 3-way handshakes. Set to "Connection: close" to tell server to terminate the connection after sending the response.'
  },
  'req-keepalive': {
    title: 'Keep-Alive Header: Keep-Alive: timeout=5, max=100',
    desc: 'Crucial instructor exam point! timeout=5 specifies that the server should keep the idle TCP connection open for at most 5 seconds waiting for the next request. max=100 means the server will service at most 100 requests over this single persistent TCP connection before forcing a close.'
  },
  'req-agent': {
    title: 'User-Agent Header: User-Agent: Mozilla/5.0...',
    desc: 'Identifies the client software (browser, OS version, rendering engine). The server uses this to perform content negotiation (e.g., serving mobile-optimized layouts to phones or legacy HTML to older browsers).'
  },
  'req-accept': {
    title: 'Accept-Language: Accept-Language: en-US,en;q=0.9,ar;q=0.8',
    desc: 'Indicates the user preferences for languages. q values (quality factors from 0 to 1) express relative preference. If an Arabic version is available and preferred, server can return it.'
  },
  'req-ifmod': {
    title: 'Conditional GET: If-Modified-Since: Wed, 21 Oct 2026 07:28:00 GMT',
    desc: 'Enables Web Caching! Sent by browser/proxy containing the Last-Modified timestamp of its cached copy. If the file has NOT been modified since that date, the server returns status "304 Not Modified" with NO entity body, saving precious bandwidth!'
  },
  'res-status': {
    title: 'Status Line: HTTP/1.1 200 OK',
    desc: 'Contains protocol version (HTTP/1.1), 3-digit status code (200), and human-readable phrase (OK). 200 means request succeeded and object is delivered in entity body.'
  },
  'res-conn': {
    title: 'Response Connection: Connection: keep-alive',
    desc: 'Server acknowledges that it will keep the TCP connection open for subsequent requests from this client.'
  },
  'res-date': {
    title: 'Date Header: Date: Thu, 05 Nov 2026 07:31:00 GMT',
    desc: 'The exact time and date when the server created and sent the HTTP response message (NOT when the object was created or last modified).'
  },
  'res-server': {
    title: 'Server Header: Server: Apache/2.4.52 (Ubuntu)',
    desc: 'Identifies the web server software and operating system version generating the response (analogous to User-Agent in requests).'
  },
  'res-lastmod': {
    title: 'Last-Modified Header: Last-Modified: Wed, 21 Oct 2026...',
    desc: 'The date and time when the requested object was created or last modified on the server disk. Crucial for caching: the client stores this timestamp and returns it in If-Modified-Since on future requests.'
  },
  'res-length': {
    title: 'Content-Length Header: Content-Length: 6821',
    desc: 'The exact size of the payload entity body in bytes. Essential in persistent connections because it tells the client when the current object ends and the next object begins in the byte stream!'
  },
  'res-type': {
    title: 'Content-Type: Content-Type: text/html; charset=UTF-8',
    desc: 'Specifies the MIME type of the object contained in the entity body (e.g., text/html, image/jpeg, application/json), instructing the browser how to render it.'
  }
};

function showDissectorDetail(key) {
  const item = DISSECTOR_DATA[key];
  if (!item) return;
  document.getElementById('dissector-title').innerText = item.title;
  document.getElementById('dissector-body').innerHTML = item.desc;
}

// ==========================================
// CALCULATOR IMPLEMENTATIONS
// ==========================================
function computeNodalDelay() {
  const L_val = parseFloat(document.getElementById('calc-delay-L').value);
  const L_unit = document.getElementById('calc-delay-L-unit').value;
  let L_bits = L_val;
  if (L_unit === 'bytes') L_bits = L_val * 8;
  if (L_unit === 'kbits') L_bits = L_val * 1000;

  const R_val = parseFloat(document.getElementById('calc-delay-R').value);
  const R_unit = document.getElementById('calc-delay-R-unit').value;
  let R_bps = R_val;
  if (R_unit === 'kbps') R_bps = R_val * 1000;
  if (R_unit === 'mbps') R_bps = R_val * 1000000;
  if (R_unit === 'gbps') R_bps = R_val * 1000000000;

  const d_val = parseFloat(document.getElementById('calc-delay-d').value);
  const d_unit = document.getElementById('calc-delay-d-unit').value;
  let d_meters = d_val;
  if (d_unit === 'km') d_meters = d_val * 1000;

  const s_km_s = parseFloat(document.getElementById('calc-delay-s').value);
  const s_m_s = s_km_s * 1000;

  const d_trans_s = L_bits / R_bps;
  const d_trans_ms = d_trans_s * 1000;

  const d_prop_s = d_meters / s_m_s;
  const d_prop_ms = d_prop_s * 1000;

  const total_ms = d_trans_ms + d_prop_ms;

  const out = document.getElementById('calc-delay-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">1. Transmission Delay (d_trans = L / R): ${L_bits} bits / ${R_bps.toLocaleString()} bps = ${d_trans_s.toFixed(6)} s = <strong>${d_trans_ms.toFixed(4)} ms</strong></div>
    <div class="calc-step">2. Propagation Delay (d_prop = d / s): ${d_meters.toLocaleString()} m / ${s_m_s.toExponential(2)} m/s = ${d_prop_s.toFixed(6)} s = <strong>${d_prop_ms.toFixed(4)} ms</strong></div>
    <div class="calc-step">3. Bandwidth-Delay Product (R × d_prop): ${Math.round(R_bps * d_prop_s).toLocaleString()} bits in flight</div>
    <div class="calc-step">Total Link Delay (d_trans + d_prop): <strong>${total_ms.toFixed(4)} ms</strong></div>
  `;
}

function computeUsersComparison() {
  const C_mbps = parseFloat(document.getElementById('calc-users-C').value);
  const R_kbps = parseFloat(document.getElementById('calc-users-R').value);
  const p = parseFloat(document.getElementById('calc-users-p').value);

  const C_kbps = C_mbps * 1000;
  const n_circuit = Math.floor(C_kbps / R_kbps);

  const out = document.getElementById('calc-users-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Circuit Switching Max Guaranteed Users: C / R = ${C_kbps} kbps / ${R_kbps} kbps = <strong>${n_circuit} users</strong></div>
    <div class="calc-step">Packet Switching: Each user active only ${(p * 100).toFixed(0)}% of the time.</div>
    <div class="calc-step">For N = 35 packet-switched users, probability that > ${n_circuit} users transmit simultaneously is <strong>< 0.04%</strong>!</div>
    <div class="calc-step">Conclusion: Packet switching supports <strong>3.5× more users</strong> with virtually negligible queuing!</div>
  `;
}

function computeCacheDelay() {
  const h = parseFloat(document.getElementById('calc-cache-h').value);
  const d_lan = parseFloat(document.getElementById('calc-cache-dlan').value);
  const d_wan = parseFloat(document.getElementById('calc-cache-dwan').value);

  const avg_delay = (h * d_lan) + ((1 - h) * (d_lan + d_wan));

  const out = document.getElementById('calc-cache-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Formula: T_avg = (h × D_LAN) + ((1 - h) × (D_LAN + D_Origin))</div>
    <div class="calc-step">Substitution: (${h} × ${d_lan} ms) + (${(1-h).toFixed(2)} × ${(d_lan + d_wan)} ms)</div>
    <div class="calc-step">Average Response Time: <strong>${avg_delay.toFixed(2)} ms</strong></div>
    <div class="calc-step">Latency Reduction: <strong>${(((d_wan - avg_delay) / d_wan) * 100).toFixed(1)}% faster</strong> with cache!</div>
  `;
}

function computeP2PTime() {
  const F = parseFloat(document.getElementById('calc-p2p-F').value);
  const N = parseFloat(document.getElementById('calc-p2p-N').value);
  const u_s = parseFloat(document.getElementById('calc-p2p-us').value);
  const d_min = parseFloat(document.getElementById('calc-p2p-dmin').value);
  const u = parseFloat(document.getElementById('calc-p2p-u').value);

  const d_cs = Math.max((N * F) / u_s, F / d_min);
  const d_p2p = Math.max(F / u_s, F / d_min, (N * F) / (u_s + N * u));

  const out = document.getElementById('calc-p2p-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Client-Server Time (D_CS): max( ${N}×${F}/${u_s} , ${F}/${d_min} ) = <strong>${d_cs.toFixed(1)} seconds</strong></div>
    <div class="calc-step">P2P Distribution Time (D_P2P): max( ${F}/${u_s} , ${F}/${d_min} , ${N*F}/(${u_s} + ${N}×${u}) ) = <strong>${d_p2p.toFixed(1)} seconds</strong></div>
    <div class="calc-step">P2P Speedup Factor: <strong>${(d_cs / d_p2p).toFixed(2)}× faster</strong></div>
  `;
}

function computeInternetChecksum() {
  const w1 = parseInt(document.getElementById('calc-check-w1').value, 16) || 0;
  const w2 = parseInt(document.getElementById('calc-check-w2').value, 16) || 0;
  const w3 = parseInt(document.getElementById('calc-check-w3').value, 16) || 0;

  let sum = w1 + w2;
  while (sum > 0xFFFF) {
    sum = (sum & 0xFFFF) + (sum >> 16);
  }
  sum += w3;
  while (sum > 0xFFFF) {
    sum = (sum & 0xFFFF) + (sum >> 16);
  }

  const checksum = (~sum) & 0xFFFF;

  const out = document.getElementById('calc-check-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Word 1: 0x${w1.toString(16).toUpperCase().padStart(4, '0')} (${w1.toString(2).padStart(16, '0')})</div>
    <div class="calc-step">Word 2: 0x${w2.toString(16).toUpperCase().padStart(4, '0')} (${w2.toString(2).padStart(16, '0')})</div>
    <div class="calc-step">Word 3: 0x${w3.toString(16).toUpperCase().padStart(4, '0')} (${w3.toString(2).padStart(16, '0')})</div>
    <div class="calc-step">1's Complement Sum (with end-around carry): 0x${sum.toString(16).toUpperCase().padStart(4, '0')}</div>
    <div class="calc-step">Bitwise Inversion (1's Complement): <strong>0x${checksum.toString(16).toUpperCase().padStart(4, '0')}</strong> (${checksum.toString(2).padStart(16, '0')})</div>
  `;
}

function computeUtilization() {
  const L = parseFloat(document.getElementById('calc-util-L').value) * 8;
  const R = parseFloat(document.getElementById('calc-util-R').value) * 1000000;
  const rtt = parseFloat(document.getElementById('calc-util-rtt').value) / 1000;
  const N = parseFloat(document.getElementById('calc-util-N').value);

  const d_trans = L / R;
  const u_stop = d_trans / (rtt + d_trans);
  const u_pipe = Math.min(1.0, (N * d_trans) / (rtt + d_trans));

  const out = document.getElementById('calc-util-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Transmission Delay (d_trans = L/R): ${(d_trans * 1000).toFixed(4)} ms</div>
    <div class="calc-step">Stop-and-Wait Utilization: <strong>${(u_stop * 100).toFixed(3)}%</strong></div>
    <div class="calc-step">Pipelined Utilization (Window N = ${N}): <strong>${(u_pipe * 100).toFixed(2)}%</strong></div>
    <div class="calc-step">Pipelining Throughput Gain: <strong>${(u_pipe / u_stop).toFixed(1)}× increase</strong></div>
  `;
}

function computeTCPRTO() {
  const est = parseFloat(document.getElementById('calc-rtt-est').value);
  const dev = parseFloat(document.getElementById('calc-rtt-dev').value);
  const sample = parseFloat(document.getElementById('calc-rtt-sample').value);

  const alpha = 0.125;
  const beta = 0.25;

  const newEst = (1 - alpha) * est + alpha * sample;
  const newDev = (1 - beta) * dev + beta * Math.abs(sample - est);
  const rto = newEst + 4 * newDev;

  const out = document.getElementById('calc-rto-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Updated EstimatedRTT: (0.875 × ${est}) + (0.125 × ${sample}) = <strong>${newEst.toFixed(2)} ms</strong></div>
    <div class="calc-step">Updated DevRTT: (0.75 × ${dev}) + (0.25 × |${sample} - ${est}|) = <strong>${newDev.toFixed(2)} ms</strong></div>
    <div class="calc-step">New TimeoutInterval (RTO): EstimatedRTT + 4×DevRTT = <strong>${rto.toFixed(2)} ms</strong></div>
  `;
}

function computeCIDR() {
  const ipStr = document.getElementById('calc-cidr-ip').value.trim();
  const prefix = parseInt(document.getElementById('calc-cidr-prefix').value);

  const parts = ipStr.split('.').map(Number);
  if (parts.length !== 4 || parts.some(p => isNaN(p) || p < 0 || p > 255)) {
    alert('Please enter a valid IPv4 address (e.g. 192.168.1.130)');
    return;
  }

  const ipInt = (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3];
  const maskInt = prefix === 0 ? 0 : (~0 << (32 - prefix)) >>> 0;
  const netInt = (ipInt & maskInt) >>> 0;
  const bcastInt = (netInt | (~maskInt >>> 0)) >>> 0;

  function intToIp(val) {
    return [
      (val >>> 24) & 255,
      (val >>> 16) & 255,
      (val >>> 8) & 255,
      val & 255
    ].join('.');
  }

  const totalHosts = Math.pow(2, 32 - prefix);
  const usableHosts = totalHosts > 2 ? totalHosts - 2 : 0;

  const out = document.getElementById('calc-cidr-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Subnet Mask: <strong>${intToIp(maskInt)}</strong></div>
    <div class="calc-step">Network Address: <strong>${intToIp(netInt)}/${prefix}</strong></div>
    <div class="calc-step">Broadcast Address: <strong>${intToIp(bcastInt)}</strong></div>
    <div class="calc-step">Usable Host Range: <strong>${intToIp(netInt + 1)}</strong> to <strong>${intToIp(bcastInt - 1)}</strong></div>
    <div class="calc-step">Total Addresses: <strong>${totalHosts}</strong> | Usable Hosts: <strong>${usableHosts}</strong></div>
  `;
}

function computeFragmentation() {
  const total = parseInt(document.getElementById('calc-frag-total').value);
  const mtu = parseInt(document.getElementById('calc-frag-mtu').value);

  const maxDataPerFrag = Math.floor((mtu - 20) / 8) * 8;
  const payloadTotal = total - 20;

  let offset = 0;
  let remaining = payloadTotal;
  let fragNum = 1;

  let rows = '';
  while (remaining > 0) {
    const dataSize = Math.min(remaining, maxDataPerFrag);
    remaining -= dataSize;
    const mf = remaining > 0 ? 1 : 0;
    const fragTotalLen = dataSize + 20;
    const offsetUnits = offset / 8;

    rows += `<tr>
      <td style="padding:4px 8px; border:1px solid var(--border);">Frag ${fragNum}</td>
      <td style="padding:4px 8px; border:1px solid var(--border);">${fragTotalLen} B</td>
      <td style="padding:4px 8px; border:1px solid var(--border);">${dataSize} B</td>
      <td style="padding:4px 8px; border:1px solid var(--border);">${offsetUnits}</td>
      <td style="padding:4px 8px; border:1px solid var(--border); font-weight:700;">${mf}</td>
    </tr>`;

    offset += dataSize;
    fragNum++;
  }

  const out = document.getElementById('calc-frag-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Max Payload Data per Fragment (multiple of 8): (MTU - 20) = ${maxDataPerFrag} Bytes</div>
    <table style="width:100%; border-collapse:collapse; margin-top:0.5rem; font-size:0.85rem; text-align:center;">
      <thead>
        <tr style="background:var(--bg-elevated); font-weight:700;">
          <th style="padding:4px 8px; border:1px solid var(--border);">Fragment</th>
          <th style="padding:4px 8px; border:1px solid var(--border);">Total Length</th>
          <th style="padding:4px 8px; border:1px solid var(--border);">Payload</th>
          <th style="padding:4px 8px; border:1px solid var(--border);">Offset (8-B units)</th>
          <th style="padding:4px 8px; border:1px solid var(--border);">MF Flag</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function computeCRCDivision() {
  const D = document.getElementById('calc-crc-D').value.trim();
  const G = document.getElementById('calc-crc-G').value.trim();

  const r = G.length - 1;
  let padded = D + '0'.repeat(r);
  let cur = padded.split('').map(Number);
  const gen = G.split('').map(Number);

  for (let i = 0; i <= cur.length - gen.length; i++) {
    if (cur[i] === 1) {
      for (let j = 0; j < gen.length; j++) {
        cur[i + j] = cur[i + j] ^ gen[j];
      }
    }
  }

  const rem = cur.slice(-r).join('');
  const transmitted = D + rem;

  const out = document.getElementById('calc-crc-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Generator G: ${G} (degree r = ${r})</div>
    <div class="calc-step">Appended Dividend: ${padded}</div>
    <div class="calc-step">Calculated CRC Remainder R: <strong>${rem}</strong></div>
    <div class="calc-step">Final Transmitted Frame &lt;D, R&gt;: <strong>${transmitted}</strong></div>
  `;
}

function computeRSA() {
  const p = parseInt(document.getElementById('calc-rsa-p').value);
  const q = parseInt(document.getElementById('calc-rsa-q').value);
  const m = parseInt(document.getElementById('calc-rsa-m').value);

  const n = p * q;
  const z = (p - 1) * (q - 1);

  // Find e coprime to z
  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
  let e = 3;
  while (e < z && gcd(e, z) !== 1) e += 2;

  // Find d
  let d = 1;
  while ((e * d) % z !== 1 && d < 10000) d++;

  // Modular exponentiation
  function modPow(base, exp, mod) {
    let res = 1;
    base = base % mod;
    while (exp > 0) {
      if (exp % 2 === 1) res = (res * base) % mod;
      base = (base * base) % mod;
      exp = Math.floor(exp / 2);
    }
    return res;
  }

  const c = modPow(m, e, n);
  const decrypted = modPow(c, d, n);

  const out = document.getElementById('calc-rsa-result');
  out.style.display = 'block';
  out.innerHTML = `
    <div class="calc-step">Modulus (n = p×q): ${p} × ${q} = <strong>${n}</strong></div>
    <div class="calc-step">Totient (z = (p-1)(q-1)): (${p}-1) × (${q}-1) = <strong>${z}</strong></div>
    <div class="calc-step">Public Key (n, e): <strong>(${n}, ${e})</strong></div>
    <div class="calc-step">Private Key (n, d): <strong>(${n}, ${d})</strong></div>
    <div class="calc-step">Encryption: c = ${m}^${e} mod ${n} = <strong>${c}</strong></div>
    <div class="calc-step">Decryption: m = ${c}^${d} mod ${n} = <strong>${decrypted}</strong> (Matches original plaintext!)</div>
  `;
}

// ==========================================
// SIMULATOR ENGINES
// ==========================================
let sfStepIndex = 0;
function simSFReset() {
  sfStepIndex = 0;
  const pkt = document.getElementById('sim-sf-pkt');
  if (pkt) {
    pkt.setAttribute('opacity', '0');
    pkt.setAttribute('x', '60');
  }
  document.getElementById('sim-sf-status').innerText = 'Ready. Click Step or Play to transmit packet.';
}

function simSFStep() {
  const pkt = document.getElementById('sim-sf-pkt');
  const status = document.getElementById('sim-sf-status');
  if (sfStepIndex === 0) {
    pkt.setAttribute('opacity', '1');
    pkt.setAttribute('x', '80');
    status.innerText = 'Step 1: Host A begins transmitting packet onto Link 1.';
    sfStepIndex = 1;
  } else if (sfStepIndex === 1) {
    pkt.setAttribute('x', '295');
    status.innerText = 'Step 2: Router receives all bits and stores packet in buffer (Store-and-Forward).';
    sfStepIndex = 2;
  } else if (sfStepIndex === 2) {
    pkt.setAttribute('x', '350');
    status.innerText = 'Step 3: Router looks up forwarding table and transmits packet onto Link 2.';
    sfStepIndex = 3;
  } else if (sfStepIndex === 3) {
    pkt.setAttribute('x', '550');
    status.innerText = 'Step 4: Host B receives packet completely! Transmission complete.';
    sfStepIndex = 4;
  } else {
    simSFReset();
  }
}

function simSFPlay() {
  simSFReset();
  let step = 0;
  const interval = setInterval(() => {
    simSFStep();
    step++;
    if (step >= 4) clearInterval(interval);
  }, 700);
}

// DNS Simulator
let dnsStepIdx = 0;
function simDNSReset() {
  dnsStepIdx = 0;
  document.getElementById('sim-dns-log').innerText = '[Ready] Choose Iterative or Recursive and click Step.';
}

function simDNSStep() {
  const mode = document.getElementById('sim-dns-mode').value;
  const log = document.getElementById('sim-dns-log');

  if (mode === 'iterative') {
    const steps = [
      '1. Client asks Local DNS Server for www.kau.edu.sa (Recursive from client to Local DNS).',
      '2. Local DNS asks Root DNS Server -> Root replies with IP of .sa TLD Server.',
      '3. Local DNS asks .sa TLD Server -> TLD replies with IP of kau.edu.sa Authoritative Server.',
      '4. Local DNS asks Authoritative Server -> Authoritative replies with IP 212.26.68.10.',
      '5. Local DNS caches IP and returns 212.26.68.10 to Client. Done!'
    ];
    if (dnsStepIdx < steps.length) {
      log.innerText += '\\n' + steps[dnsStepIdx];
      dnsStepIdx++;
    }
  } else {
    const steps = [
      '1. Client asks Local DNS Server for www.kau.edu.sa.',
      '2. Local DNS asks Root DNS Server recursively.',
      '3. Root DNS queries .sa TLD Server on behalf of Local DNS.',
      '4. TLD queries kau.edu.sa Authoritative Server directly.',
      '5. Answer bubbles all the way back: Authoritative -> TLD -> Root -> Local DNS -> Client.'
    ];
    if (dnsStepIdx < steps.length) {
      log.innerText += '\\n' + steps[dnsStepIdx];
      dnsStepIdx++;
    }
  }
}

// RDT Scenario
function simRDTScenario(type) {
  const state = document.getElementById('sim-rdt-state');
  const desc = document.getElementById('sim-rdt-desc');

  if (type === 'normal') {
    state.innerText = 'State: Wait for Call 0 -> Wait for ACK 0 -> Wait for Call 1';
    desc.innerText = 'Packet 0 sent -> ACK 0 received. Sequence number flips to 1. No retransmissions needed.';
  } else if (type === 'loss') {
    state.innerText = 'State: Timeout in Wait for ACK 0';
    desc.innerText = 'Packet 0 sent, but LOST on channel! Sender countdown timer expires. Sender retransmits Packet 0 and restarts timer.';
  } else if (type === 'ackloss') {
    state.innerText = 'State: Duplicate Packet Detected at Receiver';
    desc.innerText = 'Packet 0 received, but ACK 0 LOST on return path! Sender timer expires and retransmits Packet 0. Receiver detects duplicate seq 0, discards duplicate data, and resends ACK 0!';
  }
}

// TCP CWND Simulator
let cwndRound = 1;
let currentCWND = 1;
let ssthresh = 16;
let cwndPoints = [[40, 130]];

function simCWNDStep() {
  cwndRound++;
  if (currentCWND < ssthresh) {
    currentCWND = currentCWND * 2; // Slow start
  } else {
    currentCWND += 1; // Congestion avoidance
  }
  updateCWNDPlot();
}

function simCWNDEvent(evt) {
  if (evt === '3dup') {
    ssthresh = Math.max(2, Math.floor(currentCWND / 2));
    currentCWND = ssthresh + 3; // Fast recovery
  } else if (evt === 'timeout') {
    ssthresh = Math.max(2, Math.floor(currentCWND / 2));
    currentCWND = 1; // Drop to 1 MSS
  }
  cwndRound++;
  updateCWNDPlot();
}

function updateCWNDPlot() {
  const x = Math.min(560, 40 + (cwndRound - 1) * 22);
  const y = Math.max(20, 130 - (currentCWND * 3));
  cwndPoints.push([x, y]);

  const poly = document.getElementById('sim-cwnd-poly');
  if (poly) {
    poly.setAttribute('points', cwndPoints.map(p => p.join(',')).join(' '));
  }
  const modeStr = currentCWND < ssthresh ? 'Slow Start' : 'Congestion Avoidance';
  document.getElementById('sim-cwnd-info').innerText = `Round ${cwndRound}: cwnd = ${currentCWND} MSS (${modeStr}). ssthresh = ${ssthresh} MSS.`;
}

function simCWNDReset() {
  cwndRound = 1;
  currentCWND = 1;
  ssthresh = 16;
  cwndPoints = [[40, 130]];
  const poly = document.getElementById('sim-cwnd-poly');
  if (poly) poly.setAttribute('points', '40,130');
  document.getElementById('sim-cwnd-info').innerText = 'Round 1: cwnd = 1 MSS (Slow Start). ssthresh = 16 MSS.';
}

// Self-Learning Switch Simulator
const switchTable = {};
function simSwitchSend() {
  const src = document.getElementById('sim-sw-src').value;
  const dst = document.getElementById('sim-sw-dst').value;
  const [srcHost, srcPort] = src.split(':');

  // Learn source
  switchTable[srcHost] = srcPort;

  // Render table
  const tbody = document.getElementById('sim-switch-table');
  tbody.innerHTML = Object.keys(switchTable).map(h => `
    <tr><td>Host ${h}</td><td>${switchTable[h]}</td><td>300s</td></tr>
  `).join('');

  // Check destination
  const act = document.getElementById('sim-switch-action');
  if (switchTable[dst]) {
    if (switchTable[dst] === srcPort) {
      act.innerHTML = `<span style="color:var(--danger-text);">FILTERED:</span> Destination Host ${dst} is on the same port (${srcPort}). Frame dropped.`;
    } else {
      act.innerHTML = `<span style="color:var(--accent-text);">SELECTIVE FORWARD:</span> Destination Host ${dst} found in MAC table. Forwarding out ${switchTable[dst]} only!`;
    }
  } else {
    act.innerHTML = `<span style="color:var(--warning-text);">FLOODING:</span> Destination ${dst} unknown. Frame flooded out all ports except ${srcPort}!`;
  }
}

// ==========================================
// CHAPTER SECTION EMBEDDED INTERACTIVES
// ==========================================

// --- CHAPTER 1 INTERACTIVES ---
let fig1PacketTimer = null;
let fig1CurrentHop = 0;
const FIG1_HOPS = [
  { x: 80, y: 95, name: 'Client Laptop', desc: '1. Laptop creates an IP packet (20B IP header + 20B TCP header + 1460B HTTP GET payload) and transmits it onto access link.' },
  { x: 215, y: 170, name: 'Access Switch / AP', desc: '2. Access Switch reads Layer-2 Ethernet frame MAC address and forwards frame bits to default gateway edge router.' },
  { x: 335, y: 115, name: 'Edge Router R1', desc: '3. Router R1 performs store-and-forward: buffers packet, decrements TTL, checks destination IP, and forwards across 10 Gbps trunk.' },
  { x: 520, y: 115, name: 'Core Router R3', desc: '4. Router R3 forwards packet over high-speed optical backbone link into destination Autonomous System.' },
  { x: 765, y: 170, name: 'Data Center Web Server', desc: '5. Packet received by destination server! TCP handshake completed, HTTP 200 OK response sent back!' }
];

function animateFigure1Packet() {
  resetFigure1Packet();
  const pkt = document.getElementById('anim-packet-circle');
  const lbl = document.getElementById('anim-packet-label');
  const info = document.getElementById('fig1-info');
  if (!pkt || !info) return;
  pkt.setAttribute('opacity', '1');
  if (lbl) lbl.setAttribute('opacity', '1');
  fig1CurrentHop = 0;

  function advanceHop() {
    if (fig1CurrentHop >= FIG1_HOPS.length) {
      info.innerHTML = '<strong>Delivery Complete:</strong> Packet reached Destination Data Center successfully! (Click "Send Packet" to trace again)';
      return;
    }
    const hop = FIG1_HOPS[fig1CurrentHop];
    pkt.setAttribute('cx', hop.x);
    pkt.setAttribute('cy', hop.y);
    if (lbl) {
      lbl.setAttribute('x', hop.x);
      lbl.setAttribute('y', hop.y - 14);
    }
    info.innerHTML = `<strong>${hop.name}:</strong> ${hop.desc}`;
    fig1CurrentHop++;
    fig1PacketTimer = setTimeout(advanceHop, 1200);
  }
  advanceHop();
}

function resetFigure1Packet() {
  if (fig1PacketTimer) clearTimeout(fig1PacketTimer);
  const pkt = document.getElementById('anim-packet-circle');
  const lbl = document.getElementById('anim-packet-label');
  const info = document.getElementById('fig1-info');
  if (pkt) {
    pkt.setAttribute('cx', 80);
    pkt.setAttribute('cy', 95);
    pkt.setAttribute('opacity', '0');
  }
  if (lbl) {
    lbl.setAttribute('x', 80);
    lbl.setAttribute('y', 80);
    lbl.setAttribute('opacity', '0');
  }
  if (info) {
    info.innerHTML = "Status: Ready. Click 'Send Packet' to trace packet flow.";
  }
}

function inspectNode(title, details) {
  const box = document.getElementById('fig1-info');
  if (!box) return;
  box.innerHTML = `<strong>${title}:</strong> ${details}`;
}

// §1.3 Store-and-Forward Stepper
let sec1SfStepIdx = 0;
const SEC1_SF_STEPS = [
  { p1: 'transmitting', p2: 'queued', p3: 'queued', status: 'Time 0 to L/R: Host 1 is transmitting Packet 1 onto Link 1. Packets 2 and 3 are queued in Host buffer.' },
  { p1: 'received-r1', p2: 'transmitting', p3: 'queued', status: 'Time L/R to 2L/R: Packet 1 is fully stored at Router 1 and now transmitting onto Link 2! Host 1 begins transmitting Packet 2 onto Link 1.' },
  { p1: 'delivered', p2: 'received-r1', p3: 'transmitting', status: 'Time 2L/R to 3L/R: Packet 1 is delivered to Destination! Router 1 is transmitting Packet 2 onto Link 2. Host 1 is transmitting Packet 3 onto Link 1.' },
  { p1: 'delivered', p2: 'delivered', p3: 'received-r1', status: 'Time 3L/R to 4L/R: Packet 2 is delivered to Destination! Router 1 is transmitting Packet 3 onto Link 2.' },
  { p1: 'delivered', p2: 'delivered', p3: 'delivered', status: 'Time 4L/R: All 3 packets delivered! Total delay = 4 × (L / R) seconds.' }
];

function stepSec1SF() {
  if (sec1SfStepIdx >= SEC1_SF_STEPS.length) sec1SfStepIdx = 0;
  const s = SEC1_SF_STEPS[sec1SfStepIdx];
  const stat = document.getElementById('sec1-sf-status');
  if (stat) stat.innerText = s.status;
  ['p1', 'p2', 'p3'].forEach(p => {
    const el = document.getElementById('sec1-sf-' + p);
    if (el) {
      const state = s[p];
      if (state === 'transmitting') el.style.background = 'var(--primary)';
      else if (state === 'received-r1') el.style.background = '#8b5cf6';
      else if (state === 'delivered') el.style.background = 'var(--accent)';
      else el.style.background = 'var(--bg-secondary)';
    }
  });
  sec1SfStepIdx++;
}

function resetSec1SF() {
  sec1SfStepIdx = 0;
  stepSec1SF();
}

// §1.4 Nodal Delay Calculator
function calcSec1Delay() {
  const dproc = parseFloat(document.getElementById('sec1-dproc')?.value || 5);
  const dqueue = parseFloat(document.getElementById('sec1-dqueue')?.value || 10);
  const pktlen = parseFloat(document.getElementById('sec1-pktlen')?.value || 12000);
  const rateMbps = parseFloat(document.getElementById('sec1-rate')?.value || 100);
  const distKm = parseFloat(document.getElementById('sec1-dist')?.value || 1000);
  const propSpeed = parseFloat(document.getElementById('sec1-propspeed')?.value || 200000);

  // Update slider labels
  const setTxt = (id, txt) => { const el = document.getElementById(id); if (el) el.innerText = txt; };
  setTxt('sec1-dproc-val', dproc + ' ms');
  setTxt('sec1-dqueue-val', dqueue + ' ms');
  setTxt('sec1-pktlen-val', (pktlen / 8).toLocaleString() + ' Bytes (' + pktlen.toLocaleString() + ' bits)');
  setTxt('sec1-rate-val', rateMbps + ' Mbps');
  setTxt('sec1-dist-val', distKm.toLocaleString() + ' km');
  setTxt('sec1-propspeed-val', propSpeed.toLocaleString() + ' km/s');

  const dtrans = (pktlen / (rateMbps * 1000000)) * 1000; // ms
  const dprop = (distKm / propSpeed) * 1000; // ms
  const dnodal = dproc + dqueue + dtrans + dprop;

  const out = document.getElementById('sec1-delay-output');
  if (out) {
    out.innerHTML = `
      <div style="font-weight:700; margin-bottom:0.5rem; color:var(--text-primary);">Total Nodal Delay Breakdown:</div>
      <div class="calc-step">&bull; <strong>Processing Delay (d_proc):</strong> ${dproc.toFixed(2)} ms</div>
      <div class="calc-step">&bull; <strong>Queuing Delay (d_queue):</strong> ${dqueue.toFixed(2)} ms</div>
      <div class="calc-step">&bull; <strong>Transmission Delay (d_trans = L / R):</strong> ${pktlen} bits / ${(rateMbps * 1e6).toLocaleString()} bps = <strong>${dtrans.toFixed(4)} ms</strong></div>
      <div class="calc-step">&bull; <strong>Propagation Delay (d_prop = d / s):</strong> ${distKm} km / ${propSpeed} km/s = <strong>${dprop.toFixed(4)} ms</strong></div>
      <div class="calc-step" style="font-weight:700; font-size:1.05rem; color:var(--accent-text); margin-top:0.5rem;">
        Total d_nodal = ${dproc.toFixed(2)} + ${dqueue.toFixed(2)} + ${dtrans.toFixed(4)} + ${dprop.toFixed(4)} = <strong>${dnodal.toFixed(4)} ms</strong>
      </div>
    `;
  }
}

// §1.5 Encapsulation Stepper
let encapStepIdx = 0;
const ENCAP_STEPS = [
  {
    layer: '1. Application Layer (Message M)',
    visual: '<div style="background:#0ea5e9; color:#fff; padding:10px 20px; border-radius:6px; font-weight:700; text-align:center;">Application Message M (HTTP GET /index.html)</div>',
    info: 'The user application process creates raw application data (e.g. an HTTP GET request message). PDU: <strong>Message</strong>.'
  },
  {
    layer: '2. Transport Layer (Segment = H_t + M)',
    visual: '<div style="display:flex; gap:4px;"><div style="background:#8b5cf6; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:1; text-align:center;">TCP Header (H_t)<br><span style="font-size:0.75rem;">Src: 51234, Dst: 80, Seq#</span></div><div style="background:#0ea5e9; color:#fff; padding:10px 20px; border-radius:6px; font-weight:700; flex:2; text-align:center;">Message M</div></div>',
    info: 'Transport layer encapsulates message by adding TCP header (port numbers, sequence numbers, checksum, flow control). PDU: <strong>Segment</strong>.'
  },
  {
    layer: '3. Network Layer (Datagram = H_n + H_t + M)',
    visual: '<div style="display:flex; gap:4px;"><div style="background:#10b981; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:1; text-align:center;">IP Header (H_n)<br><span style="font-size:0.75rem;">Src IP, Dst IP, TTL</span></div><div style="background:#8b5cf6; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:1; text-align:center;">TCP Header</div><div style="background:#0ea5e9; color:#fff; padding:10px 20px; border-radius:6px; font-weight:700; flex:2; text-align:center;">Message M</div></div>',
    info: 'Network layer adds IP header containing 32-bit Source & Destination IP addresses, TTL, protocol type (TCP=6), and checksum. PDU: <strong>Datagram</strong>.'
  },
  {
    layer: '4. Link Layer (Frame = H_l + H_n + H_t + M + Trailer)',
    visual: '<div style="display:flex; gap:4px;"><div style="background:#f59e0b; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:1; text-align:center;">Ethernet Hdr (H_l)<br><span style="font-size:0.75rem;">Src MAC, Dst MAC</span></div><div style="background:#10b981; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:1; text-align:center;">IP Hdr</div><div style="background:#8b5cf6; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:1; text-align:center;">TCP Hdr</div><div style="background:#0ea5e9; color:#fff; padding:10px 14px; border-radius:6px; font-weight:700; flex:2; text-align:center;">Message M</div><div style="background:#ef4444; color:#fff; padding:10px; border-radius:6px; font-weight:700; flex:0.8; text-align:center;">CRC Trailer</div></div>',
    info: 'Link layer wraps datagram with Ethernet header (48-bit MAC addresses, EtherType) and CRC checksum trailer for error detection. PDU: <strong>Frame</strong>.'
  },
  {
    layer: '5. Physical Layer (Bitstream Modulation)',
    visual: '<div style="background:#334155; color:#38bdf8; font-family:monospace; padding:12px; border-radius:6px; font-weight:700; text-align:center; letter-spacing:2px; overflow-x:auto;">01001000 01100101 01101100 01101100 01101111 00100000 01001110 01100101 01110100 01110111 01101111 01110010 01101011</div>',
    info: 'Physical layer converts frame bytes into physical analog signals (voltages on twisted-pair, light pulses on optical fiber, or EM radio waves).'
  }
];

function renderEncapUI() {
  const step = ENCAP_STEPS[encapStepIdx];
  const lEl = document.getElementById('sec1-encap-layer');
  const vEl = document.getElementById('sec1-encap-visual');
  const iEl = document.getElementById('sec1-encap-info');
  if (lEl) lEl.innerText = step.layer;
  if (vEl) vEl.innerHTML = step.visual;
  if (iEl) iEl.innerHTML = step.info;
}

function stepEncapDown() {
  if (encapStepIdx < ENCAP_STEPS.length - 1) encapStepIdx++;
  renderEncapUI();
}

function stepEncapUp() {
  if (encapStepIdx > 0) encapStepIdx--;
  renderEncapUI();
}

function resetEncap() {
  encapStepIdx = 0;
  renderEncapUI();
}

// --- CHAPTER 2 INTERACTIVES ---
let sec2DnsStepIdx = 0;
const SEC2_DNS_STEPS = [
  { step: 'Step 1: Host to Local DNS', desc: 'Client Host (192.168.1.15) queries its configured Local DNS Server (192.168.1.1) asking for the IP address of <code>www.kau.edu.sa</code>. This query is <strong>recursive</strong> (local DNS takes responsibility to resolve it).' },
  { step: 'Step 2: Local DNS to Root Server', desc: 'Local DNS cache does not have the record. Local DNS sends an <strong>iterative query</strong> to one of the 13 Root DNS Server clusters (e.g., <code>[a-m].root-servers.net</code>).' },
  { step: 'Step 3: Root Server Referral', desc: 'Root DNS server does not know the exact host IP, but extracts the top-level domain (<code>.sa</code> / <code>.edu.sa</code>) and returns a referral list of TLD DNS Server IP addresses.' },
  { step: 'Step 4: Local DNS to TLD Server', desc: 'Local DNS server queries the <code>.sa</code> TLD Server asking for <code>www.kau.edu.sa</code>.' },
  { step: 'Step 5: TLD Server Referral', desc: 'TLD server inspects its database, finds the domain registration for <code>kau.edu.sa</code>, and returns the IP address of KAU\'s Authoritative DNS server (e.g., <code>ns1.kau.edu.sa</code>).' },
  { step: 'Step 6: Local DNS to Authoritative Server', desc: 'Local DNS server sends query directly to KAU\'s Authoritative DNS server.' },
  { step: 'Step 7: Authoritative Server Answer', desc: 'Authoritative server owns the zone! It looks up its Type A Resource Record and replies with: <code>www.kau.edu.sa IN A 212.111.45.10 (TTL=86400)</code>.' },
  { step: 'Step 8: Local DNS Caches & Delivers to Host', desc: 'Local DNS server caches the mapping in its local cache to quickly answer future requests, and delivers the IP address <code>212.111.45.10</code> to the client host. Web browser now initiates TCP handshake!' }
];

function stepSec2DNS() {
  if (sec2DnsStepIdx >= SEC2_DNS_STEPS.length) sec2DnsStepIdx = 0;
  const s = SEC2_DNS_STEPS[sec2DnsStepIdx];
  const stEl = document.getElementById('sec2-dns-step');
  const dEl = document.getElementById('sec2-dns-desc');
  if (stEl) stEl.innerText = s.step;
  if (dEl) dEl.innerHTML = s.desc;
  sec2DnsStepIdx++;
}

function resetSec2DNS() {
  sec2DnsStepIdx = 0;
  stepSec2DNS();
}

function calcSec2P2P() {
  const F = parseFloat(document.getElementById('sec2-p2p-f')?.value || 1000);
  const us = parseFloat(document.getElementById('sec2-p2p-us')?.value || 30);
  const N = parseInt(document.getElementById('sec2-p2p-n')?.value || 10);
  const dmin = parseFloat(document.getElementById('sec2-p2p-dmin')?.value || 2);
  const upeer = parseFloat(document.getElementById('sec2-p2p-upeer')?.value || 1);

  const d_cs = Math.max((N * F) / us, F / dmin);
  const sum_u = us + N * upeer;
  const d_p2p = Math.max(F / us, F / dmin, (N * F) / sum_u);

  const out = document.getElementById('sec2-p2p-result');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">&bull; <strong>Client-Server Distribution Time:</strong> D_CS = max(N&times;F/u_s, F/d_min) = max(${((N*F)/us).toFixed(1)} s, ${(F/dmin).toFixed(1)} s) = <strong>${d_cs.toFixed(1)} seconds</strong></div>
      <div class="calc-step">&bull; <strong>P2P Distribution Time:</strong> D_P2P = max(F/u_s, F/d_min, N&times;F/(u_s + &sum;u_i)) = max(${(F/us).toFixed(1)} s, ${(F/dmin).toFixed(1)} s, ${((N*F)/sum_u).toFixed(1)} s) = <strong>${d_p2p.toFixed(1)} seconds</strong></div>
      <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
        P2P is ${(d_cs / d_p2p).toFixed(2)}&times; faster for distributing this file to ${N} peers!
      </div>
    `;
  }
}

// --- CHAPTER 3 INTERACTIVES ---
function calcSec3Checksum() {
  const w1Str = document.getElementById('sec3-word1')?.value || '4500';
  const w2Str = document.getElementById('sec3-word2')?.value || '003c';
  const w1 = parseInt(w1Str, 16) || 0;
  const w2 = parseInt(w2Str, 16) || 0;

  const sum = w1 + w2;
  const carry = sum >> 16;
  const wrapped = (sum & 0xFFFF) + carry;
  const checksum = (~wrapped) & 0xFFFF;

  const toBin16 = v => (v >>> 0).toString(2).padStart(16, '0');
  const toHex4 = v => (v >>> 0).toString(16).toUpperCase().padStart(4, '0');

  const out = document.getElementById('sec3-checksum-result');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">&bull; <strong>Word 1 (0x${toHex4(w1)}):</strong> <code>${toBin16(w1)}</code></div>
      <div class="calc-step">&bull; <strong>Word 2 (0x${toHex4(w2)}):</strong> <code>${toBin16(w2)}</code></div>
      <div class="calc-step">&bull; <strong>32-Bit Sum:</strong> <code>0x${sum.toString(16).toUpperCase()}</code> (Carry bit = ${carry})</div>
      <div class="calc-step">&bull; <strong>Wrap-Around Sum:</strong> <code>${toBin16(wrapped)}</code> (0x${toHex4(wrapped)})</div>
      <div class="calc-step" style="font-weight:700; color:var(--accent-text);">&bull; <strong>1's Complement Checksum:</strong> <code>${toBin16(checksum)}</code> (0x${toHex4(checksum)})</div>
    `;
  }
}

let sec3TcpStepIdx = 0;
const SEC3_TCP_STEPS = [
  { badge: 'Step 1: SYN', desc: '<strong>Client &rarr; Server:</strong> TCP SYN Segment (SYN=1, ACK=0, Seq=100). Client enters <code>SYN_SENT</code> state.' },
  { badge: 'Step 2: SYN-ACK', desc: '<strong>Server &rarr; Client:</strong> TCP SYN-ACK Segment (SYN=1, ACK=1, Seq=300, Ack=101). Server allocates buffers and enters <code>SYN_RCVD</code> state.' },
  { badge: 'Step 3: ACK (Established)', desc: '<strong>Client &rarr; Server:</strong> TCP ACK Segment (SYN=0, ACK=1, Seq=101, Ack=301). Connection is now <code>ESTABLISHED</code> on both endpoints!' },
  { badge: 'Step 4: Client FIN', desc: '<strong>Client &rarr; Server:</strong> Client closes socket: sends FIN Segment (FIN=1, Seq=101, Ack=301). Client enters <code>FIN_WAIT_1</code> state.' },
  { badge: 'Step 5: Server ACK', desc: '<strong>Server &rarr; Client:</strong> Server acknowledges client FIN (ACK=1, Ack=102). Client moves to <code>FIN_WAIT_2</code>; Server enters <code>CLOSE_WAIT</code>.' },
  { badge: 'Step 6: Server FIN', desc: '<strong>Server &rarr; Client:</strong> Server finishes sending pending data: sends FIN Segment (FIN=1, Seq=301, Ack=102). Server enters <code>LAST_ACK</code>.' },
  { badge: 'Step 7: Client ACK & TIME_WAIT', desc: '<strong>Client &rarr; Server:</strong> Client sends ACK (Ack=302) and enters <code>TIME_WAIT</code> (waits 2&times;MSL = 60s) before final CLOSE to guarantee server received ACK!' }
];

function stepSec3TCPHandshake() {
  if (sec3TcpStepIdx >= SEC3_TCP_STEPS.length) sec3TcpStepIdx = 0;
  const s = SEC3_TCP_STEPS[sec3TcpStepIdx];
  const bEl = document.getElementById('sec3-tcp-step-badge');
  const dEl = document.getElementById('sec3-tcp-info');
  if (bEl) bEl.innerText = s.badge;
  if (dEl) dEl.innerHTML = s.desc;
  sec3TcpStepIdx++;
}

function resetSec3TCPHandshake() {
  sec3TcpStepIdx = 0;
  stepSec3TCPHandshake();
}

// --- CHAPTER 4 INTERACTIVES ---
function calcSec4CIDR() {
  const ipStr = document.getElementById('sec4-ip')?.value || '203.0.113.75';
  const prefix = parseInt(document.getElementById('sec4-prefix')?.value || 26);

  function ipToInt(ip) {
    return ip.split('.').reduce((acc, oct) => ((acc << 8) + parseInt(oct, 10)) >>> 0, 0);
  }
  function intToIp(val) {
    return [(val >>> 24) & 255, (val >>> 16) & 255, (val >>> 8) & 255, val & 255].join('.');
  }

  const ipInt = ipToInt(ipStr);
  const maskInt = prefix === 0 ? 0 : (~0 << (32 - prefix)) >>> 0;
  const netInt = (ipInt & maskInt) >>> 0;
  const bcastInt = (netInt | (~maskInt >>> 0)) >>> 0;
  const firstHost = prefix >= 31 ? netInt : (netInt + 1) >>> 0;
  const lastHost = prefix >= 31 ? bcastInt : (bcastInt - 1) >>> 0;
  const totalHosts = prefix >= 31 ? 0 : Math.pow(2, 32 - prefix) - 2;

  const out = document.getElementById('sec4-cidr-result');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">&bull; <strong>Subnet Mask:</strong> ${intToIp(maskInt)} (/ ${prefix})</div>
      <div class="calc-step">&bull; <strong>Network Address:</strong> ${intToIp(netInt)}</div>
      <div class="calc-step">&bull; <strong>Broadcast Address:</strong> ${intToIp(bcastInt)}</div>
      <div class="calc-step">&bull; <strong>Usable Host Range:</strong> ${intToIp(firstHost)} &mdash; ${intToIp(lastHost)}</div>
      <div class="calc-step" style="font-weight:700; color:var(--accent-text);">&bull; <strong>Total Usable Host Addresses:</strong> ${totalHosts.toLocaleString()} hosts (2<sup>${32 - prefix}</sup> &minus; 2)</div>
    `;
  }
}

let sec4DijkstraStepIdx = 0;
const SEC4_DIJKSTRA_STEPS = [
  { step: 'Init: N\' = {u}', info: 'Starting at source node <strong>u</strong>. Immediate neighbors: D(v)=2, D(x)=1, D(w)=5. Non-neighbors: D(y)=&infin;, D(z)=&infin;. Minimum unvisited is <strong>x (cost 1)</strong>.' },
  { step: 'Step 1: N\' = {u, x}', info: 'Add <strong>x</strong> to N\'. Examine neighbors of x: updates D(v)=min(2, 1+2)=2, D(w)=min(5, 1+3)=4, D(y)=min(&infin;, 1+1)=2. Minimum unvisited are <strong>v (cost 2)</strong> and <strong>y (cost 2)</strong>.' },
  { step: 'Step 2: N\' = {u, x, y}', info: 'Add <strong>y</strong> to N\'. Examine neighbors of y: updates D(w)=min(4, 2+1)=3, D(z)=min(&infin;, 2+2)=4. Minimum unvisited is <strong>v (cost 2)</strong>.' },
  { step: 'Step 3: N\' = {u, x, y, v}', info: 'Add <strong>v</strong> to N\'. Examine neighbors of v: D(w)=min(3, 2+3)=3. Minimum unvisited is <strong>w (cost 3)</strong>.' },
  { step: 'Step 4: N\' = {u, x, y, v, w}', info: 'Add <strong>w</strong> to N\'. Examine neighbors of w: D(z)=min(4, 3+5)=4. Only node <strong>z (cost 4)</strong> remains.' },
  { step: 'Step 5: N\' = {u, x, y, v, w, z}', info: 'All nodes visited! Final least-cost forwarding paths from u: to v: 2 (via v), to x: 1 (via x), to y: 2 (via x), to w: 3 (via x), to z: 4 (via x).' }
];

function stepSec4Dijkstra() {
  if (sec4DijkstraStepIdx >= SEC4_DIJKSTRA_STEPS.length) sec4DijkstraStepIdx = 0;
  const s = SEC4_DIJKSTRA_STEPS[sec4DijkstraStepIdx];
  const stEl = document.getElementById('sec4-dijkstra-step');
  const inEl = document.getElementById('sec4-dijkstra-info');
  if (stEl) stEl.innerText = s.step;
  if (inEl) inEl.innerHTML = s.info;
  sec4DijkstraStepIdx++;
}

function resetSec4Dijkstra() {
  sec4DijkstraStepIdx = 0;
  stepSec4Dijkstra();
}

// --- CHAPTER 5 INTERACTIVES ---
function detectCorrectParity() {
  const m = [
    [document.getElementById('sec5-p-r0c0')?.checked ? 1 : 0, document.getElementById('sec5-p-r0c1')?.checked ? 1 : 0, document.getElementById('sec5-p-r0c2')?.checked ? 1 : 0],
    [document.getElementById('sec5-p-r1c0')?.checked ? 1 : 0, document.getElementById('sec5-p-r1c1')?.checked ? 1 : 0, document.getElementById('sec5-p-r1c2')?.checked ? 1 : 0],
    [document.getElementById('sec5-p-r2c0')?.checked ? 1 : 0, document.getElementById('sec5-p-r2c1')?.checked ? 1 : 0, document.getElementById('sec5-p-r2c2')?.checked ? 1 : 0]
  ];

  const origRowParity = [1, 0, 0];
  const origColParity = [0, 0, 1];

  let badRow = -1;
  let badCol = -1;

  for (let r = 0; r < 3; r++) {
    const sum = m[r][0] + m[r][1] + m[r][2];
    if ((sum % 2) !== origRowParity[r]) badRow = r;
  }
  for (let c = 0; c < 3; c++) {
    const sum = m[0][c] + m[1][c] + m[2][c];
    if ((sum % 2) !== origColParity[c]) badCol = c;
  }

  const out = document.getElementById('sec5-parity-result');
  if (!out) return;

  if (badRow === -1 && badCol === -1) {
    out.innerHTML = '<span style="color:var(--accent-text); font-weight:700;">✅ Parity Check Passed:</span> All row and column parity bits match! No bit errors detected.';
  } else if (badRow !== -1 && badCol !== -1) {
    out.innerHTML = `
      <span style="color:var(--danger-text); font-weight:700;">⚠️ Single-Bit Error Detected!</span>
      <br>Mismatch at <strong>Row ${badRow + 1}</strong> and <strong>Column ${badCol + 1}</strong>.
      <br>The corrupted bit is at position (row ${badRow + 1}, col ${badCol + 1}) with current value <code>${m[badRow][badCol]}</code>.
      <br><button class="btn-primary" style="margin-top:0.5rem;" onclick="fixParityBit(${badRow}, ${badCol})">Auto-Correct Flipped Bit to ${1 - m[badRow][badCol]}</button>
    `;
  } else {
    out.innerHTML = '<span style="color:var(--warning-text); font-weight:700;">Multiple-bit or parity-bit error detected!</span>';
  }
}

function fixParityBit(r, c) {
  const cb = document.getElementById(`sec5-p-r${r}c${c}`);
  if (cb) {
    cb.checked = !cb.checked;
    detectCorrectParity();
  }
}

function resetParityMatrix() {
  const def = [[0, 1, 0], [1, 0, 1], [1, 1, 0]];
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      const cb = document.getElementById(`sec5-p-r${r}c${c}`);
      if (cb) cb.checked = (def[r][c] === 1);
    }
  }
  detectCorrectParity();
}

let sec5DayLifeIdx = 0;
const SEC5_DAYLIFE_STEPS = [
  { step: '1. DHCP: Obtaining Network Configuration', desc: 'Laptop connects to school ethernet. Operates 4-step DHCP: Discover (broadcast), Offer, Request, ACK. Laptop receives: IP <code>68.85.2.101</code>, Subnet Mask <code>/24</code>, Default Gateway Router <code>68.85.2.1</code>, and Local DNS <code>68.87.71.226</code>.' },
  { step: '2. ARP: Finding Default Gateway MAC', desc: 'To send a packet outside its subnet, laptop needs gateway\'s Layer-2 MAC address. Laptop broadcasts ARP Request: <em>"Who has IP 68.85.2.1? Tell 68.85.2.101"</em>. First-hop router replies with its MAC address <code>00:22:6b:45:11:00</code>.' },
  { step: '3. DNS: Resolving www.google.com', desc: 'Laptop creates DNS query for <code>www.google.com</code>, places it in UDP segment, IP datagram, and sends to DNS server via default gateway. Inter-domain BGP/OSPF routers forward datagram. DNS server returns IP address <code>64.233.169.103</code>.' },
  { step: '4. TCP 3-Way Handshake', desc: 'Laptop creates TCP socket and initiates 3-way handshake with Google server: SYN &rarr; SYN-ACK &rarr; ACK. Connection established.' },
  { step: '5. HTTP GET Request', desc: 'Laptop sends <code>GET / HTTP/1.1</code> inside TCP segment. Router forwards it across Internet backbone to Google web server.' },
  { step: '6. HTTP 200 OK & Page Rendering', desc: 'Google web server generates <code>HTTP/1.1 200 OK</code> with HTML content. Web browser renders page! Complete round-trip accomplished.' }
];

function stepSec5DayLife() {
  if (sec5DayLifeIdx >= SEC5_DAYLIFE_STEPS.length) sec5DayLifeIdx = 0;
  const s = SEC5_DAYLIFE_STEPS[sec5DayLifeIdx];
  const stEl = document.getElementById('sec5-daylife-step');
  const dEl = document.getElementById('sec5-daylife-desc');
  if (stEl) stEl.innerText = s.step;
  if (dEl) dEl.innerHTML = s.desc;
  sec5DayLifeIdx++;
}

function resetSec5DayLife() {
  sec5DayLifeIdx = 0;
  stepSec5DayLife();
}

// --- CHAPTER 6 INTERACTIVES ---
function calcSec6CDMA() {
  const bitA = parseInt(document.getElementById('sec6-bit-a')?.value || 1);
  const bitB = parseInt(document.getElementById('sec6-bit-b')?.value || -1);

  const cA = [-1, -1, -1, 1, 1, -1, 1, 1];
  const cB = [-1, -1, 1, -1, 1, 1, 1, -1];

  const S = [];
  for (let i = 0; i < 8; i++) {
    S.push(bitA * cA[i] + bitB * cB[i]);
  }

  let dotA = 0;
  for (let i = 0; i < 8; i++) {
    dotA += S[i] * cA[i];
  }
  const decodedA = dotA / 8;

  const out = document.getElementById('sec6-cdma-result');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">&bull; <strong>Sender A Code (c<sub>A</sub>):</strong> [${cA.join(', ')}] (Sending: ${bitA === 1 ? 'Bit 1 (+1)' : bitA === -1 ? 'Bit 0 (&minus;1)' : 'Silent (0)'})</div>
      <div class="calc-step">&bull; <strong>Sender B Code (c<sub>B</sub>):</strong> [${cB.join(', ')}] (Sending: ${bitB === 1 ? 'Bit 1 (+1)' : bitB === -1 ? 'Bit 0 (&minus;1)' : 'Silent (0)'})</div>
      <div class="calc-step">&bull; <strong>Superimposed Channel Signal S:</strong> <code>[${S.join(', ')}]</code></div>
      <div class="calc-step">&bull; <strong>Inner Dot Product (S &sdot; c<sub>A</sub>):</strong> ${dotA}</div>
      <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
        &bull; <strong>Decoded Bit for Sender A:</strong> (${dotA} / 8) = <strong>${decodedA}</strong> &rarr; ${decodedA === 1 ? 'Successfully decoded Bit 1!' : decodedA === -1 ? 'Successfully decoded Bit 0!' : 'Sender A was Silent.'}
      </div>
    `;
  }
}

let sec6CsmaStepIdx = 0;
const SEC6_CSMA_STEPS = [
  { step: '1. Carrier Sense & DIFS', desc: 'Station senses wireless channel. If sensed idle for <strong>DIFS (Distributed Inter-Frame Space)</strong> duration, station may transmit immediately if no previous collision occurred.' },
  { step: '2. Channel Busy: NAV Set', desc: 'If channel is busy, station defers transmission and sets <strong>Network Allocation Vector (NAV)</strong> timer based on duration field in overheard frame.' },
  { step: '3. Random Backoff Countdown', desc: 'Station chooses random backoff counter in [0, CW]. Counts down only while channel is sensed idle. Freezes counter when channel becomes busy.' },
  { step: '4. Transmit Frame', desc: 'Backoff counter reaches 0! Station transmits its 802.11 Data frame onto the wireless medium.' },
  { step: '5. SIFS & Link-Layer ACK', desc: 'Destination receives frame, checks CRC, waits <strong>SIFS (Short Inter-Frame Space)</strong>, and replies with ACK frame. If sender receives no ACK, it doubles contention window (exponential backoff) and retransmits.' }
];

function stepSec6CSMACA() {
  if (sec6CsmaStepIdx >= SEC6_CSMA_STEPS.length) sec6CsmaStepIdx = 0;
  const s = SEC6_CSMA_STEPS[sec6CsmaStepIdx];
  const stEl = document.getElementById('sec6-csma-step');
  const dEl = document.getElementById('sec6-csma-desc');
  if (stEl) stEl.innerText = s.step;
  if (dEl) dEl.innerHTML = s.desc;
  sec6CsmaStepIdx++;
}

function resetSec6CSMACA() {
  sec6CsmaStepIdx = 0;
  stepSec6CSMACA();
}

// --- CHAPTER 7 INTERACTIVES ---
function setSec7BW(bwKbps) {
  let res = '240p (Mobile)';
  let bufferPct = 30;
  let color = '#ef4444';

  if (bwKbps >= 15000) {
    res = '4K Ultra-HD (2160p)';
    bufferPct = 95;
    color = '#10b981';
  } else if (bwKbps >= 5000) {
    res = '1080p Full-HD';
    bufferPct = 80;
    color = '#10b981';
  } else if (bwKbps >= 2500) {
    res = '720p HD';
    bufferPct = 60;
    color = '#3b82f6';
  } else if (bwKbps >= 1000) {
    res = '480p SD';
    bufferPct = 45;
    color = '#f59e0b';
  }

  const bwEl = document.getElementById('sec7-dash-bw');
  const resEl = document.getElementById('sec7-dash-res');
  const bufEl = document.getElementById('sec7-dash-buffer');
  const fillEl = document.getElementById('sec7-dash-buffer-fill');

  if (bwEl) bwEl.innerText = bwKbps.toLocaleString() + ' kbps';
  if (resEl) resEl.innerText = res;
  if (bufEl) bufEl.innerText = `${(bufferPct * 0.3).toFixed(1)}s (${bufferPct}% buffer capacity)`;
  if (fillEl) {
    fillEl.style.width = bufferPct + '%';
    fillEl.style.background = color;
  }
}

function calcSec7TokenBucket() {
  const b = parseFloat(document.getElementById('sec7-tb-b')?.value || 1000);
  const r = parseFloat(document.getElementById('sec7-tb-r')?.value || 100);
  const t = parseFloat(document.getElementById('sec7-tb-t')?.value || 5);

  const maxBurstBits = b + r * t;
  const maxBurstMB = (maxBurstBits / 8000).toFixed(3);

  const out = document.getElementById('sec7-tb-result');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">&bull; <strong>Bucket Capacity (b):</strong> ${b.toLocaleString()} kbits</div>
      <div class="calc-step">&bull; <strong>Token Generation Rate (r):</strong> ${r.toLocaleString()} kbps</div>
      <div class="calc-step">&bull; <strong>Burst Duration (t):</strong> ${t} seconds</div>
      <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
        &bull; <strong>Maximum Transmitted Bits in Interval t:</strong> M = b + r&times;t = ${b} + (${r} &times; ${t}) = <strong>${maxBurstBits.toLocaleString()} kbits</strong> (~${maxBurstMB} MB)
      </div>
    `;
  }
}

// --- CHAPTER 8 INTERACTIVES ---
function calcSec8RSA() {
  const p = parseInt(document.getElementById('rsa-p-input')?.value || 3);
  const q = parseInt(document.getElementById('rsa-q-input')?.value || 11);
  let m = parseInt(document.getElementById('rsa-m-input')?.value || 8);

  const n = p * q;
  const z = (p - 1) * (q - 1);

  if (m >= n) {
    m = n - 1;
    const mInp = document.getElementById('rsa-m-input');
    if (mInp) mInp.value = m;
  }

  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
  function modPow(base, exp, mod) {
    let res = 1;
    base = base % mod;
    while (exp > 0) {
      if (exp % 2 === 1) res = (res * base) % mod;
      exp = Math.floor(exp / 2);
      base = (base * base) % mod;
    }
    return res;
  }

  let e = 3;
  while (e < z && gcd(e, z) !== 1) e += 2;

  let d = 1;
  while ((d * e) % z !== 1 && d < 1000) d++;

  const c = modPow(m, e, n);
  const decrypted = modPow(c, d, n);

  const out = document.getElementById('rsa-output-box');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">1. <strong>Primes:</strong> p = ${p}, q = ${q}</div>
      <div class="calc-step">2. <strong>Modulus n:</strong> n = p &times; q = ${p} &times; ${q} = <strong>${n}</strong></div>
      <div class="calc-step">3. <strong>Euler's Totient z:</strong> z = (p &minus; 1)(q &minus; 1) = ${p - 1} &times; ${q - 1} = <strong>${z}</strong></div>
      <div class="calc-step">4. <strong>Public Exponent e:</strong> Chosen e = <strong>${e}</strong> (gcd(${e}, ${z}) = 1) &rarr; <strong>Public Key: (${n}, ${e})</strong></div>
      <div class="calc-step">5. <strong>Private Exponent d:</strong> Found d = <strong>${d}</strong> ((${e} &times; ${d}) mod ${z} = ${(e * d) % z}) &rarr; <strong>Private Key: (${n}, ${d})</strong></div>
      <div class="calc-step">6. <strong>Encryption:</strong> c = m<sup>e</sup> mod n = ${m}<sup>${e}</sup> mod ${n} = <strong>${c}</strong></div>
      <div class="calc-step" style="font-weight:700; color:var(--accent-text);">7. <strong>Decryption:</strong> m = c<sup>d</sup> mod n = ${c}<sup>${d}</sup> mod ${n} = <strong>${decrypted}</strong> (Original plaintext recovered!)</div>
    `;
  }
}

const SEC8_AUTH_DATA = {
  ap1: {
    title: 'Protocol ap1.0: Naive Claim',
    exchange: 'Alice &rarr; Bob: <code>"I am Alice"</code>',
    flaw: '<strong>Fatal Flaw:</strong> Trudy eavesdrops and sends the exact same string <code>"I am Alice"</code>. Bob has zero cryptographic proof and accepts Trudy!',
    status: 'Vulnerable to Impersonation ❌'
  },
  ap2: {
    title: 'Protocol ap2.0: IP Source Address Verification',
    exchange: 'Alice &rarr; Bob: <code>"I am Alice"</code> inside IP Datagram with Src IP <code>192.168.1.15</code>',
    flaw: '<strong>Fatal Flaw:</strong> Trudy crafts raw IP datagram with <strong>spoofed source IP</strong> <code>192.168.1.15</code>. Bob validates the IP header and accepts Trudy!',
    status: 'Vulnerable to IP Spoofing ❌'
  },
  ap3: {
    title: 'Protocol ap3.0: Secret Password',
    exchange: 'Alice &rarr; Bob: <code>"I am Alice, Password: secret123"</code>',
    flaw: '<strong>Fatal Flaw:</strong> Trudy sniffs the wire (packet capture) using Wireshark, reads the cleartext password, and reuses it in subsequent sessions.',
    status: 'Vulnerable to Wiretapping / Sniffing ❌'
  },
  ap31: {
    title: 'Protocol ap3.1: Encrypted Password',
    exchange: 'Alice &rarr; Bob: <code>"I am Alice, Ciphertext: K_AB(secret123)"</code>',
    flaw: '<strong>Fatal Flaw (Playback / Replay Attack):</strong> Trudy does NOT need to decrypt the password! Trudy records the exact encrypted ciphertext and replays it to Bob tomorrow. Bob decrypts it with K_AB, gets "secret123", and grants Trudy access!',
    status: 'Vulnerable to Playback / Replay Attack ❌'
  },
  ap4: {
    title: 'Protocol ap4.0: Nonce Challenge-Response',
    exchange: '1. Alice &rarr; Bob: <code>"I am Alice"</code><br>2. Bob &rarr; Alice: Nonce <code>R = 894321</code> (Challenge)<br>3. Alice &rarr; Bob: Response <code>K_AB(894321)</code><br>4. Bob decrypts with K_AB: matches R!',
    flaw: '<strong>Secure Against Replay:</strong> Bob generates a fresh random nonce R for every single session. An old recorded response K_AB(R_old) is useless to Trudy because Bob expects K_AB(R_new)!',
    status: 'Secure & Robust ✅'
  }
};

function stepSec8Auth(proto) {
  const p = SEC8_AUTH_DATA[proto];
  if (!p) return;

  ['ap1', 'ap2', 'ap3', 'ap31', 'ap4'].forEach(id => {
    const btn = document.getElementById('sec8-btn-' + id);
    if (btn) {
      if (id === proto) {
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
      } else {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
      }
    }
  });

  const out = document.getElementById('sec8-auth-diagram');
  if (out) {
    out.innerHTML = `
      <div style="font-weight:700; font-size:1rem; margin-bottom:0.5rem; color:var(--text-primary);">${p.title}</div>
      <div class="calc-step" style="background:var(--bg-secondary); border-radius:6px; padding:8px 12px; margin-bottom:0.5rem;">${p.exchange}</div>
      <div class="calc-step" style="margin-bottom:0.5rem;">${p.flaw}</div>
      <div style="font-weight:700; color:${proto === 'ap4' ? 'var(--accent-text)' : 'var(--danger-text)'}; font-size:0.95rem;">Security Verdict: ${p.status}</div>
    `;
  }
}

function testSec8Firewall() {
  const srcIp = document.getElementById('fw-src-ip')?.value || '192.168.1.15';
  const dstIp = document.getElementById('fw-dst-ip')?.value || '198.51.100.1';
  const dstPort = parseInt(document.getElementById('fw-dst-port')?.value || 80);
  const ack = parseInt(document.getElementById('fw-ack-flag')?.value || 0);

  for (let i = 1; i <= 5; i++) {
    const row = document.getElementById('sec8-acl-row-' + i);
    if (row) row.style.background = 'transparent';
  }

  let matchedRule = 5;
  let action = 'DROP';
  let reason = 'Default deny rule matched (no earlier specific rule permitted this packet).';

  if (srcIp.startsWith('192.168.1.') && !dstIp.startsWith('192.168.1.') && (dstPort === 80 || dstPort === 443)) {
    matchedRule = 1;
    action = 'ALLOW';
    reason = 'Rule 1 Match: Outbound HTTP/HTTPS web browsing from internal LAN client to external server.';
  } else if (dstIp === '192.168.1.50' && dstPort === 80) {
    matchedRule = 2;
    action = 'ALLOW';
    reason = 'Rule 2 Match: Inbound HTTP traffic destined to organization public web server.';
  } else if (dstIp.startsWith('192.168.1.') && ack === 1) {
    matchedRule = 3;
    action = 'ALLOW';
    reason = 'Rule 3 Match: Inbound TCP packet with ACK=1 (belongs to an established outbound connection).';
  } else if (dstIp.startsWith('192.168.1.') && ack === 0) {
    matchedRule = 4;
    action = 'DROP';
    reason = 'Rule 4 Match: Inbound connection initiation request (ACK=0) to arbitrary internal host blocked!';
  }

  const row = document.getElementById('sec8-acl-row-' + matchedRule);
  if (row) row.style.background = action === 'ALLOW' ? 'var(--accent-light)' : 'var(--danger-light)';

  const out = document.getElementById('fw-result-box');
  if (out) {
    out.innerHTML = `
      <div style="font-weight:700; font-size:1.05rem; color:${action === 'ALLOW' ? 'var(--accent-text)' : 'var(--danger-text)'};">
        Firewall Action: ${action} (Matched Rule #${matchedRule})
      </div>
      <div style="font-size:0.9rem; margin-top:0.35rem; color:var(--text-secondary);">${reason}</div>
    `;
  }
}

// --- CHAPTER 9 INTERACTIVES ---
const MIB_DATA = {
  system: {
    oid: '1.3.6.1.2.1.1',
    name: 'system',
    desc: 'Provides overall identification and hardware description of the managed entity.',
    vars: [
      { name: 'sysDescr (1.1)', type: 'DisplayString', access: 'read-only', desc: 'Hardware, OS release, and system software version.' },
      { name: 'sysObjectID (1.2)', type: 'OBJECT IDENTIFIER', access: 'read-only', desc: 'Vendor-specific identification in enterprise MIB tree.' },
      { name: 'sysUpTime (1.3)', type: 'TimeTicks', access: 'read-only', desc: 'Time in 100ths of a second since device network software rebooted.' },
      { name: 'sysContact (1.4)', type: 'DisplayString', access: 'read-write', desc: 'Contact person for this node (e.g. noc@kau.edu.sa).' },
      { name: 'sysName (1.5)', type: 'DisplayString', access: 'read-write', desc: 'Fully-qualified domain name of node.' }
    ]
  },
  interfaces: {
    oid: '1.3.6.1.2.1.2',
    name: 'interfaces',
    desc: 'Information regarding the subnetwork interfaces of the managed device (Ethernet, Serial, Loopback).',
    vars: [
      { name: 'ifNumber (2.1)', type: 'INTEGER', access: 'read-only', desc: 'Total number of network interfaces present.' },
      { name: 'ifTable (2.2)', type: 'SEQUENCE OF', access: 'not-accessible', desc: 'Interface entry table containing MTU, speed, in/out octets, errors.' },
      { name: 'ifInOctets (2.2.1.10)', type: 'Counter32', access: 'read-only', desc: 'Total bytes received on interface (used to calculate link utilization).' },
      { name: 'ifOutOctets (2.2.1.16)', type: 'Counter32', access: 'read-only', desc: 'Total bytes transmitted out of interface.' },
      { name: 'ifInErrors (2.2.1.14)', type: 'Counter32', access: 'read-only', desc: 'Number of inbound packets with CRC/framing errors dropped.' }
    ]
  },
  ip: {
    oid: '1.3.6.1.2.1.4',
    name: 'ip',
    desc: 'Management variables related to Internet Protocol version 4 processing on the device.',
    vars: [
      { name: 'ipForwarding (4.1)', type: 'INTEGER (1=yes, 2=no)', access: 'read-write', desc: 'Specifies whether this entity acts as an IP router forwarding datagrams.' },
      { name: 'ipDefaultTTL (4.2)', type: 'INTEGER', access: 'read-write', desc: 'Default Time-to-Live value inserted in IP headers originated by device.' },
      { name: 'ipInReceives (4.3)', type: 'Counter32', access: 'read-only', desc: 'Total datagrams received from interfaces.' },
      { name: 'ipInDiscards (4.8)', type: 'Counter32', access: 'read-only', desc: 'Input datagrams discarded due to lack of buffer space.' },
      { name: 'ipRouteTable (4.21)', type: 'SEQUENCE OF', access: 'not-accessible', desc: 'Current IP routing table (Destinations, Next-Hop, Metrics).' }
    ]
  },
  tcp: {
    oid: '1.3.6.1.2.1.6',
    name: 'tcp',
    desc: 'TCP connection state information, retransmission parameters, and segment counters.',
    vars: [
      { name: 'tcpRtoMin (6.2)', type: 'INTEGER', access: 'read-only', desc: 'Minimum Retransmission Timeout value in milliseconds.' },
      { name: 'tcpRtoMax (6.3)', type: 'INTEGER', access: 'read-only', desc: 'Maximum Retransmission Timeout value in milliseconds.' },
      { name: 'tcpActiveOpens (6.5)', type: 'Counter32', access: 'read-only', desc: 'Number of transitions from CLOSED to SYN-SENT.' },
      { name: 'tcpPassiveOpens (6.6)', type: 'Counter32', access: 'read-only', desc: 'Number of transitions from LISTEN to SYN-RCVD.' },
      { name: 'tcpCurrEstab (6.9)', type: 'Gauge32', access: 'read-only', desc: 'Current number of connections in ESTABLISHED or CLOSE-WAIT.' }
    ]
  },
  udp: {
    oid: '1.3.6.1.2.1.7',
    name: 'udp',
    desc: 'UDP statistics and listener port table.',
    vars: [
      { name: 'udpInDatagrams (7.1)', type: 'Counter32', access: 'read-only', desc: 'Total UDP datagrams delivered to application users.' },
      { name: 'udpNoPorts (7.2)', type: 'Counter32', access: 'read-only', desc: 'Received datagrams for which no application socket existed at port.' },
      { name: 'udpInErrors (7.3)', type: 'Counter32', access: 'read-only', desc: 'UDP datagrams discarded due to invalid checksum or header format.' },
      { name: 'udpOutDatagrams (7.4)', type: 'Counter32', access: 'read-only', desc: 'Total UDP datagrams sent from this entity.' }
    ]
  }
};

function inspectMibNode(groupId) {
  const g = MIB_DATA[groupId];
  if (!g) return;

  ['system', 'interfaces', 'ip', 'tcp', 'udp'].forEach(id => {
    const btn = document.getElementById('sec9-mib-' + id);
    if (btn) {
      if (id === groupId) {
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
      } else {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
      }
    }
  });

  const out = document.getElementById('sec9-mib-display');
  if (out) {
    out.innerHTML = `
      <div style="font-weight:700; font-size:1.05rem; margin-bottom:0.25rem; color:var(--text-primary);">${g.name} Group (OID: ${g.oid})</div>
      <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">${g.desc}</p>
      <table style="width:100%; border-collapse:collapse; font-size:0.8rem; border:1px solid var(--border);">
        <thead>
          <tr style="background:var(--bg-secondary); border-bottom:1px solid var(--border); text-align:left;">
            <th style="padding:6px 8px;">Variable</th>
            <th style="padding:6px 8px;">ASN.1 Type</th>
            <th style="padding:6px 8px;">Access</th>
            <th style="padding:6px 8px;">Description</th>
          </tr>
        </thead>
        <tbody>
          ${g.vars.map(v => `
            <tr style="border-bottom:1px solid var(--border-light);">
              <td style="padding:6px 8px; font-weight:600; font-family:monospace;">${v.name}</td>
              <td style="padding:6px 8px; color:var(--primary);">${v.type}</td>
              <td style="padding:6px 8px;">${v.access}</td>
              <td style="padding:6px 8px; color:var(--text-secondary);">${v.desc}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  }
}

function calcSec9TLV() {
  const type = document.getElementById('tlv-type-input')?.value || 'int';
  const valStr = document.getElementById('tlv-val-input')?.value.trim() || '257';

  let tagHex = '02';
  let lenHex = '01';
  let valHex = '00';
  let explanation = '';

  if (type === 'int') {
    tagHex = '02';
    const num = parseInt(valStr, 10) || 0;
    if (num >= 0 && num <= 127) {
      lenHex = '01';
      valHex = num.toString(16).toUpperCase().padStart(2, '0');
      explanation = `INTEGER ${num} fits in a single byte (0x${valHex}).`;
    } else if (num >= 128 && num <= 32767) {
      lenHex = '02';
      valHex = [(num >> 8) & 0xFF, num & 0xFF].map(b => b.toString(16).toUpperCase().padStart(2, '0')).join(' ');
      explanation = `INTEGER ${num} requires 2 bytes in big-endian representation.`;
    } else {
      lenHex = '04';
      valHex = [(num >> 24) & 0xFF, (num >> 16) & 0xFF, (num >> 8) & 0xFF, num & 0xFF].map(b => b.toString(16).toUpperCase().padStart(2, '0')).join(' ');
      explanation = `INTEGER ${num} encoded across 4 bytes.`;
    }
  } else {
    tagHex = '04';
    const len = valStr.length;
    lenHex = len.toString(16).toUpperCase().padStart(2, '0');
    valHex = Array.from(valStr).map(ch => ch.charCodeAt(0).toString(16).toUpperCase().padStart(2, '0')).join(' ');
    explanation = `OCTET STRING "${valStr}" contains ${len} ASCII characters.`;
  }

  const fullBytes = `${tagHex} ${lenHex} ${valHex}`;

  const out = document.getElementById('tlv-result-box');
  if (out) {
    out.innerHTML = `
      <div class="calc-step">&bull; <strong>Tag (Type):</strong> <code>0x${tagHex}</code> (${type === 'int' ? 'INTEGER' : 'OCTET STRING'})</div>
      <div class="calc-step">&bull; <strong>Length:</strong> <code>0x${lenHex}</code> (${parseInt(lenHex, 16)} byte${parseInt(lenHex, 16) > 1 ? 's' : ''})</div>
      <div class="calc-step">&bull; <strong>Value Bytes:</strong> <code>${valHex}</code></div>
      <div class="calc-step" style="font-weight:700; font-size:1.05rem; color:var(--accent-text); margin-top:0.35rem;">
        Complete BER TLV Byte Sequence: <strong><code>${fullBytes}</code></strong> (${1 + 1 + parseInt(lenHex, 16)} bytes total)
      </div>
      <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.25rem;">${explanation}</div>
    `;
  }
}

// Universal Client-side LaTeX-to-HTML Sanitizer & Renderer
function replaceFractionsJS(s) {
  while (s.includes('\\frac')) {
    const idx = s.indexOf('\\frac');
    const open1 = s.indexOf('{', idx);
    if (open1 === -1) break;
    let depth = 1;
    let pos1 = open1 + 1;
    while (pos1 < s.length && depth > 0) {
      if (s[pos1] === '{') depth++;
      else if (s[pos1] === '}') depth--;
      pos1++;
    }
    if (depth !== 0) break;
    let num = s.substring(open1 + 1, pos1 - 1);

    const open2 = s.indexOf('{', pos1);
    if (open2 === -1 || s.substring(pos1, open2).trim() !== '') break;
    depth = 1;
    let pos2 = open2 + 1;
    while (pos2 < s.length && depth > 0) {
      if (s[pos2] === '{') depth++;
      else if (s[pos2] === '}') depth--;
      pos2++;
    }
    if (depth !== 0) break;
    let denom = s.substring(open2 + 1, pos2 - 1);

    num = replaceFractionsJS(num);
    denom = replaceFractionsJS(denom);

    const repl = '<span class="math-frac"><span class="math-num">' + num + '</span><span class="math-denom">' + denom + '</span></span>';
    s = s.substring(0, idx) + repl + s.substring(pos2);
  }
  return s;
}

function cleanMathString(m) {
  if (!m) return '';
  let s = m;
  // Handle ASCII bell and raw pprox / escapes
  s = s.replace(/\x07pprox/g, '&approx;')
       .replace(/\\approx/g, '&approx;')
       .replace(/(?<!&a)pprox/g, '&approx;')
       .replace(/\x07lpha/g, '&alpha;')
       .replace(/\\alpha/g, '&alpha;')
       .replace(/\x08eta/g, '&beta;')
       .replace(/\\beta/g, '&beta;')
       .replace(/\x0crac/g, '\\frac');

  // Strip \left and \right FIRST before \le to prevent &le;ft(
  s = s.replace(/\\left\s*([(\[|])/g, '$1')
       .replace(/\\right\s*([)\]|])/g, '$1')
       .replace(/\\left/g, '')
       .replace(/\\right/g, '')
       .replace(/\\max/g, 'max')
       .replace(/\\min/g, 'min')
       .replace(/\\times/g, '&times;')
       .replace(/\\cdot/g, '&sdot;')
       .replace(/\\le/g, '&le;')
       .replace(/\\ge/g, '&ge;')
       .replace(/\\ne/g, '&ne;')
       .replace(/\\in/g, '&isin;')
       .replace(/\\notin/g, '&notin;')
       .replace(/\\infty/g, '&infin;')
       .replace(/\\implies/g, '&rArr;')
       .replace(/\\to/g, '&rarr;')
       .replace(/\\leftarrow/g, '&larr;')
       .replace(/\\equiv/g, '&equiv;')
       .replace(/\\oplus/g, '&oplus;')
       .replace(/\\mu/g, '&mu;')
       .replace(/\\sigma/g, '&sigma;')
       .replace(/\\lambda/g, '&lambda;')
       .replace(/\\Delta/g, '&Delta;')
       .replace(/\\delta/g, '&delta;')
       .replace(/\\sum/g, '&sum;')
       .replace(/\\prod/g, '&prod;')
       .replace(/\\lim/g, 'lim')
       .replace(/\\mathbf\{([^}]+)\}/g, '<strong>$1</strong>')
       .replace(/\\mathbf\s+/g, '')
       .replace(/\\mathit\{([^}]+)\}/g, '<em>$1</em>')
       .replace(/\\text\{([^}]+)\}/g, '$1')
       .replace(/\\pmod\{([^}]+)\}/g, '(mod $1)')
       .replace(/\\bmod/g, 'mod')
       .replace(/\\[,;]\s*/g, '&nbsp;')
       .replace(/\\quad/g, '&emsp;').replace(/\\qquad/g, '&emsp;&emsp;').replace(/\\\s/g, '&nbsp;');

  // Sqrt before fractions
  s = s.replace(/\\sqrt\{([^{}]+)\}/g, '&radic;<span style="text-decoration:overline">$1</span>');

  // Balanced fraction parser
  s = replaceFractionsJS(s);

  // Binomial
  s = s.replace(/\\binom\{([^{}]+)\}\{([^{}]+)\}/g, '<span class="math-frac"><span class="math-num">$1</span><span class="math-denom">$2</span></span>');

  // Subscripts & Superscripts
  s = s.replace(/_\{([^}]+)\}/g, '<sub>$1</sub>')
       .replace(/_([a-zA-Z0-9]+)/g, '<sub>$1</sub>')
       .replace(/\^\{([^}]+)\}/g, '<sup>$1</sup>')
       .replace(/\^([a-zA-Z0-9]+)/g, '<sup>$1</sup>');

  return s;
}

function renderMathInDOM() {
  // 1. Clean elements explicitly marked with .math-display or .math-inline
  document.querySelectorAll('.math-display, .math-inline').forEach(el => {
    if (el.dataset.mathCleaned) return;
    if (el.innerHTML.includes('\\') || el.innerHTML.includes('_') || el.innerHTML.includes('^') || el.innerHTML.includes('pprox')) {
      el.innerHTML = cleanMathString(el.innerHTML);
    }
    el.dataset.mathCleaned = 'true';
  });

  // 2. Walk raw text nodes for $$ or $ delimiters
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  const nodesToReplace = [];

  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.parentElement && (node.parentElement.tagName === 'SCRIPT' || node.parentElement.tagName === 'STYLE' || node.parentElement.tagName === 'CODE' || node.parentElement.tagName === 'PRE' || node.parentElement.closest('.math-display') || node.parentElement.closest('.math-inline'))) {
      continue;
    }
    if (node.nodeValue && (node.nodeValue.includes('$$') || node.nodeValue.includes('$') || node.nodeValue.includes('\\text{'))) {
      nodesToReplace.push(node);
    }
  }

  nodesToReplace.forEach(node => {
    let t = node.nodeValue;
    if (!t) return;

    t = t.replace(/\$\$([\s\S]*?)\$\$/g, (match, math) => {
      return '<div class="math-display">' + cleanMathString(math) + '</div>';
    });

    t = t.replace(/(?<![\\\$])\$([^\$\n]+?)\$(?!\$)/g, (match, math) => {
      return '<span class="math-inline">' + cleanMathString(math) + '</span>';
    });

    if (t !== node.nodeValue) {
      const span = document.createElement('span');
      span.innerHTML = t;
      if (node.parentNode) {
        node.parentNode.replaceChild(span, node);
      }
    }
  });
}

function initSectionInteractives() {
  if (typeof calcSec1Delay === 'function') calcSec1Delay();
  if (typeof calcSec3Checksum === 'function') calcSec3Checksum();
  if (typeof calcSec4CIDR === 'function') calcSec4CIDR();
  if (typeof calcSec6CDMA === 'function') calcSec6CDMA();
  if (typeof calcSec7TokenBucket === 'function') calcSec7TokenBucket();
  if (typeof calcSec8RSA === 'function') calcSec8RSA();
  if (typeof stepSec8Auth === 'function') stepSec8Auth('ap4');
  if (typeof testSec8Firewall === 'function') testSec8Firewall();
  if (typeof inspectMibNode === 'function') inspectMibNode('system');
  if (typeof calcSec9TLV === 'function') calcSec9TLV();
  if (typeof renderMathInDOM === 'function') renderMathInDOM();
}

// ==========================================
// GLOSSARY & FLASHCARDS & EXAMS
// ==========================================
const GLOSSARY_TERMS = [
  { term: "Access Network", def: "The network that physically connects an end system to the first router (edge router) on a path to another end system." },
  { term: "AIMD", def: "Additive-Increase Multiplicative-Decrease: TCP's congestion control algorithm that linearly increases cwnd by 1 MSS per RTT and halves cwnd upon loss." },
  { term: "Application Programming Interface (API)", def: "The set of software rules that an application program uses to request network services from the operating system." },
  { term: "ARP", def: "Address Resolution Protocol: Resolves a 32-bit IP address to a 48-bit physical MAC address on a local subnet." },
  { term: "Autonomous System (AS)", def: "A collection of routers and subnets under common administrative control that presents a coherent routing policy to the Internet." },
  { term: "BGP", def: "Border Gateway Protocol: The standard inter-AS routing protocol in the Internet, using path vectors and commercial policies." },
  { term: "BitTorrent", def: "A popular peer-to-peer file sharing protocol employing tit-for-tat incentives and rarest-first chunk replication." },
  { term: "Bottleneck Link", def: "The communication link on an end-to-end path whose transmission rate limits the maximum throughput of the flow." },
  { term: "CDMA", def: "Code Division Multiple Access: A channel partitioning protocol that assigns orthogonal chip sequences to users allowing simultaneous transmission on the same frequency." },
  { term: "CIDR", def: "Classless Inter-Domain Routing: An IP addressing standard allocating variable-length prefix addresses denoted by a.b.c.d/x." },
  { term: "Circuit Switching", def: "A networking approach that establishes a dedicated physical channel (circuit) with reserved resources before communication begins." },
  { term: "Client-Server Architecture", def: "An application architecture where an always-on server host services requests from many client hosts." },
  { term: "Conditional GET", def: "An HTTP GET request containing an If-Modified-Since header, allowing the server to return 304 Not Modified if the object has not changed." },
  { term: "CSMA/CD", def: "Carrier Sense Multiple Access with Collision Detection: A random access protocol used in Ethernet where nodes abort transmission upon sensing a collision." },
  { term: "CSMA/CA", def: "Carrier Sense Multiple Access with Collision Avoidance: A wireless MAC protocol (802.11) using DIFS, SIFS, ACK frames, and RTS/CTS reservations." },
  { term: "DASH", def: "Dynamic Adaptive Streaming over HTTP: A multimedia video streaming protocol where the client player dynamically requests chunks of different bitrates." },
  { term: "Demultiplexing", def: "The process of delivering the payload of a transport-layer segment to the correct socket based on port numbers." },
  { term: "DHCP", def: "Dynamic Host Configuration Protocol: A 4-step DORA protocol automatically assigning IP address, subnet mask, default gateway, and DNS to a host." },
  { term: "Dijkstra's Algorithm", def: "A link-state routing algorithm that calculates the least-cost paths from a single source node to all other network nodes." },
  { term: "DNS", def: "Domain Name System: The Internet's distributed, hierarchical directory service translating hostnames to IP addresses." },
  { term: "Encapsulation", def: "The process where each protocol layer wraps data received from the layer above with its own protocol header." },
  { term: "Ethernet", def: "The dominant wired link-layer technology (IEEE 802.3) using 48-bit MAC addresses and CSMA/CD." },
  { term: "Fast Retransmit", def: "TCP mechanism where receipt of 3 duplicate ACKs triggers retransmission of the missing segment before the timeout timer expires." },
  { term: "Firewall", def: "A network security gateway that isolates an organization's internal network from the Internet by filtering packets based on header rules." },
  { term: "Flow Control", def: "A speed-matching service that prevents a fast sender from overflowing the receive buffer of a slow receiver (e.g., TCP rwnd)." },
  { term: "Forwarding", def: "The router's local hardware action of moving a packet from an incoming interface to an outgoing interface." },
  { term: "Go-Back-N (GBN)", def: "A pipelined reliable protocol using cumulative ACKs and a single timer for the oldest unacknowledged packet." },
  { term: "Head-of-Line (HOL) Blocking", def: "A queuing phenomenon where a blocked packet at the head of a line prevents all following packets from moving forward." },
  { term: "HTTP", def: "Hypertext Transfer Protocol: The stateless application-layer protocol of the World Wide Web running over TCP." },
  { term: "ICMP", def: "Internet Control Message Protocol: Used by hosts and routers to communicate network-layer control and error messages (e.g., ping, traceroute)." },
  { term: "IPsec", def: "A suite of protocols (AH and ESP) providing confidentiality, integrity, and authentication at the network (IP) layer." },
  { term: "IPv4", def: "Internet Protocol version 4: The 32-bit connectionless best-effort network-layer protocol of the Internet." },
  { term: "IPv6", def: "Internet Protocol version 6: Successor to IPv4 providing 128-bit addresses and a streamlined 40-byte base header." },
  { term: "Leaky Bucket", def: "A traffic policing mechanism that smooths bursty traffic into a strictly constant-rate output stream." },
  { term: "MAC Address", def: "A 48-bit physical link-layer address permanently burned into a Network Interface Controller (NIC)." },
  { term: "Multiplexing", def: "Gathering data chunks from multiple application sockets, adding transport headers, and passing them to the network layer." },
  { term: "NAT", def: "Network Address Translation: Translates private IP addresses and ports to a single public IP address at an edge router." },
  { term: "Nonce", def: "A random number used only once in an authentication protocol to defeat replay and playback attacks." },
  { term: "OSPF", def: "Open Shortest Path First: A widely used link-state intra-AS routing protocol using Dijkstra's algorithm and hierarchical areas." },
  { term: "Packet Switching", def: "A networking method that divides messages into packets, transmitting them hop-by-hop across shared links using store-and-forward." },
  { term: "Pipelining", def: "A technique allowing a sender to transmit multiple packets without waiting for acknowledgments, dramatically improving utilization." },
  { term: "Propagation Delay", def: "The time required for a physical bit to propagate across the physical medium from one end of a link to the other (d / s)." },
  { term: "RDT", def: "Reliable Data Transfer: A framework of protocols (rdt 1.0 to 3.0) guaranteeing error-free, lossless, in-order byte delivery." },
  { term: "RIP", def: "Routing Information Protocol: A distance-vector intra-AS routing protocol measuring path distance in hop counts (maximum 15)." },
  { term: "Router", def: "A Layer-3 packet switch that determines packet paths using routing tables and forwards IP datagrams between links." },
  { term: "Routing", def: "The network-wide control-plane process that determines the end-to-end paths packets take from source to destination." },
  { term: "RSA", def: "A widely used public-key cryptographic algorithm based on the difficulty of factoring large prime numbers." },
  { term: "RTP", def: "Real-Time Transport Protocol: Application-layer protocol running over UDP carrying sequence numbers and timestamps for streaming." },
  { term: "Selective Repeat (SR)", def: "A pipelined reliable protocol where the receiver buffers out-of-order packets and individually acknowledges each packet." },
  { term: "Self-Learning Switch", def: "A link-layer device that builds its MAC forwarding table automatically by observing the source MAC addresses of incoming frames." },
  { term: "SIP", def: "Session Initiation Protocol: A text-based signaling protocol for setting up, modifying, and tearing down VoIP calls." },
  { term: "Slotted ALOHA", def: "A random access protocol synchronizing transmissions into time slots, achieving a maximum channel efficiency of 36.8%." },
  { term: "Slow Start", def: "Initial phase of TCP congestion control where cwnd begins at 1 MSS and doubles every RTT (exponential growth)." },
  { term: "SMTP", def: "Simple Mail Transfer Protocol: The push protocol for transmitting email messages between mail servers over TCP port 25." },
  { term: "Socket", def: "The software interface (API) between an application process and the transport-layer protocol stack." },
  { term: "SSL / TLS", def: "Secure Sockets Layer / Transport Layer Security: Cryptographic protocol providing confidentiality and integrity for TCP traffic." },
  { term: "Store-and-Forward", def: "A packet switch must receive the entire packet before transmitting the first bit onto the outbound link." },
  { term: "Subnet", def: "A portion of a larger network whose devices can reach each other directly at the link layer without traversing a router." },
  { term: "TCP", def: "Transmission Control Protocol: A connection-oriented, reliable, byte-stream transport protocol providing flow and congestion control." },
  { term: "Three-Way Handshake", def: "The 3-step message exchange (SYN, SYN-ACK, ACK) used to establish a TCP connection." },
  { term: "Time-to-Live (TTL)", def: "An 8-bit field in the IPv4 header decremented by each router to prevent packets from looping infinitely." },
  { term: "Token Bucket", def: "A traffic policing mechanism that limits average rate to r while permitting controlled bursts up to bucket capacity b." },
  { term: "Transmission Delay", def: "The time required to push all bits of a packet onto the link (L / R)." },
  { term: "UDP", def: "User Datagram Protocol: A lightweight, connectionless, unreliable transport protocol with minimal 8-byte header overhead." },
  { term: "VLAN", def: "Virtual Local Area Network: Logical partitioning of a physical switch into multiple isolated broadcast domains." },
  { term: "VPN", def: "Virtual Private Network: A secure private overlay network constructed across the public Internet using IPsec tunneling." }
];

function initGlossary() {
  const container = document.getElementById('glossary-list');
  if (!container) return;
  container.innerHTML = GLOSSARY_TERMS.map(g => `
    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1rem;">
      <h4 style="color:var(--primary-text); font-size:1rem; margin-bottom:0.25rem;">${g.term}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary); line-height:1.5;">${g.def}</p>
    </div>
  `).join('');
}

function filterGlossary() {
  const q = document.getElementById('glossary-filter').value.toLowerCase();
  const filtered = GLOSSARY_TERMS.filter(g => g.term.toLowerCase().includes(q) || g.def.toLowerCase().includes(q));
  const container = document.getElementById('glossary-list');
  if (!container) return;
  container.innerHTML = filtered.map(g => `
    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1rem;">
      <h4 style="color:var(--primary-text); font-size:1rem; margin-bottom:0.25rem;">${g.term}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary); line-height:1.5;">${g.def}</p>
    </div>
  `).join('');
}

// Flashcards
const ALL_FLASHCARDS = GLOSSARY_TERMS.map((g, idx) => ({
  id: idx,
  ch: idx < 8 ? 'ch1' : idx < 16 ? 'ch2' : idx < 26 ? 'ch3' : idx < 36 ? 'ch4' : idx < 46 ? 'ch5' : idx < 52 ? 'ch6' : idx < 58 ? 'ch7' : idx < 65 ? 'ch8' : 'ch9',
  category: idx < 8 ? 'Chapter 1' : idx < 16 ? 'Chapter 2' : idx < 26 ? 'Chapter 3' : idx < 36 ? 'Chapter 4' : idx < 46 ? 'Chapter 5' : idx < 52 ? 'Chapter 6' : idx < 58 ? 'Chapter 7' : idx < 65 ? 'Chapter 8' : 'Chapter 9',
  front: g.term,
  back: g.def
}));

function filterFlashcards(ch, btn) {
  if (btn) {
    btn.closest('div').querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  if (ch === 'all') {
    filteredFlashcards = [...ALL_FLASHCARDS];
  } else {
    filteredFlashcards = ALL_FLASHCARDS.filter(f => f.ch === ch);
  }
  activeFlashcardIdx = 0;
  renderFlashcard();
}

function renderFlashcard() {
  if (!filteredFlashcards.length) filteredFlashcards = [...ALL_FLASHCARDS];
  const cur = filteredFlashcards[activeFlashcardIdx];
  document.getElementById('fc-category').innerText = cur.category;
  document.getElementById('fc-front-text').innerText = cur.front;
  document.getElementById('fc-back-text').innerText = cur.back;
  document.getElementById('fc-progress').innerText = `${activeFlashcardIdx + 1} / ${filteredFlashcards.length}`;
  document.getElementById('active-flashcard-inner').classList.remove('flipped');
}

function flipActiveCard() {
  document.getElementById('active-flashcard-inner').classList.toggle('flipped');
}

function nextFlashcard() {
  if (activeFlashcardIdx < filteredFlashcards.length - 1) {
    activeFlashcardIdx++;
  } else {
    activeFlashcardIdx = 0;
  }
  renderFlashcard();
}

function prevFlashcard() {
  if (activeFlashcardIdx > 0) {
    activeFlashcardIdx--;
  } else {
    activeFlashcardIdx = filteredFlashcards.length - 1;
  }
  renderFlashcard();
}

// ==========================================
// COMPREHENSIVE FINAL EXAM
// ==========================================
const EXAM_POOL = [
  {
    "q": "P1 Units Conversion: How many bits are in 3 Megabytes (3 MB) using decimal network notation (1 MB = 10^6 bytes)?",
    "opts": [
      "3,000,000 bits",
      "24,000,000 bits",
      "25,165,824 bits",
      "3,145,728 bits"
    ],
    "ans": 1,
    "exp": "3 MB = 3 * 10^6 bytes. Since each byte contains 8 bits, 3 * 10^6 * 8 = 24,000,000 bits (24 Mbits) (Study Guide P1)."
  },
  {
    "q": "P2 Delay Dominance: A 1,000-byte packet is transmitted over a 20 Mbps fiber link of length 4,000 km (speed s = 2*10^8 m/s). Which delay component dominates?",
    "opts": [
      "Transmission delay (d_trans = 20 ms)",
      "Propagation delay (d_prop = 20 ms)",
      "Queuing delay (d_queue = 50 ms)",
      "Processing delay (d_proc = 10 ms)"
    ],
    "ans": 1,
    "exp": "d_trans = (1,000 * 8 bits) / (20 * 10^6 bps) = 0.4 ms. d_prop = 4,000,000 m / (2 * 10^8 m/s) = 20 ms. Propagation delay (20 ms) is 50x larger than transmission delay (0.4 ms), so propagation dominates (Study Guide P2a)."
  },
  {
    "q": "P3 Store-and-Forward: A host sends three 5,000-bit packets back-to-back across a single store-and-forward router (two links, each R = 1 Mbps). Neglecting propagation, processing, and queuing delay, when does the destination receive the last bit of the third packet?",
    "opts": [
      "10 ms",
      "15 ms",
      "20 ms",
      "30 ms"
    ],
    "ans": 2,
    "exp": "Transmission time per packet L/R = 5,000 / 10^6 = 5 ms. Packet 1 reaches the destination at 2 * 5 = 10 ms. Packets 2 and 3 arrive pipelined at 5 ms intervals thereafter: 15 ms and 20 ms. Total time = (N + P - 1) * (L/R) = (2 + 3 - 1) * 5 ms = 20 ms (Study Guide P3b)."
  },
  {
    "q": "P4 Caravan Analogy: An 8-car caravan travels between toll booths 150 km apart at 100 km/h. Each booth services 1 car every 15 seconds. How long after the caravan starts at the first booth is the entire caravan lined up before the second booth?",
    "opts": [
      "90 minutes",
      "92 minutes",
      "105 minutes",
      "80 minutes"
    ],
    "ans": 1,
    "exp": "Time to service all 8 cars at first booth = 8 * 15 s = 120 s (2 min). Propagation time for cars at 100 km/h = 150 km / 100 km/h = 1.5 hours (90 min). Total time = 2 min + 90 min = 92 minutes (1 hr 32 min) (Study Guide P4a)."
  },
  {
    "q": "P5 Traffic Intensity: Packets of 500 bytes arrive at a router queue at an average rate of a = 300 packets/sec. The transmission link rate is R = 1.5 Mbps. What is the traffic intensity (La/R)?",
    "opts": [
      "0.40",
      "0.80",
      "1.00",
      "1.25"
    ],
    "ans": 1,
    "exp": "L = 500 bytes = 4,000 bits. Arrival bit rate La = 4,000 * 300 = 1,200,000 bps = 1.2 Mbps. Traffic intensity = La/R = 1.2 Mbps / 1.5 Mbps = 0.80 (Study Guide P5)."
  },
  {
    "q": "P6 Bottleneck Throughput: A file transfer traverses three consecutive links with capacities R1 = 10 Mbps, R2 = 2 Mbps, and R3 = 5 Mbps. What is the maximum theoretical end-to-end throughput?",
    "opts": [
      "10 Mbps",
      "5 Mbps",
      "2 Mbps",
      "17 Mbps"
    ],
    "ans": 2,
    "exp": "End-to-end throughput is constrained by the bottleneck link: min(R1, R2, R3) = min(10, 2, 5) = 2 Mbps (Study Guide P6)."
  },
  {
    "q": "P7 Circuit vs Packet Switching: On a 10 Mbps link, each user requires 1 Mbps when transmitting, but transmits only 10% of the time. How many users can circuit switching support, and what is packet switching's capacity?",
    "opts": [
      "Circuit: 10 users; Packet: Supports 35+ users with <0.04% overload probability",
      "Circuit: 35 users; Packet: 10 users",
      "Circuit: 100 users; Packet: 10 users",
      "Circuit: 1 user; Packet: 10 users"
    ],
    "ans": 0,
    "exp": "Circuit switching statically reserves 1 Mbps per user: 10 Mbps / 1 Mbps = 10 users. Packet switching multiplexes users statistically; with 35 users, the probability of more than 10 active simultaneously is sum_{k=11}^{35} binom(35,k) (0.1)^k (0.9)^{35-k} \u2248 0.0004 (0.04%) (Study Guide P7)."
  },
  {
    "q": "P8 Protocol Layers: In the 5-layer Internet protocol stack, which layer is responsible for process-to-process message transfer, and what is its packet called?",
    "opts": [
      "Network Layer (Datagram)",
      "Transport Layer (Segment)",
      "Link Layer (Frame)",
      "Application Layer (Message)"
    ],
    "ans": 1,
    "exp": "The Transport layer provides logical process-to-process communication; its packet of data is called a Segment (\u00a71.5.1, Study Guide P8)."
  },
  {
    "q": "P9 HTTP Response Time: An HTML page references 4 small image objects on the same server. Assuming RTT = 50 ms and negligible transmission time, what is the total elapsed time using Non-persistent HTTP without parallel TCP connections?",
    "opts": [
      "250 ms (5 RTT)",
      "500 ms (10 RTT)",
      "150 ms (3 RTT)",
      "300 ms (6 RTT)"
    ],
    "ans": 1,
    "exp": "Non-persistent HTTP requires 1 RTT for TCP handshake + 1 RTT for HTTP request/response per object (2 RTT per object). For 1 base HTML + 4 images (5 objects total): 5 * 2 RTT = 10 RTT = 10 * 50 ms = 500 ms (Study Guide P9)."
  },
  {
    "q": "P10 HTTP Status Codes: What status code is returned by a web server in response to a Conditional GET when the cached copy is still fresh and unmodified?",
    "opts": [
      "200 OK",
      "301 Moved Permanently",
      "304 Not Modified",
      "404 Not Found"
    ],
    "ans": 2,
    "exp": "The server responds with '304 Not Modified' and an empty message body, saving bandwidth and transmission time (Study Guide P10)."
  },
  {
    "q": "P11 Cookie Architecture: Which of the following is NOT one of the four essential components of HTTP cookies?",
    "opts": [
      "A Set-Cookie: header in the HTTP response",
      "A Cookie: header in subsequent HTTP requests",
      "A cookie file kept on the user's end system and managed by the browser",
      "A public-key digital certificate signed by a root CA"
    ],
    "ans": 3,
    "exp": "Cookies rely on (1) Set-Cookie response header, (2) Cookie request header, (3) client cookie file, and (4) backend database on the web server. CA certificates are used by TLS, not cookies (\u00a72.2.4, Study Guide P11)."
  },
  {
    "q": "P12 Web Caching: An institutional network has a 40% cache hit rate. Accessing an object from the origin server takes 2.01 seconds; accessing it from the local proxy cache takes 0.01 seconds. What is the average response time?",
    "opts": [
      "1.21 seconds",
      "0.81 seconds",
      "2.00 seconds",
      "1.01 seconds"
    ],
    "ans": 0,
    "exp": "Average delay = (hit_rate * cache_delay) + (miss_rate * origin_delay) = (0.40 * 0.01 s) + (0.60 * 2.01 s) = 0.004 + 1.206 = 1.21 seconds (Study Guide P12)."
  },
  {
    "q": "P13 Mail Protocols: Why does an email client use POP3 or IMAP to retrieve messages from a mail server instead of SMTP?",
    "opts": [
      "SMTP is a push protocol designed for sending; POP3/IMAP are pull protocols designed for retrieval",
      "SMTP cannot transmit text",
      "SMTP requires UDP while POP3 uses TCP",
      "SMTP is only used inside local area networks"
    ],
    "ans": 0,
    "exp": "SMTP is a push protocol: the sending host pushes mail to the receiving server. A recipient's user agent cannot use SMTP to pull mail from its mailbox; it must use a pull protocol like POP3, IMAP, or HTTP (\u00a72.3, Study Guide P13)."
  },
  {
    "q": "P14 DNS Records: If a company wants to route incoming email addressed to 'user@company.com' to mail server 'mail.company.com', which DNS Resource Record must it configure?",
    "opts": [
      "Type A record",
      "Type NS record",
      "Type MX record",
      "Type CNAME record"
    ],
    "ans": 2,
    "exp": "Type MX (Mail Exchange) records specify the mail server responsible for accepting messages on behalf of a domain name (Study Guide P14)."
  },
  {
    "q": "P15 P2P Distribution: In peer-to-peer (P2P) file distribution, why does the distribution time remain relatively constant as the number of peers N grows large, whereas client-server time grows linearly?",
    "opts": [
      "P2P uses UDP instead of TCP",
      "Each peer acts as both a consumer and an upload distributor, contributing upload capacity to the swarm",
      "P2P bypasses physical routers",
      "Trackers store the entire file in memory"
    ],
    "ans": 1,
    "exp": "In P2P, as each peer joins to download the file, it simultaneously donates upload bandwidth (u_i) to assist in serving other peers, keeping distribution time bounded: D_p2p >= N*F / (u_s + sum u_i) (\u00a72.5.1, Study Guide P15)."
  },
  {
    "q": "P16 BitTorrent Strategy: In BitTorrent, which chunk selection strategy helps ensure that rare chunks are rapidly replicated throughout the swarm so they don't disappear?",
    "opts": [
      "First-come first-served",
      "Rarest-first",
      "Random selection",
      "Largest-chunk first"
    ],
    "ans": 1,
    "exp": "BitTorrent peers use 'rarest-first' to determine which chunk to download next, ensuring that rarest chunks are replicated quickly across peers (Study Guide P16)."
  },
  {
    "q": "P17 Demultiplexing: What information does a host's transport layer examine to demultiplex an incoming connectionless UDP segment to the correct socket?",
    "opts": [
      "Source IP address and Source Port number",
      "Destination IP address and Destination Port number",
      "4-tuple: Source IP, Source Port, Destination IP, Destination Port",
      "Sequence Number and ACK Number"
    ],
    "ans": 1,
    "exp": "UDP sockets are identified solely by a 2-tuple: (Destination IP address, Destination Port number). TCP sockets require the full 4-tuple (\u00a73.2, Study Guide P17)."
  },
  {
    "q": "P18 Internet Checksum: When calculating the 16-bit Internet Checksum, what operation must be performed when an addition of two 16-bit words produces a carry out of the most significant bit?",
    "opts": [
      "Discard the carry bit",
      "Add the carry bit back into the least significant bit (end-around carry wraparound)",
      "Invert the entire sum immediately",
      "Set the checksum to 0x0000"
    ],
    "ans": 1,
    "exp": "In 1's complement arithmetic, any overflow carry from the most significant bit must be wrapped around and added to the least significant bit (Study Guide P18)."
  },
  {
    "q": "P19 Reliable Transfer (rdt 2.0 flaw): Why was the rdt 2.0 stop-and-wait protocol flawed when deployed over a channel with bit errors?",
    "opts": [
      "It had no ACK or NAK packets",
      "It did not account for the fact that ACK or NAK packets themselves could be corrupted in transit",
      "It allowed packets to arrive out of order",
      "It required too many sequence number bits"
    ],
    "ans": 1,
    "exp": "rdt 2.0 introduced ACK and NAK, but did not handle the possibility that an ACK or NAK could be corrupted, leading to possible duplicate packet delivery. rdt 2.1 fixed this by adding 1-bit sequence numbers (\u00a73.4.1, Study Guide P19)."
  },
  {
    "q": "P20 Pipelining Utilization: Over a 1 Gbps cross-country link with RTT = 30 ms, transmitting a 1,000-byte packet (L/R = 8 \u00b5s) using Stop-and-Wait yields a channel utilization of only 0.027%. Approximately how many packets N must be pipelined in flight to achieve 100% link utilization?",
    "opts": [
      "10 packets",
      "125 packets",
      "3,751 packets",
      "65,535 packets"
    ],
    "ans": 2,
    "exp": "Utilization U = (N * L/R) / (RTT + L/R). For U = 1.0: N >= (RTT + L/R) / (L/R) = (30 ms + 0.008 ms) / 0.008 ms = 30.008 / 0.008 \u2248 3,751 packets (\u00a73.4.2, Study Guide P20)."
  },
  {
    "q": "P21 TCP Sequence & ACK: Host A sends Host B two consecutive TCP segments. Segment 1 contains 200 bytes with Sequence Number 1000. What are the sequence number of Segment 2 and the ACK number returned by Host B after receiving Segment 1?",
    "opts": [
      "Segment 2 Seq = 1200; ACK = 1200",
      "Segment 2 Seq = 1001; ACK = 1001",
      "Segment 2 Seq = 1200; ACK = 1000",
      "Segment 2 Seq = 1000; ACK = 1200"
    ],
    "ans": 0,
    "exp": "Segment 1 carries bytes 1000 through 1199 (200 bytes). The next byte is 1200, so Segment 2 has Seq = 1200. Host B sends ACK = 1200, indicating it has received all bytes up to 1199 and expects byte 1200 next (Study Guide P21)."
  },
  {
    "q": "P22 RTT Estimation: Given current EstimatedRTT = 40 ms and a newly measured SampleRTT = 80 ms, what is the new EstimatedRTT using TCP's standard EWMA formula with weight alpha = 0.125 (1/8)?",
    "opts": [
      "45 ms",
      "50 ms",
      "60 ms",
      "40 ms"
    ],
    "ans": 0,
    "exp": "EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT = (0.875 * 40 ms) + (0.125 * 80 ms) = 35 ms + 10 ms = 45 ms (\u00a73.5.3, Study Guide P22)."
  },
  {
    "q": "P23 Flow Control vs Congestion Control: What is the primary purpose of TCP's Flow Control mechanism (the Receive Window `rwnd`), and how does it differ from Congestion Control?",
    "opts": [
      "Flow control prevents the sender from overwhelming the receiver's buffer; congestion control prevents the sender from overwhelming network routers",
      "Flow control detects bit errors; congestion control retransmits lost packets",
      "Flow control sets the IP address; congestion control sets the port number",
      "Flow control is implemented by routers; congestion control is implemented by hosts"
    ],
    "ans": 0,
    "exp": "Flow control is an end-to-end speed-matching service that prevents a fast sender from overflowing the receiver's buffer by advertising rwnd = RcvBuffer - [LastByteRcvd - LastByteRead]. Congestion control protects intermediate network links and router queues (\u00a73.5.5, Study Guide P23)."
  },
  {
    "q": "P24 TCP Reno Fast Recovery: When TCP Reno receives 3 duplicate ACKs (4 identical ACKs total), what actions does it perform?",
    "opts": [
      "Sets ssthresh = cwnd/2, resets cwnd = 1 MSS, and enters Slow Start",
      "Sets ssthresh = cwnd/2, inflates cwnd = ssthresh + 3 MSS, and retransmits the missing segment immediately without waiting for timeout",
      "Terminates the TCP connection with a RST flag",
      "Doubles cwnd and ignores the duplicate ACKs"
    ],
    "ans": 1,
    "exp": "3 duplicate ACKs signal a packet loss while subsequent packets got through. TCP Reno performs Fast Retransmit, cuts ssthresh = cwnd/2, sets cwnd = ssthresh + 3 MSS, and enters Fast Recovery, avoiding the drop to cwnd = 1 MSS that TCP Tahoe would do (\u00a73.7, Study Guide P24)."
  },
  {
    "q": "Data Plane vs Control Plane: In modern network architecture, which plane is responsible for per-router local packet forwarding from input link to output link?",
    "opts": [
      "Control Plane",
      "Data Plane",
      "Management Plane",
      "Application Plane"
    ],
    "ans": 1,
    "exp": "The Data plane encompasses per-router hardware functions that determine how a datagram arriving on an input link is forwarded to an output link. The Control plane determines the network-wide end-to-end path (\u00a74.1)."
  },
  {
    "q": "Longest Prefix Matching: A router's forwarding table contains prefixes: Prefix A: 11001000 00010111 00010 (21 bits) -> Interface 0; Prefix B: 11001000 00010111 00011000 (24 bits) -> Interface 1. An incoming datagram has destination address starting with 11001000 00010111 00011000 10101010. Which interface is selected?",
    "opts": [
      "Interface 0, because it appears first in the table",
      "Interface 1, because 24 bits is a longer matching prefix than 21 bits",
      "Both interfaces simultaneously via multicast",
      "The datagram is dropped due to ambiguity"
    ],
    "ans": 1,
    "exp": "Longest Prefix Matching selects the table entry with the longest matching prefix. Prefix B matches 24 bits, which is longer than Prefix A's 21 bits, so Interface 1 is selected (\u00a74.2.1)."
  },
  {
    "q": "Router Fabric: What type of switching fabric enables multiple packets to be forwarded in parallel across different input/output port pairs, provided they do not target the same output port?",
    "opts": [
      "Shared Memory Fabric",
      "Single Shared Bus Fabric",
      "Crossbar Interconnection Fabric",
      "Store-and-Forward FIFO Fabric"
    ],
    "ans": 2,
    "exp": "A crossbar fabric consists of an NxN grid of buses that can forward up to N packets in parallel simultaneously, as long as no two inputs send to the same output (\u00a74.2.2)."
  },
  {
    "q": "Head-of-Line (HOL) Blocking: Where does Head-of-Line (HOL) blocking occur in a router, and what causes it?",
    "opts": [
      "At input port queues when a queued packet at the front of the line waits for a busy output port, blocking packets behind it",
      "At output port queues when transmission link is busy",
      "Inside the routing processor during OSPF calculations",
      "In DNS caches during name resolution"
    ],
    "ans": 0,
    "exp": "HOL blocking occurs at input queues: an arriving packet must wait at the front of an input queue for its target output port to become free, preventing other packets behind it from moving forward even if their output ports are idle (\u00a74.2.4)."
  },
  {
    "q": "CIDR Subnetting: An organization is allocated the IP block 192.168.10.0/24. How many total IP addresses exist in this block, and how many are usable for host devices?",
    "opts": [
      "256 total, 254 usable (network address .0 and broadcast .255 reserved)",
      "256 total, 256 usable",
      "512 total, 510 usable",
      "128 total, 126 usable"
    ],
    "ans": 0,
    "exp": "A /24 subnet has 32 - 24 = 8 host bits, giving 2^8 = 256 addresses. The all-0s host address is reserved for network identification and the all-1s address is reserved for subnet broadcast, leaving 254 usable host addresses (\u00a74.3.2)."
  },
  {
    "q": "IPv4 Fragmentation: A 4,000-byte IPv4 datagram (20-byte IP header + 3,980 bytes payload) arrives at a link with MTU = 1,500 bytes. What is the Fragment Offset value in the second fragment header?",
    "opts": [
      "185",
      "1480",
      "1500",
      "370"
    ],
    "ans": 0,
    "exp": "Each fragment can hold at most 1,500 - 20 = 1,480 bytes payload. Fragment 1 carries 1,480 bytes (offset = 0). Fragment 2 carries the next 1,480 bytes. Since IPv4 fragment offsets are measured in 8-byte units: Offset = 1,480 / 8 = 185 (\u00a74.3.4)."
  },
  {
    "q": "NAT Operation: When a home host with private IP 192.168.1.5:4500 sends a datagram through a NAT router with public IP 203.0.113.1, what does the NAT router modify in the outbound IP/TCP headers?",
    "opts": [
      "Only the destination IP address",
      "Source IP address to 203.0.113.1 and source port to an allocated NAT port (e.g. 50001), recording the mapping in its NAT table",
      "Only the TCP sequence number",
      "The TTL field to 255"
    ],
    "ans": 1,
    "exp": "The NAT router replaces the private source IP and port with its own public IP and an allocated port number, creating an entry in the NAT translation table so incoming responses can be demultiplexed back to the private host (\u00a74.3.5)."
  },
  {
    "q": "Link-State vs Distance-Vector: Which statement correctly contrasts the Link-State (Dijkstra) algorithm with the Distance-Vector (Bellman-Ford) algorithm?",
    "opts": [
      "Link-State uses global network topology knowledge via flooding; Distance-Vector is distributed and exchanges vectors only with direct neighbors",
      "Link-State is distributed while Distance-Vector requires a centralized global server",
      "Link-State suffers from count-to-infinity while Distance-Vector never loops",
      "Link-State only works on LANs while Distance-Vector is for the global Internet"
    ],
    "ans": 0,
    "exp": "Link-State algorithms (e.g. OSPF) broadcast link-state packets so every node builds a complete global network graph before running Dijkstra. Distance-Vector (e.g. RIP) is iterative, asynchronous, and distributed, exchanging estimates only with immediate physical neighbors (\u00a75.2)."
  },
  {
    "q": "Distance-Vector Loops: What classic problem can occur in Distance-Vector routing when a link cost increases significantly or breaks, and how does 'Poisoned Reverse' address it?",
    "opts": [
      "Buffer overflow; solved by increasing RAM",
      "Count-to-infinity routing loop; poisoned reverse advertises an infinite distance (infinity) back to the neighbor through which the route passes",
      "Checksum collision; solved by SHA-256",
      "SYN flood; solved by SYN cookies"
    ],
    "ans": 1,
    "exp": "When a link fails, two nodes can exchange outdated distance vectors in a cycle, slowly incrementing path costs in a 'count-to-infinity' loop. Poisoned Reverse prevents 2-node loops by advertising distance infinity back to the next-hop node (\u00a75.2.2)."
  },
  {
    "q": "BGP Loop Prevention: How does the Border Gateway Protocol (BGP) guarantee that inter-Autonomous System (AS) routes are free of loops?",
    "opts": [
      "By calculating Dijkstra trees across all global routers",
      "By prepending each Autonomous System's ASN to the AS-PATH attribute; if a router sees its own ASN in the path, it rejects the advertisement",
      "By limiting hop count to 15",
      "By requiring all routers to be directly connected"
    ],
    "ans": 1,
    "exp": "BGP is a path vector protocol. When an AS forwards a route, it prepends its autonomous system number (ASN) to the AS-PATH attribute. If a gateway router receives an advertisement containing its own ASN in the AS-PATH, it immediately discards it to prevent loops (\u00a75.4)."
  },
  {
    "q": "CRC Error Detection: In CRC error detection, sender and receiver agree on an (r+1)-bit generator pattern G. How is the transmitted frame constructed from data D?",
    "opts": [
      "By multiplying D by G using standard decimal multiplication",
      "By dividing D * 2^r by G using modulo-2 binary arithmetic and appending the remainder R to D",
      "By applying MD5 hash to D",
      "By computing the 16-bit 1's complement sum of D"
    ],
    "ans": 1,
    "exp": "In CRC, D is bit-shifted left by r bits (D * 2^r), then divided by G using XOR modulo-2 division. The r-bit remainder R is appended to D so that the resulting (d+r)-bit pattern is exactly divisible by G without remainder (\u00a76.2.3)."
  },
  {
    "q": "Multiple Access Efficiency: What are the theoretical maximum channel efficiencies of Pure ALOHA and Slotted ALOHA, respectively?",
    "opts": [
      "Pure ALOHA: 50.0%; Slotted ALOHA: 100.0%",
      "Pure ALOHA: 1/(2e) \u2248 18.4%; Slotted ALOHA: 1/e \u2248 36.8%",
      "Pure ALOHA: 36.8%; Slotted ALOHA: 73.6%",
      "Pure ALOHA: 10.0%; Slotted ALOHA: 20.0%"
    ],
    "ans": 1,
    "exp": "Pure ALOHA has a vulnerable collision window of 2 * slot duration, resulting in max efficiency of 1/(2e) \u2248 0.184 (18.4%). Slotted ALOHA restricts transmissions to synchronized slot boundaries, halving vulnerability to 1 slot duration and doubling max efficiency to 1/e \u2248 0.368 (36.8%) (\u00a76.3.2)."
  },
  {
    "q": "CSMA/CD: Why does CSMA/CD require a minimum packet/frame size (such as 64 bytes in Ethernet)?",
    "opts": [
      "To ensure the header fits",
      "To guarantee that the frame transmission time (L/R) is at least twice the maximum round-trip propagation delay (2 * d_prop) so collisions are detected before transmission completes",
      "To prevent buffer underflow in switches",
      "To align frame data on 32-bit memory boundaries"
    ],
    "ans": 1,
    "exp": "If a frame is too small, a transmitting host could finish pushing all bits onto the wire before the collision signal returns from the far end of the cable, falsely assuming transmission succeeded. Therefore, d_trans >= 2 * d_prop (\u00a76.3.3)."
  },
  {
    "q": "ARP Operation: How does an end system resolve an IP address to a physical 48-bit MAC address on the same local subnet?",
    "opts": [
      "It sends a unicast DNS query to port 53",
      "It broadcasts an ARP Request frame (dest MAC FF:FF:FF:FF:FF:FF); the owner of the target IP responds with a unicast ARP Reply frame",
      "It queries the default gateway router via DHCP",
      "It looks up the BGP routing table"
    ],
    "ans": 1,
    "exp": "ARP broadcasts an ARP query frame to all hosts on the subnet using the broadcast MAC FF:FF:FF:FF:FF:FF. The host with the matching IP address replies with its physical MAC address via unicast (\u00a76.4.1)."
  },
  {
    "q": "Switch Self-Learning: How does an Ethernet switch learn which host is connected to which switch port?",
    "opts": [
      "The network administrator manually enters all MAC addresses",
      "The switch inspects the Source MAC address of every arriving frame and records the (MAC, Port, Timestamp) entry in its forwarding switch table",
      "By executing Dijkstra's algorithm across the LAN",
      "By reading the Destination IP address in the packet header"
    ],
    "ans": 1,
    "exp": "Ethernet switches are self-learning and transparent: when a frame arrives on port x with source MAC address S, the switch automatically records in its table that host S is reachable through port x (\u00a76.4.3)."
  },
  {
    "q": "CDMA Decoding: In Code Division Multiple Access (CDMA), how does a receiver decode the original data bit d_i sent by transmitter i from the composite aggregate signal S?",
    "opts": [
      "By filtering out the carrier frequency",
      "By computing the inner product (dot product) of composite signal S with transmitter i's unique chipping code c_i and dividing by chip length M",
      "By measuring signal power in decibels",
      "By waiting for a dedicated time slot"
    ],
    "ans": 1,
    "exp": "Because chipping codes are mutually orthogonal (c_i * c_j = 0 for i != j and c_i * c_i = M), taking the normalized dot product (1/M) * (S * c_i) cancels out all other senders' signals, leaving only d_i (\u00a77.2)."
  },
  {
    "q": "802.11 Hidden Terminal: What causes the 'Hidden Terminal Problem' in wireless 802.11 networks, and how is it resolved?",
    "opts": [
      "Physical obstacles or distance prevent two stations from detecting each other's transmissions while both transmit to the same AP; resolved by RTS/CTS reservation frames",
      "Weak encryption keys; resolved by WPA3",
      "Lack of DHCP server; resolved by static IPs",
      "High bit error rates; resolved by Hamming codes"
    ],
    "ans": 0,
    "exp": "In wireless environments, physical obstacles or range boundaries can prevent station A and station B from hearing each other, causing collisions at a shared Access Point. The optional RTS/CTS (Request to Send / Clear to Send) exchange reserves the channel and silences all stations hearing the AP (\u00a77.3.2)."
  },
  {
    "q": "RSA Cryptography: In RSA public-key cryptography, given two prime numbers p = 3 and q = 11, compute the modulus n and Euler totient z = (p-1)*(q-1). If public exponent e = 3, what is private key d (where e*d mod z = 1)?",
    "opts": [
      "n = 33, z = 20, d = 7",
      "n = 33, z = 30, d = 3",
      "n = 14, z = 10, d = 5",
      "n = 33, z = 20, d = 11"
    ],
    "ans": 0,
    "exp": "n = p * q = 3 * 11 = 33. z = (3 - 1) * (11 - 1) = 2 * 10 = 20. We need e * d mod z = 1 -> 3 * d mod 20 = 1. Testing d = 7: 3 * 7 = 21, and 21 mod 20 = 1. Thus d = 7 (\u00a78.2.2)."
  },
  {
    "q": "TLS Session Keys: Why does TLS use public-key cryptography (RSA/Diffie-Hellman) only during the handshake phase, rather than for encrypting all application data?",
    "opts": [
      "Public-key cryptography cannot encrypt binary data",
      "Public-key cryptography is computationally expensive (orders of magnitude slower than symmetric ciphers like AES)",
      "Public-key cryptography requires UDP",
      "TLS does not support symmetric encryption"
    ],
    "ans": 1,
    "exp": "Asymmetric public-key encryption is computationally intensive. TLS uses public-key encryption during the initial handshake solely to authenticate the server and securely exchange a shared premaster secret, which is then used to derive fast symmetric session keys (e.g. AES-256-GCM) for application data (\u00a78.6)."
  },
  {
    "q": "IPsec Tunnel Mode: In IPsec Tunnel Mode, what portions of the original IP datagram are protected?",
    "opts": [
      "Only the transport layer payload",
      "The entire original IPv4 datagram (including original IP header and payload) is encrypted, authenticated, and encapsulated inside a new outer IP header",
      "Only the TCP ACK flag",
      "Only the Ethernet MAC addresses"
    ],
    "ans": 1,
    "exp": "In IPsec Tunnel Mode (widely used in site-to-site VPNs), the entire original IP packet is encrypted and encapsulated as the payload of a brand new IP datagram with a new outer IP header addressed to the tunnel endpoint gateway (\u00a78.7.2)."
  },
  {
    "q": "Firewall Filtering: How does a stateless packet-filtering router allow internal intranet clients to establish outbound connections to external web servers while blocking unsolicited incoming connections from the outside?",
    "opts": [
      "By checking if incoming TCP packets have the ACK bit set to 1 (meaning they are part of an already-established connection initiated internally) and blocking incoming SYN-only packets",
      "By decrypting all packets using AES",
      "By inspecting the HTTP User-Agent header",
      "By assigning public IP addresses to all clients"
    ],
    "ans": 0,
    "exp": "Inbound TCP connection setup starts with a SYN packet (ACK=0). A stateless packet filter drops any external TCP packet targeting port 80/443 with ACK=0, but allows packets with ACK=1 because they represent replies to connections initiated by internal clients (\u00a78.9.1)."
  },
  {
    "q": "Token Bucket Rate Limiting: A token bucket policer has bucket capacity b = 100 kbits and token arrival rate r = 5 Mbps. What is the maximum burst of data that can enter the network at peak link rate, and what is the maximum sustained data rate over long time periods?",
    "opts": [
      "Maximum burst: 100 kbits; Long-term rate: 5 Mbps",
      "Maximum burst: 5 Mbps; Long-term rate: 100 kbits",
      "Maximum burst: 500 kbits; Long-term rate: 1 Mbps",
      "Maximum burst: 10 kbits; Long-term rate: 10 Mbps"
    ],
    "ans": 0,
    "exp": "A token bucket limits the maximum burst size to bucket capacity b (100 kbits) because at most b tokens can accumulate. Over any long time interval t, the average rate cannot exceed the token generation rate r = 5 Mbps (\u00a79.4.2)."
  },
  {
    "q": "SNMP Trap: In the SNMP network management architecture, what is the role of an SNMP 'Trap' message?",
    "opts": [
      "It allows the managing server to query a MIB variable",
      "It is an unsolicited notification sent asynchronously by an SNMP agent to the managing server to report an exceptional event (such as a link failure)",
      "It shuts down the router interface permanently",
      "It sets the IP address of a managed device"
    ],
    "ans": 1,
    "exp": "Most SNMP operations are request-response initiated by the manager (GetRequest, SetRequest). An SNMP Trap is an asynchronous, unsolicited message sent by a managed device agent to notify the managing server immediately of an urgent event or fault (\u00a79.5.3)."
  },
  {
    "q": "SYN Flood Defense: How does a server use SYN Cookies to defend against a TCP SYN Flood Denial-of-Service attack without exhausting its memory buffers?",
    "opts": [
      "By allocating half-open connection buffers in swap memory",
      "By encoding the connection state into an initial sequence number (cookie) and not allocating any server memory until the client's ACK returns",
      "By dropping all TCP connections after 10 seconds",
      "By requiring clients to solve a proof-of-work puzzle"
    ],
    "ans": 1,
    "exp": "With SYN cookies, when a SYN arrives, the server creates an initial sequence number (cookie) computed from a cryptographic hash of source/dest IPs, ports, and a secret counter. The server sends this SYNACK without allocating any memory or connection state. State is only allocated when the client responds with a valid ACK containing cookie + 1 (\u00a73.5.6)."
  },
  {
    "q": "HTTP/2 vs HTTP/3: Why does HTTP/2 still suffer from transport-level Head-of-Line (HOL) blocking when packet loss occurs, and how does HTTP/3 solve this?",
    "opts": [
      "HTTP/2 uses multiple TCP connections; HTTP/3 uses one",
      "HTTP/2 multiplexes all streams over a single TCP connection, so loss of one packet stalls all streams; HTTP/3 runs over UDP-based QUIC, isolating packet loss to the affected stream only",
      "HTTP/2 does not support binary framing",
      "HTTP/3 replaces IP with MPLS"
    ],
    "ans": 1,
    "exp": "In HTTP/2, multiple application streams are multiplexed over a single TCP connection; when one TCP segment is lost, TCP's in-order byte stream semantics freeze all multiplexed streams until retransmission succeeds. HTTP/3 runs over QUIC on UDP, providing independent stream framing so loss on one stream does not block unrelated streams (\u00a72.2.7)."
  },
  {
    "q": "Selective Repeat Window Dilemma: In the Selective Repeat (SR) pipelined protocol, given a sequence number space of size 2^k, what is the maximum permissible sender and receiver window size W to avoid ambiguity between new packets and retransmitted duplicate packets?",
    "opts": [
      "W <= 2^k",
      "W <= 2^{k-1}",
      "W <= 2^{k+1}",
      "W = 2^k - 1"
    ],
    "ans": 1,
    "exp": "If window size W exceeds half the sequence number space (W > 2^{k-1}), the receiver cannot tell whether an arriving packet with a sequence number in the current window is a retransmission of a previous packet or a new packet from the next sequence cycle. Thus, window size must satisfy W <= 2^{k-1} (\u00a73.4.4)."
  }
];

function startFinalExam() {
  examState.active = true;
  examState.qIndex = 0;
  examState.userAnswers = {};
  examState.timeRemaining = 1800; // 30 mins

  document.getElementById('exam-welcome-card').style.display = 'none';
  document.getElementById('exam-results-card').style.display = 'none';
  document.getElementById('exam-active-card').style.display = 'block';

  renderExamQuestion();

  if (examState.timerInterval) clearInterval(examState.timerInterval);
  examState.timerInterval = setInterval(() => {
    examState.timeRemaining--;
    const mins = Math.floor(examState.timeRemaining / 60);
    const secs = examState.timeRemaining % 60;
    const timerEl = document.getElementById('exam-timer');
    if (timerEl) timerEl.innerText = `⏱ ${mins}:${secs < 10 ? '0' : ''}${secs}`;
    if (examState.timeRemaining <= 0) {
      clearInterval(examState.timerInterval);
      finishExam();
    }
  }, 1000);
}

function renderExamQuestion() {
  const q = EXAM_POOL[examState.qIndex];
  document.getElementById('exam-q-title').innerText = `Question ${examState.qIndex + 1} of ${EXAM_POOL.length}`;
  document.getElementById('exam-q-text').innerText = q.q;

  const optsContainer = document.getElementById('exam-q-options');
  optsContainer.innerHTML = q.opts.map((opt, idx) => `
    <div class="quiz-opt ${examState.userAnswers[examState.qIndex] === idx ? 'selected' : ''}" onclick="selectExamOption(${idx})">
      <span>${['A', 'B', 'C', 'D'][idx]}.</span> ${opt}
    </div>
  `).join('');

  const submitBtn = document.getElementById('exam-submit-btn');
  if (examState.qIndex === EXAM_POOL.length - 1) {
    submitBtn.innerText = 'Finish & Grade Exam';
  } else {
    submitBtn.innerText = 'Next Question →';
  }
}

function selectExamOption(idx) {
  examState.userAnswers[examState.qIndex] = idx;
  renderExamQuestion();
}

function nextExamQuestion() {
  if (examState.qIndex < EXAM_POOL.length - 1) {
    examState.qIndex++;
    renderExamQuestion();
  } else {
    finishExam();
  }
}

function prevExamQuestion() {
  if (examState.qIndex > 0) {
    examState.qIndex--;
    renderExamQuestion();
  }
}

function finishExam() {
  if (examState.timerInterval) clearInterval(examState.timerInterval);
  document.getElementById('exam-active-card').style.display = 'none';
  document.getElementById('exam-results-card').style.display = 'block';

  let correctCount = 0;
  let reviewHtml = '';

  EXAM_POOL.forEach((q, idx) => {
    const userAns = examState.userAnswers[idx];
    const isCorrect = userAns === q.ans;
    if (isCorrect) correctCount++;

    reviewHtml += `
      <div style="border:1px solid var(--border); border-radius:8px; padding:1rem; margin-bottom:0.75rem; background:var(--bg-secondary);">
        <p style="font-weight:700;">Q${idx + 1}: ${q.q}</p>
        <p style="font-size:0.85rem; margin-top:0.25rem; color:${isCorrect ? 'var(--accent-text)' : 'var(--danger-text)'};">
          Your Answer: ${userAns !== undefined ? q.opts[userAns] : 'Not Answered'} ${isCorrect ? '✅' : '❌'}
        </p>
        ${!isCorrect ? `<p style="font-size:0.85rem; color:var(--accent-text);">Correct Answer: ${q.opts[q.ans]}</p>` : ''}
        <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.25rem;"><em>Explanation:</em> ${q.exp}</p>
      </div>
    `;
  });

  const pct = Math.round((correctCount / EXAM_POOL.length) * 100);
  document.getElementById('exam-score-circle').innerText = `${pct}%`;
  document.getElementById('exam-score-msg').innerText = `You answered ${correctCount} of ${EXAM_POOL.length} questions correctly.`;
  document.getElementById('exam-review-list').innerHTML = reviewHtml;
}

// Checklist System
const CHECKLIST_ITEMS = [
  {
    "id": "c1",
    "ch": "Ch 1",
    "text": "I can describe the Internet from the 'nuts and bolts' view and the 'service' view"
  },
  {
    "id": "c2",
    "ch": "Ch 1",
    "text": "I can define a protocol (format, order of messages, and actions taken)"
  },
  {
    "id": "c3",
    "ch": "Ch 1",
    "text": "I can compare cable (HFC), DSL, FTTH (PON/AON), enterprise, and wireless access networks"
  },
  {
    "id": "c4",
    "ch": "Ch 1",
    "text": "I can compare guided media (twisted pair, coax, fiber) and unguided physical media (radio, satellite)"
  },
  {
    "id": "c5",
    "ch": "Ch 1",
    "text": "I can explain store-and-forward transmission, queuing, and packet loss"
  },
  {
    "id": "c6",
    "ch": "Ch 1",
    "text": "I can distinguish routing (network-wide path selection) from forwarding (local router transfer)"
  },
  {
    "id": "c7",
    "ch": "Ch 1",
    "text": "I can compare packet switching with circuit switching (FDM, TDM, and statistical multiplexing capacity)"
  },
  {
    "id": "c8",
    "ch": "Ch 1",
    "text": "I can describe the 5-tier 'network of networks' structure (Access ISPs, Regional ISPs, Tier-1 ISPs, IXPs, Content Providers)"
  },
  {
    "id": "c9",
    "ch": "Ch 1",
    "text": "I can compute the 4 components of nodal delay: d_nodal = d_proc + d_queue + d_trans + d_prop"
  },
  {
    "id": "c10",
    "ch": "Ch 1",
    "text": "I can use traffic intensity (La/R) to reason about queuing delay and packet loss"
  },
  {
    "id": "c11",
    "ch": "Ch 1",
    "text": "I can find the end-to-end throughput and identify the bottleneck link of a network path"
  },
  {
    "id": "c12",
    "ch": "Ch 1",
    "text": "I can describe malware (virus, worm, spyware, botnets), DoS/DDoS attacks, packet sniffing, and IP spoofing"
  },
  {
    "id": "c13",
    "ch": "Ch 1",
    "text": "I can name the 5 layers of the Internet stack, their functions, and example protocols"
  },
  {
    "id": "c14",
    "ch": "Ch 1",
    "text": "I can explain encapsulation and identify the packet name at each layer (Message, Segment, Datagram, Frame, Bit)"
  },
  {
    "id": "c15",
    "ch": "Ch 2",
    "text": "I can compare the client-server and peer-to-peer (P2P) application architectures"
  },
  {
    "id": "c16",
    "ch": "Ch 2",
    "text": "I can explain processes, sockets (API door analogy), and how a process is addressed (IP + Port)"
  },
  {
    "id": "c17",
    "ch": "Ch 2",
    "text": "I can list the four things an application-layer protocol defines (types, syntax, semantics, rules)"
  },
  {
    "id": "c18",
    "ch": "Ch 2",
    "text": "I can match network applications to their transport-service requirements (loss, throughput, timing, security)"
  },
  {
    "id": "c19",
    "ch": "Ch 2",
    "text": "I can compare TCP and UDP transport services and explain what TLS adds"
  },
  {
    "id": "c20",
    "ch": "Ch 2",
    "text": "I can dissect real HTTP request and response messages, header lines, and status codes (200, 301, 304, 400, 404, 505)"
  },
  {
    "id": "c21",
    "ch": "Ch 2",
    "text": "I can compare non-persistent (2 RTT + L/R per object) and persistent HTTP and compute response times"
  },
  {
    "id": "c22",
    "ch": "Ch 2",
    "text": "I can explain the four components of HTTP cookies (header, request, client file, server database)"
  },
  {
    "id": "c23",
    "ch": "Ch 2",
    "text": "I can explain Web caching, hit-rate delay reduction, and the Conditional GET mechanism (304 Not Modified)"
  },
  {
    "id": "c24",
    "ch": "Ch 2",
    "text": "I can explain Head-of-Line (HOL) blocking and how HTTP/2 (binary framing) and HTTP/3 (QUIC/UDP) reduce delay"
  },
  {
    "id": "c25",
    "ch": "Ch 2",
    "text": "I can describe e-mail components, SMTP push protocol trace, and mail access protocols (POP3, IMAP, Webmail)"
  },
  {
    "id": "c26",
    "ch": "Ch 2",
    "text": "I can explain the DNS hierarchy, iterated vs recursive queries, DNS caching, and Resource Records (A, NS, CNAME, MX)"
  },
  {
    "id": "c27",
    "ch": "Ch 2",
    "text": "I can explain BitTorrent (torrents, trackers, 256KB chunks, rarest-first requesting, tit-for-tat unchoking)"
  },
  {
    "id": "c28",
    "ch": "Ch 2",
    "text": "I can explain video encoding, playout buffering, DASH manifest files, and CDN server placement architectures"
  },
  {
    "id": "c29",
    "ch": "Ch 3",
    "text": "I can contrast transport-layer (process-to-process) and network-layer (host-to-host) logical communication"
  },
  {
    "id": "c30",
    "ch": "Ch 3",
    "text": "I can explain transport-layer multiplexing (headers) and demultiplexing (port numbers)"
  },
  {
    "id": "c31",
    "ch": "Ch 3",
    "text": "I can demultiplex connectionless UDP (2-tuple) and connection-oriented TCP (4-tuple) segments to sockets"
  },
  {
    "id": "c32",
    "ch": "Ch 3",
    "text": "I can explain why UDP exists, its advantages, and list its 4 header fields (Src Port, Dest Port, Length, Checksum)"
  },
  {
    "id": "c33",
    "ch": "Ch 3",
    "text": "I can compute and verify the 16-bit 1's complement Internet checksum with end-around wraparound carry"
  },
  {
    "id": "c34",
    "ch": "Ch 3",
    "text": "I can trace reliable data transfer FSMs from rdt 1.0 through rdt 3.0 and explain the corrupted ACK/NAK flaw"
  },
  {
    "id": "c35",
    "ch": "Ch 3",
    "text": "I can draw and analyze all four rdt 3.0 timeline scenarios (no loss, packet loss, ACK loss, premature timeout)"
  },
  {
    "id": "c36",
    "ch": "Ch 3",
    "text": "I can compute stop-and-wait utilization U = (L/R)/(RTT + L/R) and pipelined window size N to achieve 100% link utilization"
  },
  {
    "id": "c37",
    "ch": "Ch 3",
    "text": "I can compare Go-Back-N cumulative ACKs with Selective Repeat individual ACKs and solve the SR window dilemma"
  },
  {
    "id": "c38",
    "ch": "Ch 3",
    "text": "I can describe the 20-byte TCP header fields: Sequence Number, ACK Number, 6 control flags, Receive Window, Urgent"
  },
  {
    "id": "c39",
    "ch": "Ch 3",
    "text": "I can trace multi-step TCP sequence and acknowledgment numbers with gap-filling buffering and Telnet echo"
  },
  {
    "id": "c40",
    "ch": "Ch 3",
    "text": "I can compute EWMA EstimatedRTT, DevRTT, and the TCP TimeoutInterval using Karn's algorithm"
  },
  {
    "id": "c41",
    "ch": "Ch 3",
    "text": "I can explain TCP fast retransmit on 3 duplicate ACKs and contrast Tahoe vs Reno loss recovery"
  },
  {
    "id": "c42",
    "ch": "Ch 3",
    "text": "I can explain TCP flow control (rwnd), the 3-way connection handshake, teardown (TIME_WAIT), and SYN flood cookies"
  },
  {
    "id": "c43",
    "ch": "Ch 4",
    "text": "I can contrast data plane (per-router forwarding) and control plane (network-wide routing)"
  },
  {
    "id": "c44",
    "ch": "Ch 4",
    "text": "I can explain router architecture: input ports, switching fabrics (memory, bus, crossbar), and HOL blocking"
  },
  {
    "id": "c45",
    "ch": "Ch 4",
    "text": "I can perform longest prefix matching lookup and calculate CIDR subnet addresses and usable host ranges"
  },
  {
    "id": "c46",
    "ch": "Ch 4",
    "text": "I can compute IPv4 datagram fragmentation (identification, flags, fragment offset) and explain NAT operation"
  },
  {
    "id": "c47",
    "ch": "Ch 5",
    "text": "I can contrast link-state (Dijkstra) and distance-vector (Bellman-Ford) routing algorithms"
  },
  {
    "id": "c48",
    "ch": "Ch 5",
    "text": "I can explain BGP inter-domain routing: eBGP, iBGP, AS-PATH loop prevention, NEXT-HOP, and policy"
  },
  {
    "id": "c49",
    "ch": "Ch 6",
    "text": "I can compute CRC error detection using modulo-2 generator polynomial division G(D)"
  },
  {
    "id": "c50",
    "ch": "Ch 6",
    "text": "I can analyze multiple access efficiencies: Slotted ALOHA (36.8%), Pure ALOHA (18.4%), and CSMA/CD"
  },
  {
    "id": "c51",
    "ch": "Ch 6",
    "text": "I can explain ARP IP-to-MAC resolution and self-learning Ethernet switch forwarding"
  },
  {
    "id": "c52",
    "ch": "Ch 7",
    "text": "I can calculate CDMA decoding using orthogonal chip sequences and inner product operations"
  },
  {
    "id": "c53",
    "ch": "Ch 7",
    "text": "I can explain 802.11 WiFi CSMA/CA, RTS/CTS reservation frames, and the hidden terminal problem"
  },
  {
    "id": "c54",
    "ch": "Ch 8",
    "text": "I can compute RSA public/private key generation, encryption, TLS session keys, and IPsec tunnel mode"
  },
  {
    "id": "c55",
    "ch": "Ch 9",
    "text": "I can compute token bucket leaky bucket rate limiting and explain SNMP architecture and SMI MIB structures"
  }
];

function initChecklist() {
  const container = document.getElementById('checklist-container');
  if (!container) return;
  container.innerHTML = CHECKLIST_ITEMS.map(item => `
    <div style="display:flex; align-items:center; gap:0.75rem; padding:0.65rem 0; border-bottom:1px solid var(--border-light);">
      <input type="checkbox" id="${item.id}" ${completedChecklist.has(item.id) ? 'checked' : ''} onchange="toggleCheckItem('${item.id}')" style="width:18px; height:18px; cursor:pointer;">
      <label for="${item.id}" style="font-size:0.9rem; cursor:pointer; color:var(--text-primary);">
        <strong style="color:var(--primary); margin-right:0.35rem;">[${item.ch}]</strong> ${item.text}
      </label>
    </div>
  `).join('');
}

function toggleCheckItem(id) {
  if (completedChecklist.has(id)) {
    completedChecklist.delete(id);
  } else {
    completedChecklist.add(id);
  }
  localStorage.setItem('cpcs371_checklist', JSON.stringify(Array.from(completedChecklist)));
}

// Global Search
function handleGlobalSearch() {
  const q = document.getElementById('global-search-input').value.toLowerCase().trim();
  if (!q) return;

  // Search across sections
  const secItems = document.querySelectorAll('.sec-item');
  let matchFound = false;
  secItems.forEach(item => {
    const text = item.innerText.toLowerCase();
    if (text.includes(q)) {
      item.style.display = 'flex';
      if (!matchFound) {
        navigateTo(item.dataset.sec);
        matchFound = true;
      }
    } else {
      item.style.display = 'none';
    }
  });

  if (!q) {
    secItems.forEach(item => item.style.display = 'flex');
  }
}

// Initialize on Load
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initGlossary();
  filteredFlashcards = [...ALL_FLASHCARDS];
  renderFlashcard();
  initChecklist();
  handleRoute();
});
"""
