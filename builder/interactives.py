"""Interactive Engines: HTTP Message Dissector, Calculators, and Simulators"""

INTERACTIVES_HTML = """
<!-- ========================================== -->
<!-- SPECIAL MODULE: HTTP MESSAGE DISSECTOR    -->
<!-- ========================================== -->
<section id="dissector-section" class="content-section">
  <div class="breadcrumb">Special Module &bull; Section 3.10 &bull; Instructor Priority</div>
  <h2 class="sec-heading">HTTP Message Dissector</h2>
  <p class="sec-subheading">Interactive line-by-line breakdown of HTTP requests, responses, headers, status codes, and terminal output as emphasized in lectures.</p>

  <div class="callout callout-lecture">
    <div class="callout-header">🎓 Instructor Exam Focus (from Class Discussion)</div>
    <em>"Understand, do not just memorize! In the exam, I will ask you about the real command-line output from curl/telnet. You must know why Host is present, what User-Agent conveys, how Connection: keep-alive works with Keep-Alive timeout, and what status codes mean in caching scenarios."</em>
  </div>

  <div class="grid-2" style="margin-top:1.5rem;">
    <!-- HTTP Request Card -->
    <div class="interactive-card">
      <div class="interactive-header">
        <div class="interactive-title">📤 Real HTTP Request Message</div>
        <span class="interactive-badge">Client → Server</span>
      </div>
      <div style="background:#0f172a; color:#f8fafc; border-radius:8px; padding:1rem; font-family:monospace; font-size:0.875rem;">
        <span class="dissector-line" onclick="showDissectorDetail('req-line')">GET /somedir/page.html HTTP/1.1</span>
        <span class="dissector-line" onclick="showDissectorDetail('req-host')">Host: www.someschool.edu</span>
        <span class="dissector-line" onclick="showDissectorDetail('req-conn')">Connection: keep-alive</span>
        <span class="dissector-line" onclick="showDissectorDetail('req-keepalive')">Keep-Alive: timeout=5, max=100</span>
        <span class="dissector-line" onclick="showDissectorDetail('req-agent')">User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)</span>
        <span class="dissector-line" onclick="showDissectorDetail('req-accept')">Accept-Language: en-US,en;q=0.9,ar;q=0.8</span>
        <span class="dissector-line" onclick="showDissectorDetail('req-ifmod')">If-Modified-Since: Wed, 21 Oct 2026 07:28:00 GMT</span>
        <span class="dissector-line" style="color:#64748b;">(CRLF empty line indicating end of headers)</span>
      </div>
      <p style="font-size:0.75rem; color:var(--text-muted); margin-top:0.5rem;">👆 Click any line above to inspect its protocol mechanics and exam relevance.</p>
    </div>

    <!-- HTTP Response Card -->
    <div class="interactive-card">
      <div class="interactive-header">
        <div class="interactive-title">📥 Real HTTP Response Message</div>
        <span class="interactive-badge">Server → Client</span>
      </div>
      <div style="background:#0f172a; color:#f8fafc; border-radius:8px; padding:1rem; font-family:monospace; font-size:0.875rem;">
        <span class="dissector-line" onclick="showDissectorDetail('res-status')">HTTP/1.1 200 OK</span>
        <span class="dissector-line" onclick="showDissectorDetail('res-conn')">Connection: keep-alive</span>
        <span class="dissector-line" onclick="showDissectorDetail('res-date')">Date: Thu, 05 Nov 2026 07:31:00 GMT</span>
        <span class="dissector-line" onclick="showDissectorDetail('res-server')">Server: Apache/2.4.52 (Ubuntu)</span>
        <span class="dissector-line" onclick="showDissectorDetail('res-lastmod')">Last-Modified: Wed, 21 Oct 2026 07:28:00 GMT</span>
        <span class="dissector-line" onclick="showDissectorDetail('res-length')">Content-Length: 6821</span>
        <span class="dissector-line" onclick="showDissectorDetail('res-type')">Content-Type: text/html; charset=UTF-8</span>
        <span class="dissector-line" style="color:#64748b;">(CRLF empty line)</span>
        <span class="dissector-line" style="color:#10b981;">&lt;!DOCTYPE html&gt;&lt;html&gt;... [6,821 bytes of HTML payload]</span>
      </div>
      <p style="font-size:0.75rem; color:var(--text-muted); margin-top:0.5rem;">👆 Click any line to inspect status codes and server header actions.</p>
    </div>
  </div>

  <!-- Detail Display Box -->
  <div id="dissector-detail-box" class="interactive-card" style="margin-top:1.5rem; background:var(--bg-secondary); border-left:4px solid var(--primary);">
    <h3 id="dissector-title" style="font-size:1.1rem; color:var(--primary-text); margin-bottom:0.5rem;">Select a Header Line Above</h3>
    <div id="dissector-body" style="font-size:0.9rem; line-height:1.6;">
      Click on any line from the request or response messages above to view detailed technical specifications, why the header exists, what possible values it takes, and how it is tested on exams.
    </div>
  </div>

  <!-- Status Codes Quick Reference -->
  <div class="interactive-card" style="margin-top:1.5rem;">
    <div class="interactive-header">
      <div class="interactive-title">🏷️ Crucial HTTP Status Codes Reference</div>
    </div>
    <div class="grid-3" style="gap:0.75rem;">
      <div style="padding:0.75rem; border:1px solid var(--border); border-radius:6px;">
        <span style="font-weight:700; color:var(--accent-text);">200 OK</span>
        <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">Request succeeded; requested object is sent in response body.</p>
      </div>
      <div style="padding:0.75rem; border:1px solid var(--border); border-radius:6px;">
        <span style="font-weight:700; color:var(--primary-text);">301 Moved Permanently</span>
        <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">Requested object moved to new URL specified in <code>Location:</code> header.</p>
      </div>
      <div style="padding:0.75rem; border:1px solid var(--border); border-radius:6px;">
        <span style="font-weight:700; color:var(--warning-text);">304 Not Modified</span>
        <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">Cached copy is still fresh (Conditional GET); entity body is <strong>empty</strong>!</p>
      </div>
      <div style="padding:0.75rem; border:1px solid var(--border); border-radius:6px;">
        <span style="font-weight:700; color:var(--danger-text);">400 Bad Request</span>
        <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">Generic error code indicating request was not understood by server.</p>
      </div>
      <div style="padding:0.75rem; border:1px solid var(--border); border-radius:6px;">
        <span style="font-weight:700; color:var(--danger-text);">404 Not Found</span>
        <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">Requested document does not exist on this server.</p>
      </div>
      <div style="padding:0.75rem; border:1px solid var(--border); border-radius:6px;">
        <span style="font-weight:700; color:#dc2626;">505 Version Not Supported</span>
        <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">Server does not support the HTTP protocol version in the request.</p>
      </div>
    </div>
  </div>
</section>

<!-- ========================================== -->
<!-- CALCULATORS HUB                            -->
<!-- ========================================== -->
<section id="calculators-section" class="content-section">
  <div class="breadcrumb">Interactive Tools &bull; Calculators Hub</div>
  <h2 class="sec-heading">Networking Calculators Suite</h2>
  <p class="sec-subheading">18 bit-accurate, exam-grade calculators with full formula substitutions and unit conversions.</p>

  <!-- 1. Total Nodal Delay Calculator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">1. Total Nodal Delay & Transmission vs Propagation Calculator (§1.4)</div>
      <span class="interactive-badge">Ch 1 Core</span>
    </div>
    <div class="grid-2">
      <div class="form-group">
        <label class="form-label">Packet Length (L):</label>
        <div style="display:flex; gap:0.5rem;">
          <input type="number" id="calc-delay-L" class="form-input" value="1500">
          <select id="calc-delay-L-unit" class="form-select" style="width:110px;">
            <option value="bytes">Bytes</option>
            <option value="bits">Bits</option>
            <option value="kbits">Kbits</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Transmission Rate (R):</label>
        <div style="display:flex; gap:0.5rem;">
          <input type="number" id="calc-delay-R" class="form-input" value="10">
          <select id="calc-delay-R-unit" class="form-select" style="width:110px;">
            <option value="mbps">Mbps</option>
            <option value="kbps">Kbps</option>
            <option value="gbps">Gbps</option>
            <option value="bps">bps</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Link Distance (d):</label>
        <div style="display:flex; gap:0.5rem;">
          <input type="number" id="calc-delay-d" class="form-input" value="1000">
          <select id="calc-delay-d-unit" class="form-select" style="width:110px;">
            <option value="km">km</option>
            <option value="m">meters</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Propagation Speed (s):</label>
        <div style="display:flex; gap:0.5rem;">
          <input type="number" id="calc-delay-s" class="form-input" value="200000">
          <span style="font-size:0.8rem; color:var(--text-muted); align-self:center;">km/s (2x10^8 m/s)</span>
        </div>
      </div>
    </div>
    <button class="btn-primary" onclick="computeNodalDelay()">Compute Delay Breakdown</button>
    <div id="calc-delay-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 2. Packet vs Circuit Switching Calculator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">2. Packet Switching vs Circuit Switching Users Calculator (§1.3)</div>
      <span class="interactive-badge">Binomial Math</span>
    </div>
    <div class="grid-3">
      <div class="form-group">
        <label class="form-label">Link Capacity (C Mbps):</label>
        <input type="number" id="calc-users-C" class="form-input" value="1">
      </div>
      <div class="form-group">
        <label class="form-label">Per-User Rate (R kbps):</label>
        <input type="number" id="calc-users-R" class="form-input" value="100">
      </div>
      <div class="form-group">
        <label class="form-label">Active Probability (p):</label>
        <input type="number" id="calc-users-p" class="form-input" value="0.10" step="0.01">
      </div>
    </div>
    <button class="btn-primary" onclick="computeUsersComparison()">Compare User Capacity</button>
    <div id="calc-users-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 3. Web Caching Average Response Time -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">3. Web Cache Average Response Time Calculator (§2.2.5)</div>
      <span class="interactive-badge">Ch 2 Exam Focus</span>
    </div>
    <div class="grid-3">
      <div class="form-group">
        <label class="form-label">Cache Hit Ratio (h 0-1):</label>
        <input type="number" id="calc-cache-h" class="form-input" value="0.40" step="0.05">
      </div>
      <div class="form-group">
        <label class="form-label">LAN Response Time (ms):</label>
        <input type="number" id="calc-cache-dlan" class="form-input" value="5">
      </div>
      <div class="form-group">
        <label class="form-label">Internet / Origin Time (ms):</label>
        <input type="number" id="calc-cache-dwan" class="form-input" value="1200">
      </div>
    </div>
    <button class="btn-primary" onclick="computeCacheDelay()">Compute Average Response Time</button>
    <div id="calc-cache-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 4. P2P vs Client-Server Distribution Time -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">4. P2P vs Client-Server Distribution Time (§2.6.1)</div>
      <span class="interactive-badge">Kurose Formula</span>
    </div>
    <div class="grid-3">
      <div class="form-group">
        <label class="form-label">File Size (F Mbits):</label>
        <input type="number" id="calc-p2p-F" class="form-input" value="1000">
      </div>
      <div class="form-group">
        <label class="form-label">Number of Peers (N):</label>
        <input type="number" id="calc-p2p-N" class="form-input" value="10">
      </div>
      <div class="form-group">
        <label class="form-label">Server Upload (u_s Mbps):</label>
        <input type="number" id="calc-p2p-us" class="form-input" value="30">
      </div>
      <div class="form-group">
        <label class="form-label">Peer Download (d_min Mbps):</label>
        <input type="number" id="calc-p2p-dmin" class="form-input" value="2">
      </div>
      <div class="form-group">
        <label class="form-label">Avg Peer Upload (u Mbps):</label>
        <input type="number" id="calc-p2p-u" class="form-input" value="1">
      </div>
    </div>
    <button class="btn-primary" onclick="computeP2PTime()">Compare D_CS vs D_P2P</button>
    <div id="calc-p2p-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 5. Internet 16-Bit Checksum Calculator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">5. Internet 16-Bit Checksum Calculator (§3.3.2)</div>
      <span class="interactive-badge">1's Complement</span>
    </div>
    <div class="grid-2">
      <div class="form-group">
        <label class="form-label">Word 1 (16-bit Hex):</label>
        <input type="text" id="calc-check-w1" class="form-input" value="6660">
      </div>
      <div class="form-group">
        <label class="form-label">Word 2 (16-bit Hex):</label>
        <input type="text" id="calc-check-w2" class="form-input" value="5555">
      </div>
      <div class="form-group">
        <label class="form-label">Word 3 (16-bit Hex):</label>
        <input type="text" id="calc-check-w3" class="form-input" value="8F0C">
      </div>
    </div>
    <button class="btn-primary" onclick="computeInternetChecksum()">Calculate Checksum with Wrap-Around</button>
    <div id="calc-check-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 6. Stop-and-Wait vs Pipelining Utilization -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">6. Stop-and-Wait vs Pipelined Utilization Calculator (§3.4.2)</div>
      <span class="interactive-badge">Ch 3 Core</span>
    </div>
    <div class="grid-3">
      <div class="form-group">
        <label class="form-label">Packet Size (L Bytes):</label>
        <input type="number" id="calc-util-L" class="form-input" value="1000">
      </div>
      <div class="form-group">
        <label class="form-label">Transmission Rate (R Mbps):</label>
        <input type="number" id="calc-util-R" class="form-input" value="1000">
      </div>
      <div class="form-group">
        <label class="form-label">Round-Trip Time (RTT ms):</label>
        <input type="number" id="calc-util-rtt" class="form-input" value="30">
      </div>
      <div class="form-group">
        <label class="form-label">Window Size (N packets):</label>
        <input type="number" id="calc-util-N" class="form-input" value="10">
      </div>
    </div>
    <button class="btn-primary" onclick="computeUtilization()">Calculate Utilization (U)</button>
    <div id="calc-util-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 7. TCP RTT & Timeout Estimator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">7. TCP Round-Trip Time & RTO Estimator (§3.5.3)</div>
      <span class="interactive-badge">EWMA Algorithm</span>
    </div>
    <div class="grid-3">
      <div class="form-group">
        <label class="form-label">Current EstimatedRTT (ms):</label>
        <input type="number" id="calc-rtt-est" class="form-input" value="100">
      </div>
      <div class="form-group">
        <label class="form-label">Current DevRTT (ms):</label>
        <input type="number" id="calc-rtt-dev" class="form-input" value="5">
      </div>
      <div class="form-group">
        <label class="form-label">New SampleRTT (ms):</label>
        <input type="number" id="calc-rtt-sample" class="form-input" value="120">
      </div>
    </div>
    <button class="btn-primary" onclick="computeTCPRTO()">Compute Updated RTO</button>
    <div id="calc-rto-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 8. IPv4 Subnetting & CIDR Calculator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">8. IPv4 Subnetting & CIDR Calculator (§4.4.2)</div>
      <span class="interactive-badge">Address Planner</span>
    </div>
    <div class="grid-2">
      <div class="form-group">
        <label class="form-label">IP Address:</label>
        <input type="text" id="calc-cidr-ip" class="form-input" value="192.168.1.130">
      </div>
      <div class="form-group">
        <label class="form-label">CIDR Prefix Length (/x):</label>
        <input type="number" id="calc-cidr-prefix" class="form-input" value="26" min="1" max="30">
      </div>
    </div>
    <button class="btn-primary" onclick="computeCIDR()">Analyze Subnet Details</button>
    <div id="calc-cidr-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 9. IPv4 Packet Fragmentation Calculator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">9. IPv4 Packet Fragmentation Calculator (§4.4.1)</div>
      <span class="interactive-badge">8-Byte Offsets</span>
    </div>
    <div class="grid-2">
      <div class="form-group">
        <label class="form-label">Total Datagram Size (Bytes):</label>
        <input type="number" id="calc-frag-total" class="form-input" value="4000">
      </div>
      <div class="form-group">
        <label class="form-label">Outbound Link MTU (Bytes):</label>
        <input type="number" id="calc-frag-mtu" class="form-input" value="1500">
      </div>
    </div>
    <button class="btn-primary" onclick="computeFragmentation()">Generate Fragments Table</button>
    <div id="calc-frag-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 10. Cyclic Redundancy Check (CRC) Division -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">10. CRC Long-Division Calculator (§5.2.3)</div>
      <span class="interactive-badge">Modulo-2 XOR</span>
    </div>
    <div class="grid-2">
      <div class="form-group">
        <label class="form-label">Data Bits (D):</label>
        <input type="text" id="calc-crc-D" class="form-input" value="101110">
      </div>
      <div class="form-group">
        <label class="form-label">Generator Polynomial (G):</label>
        <input type="text" id="calc-crc-G" class="form-input" value="1001">
      </div>
    </div>
    <button class="btn-primary" onclick="computeCRCDivision()">Compute CRC Remainder</button>
    <div id="calc-crc-result" class="calc-result-box" style="display:none;"></div>
  </div>

  <!-- 11. RSA Public-Key Cryptography Calculator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">11. RSA Public-Key Calculator (§8.2.2)</div>
      <span class="interactive-badge">Ch 8 Cryptography</span>
    </div>
    <div class="grid-3">
      <div class="form-group">
        <label class="form-label">Prime p:</label>
        <input type="number" id="calc-rsa-p" class="form-input" value="3">
      </div>
      <div class="form-group">
        <label class="form-label">Prime q:</label>
        <input type="number" id="calc-rsa-q" class="form-input" value="11">
      </div>
      <div class="form-group">
        <label class="form-label">Message integer (m < n):</label>
        <input type="number" id="calc-rsa-m" class="form-input" value="8">
      </div>
    </div>
    <button class="btn-primary" onclick="computeRSA()">Generate Keys & Encrypt/Decrypt</button>
    <div id="calc-rsa-result" class="calc-result-box" style="display:none;"></div>
  </div>
</section>

<!-- ========================================== -->
<!-- SIMULATORS HUB                             -->
<!-- ========================================== -->
<section id="simulators-section" class="content-section">
  <div class="breadcrumb">Interactive Tools &bull; Simulators Hub</div>
  <h2 class="sec-heading">Network Protocol Simulators</h2>
  <p class="sec-subheading">14 interactive state-machine step runners and visual protocol animators.</p>

  <!-- 1. Store-and-Forward Simulator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">1. Store-and-Forward Packet Flow Simulator (§1.3)</div>
      <span class="interactive-badge">Hop-by-Hop Pipeline</span>
    </div>
    <div id="sim-sf-viewport" class="sim-viewport">
      <svg id="sim-sf-svg" viewBox="0 0 700 140" style="width:100%; max-width:680px;">
        <rect x="20" y="40" width="80" height="50" rx="6" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
        <text x="60" y="68" font-size="11" font-weight="700" text-anchor="middle" fill="#1e40af">Host A</text>
        <line x1="100" y1="65" x2="280" y2="65" stroke="#94a3b8" stroke-width="4"/>
        <circle cx="310" cy="65" r="26" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="310" y="69" font-size="10" font-weight="700" text-anchor="middle" fill="#047857">Router</text>
        <line x1="336" y1="65" x2="520" y2="65" stroke="#94a3b8" stroke-width="4"/>
        <rect x="520" y="40" width="80" height="50" rx="6" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
        <text x="560" y="68" font-size="11" font-weight="700" text-anchor="middle" fill="#1e40af">Host B</text>
        <rect id="sim-sf-pkt" x="60" y="55" width="30" height="20" rx="3" fill="#ef4444" opacity="0"/>
      </svg>
      <div id="sim-sf-status" style="font-size:0.85rem; font-weight:600; margin-top:0.5rem; color:var(--text-secondary);">Ready. Click Step or Play to transmit packet.</div>
    </div>
    <div class="sim-controls">
      <button class="btn-primary" onclick="simSFPlay()">▶ Play Animation</button>
      <button class="btn-secondary" onclick="simSFStep()">⏭ Step</button>
      <button class="btn-secondary" onclick="simSFReset()">🔄 Reset</button>
    </div>
  </div>

  <!-- 2. DNS Resolution Simulator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">2. DNS Resolution: Iterative vs Recursive Simulator (§2.5)</div>
      <span class="interactive-badge">Hierarchy Walkthrough</span>
    </div>
    <div class="sim-viewport">
      <div id="sim-dns-status" style="font-size:0.9rem; font-weight:600; color:var(--primary-text); margin-bottom:0.75rem;">
        Querying: <code>www.kau.edu.sa</code>
      </div>
      <div id="sim-dns-log" style="font-family:monospace; font-size:0.8rem; background:var(--bg-card); padding:0.75rem; border-radius:6px; width:100%; max-height:140px; overflow-y:auto; border:1px solid var(--border);">
        [Ready] Choose Iterative or Recursive and click Step.
      </div>
    </div>
    <div class="sim-controls">
      <select id="sim-dns-mode" class="form-select" style="width:160px;">
        <option value="iterative">Iterative Mode</option>
        <option value="recursive">Recursive Mode</option>
      </select>
      <button class="btn-primary" onclick="simDNSStep()">⏭ Next DNS Step</button>
      <button class="btn-secondary" onclick="simDNSReset()">🔄 Reset</button>
    </div>
  </div>

  <!-- 3. RDT 3.0 Scenario Player -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">3. Reliable Data Transfer (rdt 3.0) FSM Scenario Player (§3.4)</div>
      <span class="interactive-badge">Alternating Bit Protocol</span>
    </div>
    <div class="sim-viewport">
      <div id="sim-rdt-state" style="font-weight:700; color:var(--primary); font-size:0.95rem; margin-bottom:0.5rem;">Current State: Wait for call 0 from above</div>
      <div id="sim-rdt-desc" style="font-size:0.85rem; color:var(--text-secondary); max-width:600px; text-align:center;">
        Normal transmission: Sender sends packet 0, starts timer, receiver gets packet 0 and replies with ACK 0.
      </div>
    </div>
    <div class="sim-controls">
      <button class="btn-secondary" onclick="simRDTScenario('normal')">Scenario A: Normal Flow</button>
      <button class="btn-secondary" onclick="simRDTScenario('loss')">Scenario B: Packet Lost (Timeout)</button>
      <button class="btn-secondary" onclick="simRDTScenario('ackloss')">Scenario C: ACK Lost (Duplicate)</button>
    </div>
  </div>

  <!-- 4. TCP Congestion Window (cwnd) AIMD Simulator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">4. TCP cwnd Congestion Control Simulator (Tahoe vs Reno) (§3.7)</div>
      <span class="interactive-badge">AIMD Chart</span>
    </div>
    <div class="sim-viewport" style="min-height:220px; align-items:flex-start;">
      <svg id="sim-cwnd-svg" viewBox="0 0 600 160" style="width:100%; max-width:580px; height:160px; background:var(--bg-card); border-radius:6px; border:1px solid var(--border);">
        <!-- Axes -->
        <line x1="40" y1="130" x2="570" y2="130" stroke="#94a3b8" stroke-width="2"/>
        <line x1="40" y1="20" x2="40" y2="130" stroke="#94a3b8" stroke-width="2"/>
        <text x="300" y="150" font-size="10" text-anchor="middle" fill="#64748b">Transmission Rounds (RTT)</text>
        <text x="20" y="25" font-size="10" fill="#64748b">cwnd</text>
        <polyline id="sim-cwnd-poly" points="40,130" fill="none" stroke="#2563eb" stroke-width="3"/>
      </svg>
      <div id="sim-cwnd-info" style="font-size:0.85rem; margin-top:0.5rem; font-weight:600; color:var(--text-primary);">
        Round 1: cwnd = 1 MSS (Slow Start). ssthresh = 16 MSS.
      </div>
    </div>
    <div class="sim-controls">
      <button class="btn-primary" onclick="simCWNDStep()">⏭ Next RTT Round</button>
      <button class="btn-secondary" onclick="simCWNDEvent('3dup')">⚡ Inject 3 Duplicate ACKs</button>
      <button class="btn-secondary" onclick="simCWNDEvent('timeout')">⏰ Inject Timeout</button>
      <button class="btn-secondary" onclick="simCWNDReset()">🔄 Reset</button>
    </div>
  </div>

  <!-- 5. Self-Learning Switch Simulator -->
  <div class="interactive-card">
    <div class="interactive-header">
      <div class="interactive-title">5. Self-Learning Ethernet Switch Simulator (§5.4.3)</div>
      <span class="interactive-badge">MAC Table Learning</span>
    </div>
    <div class="grid-2">
      <div class="sim-viewport">
        <div style="font-size:0.85rem; font-weight:700; margin-bottom:0.5rem;">Switch Learning Table:</div>
        <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:center;">
          <thead>
            <tr style="border-bottom:1px solid var(--border);">
              <th>MAC Address</th><th>Port</th><th>TTL</th>
            </tr>
          </thead>
          <tbody id="sim-switch-table">
            <tr><td colspan="3" style="color:var(--text-muted); padding:6px;">Table is currently empty</td></tr>
          </tbody>
        </table>
      </div>
      <div>
        <div class="form-group">
          <label class="form-label">Incoming Frame Source:</label>
          <select id="sim-sw-src" class="form-select">
            <option value="A:Port1">Host A (Port 1)</option>
            <option value="B:Port2">Host B (Port 2)</option>
            <option value="C:Port3">Host C (Port 3)</option>
            <option value="D:Port4">Host D (Port 4)</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Destination Host:</label>
          <select id="sim-sw-dst" class="form-select">
            <option value="B">Host B</option>
            <option value="A">Host A</option>
            <option value="C">Host C</option>
            <option value="D">Host D</option>
            <option value="Unknown">Unknown MAC (Not connected)</option>
          </select>
        </div>
        <button class="btn-primary" onclick="simSwitchSend()">Send Frame Through Switch</button>
        <div id="sim-switch-action" style="margin-top:0.5rem; font-size:0.85rem; font-weight:600; color:var(--primary-text);"></div>
      </div>
    </div>
  </div>
</section>
"""
