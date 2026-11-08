"""Chapter 5 Data: The Link Layer and LANs (Kurose & Ross 6th Ed.)
Comprehensive, textbook-grade expansion covering all subsections, inline SVGs, 
worked problems, and interactive simulators.
"""

CH5_DATA = {
    "id": "ch5",
    "num": 5,
    "title": "The Link Layer and LANs",
    "subtitle": "Error Detection/Correction, Multiple Access (ALOHA, CSMA/CD), ARP, Ethernet, Switches & Day in the Life",
    "layer": "Link Layer",
    "color": "#f59e0b",
    "objectives": [
        "Explain link-layer services (framing, link access, reliable delivery, error detection/correction) and NIC hardware implementation",
        "Formulate error-detection and error-correction codes: 1D Parity, 2D Parity single-bit correction, and CRC polynomial division",
        "Derive and contrast multiple access protocol efficiencies: Pure ALOHA (18.4%), Slotted ALOHA (36.8%), and CSMA/CD",
        "Trace CSMA/CD collision detection, the 48-bit jam signal, and Binary Exponential Backoff timing",
        "Contrast 48-bit MAC addresses with 32-bit IP addresses, and trace Address Resolution Protocol (ARP) query/response exchanges",
        "Dissect the bit-accurate IEEE 802.3 Ethernet frame and explain runt frame padding to the 64-byte minimum size",
        "Analyze the self-learning switch algorithm (filtering, forwarding, flooding) and contrast switches with routers",
        "Construct Virtual Local Area Networks (VLANs) with IEEE 802.1Q 4-byte trunk tag encapsulation",
        "Evaluate Multiprotocol Label Switching (MPLS) label-switched routing and modern Data Center fat-tree architectures",
        "Synthesize 'A Day in the Life of a Web Page Request' across DHCP, ARP, DNS, OSPF, BGP, TCP, and HTTP"
    ],
    "sections": [
        {
            "id": "ch5-1",
            "num": "5.1",
            "title": "Introduction to the Link Layer",
            "subtitle": "Services, nodes, links, and implementation in Network Interface Controllers (NICs)",
            "content": r"""
<p>While the network layer provides end-to-end communication from the original source host to the final destination host across the global Internet, the <strong>link layer</strong> is responsible for transporting a datagram across an <em>individual communication link</em> between two directly adjacent nodes.</p>

<div class="callout callout-insight">
  <div class="callout-header">💡 The Transportation Analogy (Kurose & Ross)</div>
  <p>Consider a traveler taking a trip from Jeddah to New York City:</p>
  <ul>
    <li>The traveler is an <strong>IP datagram</strong>.</li>
    <li>The travel agent that plans the entire itinerary (Jeddah &rarr; Riyadh &rarr; London &rarr; New York) is the <strong>routing algorithm</strong>.</li>
    <li>Each individual transportation segment (taxi from home to Jeddah airport, plane to Riyadh, plane to London, plane to JFK, train into Manhattan) is a <strong>link</strong>.</li>
    <li>The specific mode of transport (car, widebody jet, electric commuter train) is the <strong>link-layer protocol</strong> (Ethernet, WiFi, optical fiber, PPP).</li>
  </ul>
</div>

<h3>5.1.1 Services Provided by the Link Layer</h3>
<p>Different link-layer protocols provide different subsets of services:</p>
<ul>
  <li><strong>Framing:</strong> Almost all link-layer protocols encapsulate the network-layer datagram within a link-layer <strong>frame</strong> by adding a header and a trailer. The frame header specifies source and destination physical MAC addresses.</li>
  <li><strong>Link Access (Medium Access Control - MAC):</strong> On shared broadcast media (e.g., WiFi or coaxial cable), a MAC protocol coordinates which node is permitted to transmit at any given instant to avoid collisions.</li>
  <li><strong>Reliable Delivery:</strong> When a link-layer protocol provides reliable delivery (e.g., 802.11 WiFi link-layer ACKs), it guarantees that each datagram is moved across the link without error. This service is essential for error-prone links (wireless), but unnecessary over low-error wired links (fiber or twisted-pair), which leave reliability to end-to-end TCP.</li>
  <li><strong>Flow Control:</strong> Prevents a fast sending node on one end of a link from overwhelming a slower receiving node on the other end.</li>
  <li><strong>Error Detection:</strong> Signal attenuation and electromagnetic noise can flip bits on the physical medium. Transmitters attach Error-Detection bits (checksums, parity, CRC); receivers verify integrity and drop corrupted frames.</li>
  <li><strong>Error Correction:</strong> The receiver not only detects that bit errors occurred, but determines exactly where in the frame the errors occurred and mathematically corrects them without requesting a retransmission (Forward Error Correction - FEC).</li>
</ul>

<h3>5.1.2 Where Is the Link Layer Implemented?</h3>
<p>Unlike the application and transport layers (which execute entirely in software within the operating system kernel and user space), the link layer is implemented in a physical <strong>Network Interface Controller (NIC)</strong>, also known as a network adapter (e.g., an Ethernet card or 802.11 WiFi chip):</p>

<!-- INLINE SVG: Figure 5.1 Link Layer NIC Implementation -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 240" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Host 1 (Sender) -->
      <rect x="30" y="30" width="350" height="180" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="2"/>
      <text x="205" y="52" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">Transmitting Host Architecture</text>

      <!-- CPU & RAM (OS Software) -->
      <rect x="50" y="70" width="140" height="60" rx="6" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="120" y="95" font-size="11" font-weight="700" fill="#1d4ed8" text-anchor="middle">CPU & RAM</text>
      <text x="120" y="112" font-size="9" fill="#3b82f6" text-anchor="middle">App & OS Kernel (IP)</text>

      <!-- System Bus -->
      <line x1="190" y1="100" x2="225" y2="100" stroke="#64748b" stroke-width="4"/>
      <text x="207" y="92" font-size="8" fill="#64748b" text-anchor="middle">Bus</text>

      <!-- Network Interface Card (NIC / Hardware) -->
      <rect x="225" y="70" width="140" height="120" rx="6" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="295" y="92" font-size="11" font-weight="800" fill="#1e40af" text-anchor="middle">NIC (Adapter)</text>
      <rect x="235" y="105" width="120" height="40" rx="4" fill="#3b82f6"/>
      <text x="295" y="122" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">Link Controller Chip</text>
      <text x="295" y="136" font-size="8" fill="#dbeafe" text-anchor="middle">Framing & CRC Hardware</text>
      <rect x="245" y="155" width="100" height="25" rx="3" fill="#1d4ed8"/>
      <text x="295" y="172" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">Physical Transceiver</text>

      <!-- Physical Cable -->
      <line x1="365" y1="167" x2="475" y2="167" stroke="#059669" stroke-width="6"/>
      <text x="420" y="155" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Physical Link</text>

      <!-- Host 2 (Receiver) -->
      <rect x="475" y="30" width="335" height="180" rx="8" fill="#f8fafc" stroke="#10b981" stroke-width="2"/>
      <text x="642" y="52" font-size="12" font-weight="700" fill="#065f46" text-anchor="middle">Receiving Host Architecture</text>

      <!-- Receiving NIC -->
      <rect x="495" y="70" width="140" height="120" rx="6" fill="#d1fae5" stroke="#059669" stroke-width="2"/>
      <text x="565" y="92" font-size="11" font-weight="800" fill="#065f46" text-anchor="middle">NIC (Adapter)</text>
      <rect x="505" y="105" width="120" height="40" rx="4" fill="#10b981"/>
      <text x="565" y="122" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">Link Controller Chip</text>
      <text x="565" y="136" font-size="8" fill="#d1fae5" text-anchor="middle">CRC Check & Unpack</text>
      <rect x="515" y="155" width="100" height="25" rx="3" fill="#047857"/>
      <text x="565" y="172" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">Physical Transceiver</text>

      <!-- Receiving CPU/OS -->
      <line x1="635" y1="100" x2="670" y2="100" stroke="#64748b" stroke-width="4"/>
      <rect x="670" y="70" width="125" height="60" rx="6" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1.5"/>
      <text x="732" y="95" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">CPU & RAM</text>
      <text x="732" y="112" font-size="9" fill="#059669" text-anchor="middle">OS Kernel Interrupt</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 5.1 — Hardware vs. Software Boundary: The link layer is implemented in dedicated hardware within the Network Interface Controller (NIC) (§5.1.2).</div>
</div>
""",
            "quiz": [
                {
                    "q": "Why is the link layer primarily implemented in hardware on a Network Interface Controller (NIC) rather than in operating system software?",
                    "opts": [
                        "Because software cannot generate binary 1s and 0s",
                        "Because high-speed bit-level operations (framing, serialization, CRC calculation, and signal modulation) require specialized hardware circuits to match gigabit transmission rates without overwhelming the host CPU",
                        "Because TCP prohibits link-layer software",
                        "To prevent computer viruses from reading Ethernet frames"
                    ],
                    "ans": 1,
                    "exp": "High-speed framing, bit-level encoding, and polynomial CRC checks are implemented in hardware on the network adapter controller to achieve line-rate performance (§5.1.2)."
                }
            ]
        },
        {
            "id": "ch5-2",
            "num": "5.2",
            "title": "Error-Detection and -Correction Techniques",
            "subtitle": "Parity checks (1D & 2D), checksums, and Cyclic Redundancy Check (CRC)",
            "content": r"""
<p>Electromagnetic radiation, lightning, cross-talk, and thermal noise on physical links can inadvertently flip binary bits during transmission (turning 0s into 1s and vice-versa). To detect and correct these errors, the sending node appends <strong>Error-Detection and -Correction (EDC) bits</strong> to the transmitted data <span class="math-inline">D</span>.</p>

<h3>5.2.1 Parity Checks</h3>
<ul>
  <li><strong>Single-Bit Parity (1D):</strong> In an even-parity scheme, the sender chooses a single parity bit such that the total number of 1s in <span class="math-inline">\langle D, \text{parity} \rangle</span> is even.
    <br>&bull; <em>Limitation:</em> If an <strong>odd number</strong> of bits flip (1, 3, 5...), the error is detected. If an <strong>even number</strong> of bits flip (2, 4...), the parity sum remains even and the error passes completely undetected! Cannot correct any errors.
  </li>
  <li><strong>Two-Dimensional Parity:</strong> Data bits are arranged into a matrix of <span class="math-inline">i</span> rows and <span class="math-inline">j</span> columns. An even-parity bit is computed for every individual row and every individual column:</li>
</ul>

<!-- INLINE SVG: Figure 5.2 2D Parity Matrix Single-Bit Error Correction -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 260" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Title -->
      <text x="420" y="30" font-size="13" font-weight="700" fill="#1e293b" text-anchor="middle">2-Dimensional Parity Matrix: Locating and Correcting Single-Bit Errors</text>

      <!-- Matrix Grid Columns: col0, col1, col2, col_parity -->
      <!-- Row 0 -->
      <rect x="250" y="55" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="272" y="80" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">0</text>

      <rect x="300" y="55" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="322" y="80" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">1</text>

      <rect x="350" y="55" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="372" y="80" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">0</text>

      <rect x="415" y="55" width="45" height="40" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="437" y="80" font-size="14" font-weight="800" fill="#7e22ce" text-anchor="middle">1</text>
      <text x="490" y="80" font-size="10" fill="#64748b">Row 1 Parity (OK)</text>

      <!-- Row 1 (Corrupted Row) -->
      <rect x="250" y="100" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="272" y="125" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">1</text>

      <!-- Corrupted Bit: was 0, flipped to 1 -->
      <rect x="300" y="100" width="45" height="40" fill="#fee2e2" stroke="#ef4444" stroke-width="3"/>
      <text x="322" y="125" font-size="16" font-weight="900" fill="#b91c1c" text-anchor="middle">1*</text>

      <rect x="350" y="100" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="372" y="125" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">1</text>

      <rect x="415" y="100" width="45" height="40" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
      <text x="437" y="125" font-size="14" font-weight="800" fill="#b91c1c" text-anchor="middle">0</text>
      <text x="525" y="125" font-size="10" font-weight="700" fill="#ef4444">&larr; Row 2 Parity MISMATCH!</text>

      <!-- Row 2 -->
      <rect x="250" y="145" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="272" y="170" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">1</text>

      <rect x="300" y="145" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="322" y="170" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">1</text>

      <rect x="350" y="145" width="45" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="372" y="170" font-size="14" font-weight="700" fill="#1e40af" text-anchor="middle">0</text>

      <rect x="415" y="145" width="45" height="40" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="437" y="170" font-size="14" font-weight="800" fill="#7e22ce" text-anchor="middle">0</text>
      <text x="490" y="170" font-size="10" fill="#64748b">Row 3 Parity (OK)</text>

      <!-- Column Parity Row -->
      <rect x="250" y="200" width="45" height="40" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="272" y="225" font-size="14" font-weight="800" fill="#7e22ce" text-anchor="middle">0</text>

      <rect x="300" y="200" width="45" height="40" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
      <text x="322" y="225" font-size="14" font-weight="800" fill="#b91c1c" text-anchor="middle">1</text>

      <rect x="350" y="200" width="45" height="40" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="372" y="225" font-size="14" font-weight="800" fill="#7e22ce" text-anchor="middle">1</text>

      <!-- Intersect Pointer -->
      <text x="322" y="255" font-size="10" font-weight="700" fill="#ef4444" text-anchor="middle">&uarr; Col 2 Error</text>
      <text x="640" y="215" font-size="11" font-weight="700" fill="#047857">Intersection (Row 2, Col 2) Pinpoints Error!</text>
      <text x="640" y="235" font-size="10" fill="#334155">Invert bit 1* back to 0 &rarr; Auto-Corrected!</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 5.2 — Two-Dimensional Even Parity Check: The intersection of the row parity mismatch and column parity mismatch isolates and corrects the single corrupted bit (§5.2.1).</div>
</div>

<h3>5.2.2 Cyclic Redundancy Check (CRC)</h3>
<p>Used universally in modern link-layer adapters (Ethernet, 802.11 WiFi, HDLC). CRC codes operate using <strong>modulo-2 binary arithmetic</strong> without carries or borrows (equivalent to bitwise XOR):</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Mathematical Formulation of CRC (§5.2.3)</div>
  <p>Consider a <span class="math-inline">d</span>-bit data piece <span class="math-inline">D</span>. The sender and receiver agree on an <span class="math-inline">(r+1)</span>-bit generator pattern <span class="math-inline">G</span>, whose most significant bit is 1.</p>
  <p>We want to find <span class="math-inline">r</span> CRC bits <span class="math-inline">R</span> such that the combined <span class="math-inline">(d+r)</span>-bit pattern <span class="math-inline">D \cdot 2^r \oplus R</span> is exactly divisible by <span class="math-inline">G</span> using modulo-2 arithmetic:</p>
  <div class="math-display">
    \frac{D \cdot 2^r \oplus R}{G} = n \implies R = \text{remainder of } \left( \frac{D \cdot 2^r}{G} \right)
  </div>
  <p><strong>Error Detection at Receiver:</strong> The receiver divides the arriving <span class="math-inline">(d+r)</span> bits by generator <span class="math-inline">G</span>. If the remainder is non-zero, an error has occurred! Standard 32-bit CRC (CRC-32 used in Ethernet) detects all burst errors of 32 bits or fewer, and 99.9999999% of all larger bursts.</p>
</div>

<!-- EMBEDDED INTERACTIVE: 2D PARITY MATRIX CHECKER -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🔍 Interactive 2D Parity Matrix & Single-Bit Error Corrector</div>
    <span class="interactive-badge">Error Correction Tool</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Toggle any bit in the data matrix below to simulate transmission noise. Click "Detect & Correct Error" to watch the parity algorithm locate and repair the bit:
  </p>
  <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1.25rem;">
    <div style="display:grid; grid-template-columns:repeat(4, 50px); gap:8px; max-width:240px; margin:0 auto 1rem auto; text-align:center;">
      <div style="font-size:0.75rem; color:var(--text-muted);">Col 1</div>
      <div style="font-size:0.75rem; color:var(--text-muted);">Col 2</div>
      <div style="font-size:0.75rem; color:var(--text-muted);">Col 3</div>
      <div style="font-size:0.75rem; font-weight:700; color:var(--primary);">Parity</div>

      <!-- Row 0 -->
      <div><input type="checkbox" id="sec5-p-r0c0"></div>
      <div><input type="checkbox" id="sec5-p-r0c1" checked></div>
      <div><input type="checkbox" id="sec5-p-r0c2"></div>
      <div style="font-weight:700; color:var(--primary);">1</div>

      <!-- Row 1 -->
      <div><input type="checkbox" id="sec5-p-r1c0" checked></div>
      <div><input type="checkbox" id="sec5-p-r1c1"></div>
      <div><input type="checkbox" id="sec5-p-r1c2" checked></div>
      <div style="font-weight:700; color:var(--primary);">0</div>

      <!-- Row 2 -->
      <div><input type="checkbox" id="sec5-p-r2c0" checked></div>
      <div><input type="checkbox" id="sec5-p-r2c1" checked></div>
      <div><input type="checkbox" id="sec5-p-r2c2"></div>
      <div style="font-weight:700; color:var(--primary);">0</div>

      <!-- Col Parity -->
      <div style="font-weight:700; color:var(--primary);">0</div>
      <div style="font-weight:700; color:var(--primary);">0</div>
      <div style="font-weight:700; color:var(--primary);">1</div>
      <div style="color:var(--text-muted);">&mdash;</div>
    </div>
    <div class="fig-controls">
      <button class="btn-primary" onclick="detectCorrectParity()">🔍 Detect & Correct Error</button>
      <button class="btn-secondary" onclick="resetParityMatrix()">🔄 Reset Clean Matrix</button>
    </div>
    <div id="sec5-parity-result" class="calc-result-box" style="margin-top:1rem;">
      Matrix is currently clean with zero errors.
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the primary advantage of 2-Dimensional Parity over standard 1-Dimensional Parity?",
                    "opts": [
                        "It consumes fewer total bits",
                        "It can both detect and automatically correct any single-bit error by identifying the row and column intersection",
                        "It eliminates the need for IP addresses",
                        "It runs over optical fiber only"
                    ],
                    "ans": 1,
                    "exp": "The intersection of the single row parity failure and single column parity failure uniquely locates the flipped bit, enabling forward error correction (§5.2.1)."
                },
                {
                    "q": "In CRC calculation with a 4-bit generator G = 1001, how many zero bits must be appended to data D before performing modulo-2 division?",
                    "opts": [
                        "1 bit",
                        "3 bits (r bits, where generator has r+1 bits)",
                        "4 bits",
                        "16 bits"
                    ],
                    "ans": 1,
                    "exp": "If the generator G has length r + 1 bits (here 4 bits), exactly r = 3 zeros are appended to data D (§5.2.3)."
                }
            ]
        },
        {
            "id": "ch5-3",
            "num": "5.3",
            "title": "Multiple Access Links and Protocols",
            "subtitle": "Channel partitioning, Random Access (ALOHA, CSMA/CD), and Taking-Turns protocols",
            "content": r"""
<p>Network links fall into two broad classifications:</p>
<ol>
  <li><strong>Point-to-Point Links:</strong> Connect a single sender directly to a single receiver (e.g. PPP, HDLC, or an optical link between two backbone routers).</li>
  <li><strong>Broadcast Links (Shared Medium):</strong> Multiple transmitting nodes share the exact same physical communication channel (e.g., traditional coaxial Ethernet, wireless WiFi, or satellite uplinks).</li>
</ol>
<p>When multiple nodes transmit simultaneously over a broadcast link, their signals collide, destroying data. A <strong>Multiple Access Protocol (MAC)</strong> coordinates transmissions to prevent and resolve collisions.</p>

<h3>5.3.1 Taxonomy of Multiple Access Protocols</h3>
<p>Kurose & Ross classify all MAC protocols into three broad categories:</p>

<h4>1. Channel Partitioning Protocols</h4>
<ul>
  <li><strong>TDM (Time-Division Multiplexing):</strong> Time is divided into frames, with each frame partitioned into <span class="math-inline">N</span> fixed time slots (one per node). Eliminates collisions, but inefficient: even if only one node has data to send, its throughput is capped at <span class="math-inline">R/N</span>!</li>
  <li><strong>FDM (Frequency-Division Multiplexing):</strong> Bandwidth is divided into <span class="math-inline">N</span> distinct frequency bands. Suffers from the exact same <span class="math-inline">R/N</span> under-utilization when traffic is bursty.</li>
  <li><strong>CDMA (Code-Division Multiple Access):</strong> Assigns orthogonal codes to users; transmits simultaneously across the same frequency (detailed in Chapter 6).</li>
</ul>

<h4>2. Random Access Protocols</h4>
<p>Nodes transmit at the full channel rate <span class="math-inline">R</span> without prior coordination. When collisions occur, nodes retransmit after independent random delays.</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Mathematical Derivation of ALOHA Efficiencies (§5.3.2)</div>
  <p><strong>Slotted ALOHA:</strong> Time is divided into slots of duration <span class="math-inline">L/R</span>. Nodes transmit only at slot boundaries. If a collision occurs, each node retransmits in subsequent slots with probability <span class="math-inline">p</span>.</p>
  <ul>
    <li>Probability that a specific node succeeds in a slot: <span class="math-inline">p(1 - p)^{N-1}</span>.</li>
    <li>Probability that any of the <span class="math-inline">N</span> nodes succeeds: <span class="math-inline">S = N p (1 - p)^{N-1}</span>.</li>
    <li>Maximizing with respect to <span class="math-inline">p</span> yields optimal <span class="math-inline">p^* = 1/N</span>. Taking the limit as <span class="math-inline">N \to \infty</span>:
      <div class="math-display">
        \text{Maximum Efficiency (Slotted ALOHA)} = \lim_{N \to \infty} N \left(\frac{1}{N}\right) \left(1 - \frac{1}{N}\right)^{N-1} = \frac{1}{e} \approx \mathbf{0.368\ (36.8\%)}
      </div>
    </li>
  </ul>
  <p><strong>Pure (Unslotted) ALOHA:</strong> Nodes transmit immediately upon frame arrival. A transmission at time <span class="math-inline">t_0</span> will collide if any other node transmits in interval <span class="math-inline">[t_0 - t_{\text{frame}}, t_0 + t_{\text{frame}}]</span> (vulnerable window is <strong>twice as large</strong>: <span class="math-inline">2 \times t_{\text{frame}}</span>!).</p>
  <ul>
    <li>Probability of success: <span class="math-inline">S = N p (1 - p)^{2(N-1)}</span>.</li>
    <li>Maximum efficiency in the limit:
      <div class="math-display">
        \text{Maximum Efficiency (Pure ALOHA)} = \frac{1}{2e} \approx \mathbf{0.184\ (18.4\%)}
      </div>
    </li>
  </ul>
</div>

<h3>5.3.2 CSMA/CD (Carrier Sense Multiple Access with Collision Detection)</h3>
<p>Ethernet improves drastically over ALOHA by introducing two key rules:</p>
<ol>
  <li><strong>Carrier Sensing ("Listen before speaking"):</strong> A node listens to the channel before transmitting. If another node is transmitting, it defers.</li>
  <li><strong>Collision Detection ("Listen while speaking"):</strong> The node continuously listens to the wire <em>during its own transmission</em>. If it detects that another node is transmitting concurrently (detected by measuring elevated voltage levels on copper), it aborts its transmission immediately!</li>
</ol>

<div class="callout callout-def">
  <div class="callout-header">📘 The 48-bit Jam Signal & Binary Exponential Backoff</div>
  <p>Upon detecting a collision, the transmitting adapter aborts and broadcasts a <strong>48-bit Jam Signal</strong> to ensure that all other transmitting adapters detect the collision.</p>
  <p>The adapter then executes <strong>Binary Exponential Backoff</strong>:</p>
  <ul>
    <li>After collision <span class="math-inline">n</span> (capped at <span class="math-inline">n = 10</span>), the adapter chooses an integer <span class="math-inline">K</span> uniformly at random from:
      <div class="math-display">K \in \{0, 1, 2, \dots, 2^{\min(n, 10)} - 1\}</div>
    </li>
    <li>The node waits <span class="math-inline">K \times 512\text{ bit times}</span> (where 512 bit times = <span class="math-inline">51.2\ \mu\text{s}</span> on 10 Mbps Ethernet) before attempting to sense the carrier again.</li>
    <li>After 16 consecutive collisions, the adapter gives up and reports an error to higher layers.</li>
  </ul>
</div>
""",
            "quiz": [
                {
                    "q": "What is the maximum theoretical channel efficiency of Pure (Unslotted) ALOHA?",
                    "opts": [
                        "18.4% (1 / 2e)",
                        "36.8% (1 / e)",
                        "50.0%",
                        "100.0%"
                    ],
                    "ans": 0,
                    "exp": "Because unslotted ALOHA has a vulnerable collision window of twice the frame duration, its maximum efficiency is 1/(2e) ≈ 18.4% (§5.3.2)."
                },
                {
                    "q": "In CSMA/CD, what is the range of K chosen after a node experiences its 3rd consecutive collision?",
                    "opts": [
                        "{0, 1}",
                        "{0, 1, 2, 3}",
                        "{0, 1, 2, 3, 4, 5, 6, 7} (0 to 2^3 - 1)",
                        "{0, 1, ..., 1023}"
                    ],
                    "ans": 2,
                    "exp": "After collision n=3, K is chosen uniformly from {0, 1, ..., 2^3 - 1} = {0, 1, 2, 3, 4, 5, 6, 7} (§5.3.2)."
                }
            ]
        },
        {
            "id": "ch5-4",
            "num": "5.4",
            "title": "Switched Local Area Networks",
            "subtitle": "MAC addressing, ARP, Ethernet frames, self-learning switches & VLANs",
            "content": r"""
<p>Modern local area networks are dominated by switched Ethernet technologies. To understand switched LANs, we must examine MAC addresses, the Address Resolution Protocol (ARP), Ethernet frame structures, and switch forwarding.</p>

<h3>5.4.1 MAC Addresses: Physical vs. Network Addressing</h3>
<p>Hosts and routers have both network-layer IP addresses and link-layer MAC addresses:</p>
<ul>
  <li><strong>MAC Address (Physical / Hardware / Ethernet Address):</strong> A <strong>48-bit (6-byte)</strong> identifier permanently burned into the adapter's ROM (e.g. <code>00:1A:2B:3C:4D:5E</code>).
    <br>&bull; Governed by IEEE: the first 24 bits are the <strong>OUI (Organizationally Unique Identifier)</strong> assigned to the manufacturer (Intel, Cisco, Apple); the remaining 24 bits are unique to the adapter.
    <br>&bull; <em>Flat and portable:</em> A laptop's MAC address never changes regardless of whether it connects in Jeddah, Tokyo, or New York.
  </li>
  <li><strong>IP Address:</strong> 32-bit hierarchical address reflecting the node's current point of attachment to the network topology. Not portable.</li>
</ul>

<div class="callout callout-insight">
  <div class="callout-header">💡 The Analogy: Social Security Number vs. Postal Mailing Address</div>
  A person's Social Security Number (or national ID) is flat, unique, and stays with them for life (like a <strong>MAC address</strong>). A person's residential postal mailing address changes every time they move houses (like an <strong>IP address</strong>)!
</div>

<h3>5.4.2 Address Resolution Protocol (ARP, RFC 826)</h3>
<p>How does a sending host resolve a known 32-bit destination IP address into the 48-bit MAC address required to construct the Ethernet frame header?</p>

<!-- INLINE SVG: Figure 5.3 ARP Exchange -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 220" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Host A -->
      <rect x="50" y="50" width="130" height="60" rx="8" fill="#3b82f6"/>
      <text x="115" y="75" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Host A (Sender)</text>
      <text x="115" y="90" font-size="8" fill="#dbeafe" text-anchor="middle">IP: 192.168.1.10</text>
      <text x="115" y="102" font-size="8" fill="#dbeafe" text-anchor="middle">MAC: AA:AA:AA:AA:AA:AA</text>

      <!-- Shared Switch / Bus -->
      <rect x="250" y="65" width="340" height="30" rx="4" fill="#64748b"/>
      <text x="420" y="84" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Switched Ethernet Subnet (192.168.1.0/24)</text>

      <!-- Host B -->
      <rect x="660" y="50" width="130" height="60" rx="8" fill="#10b981"/>
      <text x="725" y="75" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Host B (Target)</text>
      <text x="725" y="90" font-size="8" fill="#d1fae5" text-anchor="middle">IP: 192.168.1.50</text>
      <text x="725" y="102" font-size="8" fill="#d1fae5" text-anchor="middle">MAC: BB:BB:BB:BB:BB:BB</text>

      <!-- Step 1: Broadcast Request -->
      <path d="M 180 80 Q 420 140 655 80" stroke="#3b82f6" stroke-width="3" fill="none"/>
      <text x="420" y="130" font-size="9" font-weight="700" fill="#1d4ed8" text-anchor="middle">1. ARP Request (Broadcast to FF:FF:FF:FF:FF:FF) "Who has 192.168.1.50?"</text>

      <!-- Step 2: Unicast Reply -->
      <path d="M 660 95 Q 420 185 180 95" stroke="#10b981" stroke-width="3" fill="none" stroke-dasharray="5 3"/>
      <text x="420" y="175" font-size="9" font-weight="700" fill="#047857" text-anchor="middle">2. ARP Reply (Unicast to AA:AA:AA:AA:AA:AA) "I have 192.168.1.50, my MAC is BB:..."</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 5.3 — Address Resolution Protocol (ARP): Broadcast Request on Subnet & Unicast Direct Reply (§5.4.2).</div>
</div>

<ol>
  <li><strong>Broadcast ARP Request:</strong> Host A encapsulates an ARP query inside an Ethernet frame with Destination MAC <code>FF:FF:FF:FF:FF:FF</code> (broadcast). Every adapter on the local subnet receives the frame and passes the ARP query to its operating system.</li>
  <li><strong>Unicast ARP Reply:</strong> Only Host B (whose IP matches) responds. Because Host B learned Host A's MAC from the request, it transmits a <strong>unicast ARP Reply</strong> addressed directly to Host A's MAC.</li>
  <li><strong>ARP Cache Table:</strong> Host A caches the <code>(IP, MAC, TTL)</code> mapping in its local ARP table (typical timeout 20 minutes) so future packets require no lookup.</li>
</ol>

<h3>5.4.3 The IEEE 802.3 Ethernet Frame</h3>
<!-- INLINE SVG: Figure 5.4 Ethernet Frame -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 160" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Preamble (8B) -->
      <rect x="20" y="45" width="100" height="55" fill="#f8fafc" stroke="#475569" stroke-width="1.5" rx="3"/>
      <text x="70" y="70" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">Preamble (7B)</text>
      <text x="70" y="86" font-size="8" fill="#64748b" text-anchor="middle">+ SFD (1B)</text>

      <!-- Dst MAC (6B) -->
      <rect x="120" y="45" width="110" height="55" fill="#eff6ff" stroke="#3b82f6" stroke-width="2" rx="3"/>
      <text x="175" y="70" font-size="11" font-weight="800" fill="#1d4ed8" text-anchor="middle">Dst MAC</text>
      <text x="175" y="86" font-size="8" fill="#2563eb" text-anchor="middle">6 Bytes</text>

      <!-- Src MAC (6B) -->
      <rect x="230" y="45" width="110" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="3"/>
      <text x="285" y="70" font-size="11" font-weight="800" fill="#047857" text-anchor="middle">Src MAC</text>
      <text x="285" y="86" font-size="8" fill="#059669" text-anchor="middle">6 Bytes</text>

      <!-- Type (2B) -->
      <rect x="340" y="45" width="70" height="55" fill="#fdf4ff" stroke="#c084fc" stroke-width="1.5" rx="3"/>
      <text x="375" y="70" font-size="10" font-weight="800" fill="#7e22ce" text-anchor="middle">Type</text>
      <text x="375" y="86" font-size="8" fill="#9333ea" text-anchor="middle">2 Bytes (0x0800)</text>

      <!-- Payload (46-1500B) -->
      <rect x="410" y="45" width="310" height="55" fill="#f1f5f9" stroke="#334155" stroke-width="2" rx="3"/>
      <text x="565" y="70" font-size="12" font-weight="800" fill="#0f172a" text-anchor="middle">IP Datagram Payload</text>
      <text x="565" y="88" font-size="9" fill="#475569" text-anchor="middle">46 to 1500 Bytes (MTU = 1500B)</text>

      <!-- CRC (4B) -->
      <rect x="720" y="45" width="100" height="55" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="3"/>
      <text x="770" y="70" font-size="11" font-weight="800" fill="#991b1b" text-anchor="middle">CRC-32</text>
      <text x="770" y="86" font-size="8" fill="#dc2626" text-anchor="middle">4 Bytes</text>

      <!-- Under-bracket for minimum frame size -->
      <text x="420" y="130" font-size="10" font-weight="700" fill="#475569" text-anchor="middle">Minimum Total Frame Size: 64 Bytes (6B + 6B + 2B + 46B + 4B = 64B)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 5.4 — Bit-Accurate IEEE 802.3 Ethernet Frame Format (§5.4.3).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 Why Ethernet Frames Have a 46-Byte Minimum Payload</div>
  On legacy shared coaxial Ethernet, a transmitting adapter had to transmit for at least 512 bit times (<span class="math-inline">51.2\ \mu\text{s}</span> at 10 Mbps) to ensure that collisions across maximum round-trip propagation distance were reliably detected before transmission finished. 512 bits = 64 bytes total frame size! If payload is smaller than 46 bytes, the adapter automatically inserts <strong>padding bytes</strong>.
</div>

<h3>5.4.4 Link-Layer Switches: Self-Learning and Filtering</h3>
<p>An Ethernet switch is a <strong>Layer-2 packet switch</strong>. Its primary role is to filter and forward frames based on 48-bit MAC addresses. A switch is completely <strong>plug-and-play</strong>: network administrators do not configure forwarding tables!</p>

<h4>The Self-Learning Algorithm:</h4>
<p>A switch builds its forwarding table <code>(MAC Address, Interface, Timestamp)</code> automatically:</p>
<ol>
  <li>When a frame arrives on interface <span class="math-inline">x</span> with Source MAC <span class="math-inline">S</span>:
    <br>&bull; The switch creates (or refreshes) the table entry: <span class="math-inline">(S, x, \text{current time})</span>.
  </li>
  <li>To forward the frame, the switch looks up Destination MAC <span class="math-inline">D</span> in its table:
    <br>&bull; <strong>Filtering (Drop):</strong> If <span class="math-inline">D</span> is found and mapped to the <em>same interface</em> <span class="math-inline">x</span> on which the frame arrived, the destination already received the transmission. The switch drops the frame.
    <br>&bull; <strong>Selective Forwarding:</strong> If <span class="math-inline">D</span> is found and mapped to interface <span class="math-inline">y \ne x</span>, the switch transmits the frame out interface <span class="math-inline">y</span> only!
    <br>&bull; <strong>Flooding:</strong> If <span class="math-inline">D</span> is NOT found in the table, the switch broadcasts (floods) the frame out <em>all interfaces except interface <span class="math-inline">x</span></em>.
  </li>
</ol>

<h3>5.4.5 Virtual Local Area Networks (VLANs)</h3>
<p>In a large organization, connecting all departmental hosts to a single physical switch creates three severe problems: lack of traffic isolation (broadcast frames flood across the entire company), inefficient switch resource usage, and security vulnerabilities.</p>
<p>A <strong>VLAN</strong> logically partitions a single physical switch into multiple isolated broadcast domains. In <strong>port-based VLANs</strong>, switch ports are divided into logical groups (e.g., Ports 1–8 = Engineering VLAN 100, Ports 9–16 = Finance VLAN 200).</p>

<h4>802.1Q VLAN Trunking:</h4>
<p>When multiple physical switches are interconnected, a <strong>VLAN Trunk Link</strong> carries traffic belonging to all VLANs. To preserve VLAN identity across the trunk, the sending switch inserts a <strong>4-byte 802.1Q VLAN tag</strong> directly after the Source MAC field of the Ethernet frame:</p>
<ul>
  <li><strong>TPID (Tag Protocol Identifier, 2 bytes):</strong> Fixed value <code>0x8100</code> identifying this as an 802.1Q tagged frame.</li>
  <li><strong>Tag Control Information (TCI, 2 bytes):</strong> Contains 3-bit Priority, 1-bit Canonical Format, and the <strong>12-bit VLAN ID (VID)</strong> (supporting up to <span class="math-inline">2^{12} = 4096</span> VLANs).</li>
</ul>
""",
            "quiz": [
                {
                    "q": "What action does a self-learning switch take when it receives a frame whose destination MAC address does NOT appear in its switch table?",
                    "opts": [
                        "It returns an ICMP Destination Unreachable message to the sender",
                        "It drops the frame silently",
                        "It floods the frame out all switch interfaces except the interface on which the frame arrived",
                        "It forwards the frame to the default gateway router only"
                    ],
                    "ans": 2,
                    "exp": "When the destination MAC is unknown, the switch floods the frame out all other ports so the target can receive it and respond, which allows the switch to learn its location (§5.4.4)."
                },
                {
                    "q": "How many bits long is the VLAN ID field in an IEEE 802.1Q VLAN trunk tag?",
                    "opts": [
                        "4 bits",
                        "8 bits",
                        "12 bits (supporting up to 4096 VLANs)",
                        "32 bits"
                    ],
                    "ans": 2,
                    "exp": "The 802.1Q tag contains a 12-bit VLAN identifier (VID), supporting up to 2^12 = 4096 distinct logical VLANs (§5.4.5)."
                }
            ]
        },
        {
            "id": "ch5-5",
            "num": "5.5",
            "title": "Link Virtualization: Multiprotocol Label Switching (MPLS)",
            "subtitle": "Label-switched routing, label swapping, and traffic engineering",
            "content": r"""
<p>Traditional IP routers forward datagrams by examining the 32-bit IP destination address and performing a computationally intensive <strong>Longest Prefix Match (LPM)</strong> lookup in a massive routing table. <strong>Multiprotocol Label Switching (MPLS)</strong> was designed to dramatically speed up forwarding in the network core by replacing IP lookups with fixed-length <strong>label swapping</strong>.</p>

<h3>5.5.1 The MPLS Shim Header</h3>
<p>An MPLS header is a 4-byte "shim" inserted between the link-layer (Layer 2) header and the network-layer (Layer 3) IP header (often called Layer 2.5):</p>
<ul>
  <li><strong>Label (20 bits):</strong> The fixed-length index used by Label Switched Routers (LSRs) to index directly into a high-speed forwarding table.</li>
  <li><strong>Exp (3 bits):</strong> Experimental bits used for Quality of Service (QoS) class prioritization.</li>
  <li><strong>S (1 bit):</strong> Stacking bit; set to 1 if this is the bottom of the label stack (MPLS allows hierarchical label stacking).</li>
  <li><strong>TTL (8 bits):</strong> Time-To-Live decremented at each hop to prevent infinite forwarding loops.</li>
</ul>

<h3>5.5.2 Label Swapping & Traffic Engineering</h3>
<p>When an IP datagram enters an MPLS-enabled Autonomous System at an <strong>Ingress LSR</strong>, the router inspects the IP header once and pushes an initial MPLS label onto the packet. Interior LSRs forward the packet purely by inspecting the 20-bit label: they look up the incoming label, swap it for an outgoing label, and forward it out the designated interface. The <strong>Egress LSR</strong> strips the label and delivers the original IP datagram.</p>
<p><em>Advantage:</em> Allows network operators to implement <strong>Traffic Engineering</strong>: routing different flows between the same source and destination across different physical paths (impossible with standard destination-based IP routing!).</p>
""",
            "quiz": [
                {
                    "q": "How many bits long is the primary forwarding Label in an MPLS header?",
                    "opts": [
                        "8 bits",
                        "16 bits",
                        "20 bits",
                        "32 bits"
                    ],
                    "ans": 2,
                    "exp": "The MPLS label field is exactly 20 bits long, contained within a 32-bit (4-byte) shim header (§5.5.1)."
                }
            ]
        },
        {
            "id": "ch5-6",
            "num": "5.6",
            "title": "Data Center Networking",
            "subtitle": "Hierarchical topologies, Top-of-Rack (ToR) switches, and fat-tree architectures",
            "content": r"""
<p>Modern cloud datacenters (Google, Amazon AWS, Microsoft Azure) house hundreds of thousands of computing blade servers organized into vertical <strong>server racks</strong>. Each rack typically holds 20 to 40 servers interconnected by a dedicated <strong>Top-of-Rack (ToR) switch</strong>.</p>

<h3>5.6.1 The Bisection Bandwidth Bottleneck</h3>
<p>Traditional corporate networks used simple hierarchical tree architectures (Access switches &rarr; Aggregation switches &rarr; Core routers). In a data center, this architecture suffers from a catastrophic bottleneck: <strong>low bisection bandwidth</strong>. Traffic between servers located in different racks must traverse the top-tier core switches, which quickly become congested, throttling distributed parallel computing frameworks like Hadoop and MapReduce.</p>

<h3>5.6.2 The Fat-Tree (Folded Clos) Architecture</h3>
<p>To provide massive bisection bandwidth, modern datacenters deploy <strong>Fat-Tree (Multi-Tier Clos)</strong> architectures:</p>
<ul>
  <li>Top-of-Rack switches connect to multiple parallel Aggregation switches, which in turn connect to a mesh of Core switches.</li>
  <li>Between any two server racks, there exist <strong>multiple parallel, equal-cost paths</strong>.</li>
  <li>Using <strong>Equal-Cost Multi-Path (ECMP)</strong> hashing at the link/network layer, traffic flows are distributed evenly across the entire switching fabric, allowing all servers to communicate at full line rate simultaneously!</li>
</ul>
""",
            "quiz": [
                {
                    "q": "In data center networking, what is the role of a Top-of-Rack (ToR) switch?",
                    "opts": [
                        "It acts as the authoritative DNS root server",
                        "It provides high-speed link-layer connectivity among all 20 to 40 servers mounted inside that physical rack and connects them to the data center network fabric",
                        "It encrypts all hard drives using RSA",
                        "It replaces the need for power supplies"
                    ],
                    "ans": 1,
                    "exp": "The ToR switch sits at the top of the physical equipment rack, interconnecting the rack's blade servers and linking them into the aggregation switches (§5.6.1)."
                }
            ]
        },
        {
            "id": "ch5-7",
            "num": "5.7",
            "title": "A Day in the Life of a Web Page Request",
            "subtitle": "The grand synthesis of DHCP, ARP, DNS, OSPF, BGP, TCP, and HTTP",
            "content": r"""
<p>To conclude our journey through the protocol stack (Chapters 1 to 5), let us trace every single protocol event that occurs when a student connects a new laptop to a campus network and requests <code>www.google.com</code>:</p>

<div class="summary-grid" style="margin:1rem 0;">
  <div class="summary-card" style="border-top:3px solid #3b82f6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">1. DHCP (Network Bootstrap)</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Laptop broadcasts <strong>DHCP Discover</strong> inside UDP port 67. Campus DHCP server replies with <strong>DHCP ACK</strong>: laptop receives its IP address (<code>68.85.2.101/24</code>), Default Gateway router IP (<code>68.85.2.1</code>), and Local DNS IP (<code>68.87.71.226</code>).
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #10b981;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">2. ARP (Gateway Resolution)</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      To send traffic to the Internet, the laptop must frame packets to the gateway's Layer-2 MAC. Laptop broadcasts an <strong>ARP Request</strong> on the subnet; the default gateway router replies with its MAC address (<code>00:22:6B:45:11:00</code>).
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #8b5cf6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">3. DNS (Name Resolution)</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Laptop encapsulates a DNS query for <code>www.google.com</code> inside UDP port 53, addressed to local DNS server. Campus intra-domain routing (<strong>OSPF</strong>) and inter-domain routing (<strong>BGP</strong>) forward the query. DNS server replies with Google's IP: <code>64.233.169.103</code>.
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #f59e0b;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">4. TCP & HTTP (Page Fetch)</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Laptop opens a TCP socket and executes the <strong>3-Way Handshake</strong> (<code>SYN</code> &rarr; <code>SYN-ACK</code> &rarr; <code>ACK</code>) with Google on port 80. Laptop then sends <code>GET /index.html HTTP/1.1</code>. Google replies with <code>200 OK</code> and HTML. Browser renders page!
    </p>
  </div>
</div>

<!-- CAPSTONE INTERACTIVE: DAY IN THE LIFE ANIMATOR -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🌐 Interactive Capstone: A Day in the Life Step-Through</div>
    <span class="interactive-badge">End-to-End Synthesis</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Follow each step from plugging in the ethernet cable to seeing the rendered web page:
  </p>
  <div class="fig-controls" style="margin-bottom:1rem;">
    <button class="btn-primary" onclick="stepSec5DayLife()">⏭ Next Protocol Step</button>
    <button class="btn-secondary" onclick="resetSec5DayLife()">🔄 Reset</button>
    <span id="sec5-daylife-step" class="fig-step-badge">Ready</span>
  </div>
  <div id="sec5-daylife-desc" style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1.25rem;">
    Click "Next Protocol Step" to trace the journey across DHCP, ARP, DNS, OSPF, BGP, TCP, and HTTP.
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In 'A Day in the Life of a Web Page Request', why does the laptop use ARP to find the MAC address of the default gateway router rather than Google's web server?",
                    "opts": [
                        "Because Google's web server does not have a MAC address",
                        "Because MAC addresses are local link-layer addresses valid only within the immediate subnet; packets destined for remote subnets must be framed to the local first-hop router",
                        "Because ARP only works over WiFi",
                        "Because the DNS server blocks Google's MAC address"
                    ],
                    "ans": 1,
                    "exp": "MAC addresses have local link-layer scope and cannot cross routers. To reach an external destination, datagrams must be addressed to the default gateway's MAC address (§5.4.1, §5.7)."
                }
            ]
        },
        {
            "id": "ch5-8",
            "num": "5.8",
            "title": "Chapter 5 Summary & Worked Problems",
            "subtitle": "CRC polynomial division and CSMA/CD maximum distance calculations",
            "content": r"""
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 1: CRC Long Division Trace</div>
    <span class="interactive-badge">P4 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Suppose data payload <span class="math-inline">D = 101110</span> (6 bits) and the agreed generator polynomial is <span class="math-inline">G = 1001</span> (<span class="math-inline">r+1 = 4</span> bits, so <span class="math-inline">r = 3</span> bits).
    <br>Find the CRC remainder bits <span class="math-inline">R</span> and determine the final transmitted frame.
  </p>

  <button class="btn-secondary" onclick="toggleSolution('ch5-prob1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch5-prob1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Append <span class="math-inline">r = 3</span> zeros to <span class="math-inline">D</span>: <span class="math-inline">D \cdot 2^3 = 101110000</span>.</div>
    <div class="calc-step">Step 2: Divide 101110000 by 1001 using modulo-2 bitwise XOR subtraction:
      <pre style="font-family:monospace; background:var(--bg-secondary); padding:10px; border-radius:6px; margin:0.5rem 0;">
  101110000
XOR 1001
----------
    01010000  -> 1010000
XOR 1001
----------
    0011000   -> 11000
XOR   1001
----------
      01010   -> 1010
XOR   1001
----------
      0011    -> Remainder R = 011
      </pre>
    </div>
    <div class="calc-step">Step 3: Append remainder <span class="math-inline">R = 011</span> to original data <span class="math-inline">D = 101110</span>.</div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
      Final Answer: The CRC code is <strong>R = 011</strong>. The complete transmitted frame is <strong>101110011</strong> (9 bits total).
    </div>
  </div>
</div>

<div class="interactive-card" style="margin-top:1.5rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 2: CSMA/CD Minimum Frame Size & Maximum Cable Length</div>
    <span class="interactive-badge">P14 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> On a classic 10 Mbps CSMA/CD Ethernet network, the propagation speed is <span class="math-inline">s = 2 \times 10^8\text{ m/s}</span>. The minimum frame size is 64 bytes (512 bits).
    <br>What is the maximum permissible cable distance between two nodes to ensure that all collisions are reliably detected before transmission finishes?
  </p>

  <button class="btn-secondary" onclick="toggleSolution('ch5-prob2-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch5-prob2-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Compute transmission delay for minimum frame size (512 bits at 10 Mbps):
      <div class="math-display">
        d_{\text{trans}} = \frac{L}{R} = \frac{512\text{ bits}}{10 \times 10^6\text{ bps}} = 51.2\ \mu\text{s}
      </div>
    </div>
    <div class="calc-step">Step 2: Apply the fundamental CSMA/CD condition:
      <br>&emsp;To guarantee that a sender detects any collision before finishing its transmission, the transmission delay must be greater than or equal to the <strong>Round-Trip Time (2 &times; d_prop)</strong>:
      <div class="math-display">
        d_{\text{trans}} \ge 2 \times d_{\text{prop}} = 2 \times \left( \frac{d_{\text{max}}}{s} \right)
      </div>
      <div class="math-display">
        d_{\text{max}} \le \frac{d_{\text{trans}} \times s}{2} = \frac{51.2 \times 10^{-6}\text{ s} \times 2 \times 10^8\text{ m/s}}{2} = 5,120\text{ meters} \approx \mathbf{5.12\text{ km}}
      </div>
    </div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
      Final Answer: The maximum theoretical distance is <strong>5,120 meters (~5.12 km)</strong>. (In practical standard 10BASE5, repeater delays reduce this to 2,500 meters).
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "Why must CSMA/CD Ethernet enforce a minimum frame size (e.g. 64 bytes)?",
                    "opts": [
                        "To prevent routers from running out of RAM",
                        "To ensure the transmission duration is long enough for the sender to hear a returning collision across maximum cable round-trip propagation distance",
                        "Because 64 is a power of 2",
                        "To ensure encryption keys fit in the header"
                    ],
                    "ans": 1,
                    "exp": "If a frame were too short, the sender would finish transmitting and conclude success before the colliding wave arrived back from the far end of the cable (§5.3.2)."
                }
            ]
        }
    ]
}
