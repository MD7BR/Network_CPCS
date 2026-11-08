"""Chapter 6 Data: Wireless and Mobile Networks (Kurose & Ross 6th Ed.)
Comprehensive, textbook-grade expansion covering all subsections, inline SVGs, 
worked problems, and interactive simulators.
"""

CH6_DATA = {
    "id": "ch6",
    "num": 6,
    "title": "Wireless and Mobile Networks",
    "subtitle": "CDMA, 802.11 WiFi (CSMA/CA, RTS/CTS, 4-Address Frame), Cellular 4G LTE, Mobile IP & TCP Over Wireless",
    "layer": "Wireless & Mobile",
    "color": "#06b6d4",
    "objectives": [
        "Classify wireless networks across the 2x2 taxonomy (single-hop vs multi-hop, infrastructure vs ad hoc)",
        "Analyze wireless link impairments: path loss, interference, multipath fading, SNR vs BER trade-offs, and the Hidden Terminal Problem",
        "Perform CDMA chip sequence encoding, vector superposition, and inner dot-product orthogonal decoding with worked calculations",
        "Trace IEEE 802.11 CSMA/CA protocol timing: DIFS, SIFS, random backoff countdown, RTS/CTS reservation, and NAV virtual carrier sensing",
        "Dissect the bit-accurate 802.11 frame format and explain the exact roles and forwarding semantics of Address 1, 2, 3, and 4",
        "Deconstruct 4G LTE cellular architecture: eNodeB, Mobility Management Entity (MME), Serving Gateway (S-GW), and Packet Gateway (P-GW)",
        "Contrast Mobile IP Indirect Routing (Triangle Routing) with Direct Routing, tracing foreign agents, home agents, and Care-of-Addresses (COA)",
        "Trace GSM call setup through HLR, VLR, and MSRN, and explain anchor-MSC handovers",
        "Diagnose why standard TCP congestion control fails over wireless links and evaluate link-layer ARQ, Snoop TCP, and Split-Connection TCP"
    ],
    "sections": [
        {
            "id": "ch6-1",
            "num": "6.1",
            "title": "Introduction to Wireless and Mobile Networks",
            "subtitle": "Network taxonomy, base stations, and infrastructure vs ad hoc modes",
            "content": r"""
<p>Wireless and mobile networks have revolutionized computer networking by untethering hosts from physical wires and allowing continuous communication while in motion. When analyzing these networks, Kurose & Ross establish an essential conceptual distinction between two independent dimensions:</p>
<ol>
  <li><strong>Wireless Communication:</strong> Transmission of data across the electromagnetic spectrum (radio waves, microwaves, or infrared) rather than physical copper or optical cables. A stationary desktop computer connected via WiFi is a <em>wireless, but non-mobile</em> host.</li>
  <li><strong>Mobility:</strong> The ability of an end system to change its physical point of attachment to the network infrastructure while maintaining active ongoing network-layer and transport-layer connections. A user moving between cellular towers during a VoIP call is a <em>mobile wireless</em> host.</li>
</ol>

<h3>6.1.1 Elements of a Wireless Network</h3>
<p>A wireless network consists of four fundamental architectural components:</p>
<ul>
  <li><strong>Wireless Hosts:</strong> End systems that execute user applications (smartphones, laptops, tablets, wearable health monitors, connected automobiles, and IoT sensors). A host may be stationary or mobile.</li>
  <li><strong>Wireless Communication Links:</strong> Connect hosts to base stations or to other wireless hosts. Different link technologies span vastly different transmission rates and physical distances (from centimeters in NFC/Bluetooth to tens of kilometers in 4G LTE and satellite links).</li>
  <li><strong>Base Station:</strong> A key piece of infrastructure responsible for relaying data between wireless hosts and the wired core network. In IEEE 802.11 wireless LANs, the base station is called an <strong>Access Point (AP)</strong>. In cellular telephony, it is called a <strong>Base Transceiver Station (BTS)</strong> in 2G/3G or an <strong>eNodeB</strong> in 4G LTE.</li>
  <li><strong>Network Infrastructure:</strong> The larger interconnected wired network (routers, switches, DNS/DHCP servers, and internet gateways) that lies behind the base stations, providing access to external servers and services.</li>
</ul>

<!-- INLINE SVG: Figure 6.1 Wireless Network Architecture -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 280" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <defs>
        <linearGradient id="g-wl-host" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8"/>
          <stop offset="100%" stop-color="#0284c7"/>
        </linearGradient>
        <linearGradient id="g-wl-bs" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#34d399"/>
          <stop offset="100%" stop-color="#059669"/>
        </linearGradient>
        <linearGradient id="g-wl-wire" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#94a3b8"/>
          <stop offset="100%" stop-color="#475569"/>
        </linearGradient>
      </defs>

      <!-- Shaded Wireless Coverage Cell -->
      <circle cx="240" cy="140" r="115" fill="#0284c7" fill-opacity="0.08" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6 4"/>
      <text x="240" y="42" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">Wireless Cell Coverage Area</text>

      <!-- Wireless Hosts -->
      <!-- Host 1: Laptop -->
      <rect x="70" y="80" width="70" height="44" rx="6" fill="url(#g-wl-host)"/>
      <text x="105" y="102" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">💻 Laptop</text>
      <text x="105" y="116" font-size="8" fill="#e0f2fe" text-anchor="middle">Mobile Host</text>

      <!-- Host 2: Smartphone -->
      <rect x="85" y="160" width="60" height="42" rx="6" fill="url(#g-wl-host)"/>
      <text x="115" y="181" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">📱 Phone</text>
      <text x="115" y="194" font-size="8" fill="#e0f2fe" text-anchor="middle">Mobile Host</text>

      <!-- Wireless Radio Wave Arcs -->
      <path d="M 150 100 Q 185 115 220 135" stroke="#38bdf8" stroke-width="2.5" fill="none" stroke-dasharray="4 3"/>
      <path d="M 155 175 Q 185 160 220 145" stroke="#38bdf8" stroke-width="2.5" fill="none" stroke-dasharray="4 3"/>
      <text x="175" y="120" font-size="9" fill="#0284c7" font-weight="600">RF Links</text>

      <!-- Base Station (AP / Tower) -->
      <circle cx="240" cy="140" r="26" fill="url(#g-wl-bs)"/>
      <text x="240" y="137" font-size="16" fill="#fff" text-anchor="middle">📡</text>
      <text x="240" y="156" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">Base Stn</text>
      <text x="240" y="180" font-size="9" font-weight="700" fill="#059669" text-anchor="middle">Access Point / eNodeB</text>

      <!-- High-Speed Wired Link to Core Router -->
      <line x1="266" y1="140" x2="420" y2="140" stroke="#475569" stroke-width="5"/>
      <text x="345" y="132" font-size="9" font-weight="700" fill="#475569" text-anchor="middle">Gigabit Wired Link</text>

      <!-- Edge Router -->
      <circle cx="445" cy="140" r="24" fill="url(#g-wl-wire)"/>
      <text x="445" y="144" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Router</text>
      <text x="445" y="178" font-size="9" font-weight="600" fill="#475569" text-anchor="middle">Edge Router</text>

      <!-- Wired Core Mesh / Internet -->
      <line x1="469" y1="140" x2="570" y2="140" stroke="#64748b" stroke-width="4"/>
      <rect x="570" y="90" width="220" height="100" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
      <text x="680" y="118" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">Wired Infrastructure & Internet</text>
      <text x="680" y="138" font-size="9" fill="#64748b" text-anchor="middle">&bull; DNS & DHCP Servers</text>
      <text x="680" y="153" font-size="9" fill="#64748b" text-anchor="middle">&bull; Home Agents / Packet Gateways</text>
      <text x="680" y="168" font-size="9" fill="#64748b" text-anchor="middle">&bull; Global Content Servers</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.1 — Core Elements of a Wireless Network: Mobile Hosts, Wireless Radio Links, Base Station, and Wired Network Infrastructure (§6.1.1).</div>
</div>

<h3>6.1.2 The 2x2 Taxonomy of Wireless Networks</h3>
<p>Kurose & Ross classify all wireless networks along two distinct orthogonal criteria: <strong>single-hop vs multi-hop</strong> communication, and whether a fixed <strong>infrastructure</strong> coordinates access:</p>

<table class="data-table" style="margin:1rem 0;">
  <thead>
    <tr>
      <th>Architecture</th>
      <th>Single-Hop Communication</th>
      <th>Multi-Hop Communication</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:700; color:var(--primary);">Infrastructure-Based</td>
      <td>
        <strong>Classic Cellular & Enterprise WiFi:</strong> Host connects to a base station (AP or cell tower) via a single wireless hop. The base station connects to the wired backbone.
        <br><em>Examples:</em> 802.11b/g/n/ac WiFi, 4G LTE, 5G NR.
      </td>
      <td>
        <strong>Wireless Mesh Networks:</strong> Base stations (mesh routers) relay packets over multiple wireless hops to reach a designated gateway connected to the wired Internet.
        <br><em>Examples:</em> Municipal campus mesh WiFi, Smart Grid utility networks.
      </td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--accent-text);">Infrastructure-Less (Ad Hoc)</td>
      <td>
        <strong>Direct Host-to-Host Links:</strong> No base station coordinates transmission. Nodes communicate directly over a single wireless hop.
        <br><em>Examples:</em> Bluetooth piconets, 802.11 WiFi Direct, Apple AirDrop.
      </td>
      <td>
        <strong>MANETs & VANETs:</strong> Mobile nodes relay packets for each other across arbitrary multi-hop paths with no pre-existing infrastructure.
        <br><em>Examples:</em> Mobile Ad Hoc Networks (MANETs), Vehicular Networks (VANETs), military battlefield deployments.
      </td>
    </tr>
  </tbody>
</table>

<div class="callout callout-def">
  <div class="callout-header">📘 Definition: Handoff / Handover</div>
  A <strong>handoff</strong> (or <strong>handover</strong>) occurs when a mobile host transitions its physical wireless association from one base station to another as it travels through space, ideally without dropping active TCP connections or interrupting user sessions.
</div>
""",
            "quiz": [
                {
                    "q": "Which quadrant of the wireless taxonomy does a Bluetooth connection between a smartphone and wireless earbuds belong to?",
                    "opts": [
                        "Single-hop, infrastructure-based",
                        "Single-hop, infrastructure-less (ad hoc)",
                        "Multi-hop, infrastructure-based",
                        "Multi-hop, infrastructure-less"
                    ],
                    "ans": 1,
                    "exp": "Bluetooth connects two devices directly without a coordinating base station over a single radio hop, making it single-hop, infrastructure-less (§6.1.2)."
                },
                {
                    "q": "What is the primary difference between a wireless network and a mobile network in Kurose & Ross's classification?",
                    "opts": [
                        "Wireless implies optical communication, while mobile implies copper wire",
                        "Wireless refers to the physical transmission medium (RF waves), while mobility refers to the ability of a host to change its point of attachment while maintaining active connections",
                        "Wireless networks cannot run TCP, whereas mobile networks can",
                        "Mobile networks require satellites, while wireless networks do not"
                    ],
                    "ans": 1,
                    "exp": "A stationary desktop with a WiFi card is wireless but not mobile. Mobility is the orthogonal property of changing network points of attachment in motion (§6.1)."
                }
            ]
        },
        {
            "id": "ch6-2",
            "num": "6.2",
            "title": "Wireless Links and Network Characteristics",
            "subtitle": "Path loss, multipath, SNR/BER, Hidden Terminal, and CDMA",
            "content": r"""
<p>Wireless communication differs fundamentally from wired channels. In twisted-pair copper and optical fiber, the transmitted electromagnetic wave is confined to a physical waveguide with predictable attenuation and minimal external interference. In wireless links, the broadcast medium is open space, introducing significant transmission impairments.</p>

<h3>6.2.1 Physical Link Impairments</h3>
<ul>
  <li><strong>Decreasing Signal Strength (Path Loss):</strong> As electromagnetic radiation propagates away from the transmitter, its power density attenuates with distance. In free space, signal power decreases with the square of distance (<span class="math-inline">1/d<sup>2</sup></span>); in terrestrial environments with obstacles, it attenuates much faster (proportional to <span class="math-inline">1/d<sup>3</sup></span> or <span class="math-inline">1/d<sup>4</sup></span>).</li>
  <li><strong>Interference from Other Sources:</strong> Wireless frequency bands (especially the unlicensed 2.4 GHz Industrial, Scientific, and Medical band) are shared by WiFi networks, Bluetooth devices, cordless telephones, baby monitors, and microwave ovens. Signals transmitted on overlapping frequencies disrupt one another.</li>
  <li><strong>Multipath Propagation:</strong> Radio waves bounce off the ground, buildings, vehicles, and indoor walls. Reflected waves travel slightly different path lengths and arrive at the receiving antenna at slightly different times, causing constructive or destructive interference (known as <strong>multipath fading</strong>).</li>
</ul>

<h3>6.2.2 Signal-to-Noise Ratio (SNR) and Bit Error Rate (BER)</h3>
<p>The quality of a wireless link is characterized by the <strong>Signal-to-Noise Ratio (SNR)</strong>, which measures the ratio of the received signal power to background electromagnetic noise power, typically expressed in decibels (dB):</p>
<div class="math-display">
  \text{SNR (dB)} = 10 \log_{10} \left( \frac{\text{Signal Power}}{\text{Noise Power}} \right)
</div>

<div class="callout callout-formula">
  <div class="callout-header">🧮 The Fundamental SNR vs. BER vs. Bitrate Tradeoff</div>
  Wireless physical layers must dynamically balance three interdependent quantities:
  <ol>
    <li><strong>Higher SNR yields lower Bit Error Rate (BER):</strong> For a given physical modulation scheme, increasing transmission power (raising SNR) makes signal points easier for the receiver to distinguish from background noise, reducing bit errors.</li>
    <li><strong>Higher transmission bitrates require higher SNR:</strong> To send more bits per symbol, transmitters use denser constellation modulation schemes (e.g., 64-QAM delivers 6 bits/symbol, 16-QAM delivers 4 bits/symbol, BPSK delivers only 1 bit/symbol). However, denser constellations place points closer together, requiring a dramatically higher SNR to avoid errors!</li>
    <li><strong>Dynamic Rate Adaptation:</strong> Modern wireless adapters (802.11 and cellular) continuously monitor the link's SNR. If a mobile user walks away from the AP (SNR drops), the adapter shifts down from 64-QAM to 16-QAM or BPSK to maintain an acceptable BER at the expense of lower throughput.</li>
  </ol>
</div>

<!-- INLINE SVG: Figure 6.2 Hidden Terminal Problem -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 250" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Node A Coverage Circle -->
      <circle cx="160" cy="130" r="130" fill="#3b82f6" fill-opacity="0.08" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4 4"/>
      <!-- Node B Coverage Circle -->
      <circle cx="680" cy="130" r="130" fill="#ef4444" fill-opacity="0.08" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 4"/>

      <!-- Mountain / Wall Obstacle -->
      <polygon points="380,210 420,50 460,210" fill="#94a3b8" stroke="#64748b" stroke-width="2"/>
      <text x="420" y="145" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">OBSTACLE</text>
      <text x="420" y="160" font-size="9" fill="#f1f5f9" text-anchor="middle">(Blocks RF)</text>

      <!-- Terminal A -->
      <rect x="120" y="110" width="80" height="40" rx="6" fill="#3b82f6"/>
      <text x="160" y="132" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Station A</text>
      <text x="160" y="144" font-size="8" fill="#dbeafe" text-anchor="middle">Transmitting</text>

      <!-- Base Station (AP) in Middle -->
      <circle cx="420" cy="215" r="24" fill="#10b981"/>
      <text x="420" y="212" font-size="14" fill="#fff" text-anchor="middle">📡</text>
      <text x="420" y="228" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">AP</text>
      <text x="420" y="246" font-size="9" font-weight="700" fill="#047857" text-anchor="middle">Access Point</text>

      <!-- Terminal B -->
      <rect x="640" y="110" width="80" height="40" rx="6" fill="#ef4444"/>
      <text x="680" y="132" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Station B</text>
      <text x="680" y="144" font-size="8" fill="#fee2e2" text-anchor="middle">Transmitting</text>

      <!-- Transmission arrows to AP -->
      <path d="M 190 145 Q 300 200 395 215" stroke="#3b82f6" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
      <path d="M 650 145 Q 540 200 445 215" stroke="#ef4444" stroke-width="3" fill="none" marker-end="url(#arrow)"/>

      <!-- Collision Explosion at AP -->
      <circle cx="420" cy="205" r="16" fill="#f59e0b" fill-opacity="0.8"/>
      <text x="420" y="209" font-size="9" font-weight="800" fill="#78350f" text-anchor="middle">💥 COLLISION!</text>

      <!-- Notice Labels -->
      <text x="160" y="75" font-size="10" font-weight="700" fill="#1e40af" text-anchor="middle">A cannot hear B</text>
      <text x="680" y="75" font-size="10" font-weight="700" fill="#b91c1c" text-anchor="middle">B cannot hear A</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.2 — The Hidden Terminal Problem: Station A and Station B cannot sense each other due to the physical obstacle, causing concurrent transmissions to collide destructively at the Access Point (§6.2).</div>
</div>

<h3>6.2.3 The Hidden Terminal Problem and Fading</h3>
<p>In wired Ethernet, Carrier Sense Multiple Access with Collision Detection (CSMA/CD) works because every node can hear every other node on the shared copper wire. In wireless networks, this assumption completely breaks down due to two phenomena:</p>
<ol>
  <li><strong>The Hidden Terminal Problem:</strong> Station A transmits to the base station. Station B also wishes to transmit to the base station. Because of physical distance or an obstacle (e.g., a mountain or concrete wall), A and B cannot hear each other's radio signals. Station B senses the channel, perceives it as completely idle, and begins transmitting. Both transmissions arrive simultaneously at the base station, resulting in a destructive collision! Here, Station A is <em>hidden</em> from Station B, and vice-versa.</li>
  <li><strong>Fading / Signal Attenuation:</strong> Even without physical obstacles, signal power drops off rapidly. Station A's signal strength may have dissipated below the carrier-sensing threshold of Station B, yet both signals remain strong enough at the intermediate base station to garble each other.</li>
</ol>

<h3>6.2.4 Code Division Multiple Access (CDMA)</h3>
<p>CDMA is a channel partitioning multiple access protocol widely deployed in 3G cellular systems and military communications. In CDMA, all users transmit <strong>simultaneously over the exact same frequency band</strong>, yet receivers can cleanly separate individual user transmissions without interference through the power of <strong>orthogonal codes</strong>.</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Mathematical Mechanics of CDMA (§6.2.4)</div>
  <p>Let each user <span class="math-inline">m</span> be assigned a unique <span class="math-inline">M</span>-bit <strong>chip sequence</strong> (code vector) <span class="math-inline">\mathbf{c}_m = (c_m^1, c_m^2, \dots, c_m^M)</span>, where each chip is normalized to values <span class="math-inline">\pm 1</span>.</p>
  <p>The code vectors assigned to different users are strictly <strong>orthogonal</strong>:</p>
  <div class="math-display">
    \frac{1}{M} (\mathbf{c}_i \cdot \mathbf{c}_j) = \frac{1}{M} \sum_{k=1}^M c_i^k \cdot c_j^k = 
    \begin{cases} 
      1 & \text{if } i = j \\ 
      0 & \text{if } i \ne j 
    \end{cases}
  </div>
  <ul>
    <li>To transmit a data bit <span class="math-inline">d_i = +1</span> (binary 1), user <span class="math-inline">i</span> sends its assigned chip vector: <span class="math-inline">+1 \times \mathbf{c}_i</span>.</li>
    <li>To transmit a data bit <span class="math-inline">d_i = -1</span> (binary 0), user <span class="math-inline">i</span> sends the inverted chip vector: <span class="math-inline">-1 \times \mathbf{c}_i</span>.</li>
    <li>If user <span class="math-inline">i</span> is silent, it sends vector <span class="math-inline">(0, 0, \dots, 0)</span>.</li>
  </ul>
  <p><strong>Channel Superposition:</strong> All transmitted signals superimpose linearly over the shared radio medium. The aggregate received signal vector <span class="math-inline">\mathbf{S}</span> is:</p>
  <div class="math-display">
    \mathbf{S} = \sum_{m} d_m \mathbf{c}_m
  </div>
  <p><strong>Decoding at the Receiver:</strong> To extract the original data bit sent by user <span class="math-inline">i</span>, the receiver computes the normalized inner dot product between the received composite signal <span class="math-inline">\mathbf{S}</span> and user <span class="math-inline">i</span>'s known chip code <span class="math-inline">\mathbf{c}_i</span>:</p>
  <div class="math-display">
    \text{Decoded } d_i = \frac{1}{M} (\mathbf{S} \cdot \mathbf{c}_i) = \frac{1}{M} \left( \sum_m d_m \mathbf{c}_m \cdot \mathbf{c}_i \right) = d_i \left( \frac{\mathbf{c}_i \cdot \mathbf{c}_i}{M} \right) + \sum_{m \ne i} d_m \left( \frac{\mathbf{c}_m \cdot \mathbf{c}_i}{M} \right) = d_i \cdot 1 + 0 = d_i
  </div>
  <p>Because all other users' chip codes are orthogonal to <span class="math-inline">\mathbf{c}_i</span>, their dot products collapse to zero, completely filtering out their interference!</p>
</div>

<!-- EMBEDDED INTERACTIVE: CDMA ENCODER / DECODER -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">📡 Live CDMA Chip Superposition & Decoding Calculator</div>
    <span class="interactive-badge">Orthogonal Matrix Tool</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:1rem;">
    Choose the data bits for User A and User B. The tool computes the composite signal vector S and executes the inner dot product to decode User A's data bit:
  </p>
  <div class="calc-grid">
    <div class="calc-field">
      <label class="calc-label">User A Data Bit (d<sub>A</sub>)</label>
      <select id="sec6-bit-a" class="calc-input" onchange="calcSec6CDMA()">
        <option value="1" selected>Bit 1 (+1)</option>
        <option value="-1">Bit 0 (&minus;1)</option>
        <option value="0">Silent (0)</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">User B Data Bit (d<sub>B</sub>)</label>
      <select id="sec6-bit-b" class="calc-input" onchange="calcSec6CDMA()">
        <option value="-1" selected>Bit 0 (&minus;1)</option>
        <option value="1">Bit 1 (+1)</option>
        <option value="0">Silent (0)</option>
      </select>
    </div>
  </div>
  <div id="sec6-cdma-result" class="calc-result-box" style="margin-top:1rem;">
    <!-- Computed dynamically by calcSec6CDMA() -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "Why can two wireless stations transmit simultaneously to the same base station on the exact same frequency in CDMA without corrupting each other?",
                    "opts": [
                        "Because they use different TCP port numbers",
                        "Because their assigned chip sequences are mutually orthogonal, allowing the receiver's inner product to eliminate interfering signals to zero",
                        "Because base stations use directional parabolic lasers",
                        "Because one station always transmits at 5 GHz while the other transmits at 2.4 GHz"
                    ],
                    "ans": 1,
                    "exp": "CDMA exploits the linear algebra property of orthogonality: (1/M)(C_i * C_j) = 0 for all i != j, cleanly isolating the desired signal (§6.2.4)."
                },
                {
                    "q": "What happens when a wireless mobile station moves farther away from its Access Point, causing the received SNR to drop significantly?",
                    "opts": [
                        "The adapter automatically switches to a denser modulation scheme (e.g. 256-QAM)",
                        "The adapter adapts by shifting to a lower modulation order (e.g. BPSK) to maintain an acceptable BER at the cost of lower bitrate",
                        "The Access Point converts the link from wireless to wired Ethernet",
                        "The router drops all TCP packets permanently"
                    ],
                    "ans": 1,
                    "exp": "Dynamic rate adaptation monitors SNR; when SNR falls, the physical layer steps down to more robust, lower-order modulation schemes with fewer bits per symbol to keep BER low (§6.2.2)."
                }
            ]
        },
        {
            "id": "ch6-3",
            "num": "6.3",
            "title": "WiFi: 802.11 Wireless LANs",
            "subtitle": "Architecture, CSMA/CA MAC, DIFS/SIFS, RTS/CTS, and the 4-Address 802.11 Frame",
            "content": r"""
<p>The IEEE 802.11 standard family (marketed as <strong>WiFi</strong>) represents the dominant wireless local area network technology worldwide. Understanding 802.11 requires examining its architecture, its specialized multiple access control protocol, and its unique link-layer frame format.</p>

<h3>6.3.1 The 802.11 Architecture: BSS, AP, and Channels</h3>
<p>The fundamental building block of an 802.11 network is the <strong>Basic Service Set (BSS)</strong>:</p>
<ul>
  <li>A BSS contains one or more wireless stations (hosts) and a coordinating central base station known as the <strong>Access Point (AP)</strong>.</li>
  <li>Each AP is assigned a human-readable <strong>Service Set Identifier (SSID)</strong> (e.g., <code>"KAU-Campus-WiFi"</code>) and a 48-bit MAC address for its wireless interface.</li>
  <li>Multiple BSSs are interconnected via a wired Ethernet <strong>Distribution System (DS)</strong> to form an Extended Service Set (ESS).</li>
</ul>

<h4>Frequency Channels and Non-Overlapping Bands</h4>
<p>In 802.11b/g/n, the 2.4 GHz radio spectrum (2.400–2.4835 GHz) is divided into 11 distinct channels in North America (13 in Europe). Each channel is 22 MHz wide, but adjacent channel center frequencies are separated by only 5 MHz! As a consequence, channels overlap heavily.</p>
<div class="callout callout-insight">
  <div class="callout-header">💡 The Non-Overlapping Channels: 1, 6, and 11</div>
  To deploy multiple adjacent APs in an enterprise building without mutual interference, network engineers must configure them to use the <strong>only three mutually non-overlapping channels: Channel 1, Channel 6, and Channel 11</strong>!
</div>

<h4>Association: Passive vs. Active Scanning</h4>
<p>Before a wireless host can transmit data frames through an AP, it must establish an <strong>association</strong>. Hosts discover APs through two standardized methods:</p>
<ol>
  <li><strong>Passive Scanning:</strong> Each AP periodically broadcasts <strong>Beacon Frames</strong> (typically every 100 ms) containing its SSID, supported rates, and MAC address. The mobile host scans all channels listening for beacons, selects an AP, and sends an Association Request frame. The AP replies with an Association Response.</li>
  <li><strong>Active Scanning:</strong> The mobile host broadcasts a <strong>Probe Request</strong> frame on a channel. All APs within range respond with a <strong>Probe Response</strong> frame. The host then exchanges Association Request and Response frames with its chosen AP.</li>
</ol>

<h3>6.3.2 The 802.11 CSMA/CA MAC Protocol</h3>
<p>Why doesn't 802.11 use Ethernet's CSMA/CD (Collision Detection)?</p>
<ol>
  <li><strong>Hardware Infeasibility:</strong> A wireless station's transmitted signal power is thousands of times stronger than any incoming received signal. The adapter's own transmission would completely saturate its receiver hardware, making it impossible to detect weak colliding signals during transmission.</li>
  <li><strong>Hidden Terminals & Fading:</strong> Even if a station could detect collisions at its own antenna, collisions occur at the <em>receiver's</em> antenna (the AP), where hidden terminals cannot be detected by the sender!</li>
</ol>

<p>Therefore, 802.11 uses <strong>CSMA with Collision Avoidance (CSMA/CA)</strong>:</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Step-by-Step CSMA/CA Protocol Execution (§6.3.2)</div>
  <ol>
    <li><strong>Carrier Sensing:</strong> The transmitting station senses the channel.
      <br>&bull; If the channel is sensed idle for a continuous duration of <strong>DIFS (Distributed Inter-Frame Space)</strong>, the station transmits its entire frame.
    </li>
    <li><strong>Random Backoff:</strong> If the channel is sensed busy, the station defers transmission and chooses a random backoff counter uniformly distributed in <span class="math-inline">[0, CW]</span>, where <span class="math-inline">CW</span> is the Contention Window.
      <br>&bull; The station counts down the timer <em>only while the channel is sensed idle</em>.
      <br>&bull; If another transmission is sensed, the counter is frozen!
      <br>&bull; Counting down resumes only after the channel has been idle again for a full DIFS.
    </li>
    <li><strong>Transmission:</strong> When the backoff counter counts down to zero, the station transmits the entire frame immediately.</li>
    <li><strong>Explicit Link-Layer ACK:</strong> The destination station receives the frame, verifies the CRC checksum, waits for a short period called <strong>SIFS (Short Inter-Frame Space)</strong>, and transmits an <strong>ACK frame</strong> back to the sender.</li>
    <li><strong>Binary Exponential Backoff on Loss:</strong> If the sender does not receive the ACK frame within a timeout interval, it assumes a collision occurred, doubles the contention window <span class="math-inline">CW</span> (from 31 to 63, 127, up to 1023), selects a new random backoff value, and repeats the process.</li>
  </ol>
</div>

<div class="callout callout-insight">
  <div class="callout-header">💡 Why SIFS is Strictly Shorter Than DIFS (\text{SIFS} &lt; \text{DIFS})</div>
  Notice that <span class="math-inline">\text{SIFS} &lt; \text{DIFS}</span>. Because the receiver only waits SIFS before transmitting an ACK, whereas any other station waiting to transmit a new data frame must wait a full DIFS, the <strong>ACK frame is guaranteed priority access to the channel</strong> without being interrupted by other stations!
</div>

<!-- INLINE SVG: Figure 6.3 CSMA/CA Timing with DIFS/SIFS/RTS/CTS -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 280" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Sender Timeline -->
      <line x1="50" y1="60" x2="800" y2="60" stroke="#94a3b8" stroke-width="2"/>
      <text x="45" y="45" font-size="11" font-weight="700" fill="#3b82f6">Transmitter</text>

      <!-- DIFS block -->
      <rect x="70" y="45" width="45" height="30" fill="#f59e0b" rx="4"/>
      <text x="92" y="64" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">DIFS</text>

      <!-- RTS frame -->
      <rect x="125" y="45" width="55" height="30" fill="#3b82f6" rx="4"/>
      <text x="152" y="64" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">RTS</text>

      <!-- DATA frame -->
      <rect x="305" y="45" width="240" height="30" fill="#10b981" rx="4"/>
      <text x="425" y="64" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">DATA FRAME PAYLOAD</text>

      <!-- Receiver Timeline -->
      <line x1="50" y1="150" x2="800" y2="150" stroke="#94a3b8" stroke-width="2"/>
      <text x="45" y="135" font-size="11" font-weight="700" fill="#10b981">Receiver (AP)</text>

      <!-- SIFS 1 -->
      <rect x="190" y="135" width="25" height="30" fill="#8b5cf6" rx="4"/>
      <text x="202" y="154" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">SIFS</text>

      <!-- CTS frame -->
      <rect x="225" y="135" width="55" height="30" fill="#6366f1" rx="4"/>
      <text x="252" y="154" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">CTS</text>

      <!-- SIFS 2 -->
      <rect x="555" y="135" width="25" height="30" fill="#8b5cf6" rx="4"/>
      <text x="567" y="154" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">SIFS</text>

      <!-- ACK frame -->
      <rect x="590" y="135" width="60" height="30" fill="#3b82f6" rx="4"/>
      <text x="620" y="154" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">ACK</text>

      <!-- Other Overhearing Stations (NAV) Timeline -->
      <line x1="50" y1="235" x2="800" y2="235" stroke="#94a3b8" stroke-width="2"/>
      <text x="45" y="215" font-size="11" font-weight="700" fill="#ef4444">Other Stations</text>

      <!-- NAV Bar -->
      <rect x="180" y="220" width="470" height="28" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5" rx="4"/>
      <text x="415" y="238" font-size="10" font-weight="700" fill="#b91c1c" text-anchor="middle">NAV (Network Allocation Vector) — Defer Transmission</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.3 — IEEE 802.11 CSMA/CA Timeline with RTS/CTS Channel Reservation and NAV Virtual Carrier Sensing (§6.3.2).</div>
</div>

<h3>6.3.3 RTS/CTS Virtual Channel Reservation</h3>
<p>To eliminate collisions caused by hidden terminals and reduce the cost of colliding large data frames, 802.11 includes the <strong>Request-to-Send (RTS)</strong> and <strong>Clear-to-Send (CTS)</strong> reservation exchange:</p>
<ol>
  <li><strong>RTS Transmission:</strong> Before sending a large data frame, the sender transmits a tiny 20-byte <strong>RTS frame</strong>. The RTS header contains a <code>Duration</code> field specifying the exact microsecond time required to transmit the pending DATA frame, CTS frame, and ACK frame.</li>
  <li><strong>CTS Broadcast:</strong> The AP receives the RTS and broadcasts a 14-byte <strong>CTS frame</strong>. The CTS repeats the remaining duration value.</li>
  <li><strong>Setting the NAV:</strong> Every station that overhears either the RTS or the CTS updates its internal timer called the <strong>Network Allocation Vector (NAV)</strong>. While NAV &gt; 0, the station is prohibited from transmitting, even if its physical carrier sense perceives the radio channel as idle! This is called <strong>Virtual Carrier Sensing</strong>.</li>
</ol>

<h3>6.3.4 The IEEE 802.11 Frame: Deconstructing the 4 Addresses</h3>
<p>Unlike Ethernet frames (which contain only 2 MAC addresses: Source and Destination), an 802.11 frame contains <strong>four 48-bit MAC address fields</strong>:</p>

<!-- INLINE SVG: Figure 6.4 802.11 Frame Format -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 180" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Row of Frame Fields -->
      <!-- Frame Control (2B) -->
      <rect x="20" y="50" width="75" height="55" fill="#f8fafc" stroke="#475569" stroke-width="1.5" rx="4"/>
      <text x="57" y="75" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">Frame Ctrl</text>
      <text x="57" y="93" font-size="9" fill="#64748b" text-anchor="middle">2 Bytes</text>

      <!-- Duration (2B) -->
      <rect x="95" y="50" width="70" height="55" fill="#f8fafc" stroke="#475569" stroke-width="1.5" rx="4"/>
      <text x="130" y="75" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">Duration</text>
      <text x="130" y="93" font-size="9" fill="#64748b" text-anchor="middle">2 Bytes</text>

      <!-- Address 1 (6B) -->
      <rect x="165" y="50" width="105" height="55" fill="#eff6ff" stroke="#3b82f6" stroke-width="2" rx="4"/>
      <text x="217" y="73" font-size="11" font-weight="800" fill="#1d4ed8" text-anchor="middle">Address 1</text>
      <text x="217" y="92" font-size="8" fill="#2563eb" text-anchor="middle">Receiver MAC (BSS)</text>

      <!-- Address 2 (6B) -->
      <rect x="270" y="50" width="105" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="4"/>
      <text x="322" y="73" font-size="11" font-weight="800" fill="#047857" text-anchor="middle">Address 2</text>
      <text x="322" y="92" font-size="8" fill="#059669" text-anchor="middle">Transmitter MAC</text>

      <!-- Address 3 (6B) -->
      <rect x="375" y="50" width="105" height="55" fill="#fdf4ff" stroke="#c084fc" stroke-width="2" rx="4"/>
      <text x="427" y="73" font-size="11" font-weight="800" fill="#7e22ce" text-anchor="middle">Address 3</text>
      <text x="427" y="92" font-size="8" fill="#9333ea" text-anchor="middle">Router Interface MAC</text>

      <!-- Seq Control (2B) -->
      <rect x="480" y="50" width="70" height="55" fill="#f8fafc" stroke="#475569" stroke-width="1.5" rx="4"/>
      <text x="515" y="75" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">Seq Ctrl</text>
      <text x="515" y="93" font-size="9" fill="#64748b" text-anchor="middle">2 Bytes</text>

      <!-- Address 4 (6B) -->
      <rect x="550" y="50" width="95" height="55" fill="#fff7ed" stroke="#f97316" stroke-width="1.5" rx="4"/>
      <text x="597" y="75" font-size="10" font-weight="700" fill="#c2410c" text-anchor="middle">Address 4</text>
      <text x="597" y="93" font-size="8" fill="#ea580c" text-anchor="middle">Ad-Hoc Bridge</text>

      <!-- Payload (0-2312B) -->
      <rect x="645" y="50" width="115" height="55" fill="#f1f5f9" stroke="#334155" stroke-width="1.5" rx="4"/>
      <text x="702" y="73" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">Data Payload</text>
      <text x="702" y="93" font-size="8" fill="#475569" text-anchor="middle">IP Datagram (&le;2312B)</text>

      <!-- CRC (4B) -->
      <rect x="760" y="50" width="60" height="55" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5" rx="4"/>
      <text x="790" y="75" font-size="10" font-weight="700" fill="#991b1b" text-anchor="middle">CRC</text>
      <text x="790" y="93" font-size="9" fill="#dc2626" text-anchor="middle">4 Bytes</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.4 — Complete IEEE 802.11 Frame Structure Highlighting Address 1, 2, 3, and 4 (§6.3.4).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 The Exact Roles of the 4 MAC Address Fields</div>
  <ul>
    <li><strong>Address 1 (Receiver MAC):</strong> The MAC address of the wireless station that is to receive the wireless frame. For a frame transmitted from a wireless host to the AP, Address 1 is the <strong>AP's wireless MAC address</strong>.</li>
    <li><strong>Address 2 (Transmitter MAC):</strong> The MAC address of the wireless station that transmitted the frame onto the wireless medium (e.g., the <strong>wireless host's MAC address</strong>).</li>
    <li><strong>Address 3 (Router Interface / Subnet Destination MAC):</strong> Crucial bridge between wireless 802.11 and wired 802.3 Ethernet! When the AP receives an 802.11 frame, it converts it into an 802.3 Ethernet frame to forward onto the wired subnet. The AP copies <strong>Address 3 into the Destination MAC field of the Ethernet frame</strong> (typically the default gateway router's MAC address!).</li>
    <li><strong>Address 4:</strong> Used exclusively when APs forward frames to each other in an ad-hoc wireless mesh or wireless distribution bridge network.</li>
  </ul>
</div>

<!-- EMBEDDED INTERACTIVE: CSMA/CA TIMELINE STEPPER -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">⏱️ Interactive CSMA/CA & RTS/CTS Timing Animator</div>
    <span class="interactive-badge">Protocol Timeline</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Step through the 802.11 wireless exchange to inspect how DIFS, SIFS, RTS/CTS, and NAV coordination prevent collisions:
  </p>
  <div class="fig-controls" style="margin-bottom:1rem;">
    <button class="btn-primary" onclick="stepSec6CSMACA()">⏭ Step WiFi Exchange</button>
    <button class="btn-secondary" onclick="resetSec6CSMACA()">🔄 Reset</button>
    <span id="sec6-csma-step" class="fig-step-badge">Ready</span>
  </div>
  <div id="sec6-csma-desc" style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1.25rem;">
    Click "Step WiFi Exchange" to observe the sequence of carrier sensing, backoff, and frame transmissions.
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In an 802.11 frame transmitted from a wireless laptop to an Access Point destined for a web server on the Internet, what is stored in Address 3?",
                    "opts": [
                        "The laptop's own MAC address",
                        "The Access Point's MAC address",
                        "The MAC address of the first-hop router interface on the wired subnet",
                        "The IP address of the destination web server"
                    ],
                    "ans": 2,
                    "exp": "Address 3 stores the MAC address of the default gateway router interface. When the AP converts the 802.11 frame to an 802.3 Ethernet frame, it places Address 3 into the Ethernet frame's Destination MAC field (§6.3.4)."
                },
                {
                    "q": "What is the purpose of the NAV (Network Allocation Vector) in 802.11 CSMA/CA?",
                    "opts": [
                        "It calculates the physical GPS coordinates of the mobile device",
                        "It acts as a timer during which third-party stations must defer transmission based on overheard duration values in RTS/CTS frames (Virtual Carrier Sensing)",
                        "It generates WPA2 encryption keys",
                        "It assigns IP addresses to newly joined hosts"
                    ],
                    "ans": 1,
                    "exp": "The NAV provides virtual carrier sensing: overheard RTS/CTS frames indicate how long the channel will remain reserved, preventing collisions even when physical sensing indicates idle airwaves (§6.3.3)."
                }
            ]
        },
        {
            "id": "ch6-4",
            "num": "6.4",
            "title": "Cellular Internet Access",
            "subtitle": "Cellular architecture, 2G/3G systems, and 4G LTE Evolved Packet Core (EPC)",
            "content": r"""
<p>While WiFi provides high-speed wireless connectivity over tens of meters, cellular networks provide wide-area mobile broadband covering entire nations. Cellular systems partition geographic regions into hexagonal <strong>cells</strong>, each illuminated by a cellular tower base station operating on non-interfering frequency sets.</p>

<h3>6.4.1 Evolution of Cellular Networks: From 1G to 4G LTE</h3>
<ul>
  <li><strong>1G (1980s):</strong> Analog voice communication using Frequency Division Multiple Access (FDMA) (e.g., AMPS). No digital data transmission.</li>
  <li><strong>2G (1990s):</strong> Digital voice using Time Division Multiple Access combined with FDMA (e.g., GSM) and CDMA (IS-95). Digital SMS messaging.</li>
  <li><strong>2.5G & 3G (2000s):</strong> Packet data added alongside legacy circuit-switched voice. GPRS and EDGE introduced the SGSN (Serving GPRS Support Node) and GGSN (Gateway GPRS Support Node). 3G (UMTS/WCDMA) achieved speeds up to a few Mbps.</li>
  <li><strong>4G LTE (Long-Term Evolution, 2010s):</strong> A complete revolutionary paradigm shift: <strong>all circuit-switching was abolished</strong>. 4G LTE is a pure, flat, <strong>all-IP packet-switched network</strong>! Voice calls are carried as VoIP packets (VoLTE).</li>
</ul>

<h3>6.4.2 4G LTE Architecture: Radio Access Network & Evolved Packet Core</h3>
<p>As defined by the 3GPP standards, a 4G LTE network consists of two primary subsystems:</p>

<!-- INLINE SVG: Figure 6.5 4G LTE Architecture -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 260" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- E-UTRAN (Radio Access Network) Box -->
      <rect x="20" y="25" width="220" height="215" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
      <text x="130" y="48" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">E-UTRAN (Radio Access)</text>

      <!-- UE (User Equipment) -->
      <rect x="40" y="90" width="55" height="75" rx="6" fill="#3b82f6"/>
      <text x="67" y="125" font-size="18" fill="#fff" text-anchor="middle">📱</text>
      <text x="67" y="145" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">UE (Phone)</text>

      <!-- eNodeB Base Station -->
      <circle cx="175" cy="127" r="30" fill="#10b981"/>
      <text x="175" y="125" font-size="18" fill="#fff" text-anchor="middle">🗼</text>
      <text x="175" y="145" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">eNodeB</text>

      <!-- Radio link -->
      <line x1="95" y1="127" x2="145" y2="127" stroke="#3b82f6" stroke-width="3" stroke-dasharray="4 3"/>

      <!-- EPC (Evolved Packet Core) Box -->
      <rect x="270" y="25" width="360" height="215" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>
      <text x="450" y="48" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">EPC (Evolved Packet Core — All-IP)</text>

      <!-- MME (Control Plane) -->
      <rect x="290" y="70" width="130" height="48" rx="6" fill="#8b5cf6"/>
      <text x="355" y="94" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">MME</text>
      <text x="355" y="108" font-size="8" fill="#ede9fe" text-anchor="middle">Mobility Mgmt Entity</text>

      <!-- HSS (User Database) -->
      <rect x="460" y="70" width="130" height="48" rx="6" fill="#64748b"/>
      <text x="525" y="94" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">HSS</text>
      <text x="525" y="108" font-size="8" fill="#f1f5f9" text-anchor="middle">Home Subscriber Server</text>

      <!-- S-GW (Data Plane) -->
      <rect x="290" y="145" width="130" height="48" rx="6" fill="#0284c7"/>
      <text x="355" y="169" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Serving GW (S-GW)</text>
      <text x="355" y="183" font-size="8" fill="#e0f2fe" text-anchor="middle">Data Plane Anchor</text>

      <!-- P-GW (Packet Gateway) -->
      <rect x="460" y="145" width="130" height="48" rx="6" fill="#0d9488"/>
      <text x="525" y="169" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Packet GW (P-GW)</text>
      <text x="525" y="183" font-size="8" fill="#ccfbf1" text-anchor="middle">IP Gateway to Internet</text>

      <!-- Lines connecting nodes -->
      <line x1="205" y1="110" x2="290" y2="94" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="3 3"/>
      <text x="247" y="96" font-size="7" fill="#8b5cf6">S1-MME</text>

      <line x1="205" y1="140" x2="290" y2="169" stroke="#0284c7" stroke-width="3"/>
      <text x="247" y="162" font-size="7" fill="#0284c7">S1-U</text>

      <line x1="420" y1="94" x2="460" y2="94" stroke="#8b5cf6" stroke-width="2"/>
      <line x1="420" y1="169" x2="460" y2="169" stroke="#0284c7" stroke-width="3"/>

      <!-- Internet Cloud -->
      <rect x="665" y="90" width="150" height="90" rx="10" fill="#eff6ff" stroke="#93c5fd" stroke-width="2"/>
      <text x="740" y="125" font-size="12" font-weight="800" fill="#1e40af" text-anchor="middle">Public Internet</text>
      <text x="740" y="145" font-size="9" fill="#3b82f6" text-anchor="middle">IP Routing & Web</text>
      <line x1="590" y1="169" x2="665" y2="135" stroke="#0d9488" stroke-width="4"/>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.5 — 4G LTE Evolved Packet System: E-UTRAN (eNodeB) and Evolved Packet Core (MME, HSS, S-GW, P-GW) (§6.4.2).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 Key Components of 4G LTE EPC</div>
  <ul>
    <li><strong>eNodeB:</strong> The LTE base station. Unlike 2G/3G base stations, the eNodeB contains integrated intelligence: it terminates the radio link, executes local packet retransmissions (HARQ), and handles handovers directly with adjacent eNodeBs over the <strong>X2 interface</strong> without routing through central switches.</li>
    <li><strong>MME (Mobility Management Entity):</strong> The primary <strong>Control-Plane</strong> entity. Coordinates device authentication with the HSS, tracks UE location when idle (paging), and establishes bearer tunnels. <em>User payload data never passes through the MME!</em></li>
    <li><strong>HSS (Home Subscriber Server):</strong> Central database holding permanent subscriber subscription records, security keys, and QoS entitlements.</li>
    <li><strong>Serving Gateway (S-GW):</strong> The primary <strong>Data-Plane</strong> entity. Terminates the user IP tunnel from the eNodeB and acts as a local mobility anchor when the phone moves between base stations.</li>
    <li><strong>Packet Data Network Gateway (P-GW):</strong> The interface between the cellular network and the external public Internet. The P-GW assigns public IP addresses to phones, performs NAT, executes firewall packet inspection, and enforces quality of service (QoS) bandwidth limits.</li>
  </ul>
</div>
""",
            "quiz": [
                {
                    "q": "Why is 4G LTE classified as an 'All-IP' network compared to 2G and 3G?",
                    "opts": [
                        "It requires all cell phones to have optical fiber ports",
                        "Circuit-switching was completely eliminated; all voice, data, and signaling traffic is transported as IP datagrams (e.g. VoLTE for voice)",
                        "It only works inside buildings with WiFi",
                        "Every mobile user receives a static public IPv4 address"
                    ],
                    "ans": 1,
                    "exp": "4G LTE abandoned legacy circuit-switched telephony cores in favor of the pure packet-switched, all-IP Evolved Packet Core (EPC) (§6.4.1)."
                },
                {
                    "q": "Does user application data (such as web pages or YouTube videos) pass through the Mobility Management Entity (MME) in 4G LTE?",
                    "opts": [
                        "Yes, the MME buffers and caches all video streams",
                        "No, the MME operates strictly on the Control Plane (signaling and authentication); user data flows exclusively through the S-GW and P-GW on the Data Plane",
                        "Yes, the MME compresses user TCP packets",
                        "Only if the phone is roaming abroad"
                    ],
                    "ans": 1,
                    "exp": "LTE strictly separates the Control Plane (MME) from the Data Plane (S-GW and P-GW). Application data travels directly from eNodeB to S-GW to P-GW (§6.4.2)."
                }
            ]
        },
        {
            "id": "ch6-5",
            "num": "6.5",
            "title": "Mobility Management Principles",
            "subtitle": "Home/Foreign networks, Care-of-Address, Indirect vs Direct Routing",
            "content": r"""
<p>When a host moves across networks, how can remote senders communicate with it? Why can't standard Internet routing handle host mobility automatically?</p>

<div class="callout callout-mistake">
  <div class="callout-header">⚠️ Why Standard IP Routing Cannot Handle Mobility</div>
  <p>In standard IP networking, an IP address represents a specific network attachment point (defined by its network prefix, e.g. <code>192.168.1.0/24</code>). If a laptop moves from King Abdulaziz University to an airport in London:</p>
  <ul>
    <li><strong>If the laptop keeps its original IP address:</strong> Routers across the global Internet would have to advertise a specific <code>/32</code> host route for that individual laptop. If millions of mobile devices did this, BGP routing tables would explode into billions of entries, collapsing the Internet backbone!</li>
    <li><strong>If the laptop obtains a new IP address via DHCP:</strong> Active TCP connections would instantly break, because TCP sockets are bound to the permanent 4-tuple <code>(Src IP, Src Port, Dst IP, Dst Port)</code>. Ongoing downloads, SSH sessions, and video calls would terminate abruptly.</li>
  </ul>
</div>

<h3>6.5.1 The Mobility Vocabulary: Kurose & Ross Definitions</h3>
<ul>
  <li><strong>Mobile Node (MN):</strong> The entity that moves its point of attachment from one network to another while wishing to maintain continuous connectivity.</li>
  <li><strong>Home Network:</strong> The permanent home subnet of the mobile node (e.g., <code>128.119.40.0/24</code>).</li>
  <li><strong>Permanent IP Address:</strong> The permanent IP address assigned to the mobile node in its home network (e.g., <code>128.119.40.186</code>). Active TCP connections remain bound to this address.</li>
  <li><strong>Home Agent (HA):</strong> A router or server residing on the home network that performs mobility management and packet forwarding on behalf of the mobile node when it is away.</li>
  <li><strong>Foreign (Visited) Network:</strong> The foreign subnet where the mobile node is currently residing (e.g., <code>192.32.15.0/24</code>).</li>
  <li><strong>Foreign Agent (FA):</strong> An entity on the foreign network that assists the mobile node and coordinates packet delivery.</li>
  <li><strong>Care-of Address (COA):</strong> A temporary network-layer address assigned to the mobile node in the visited network. Packets tunneled to the mobile node are addressed to the COA.</li>
  <li><strong>Correspondent Node (CN):</strong> An arbitrary remote peer host wishing to communicate with the mobile node.</li>
</ul>

<!-- INLINE SVG: Figure 6.6 Indirect vs Direct Routing -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 280" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Correspondent Node (CN) -->
      <rect x="40" y="30" width="110" height="45" rx="6" fill="#3b82f6"/>
      <text x="95" y="52" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Correspondent</text>
      <text x="95" y="66" font-size="8" fill="#dbeafe" text-anchor="middle">CN (Sender)</text>

      <!-- Home Agent (HA) -->
      <rect x="360" y="30" width="120" height="45" rx="6" fill="#8b5cf6"/>
      <text x="420" y="52" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Home Agent</text>
      <text x="420" y="66" font-size="8" fill="#ede9fe" text-anchor="middle">HA (Home Subnet)</text>

      <!-- Foreign Agent (FA) / Visited Network -->
      <rect x="360" y="200" width="120" height="45" rx="6" fill="#10b981"/>
      <text x="420" y="222" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Foreign Agent</text>
      <text x="420" y="236" font-size="8" fill="#d1fae5" text-anchor="middle">FA (Care-of-Address)</text>

      <!-- Mobile Node (MN) -->
      <rect x="680" y="200" width="110" height="45" rx="6" fill="#0284c7"/>
      <text x="735" y="222" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Mobile Node</text>
      <text x="735" y="236" font-size="8" fill="#e0f2fe" text-anchor="middle">MN (Visited Cell)</text>

      <!-- Arrow 1: CN to HA -->
      <line x1="150" y1="52" x2="360" y2="52" stroke="#3b82f6" stroke-width="3"/>
      <text x="255" y="44" font-size="9" font-weight="700" fill="#1d4ed8" text-anchor="middle">1. Destined to Permanent IP</text>

      <!-- Arrow 2: HA tunnels to FA (Triangle Route) -->
      <line x1="420" y1="75" x2="420" y2="200" stroke="#8b5cf6" stroke-width="3" stroke-dasharray="5 3"/>
      <text x="495" y="140" font-size="9" font-weight="700" fill="#7e22ce" text-anchor="middle">2. IP-in-IP Tunnel to COA</text>

      <!-- Arrow 3: FA to MN -->
      <line x1="480" y1="222" x2="680" y2="222" stroke="#10b981" stroke-width="3"/>
      <text x="580" y="214" font-size="9" font-weight="700" fill="#047857" text-anchor="middle">3. Decapsulate & Deliver</text>

      <!-- Arrow 4: Direct Return from MN to CN -->
      <path d="M 680 235 Q 360 270 95 75" stroke="#ef4444" stroke-width="2.5" fill="none" stroke-dasharray="4 4"/>
      <text x="250" y="250" font-size="9" font-weight="700" fill="#b91c1c" text-anchor="middle">4. Direct Reverse Return Path to CN</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.6 — Indirect Routing in Mobile Networks Highlighting Triangle Routing Inefficiency (§6.5.2).</div>
</div>

<h3>6.5.2 Indirect Routing (Triangle Routing)</h3>
<p>Indirect routing routes all packets via the Home Agent:</p>
<ol>
  <li><strong>Transmission:</strong> The Correspondent Node addresses an IP datagram to the Mobile Node's permanent IP address. Standard IP routers deliver it to the Home Network.</li>
  <li><strong>Interception:</strong> The Home Agent intercepts the datagram (using Proxy ARP to capture frames addressed to the mobile host's MAC).</li>
  <li><strong>Encapsulation (Tunneling):</strong> The Home Agent wraps the entire original datagram inside an outer IP datagram addressed to the Care-of-Address (COA) and transmits it across the Internet.</li>
  <li><strong>Decapsulation:</strong> The Foreign Agent receives the outer datagram, strips the outer IP header, and delivers the original datagram to the Mobile Node.</li>
  <li><strong>Direct Reverse Path:</strong> When the Mobile Node sends packets back to the Correspondent Node, it addresses them directly to the CN's IP address!</li>
</ol>

<div class="callout callout-mistake">
  <div class="callout-header">⚠️ The Triangle Routing Inefficiency</div>
  Suppose the Correspondent Node and the Mobile Node are located in the same campus building in Jeddah, but the Mobile Node's Home Agent is in Boston. In indirect routing, every packet sent from the CN must travel 10,000 km across the Atlantic to Boston, only to be tunneled 10,000 km back to Jeddah! This creates massive, unnecessary end-to-end latency.
</div>

<h3>6.5.3 Direct Routing</h3>
<p>To overcome triangle routing, <strong>Direct Routing</strong> allows the Correspondent Node to tunnel packets directly to the Mobile Node's Care-of-Address:</p>
<ul>
  <li>The CN first queries the Home Agent to learn the Mobile Node's current Care-of-Address.</li>
  <li>The CN then encapsulates datagrams directly to the COA.</li>
  <li><em>Trade-off:</em> Direct routing eliminates the triangle detour, but requires specialized correspondent software and creates complex handoff problems if the mobile host moves while the CN is communicating with an outdated COA!</li>
</ul>
""",
            "quiz": [
                {
                    "q": "What is the primary operational drawback of Triangle Routing in Mobile IP indirect routing?",
                    "opts": [
                        "It requires all packets to be encrypted with RSA",
                        "Suboptimal path latency: packets must traverse the distant Home Agent even when the sender and receiver are in the same local room",
                        "It prevents mobile devices from using TCP",
                        "It requires physical Ethernet cables"
                    ],
                    "ans": 1,
                    "exp": "Triangle routing forces packets to travel to the home agent before tunneling back to the visited network, creating severe latency delays (§6.5.2)."
                },
                {
                    "q": "Why does the reverse path (Mobile Node -> Correspondent Node) in indirect routing NOT suffer from triangle routing?",
                    "opts": [
                        "Because the mobile node sends its return packets directly to the correspondent's IP address using standard IP forwarding",
                        "Because reverse packets travel through satellites",
                        "Because reverse packets use DNS",
                        "Because return packets are dropped"
                    ],
                    "ans": 0,
                    "exp": "The mobile node knows the CN's permanent IP address from incoming packets and can route return traffic directly to the CN without passing through the Home Agent (§6.5.2)."
                }
            ]
        },
        {
            "id": "ch6-6",
            "num": "6.6",
            "title": "Mobile IP",
            "subtitle": "Agent advertisement, registration, and encapsulation tunneling (RFC 5944)",
            "content": r"""
<p><strong>Mobile IP (RFC 5944)</strong> is the Internet standard for providing network-layer mobility. It specifies three coordinated protocol mechanisms:</p>

<h3>6.6.1 Agent Discovery</h3>
<p>When a mobile node enters a new subnet, it must discover whether it is attached to its home network or a foreign network, and discover the local agent's identity and Care-of-Address:</p>
<ul>
  <li><strong>Agent Advertisement:</strong> Home Agents and Foreign Agents periodically broadcast ICMP Router Advertisement extensions (Type 9, Code 16). The advertisement includes the agent's Care-of-Address and flags indicating supported capabilities.</li>
  <li><strong>Agent Solicitation:</strong> If a newly arriving mobile node does not want to wait for the next periodic advertisement, it broadcasts an ICMP Agent Solicitation (Type 10) frame to force immediate responses.</li>
</ul>

<h3>6.6.2 Registration with the Home Agent</h3>
<p>Once a mobile node arrives at a foreign network and obtains a Care-of-Address, it must register this address with its Home Agent:</p>

<!-- INLINE SVG: Figure 6.7 Mobile IP Registration Message Exchange -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 240" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Timeline Verticals -->
      <line x1="120" y1="40" x2="120" y2="220" stroke="#3b82f6" stroke-width="2"/>
      <text x="120" y="30" font-size="11" font-weight="700" fill="#3b82f6" text-anchor="middle">Mobile Node (MN)</text>

      <line x1="420" y1="40" x2="420" y2="220" stroke="#10b981" stroke-width="2"/>
      <text x="420" y="30" font-size="11" font-weight="700" fill="#10b981" text-anchor="middle">Foreign Agent (FA)</text>

      <line x1="720" y1="40" x2="720" y2="220" stroke="#8b5cf6" stroke-width="2"/>
      <text x="720" y="30" font-size="11" font-weight="700" fill="#8b5cf6" text-anchor="middle">Home Agent (HA)</text>

      <!-- Step 1: Registration Request MN -> FA -->
      <line x1="120" y1="70" x2="420" y2="90" stroke="#0284c7" stroke-width="2.5"/>
      <polygon points="420,90 410,84 412,94" fill="#0284c7"/>
      <text x="270" y="74" font-size="9" font-weight="700" fill="#0284c7" text-anchor="middle">1. Registration Request (UDP 434)</text>

      <!-- Step 2: Forwarded Registration Request FA -> HA -->
      <line x1="420" y1="105" x2="720" y2="125" stroke="#7e22ce" stroke-width="2.5"/>
      <polygon points="720,125 710,119 712,129" fill="#7e22ce"/>
      <text x="570" y="108" font-size="9" font-weight="700" fill="#7e22ce" text-anchor="middle">2. Forwards Reg Request (HA logs binding)</text>

      <!-- Step 3: Registration Reply HA -> FA -->
      <line x1="720" y1="145" x2="420" y2="165" stroke="#7e22ce" stroke-width="2.5"/>
      <polygon points="420,165 430,159 428,169" fill="#7e22ce"/>
      <text x="570" y="148" font-size="9" font-weight="700" fill="#7e22ce" text-anchor="middle">3. Registration Reply (Binding Confirmed)</text>

      <!-- Step 4: Forwarded Registration Reply FA -> MN -->
      <line x1="420" y1="180" x2="120" y2="200" stroke="#0284c7" stroke-width="2.5"/>
      <polygon points="120,200 130,194 128,204" fill="#0284c7"/>
      <text x="270" y="184" font-size="9" font-weight="700" fill="#0284c7" text-anchor="middle">4. Forwards Reg Reply to MN</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.7 — Mobile IP 4-Step Registration Message Flow (§6.6.2).</div>
</div>

<ol>
  <li><strong>MN to FA:</strong> Mobile Node sends a Registration Request inside UDP port 434 containing:
    <br>&bull; Permanent IP address of the MN
    <br>&bull; IP address of the Home Agent
    <br>&bull; Care-of-Address (COA)
    <br>&bull; Requested registration Lifetime (seconds)
    <br>&bull; 64-bit Identification field (nonce preventing replay attacks)
  </li>
  <li><strong>FA to HA:</strong> Foreign Agent validates request and forwards it to the Home Agent.</li>
  <li><strong>HA to FA:</strong> Home Agent verifies cryptographic authentication signature, binds the Permanent IP to the COA in its binding cache, and replies with a Registration Reply confirming acceptance and granted lifetime.</li>
  <li><strong>FA to MN:</strong> Foreign Agent notes binding and relays the reply to the Mobile Node.</li>
</ol>

<h3>6.6.3 IP-in-IP Encapsulation Tunneling</h3>
<p>When an IP datagram arrives at the Home Agent addressed to the Permanent IP:</p>
<ul>
  <li>The Home Agent does not modify the original datagram.</li>
  <li>Instead, it generates a brand-new <strong>Outer IP Header</strong>:
    <br>&bull; Source IP: Home Agent IP
    <br>&bull; Destination IP: Care-of-Address (COA)
    <br>&bull; Protocol field: <code>4</code> (indicates IP encapsulated inside IP!)
  </li>
  <li>The entire original datagram (including its original IP header with Source=CN, Dst=MN) becomes the payload of the outer datagram.</li>
</ul>
""",
            "quiz": [
                {
                    "q": "What transport-layer protocol and port number does Mobile IP use for its registration requests and replies?",
                    "opts": [
                        "TCP port 80",
                        "UDP port 434",
                        "TCP port 22",
                        "ICMP type 0"
                    ],
                    "ans": 1,
                    "exp": "Mobile IP registration messages are carried inside UDP segments with well-known port 434 (§6.6.2)."
                },
                {
                    "q": "In Mobile IP encapsulation, what value is placed in the Protocol field of the outer IP header?",
                    "opts": [
                        "Protocol 6 (TCP)",
                        "Protocol 17 (UDP)",
                        "Protocol 4 (IP-in-IP encapsulation)",
                        "Protocol 1 (ICMP)"
                    ],
                    "ans": 2,
                    "exp": "IP protocol number 4 designates that the payload of this IP datagram is itself another complete IP datagram (§6.6.3)."
                }
            ]
        },
        {
            "id": "ch6-7",
            "num": "6.7",
            "title": "Managing Mobility in Cellular Networks",
            "subtitle": "HLR, VLR, roaming, and GSM handoffs",
            "content": r"""
<p>Cellular networks have managed mobile devices for decades across millions of users. While Mobile IP was designed by computer scientists for the Internet, cellular engineers in 3GPP created a highly structured, database-driven mobility architecture.</p>

<h3>6.7.1 The Cellular Location Registers: HLR and VLR</h3>
<p>Every cellular carrier network maintains two essential databases:</p>
<ul>
  <li><strong>Home Location Register (HLR):</strong> The master database maintained by the subscriber's home cellular carrier. It contains:
    <br>&bull; The subscriber's permanent identity: <strong>IMSI (International Mobile Subscriber Identity)</strong>.
    <br>&bull; Subscribed services and profile permissions.
    <br>&bull; A dynamic pointer to the <strong>Visitor Location Register (VLR)</strong> in the visited network where the user is currently roaming!
  </li>
  <li><strong>Visitor Location Register (VLR):</strong> A local database co-located with the Mobile Switching Center (MSC) in the visited network. When a mobile phone powers on in a visited cell, it registers with the local VLR. The VLR assigns a temporary roaming identifier called the <strong>MSRN (Mobile Station Roaming Number)</strong>.</li>
</ul>

<h3>6.7.2 GSM Call Routing to a Roaming Subscriber (The 5-Step Dance)</h3>
<p>When someone dials a mobile phone number, how does the cellular network connect the call?</p>

<!-- INLINE SVG: Figure 6.8 GSM Call Routing Sequence -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 250" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Node Columns -->
      <rect x="30" y="30" width="100" height="40" rx="6" fill="#3b82f6"/>
      <text x="80" y="55" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">Caller / PSTN</text>

      <rect x="180" y="30" width="110" height="40" rx="6" fill="#0284c7"/>
      <text x="235" y="55" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">Home MSC</text>

      <rect x="340" y="30" width="100" height="40" rx="6" fill="#8b5cf6"/>
      <text x="390" y="55" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">Home HLR</text>

      <rect x="500" y="30" width="110" height="40" rx="6" fill="#10b981"/>
      <text x="555" y="55" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">Visited VLR</text>

      <rect x="670" y="30" width="120" height="40" rx="6" fill="#059669"/>
      <text x="730" y="55" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">Visited MSC & Mobile</text>

      <!-- Step 1: Call to Home MSC -->
      <line x1="130" y1="95" x2="180" y2="95" stroke="#3b82f6" stroke-width="2.5"/>
      <text x="155" y="87" font-size="8" font-weight="700" fill="#1d4ed8" text-anchor="middle">1. Dial</text>

      <!-- Step 2: Query HLR -->
      <line x1="290" y1="110" x2="340" y2="110" stroke="#0284c7" stroke-width="2.5"/>
      <text x="315" y="102" font-size="8" font-weight="700" fill="#0369a1" text-anchor="middle">2. Where is X?</text>

      <!-- Step 3: Query VLR for MSRN -->
      <line x1="440" y1="125" x2="500" y2="125" stroke="#8b5cf6" stroke-width="2.5"/>
      <text x="470" y="117" font-size="8" font-weight="700" fill="#6d28d9" text-anchor="middle">3. Alloc MSRN</text>

      <!-- Step 4: Return MSRN to Home MSC -->
      <line x1="500" y1="145" x2="290" y2="145" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="4 3"/>
      <text x="400" y="139" font-size="8" font-weight="700" fill="#6d28d9" text-anchor="middle">4. Return temporary roaming MSRN number</text>

      <!-- Step 5: Direct Circuit Setup to Visited MSC -->
      <path d="M 235 70 Q 235 210 670 210" stroke="#059669" stroke-width="3" fill="none"/>
      <text x="450" y="200" font-size="9" font-weight="800" fill="#047857" text-anchor="middle">5. Set up telephone circuit direct to Visited MSC & Page Mobile!</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 6.8 — GSM 5-Step Call Routing Dance to a Roaming Cellular Subscriber (§6.7.2).</div>
</div>

<ol>
  <li><strong>Caller dials number:</strong> Call is routed through the telephone network to the subscriber's <strong>Home MSC</strong> (Gateway MSC).</li>
  <li><strong>Home MSC queries HLR:</strong> The Home MSC queries the subscriber's HLR database asking for their current location.</li>
  <li><strong>HLR queries Visited VLR:</strong> The HLR knows which visited VLR the phone is currently roaming under. It asks the visited VLR to allocate a temporary roaming number: <strong>MSRN (Mobile Station Roaming Number)</strong>.</li>
  <li><strong>VLR returns MSRN:</strong> The Visited VLR returns the temporary MSRN back to the HLR, which passes it to the Home MSC.</li>
  <li><strong>Circuit setup to Visited MSC:</strong> The Home MSC uses standard telephone trunk signaling to route the call directly to the Visited MSC. The Visited MSC pages the mobile phone within its current cell and rings the device!</li>
</ol>

<h3>6.7.3 Handoffs in GSM: The Anchor MSC</h3>
<p>When a phone moves between base stations during an active call:</p>
<ul>
  <li><strong>Intra-BSS Handoff:</strong> Mobile changes radio frequencies within the same cell tower. Handled entirely locally.</li>
  <li><strong>Inter-BSS Handoff (Same MSC):</strong> Mobile transitions to a new base station controller under the same MSC. The MSC updates routing paths between the base stations seamlessly.</li>
  <li><strong>Inter-MSC Handoff (Anchor MSC Architecture):</strong> When the mobile moves to a cell controlled by a completely different MSC, the original MSC that established the call remains the <strong>Anchor MSC</strong> for the entire duration of the call. The Anchor MSC extends the audio circuit to the new MSC, avoiding call drops!</li>
</ul>
""",
            "quiz": [
                {
                    "q": "What is the role of the Anchor MSC during a GSM inter-MSC handoff?",
                    "opts": [
                        "It disconnects the call and forces the user to redial",
                        "It remains the fixed, permanent routing point for the ongoing call, extending the circuit to the new MSC so the call is never dropped",
                        "It converts the call from cellular to WiFi",
                        "It re-encrypts the call using RSA"
                    ],
                    "ans": 1,
                    "exp": "The Anchor MSC stays connected as the anchor point throughout the call, extending circuit legs to subsequent MSCs to ensure zero interruption (§6.7.3)."
                },
                {
                    "q": "What temporary number is generated by the visited VLR to allow the Home MSC to route an incoming call directly to a roaming cellular user?",
                    "opts": [
                        "IMSI (International Mobile Subscriber Identity)",
                        "MSRN (Mobile Station Roaming Number)",
                        "MAC address",
                        "Subnet mask"
                    ],
                    "ans": 1,
                    "exp": "The MSRN (Mobile Station Roaming Number) is the temporary, routable telephone number allocated by the visited VLR for call setup (§6.7.2)."
                }
            ]
        },
        {
            "id": "ch6-8",
            "num": "6.8",
            "title": "Wireless and Mobility: Impact on Higher-Layer Protocols",
            "subtitle": "Why TCP fails over wireless and split-connection TCP",
            "content": r"""
<p>The transport layer (specifically TCP) was designed under the assumption of wired networks. When TCP is run unmodified over wireless links, its performance degrades catastrophically.</p>

<div class="callout callout-mistake">
  <div class="callout-header">⚠️ The Fundamental Flaw: TCP Loss = Congestion Assumption</div>
  <p>In wired networks, transmission bit error rates are vanishingly small (<span class="math-inline">&lt; 10^{-10}</span> on fiber). Therefore, <strong>almost all packet losses are caused by router buffer overflow (network congestion)</strong>.</p>
  <p>TCP's congestion control algorithms (Slow Start, AIMD) are built on this exact premise:</p>
  <div class="math-display">
    \text{Packet Loss Detected} \implies \text{Network is Congested} \implies \text{Cut } cwnd \text{ in Half (or to 1 MSS)!}
  </div>
  <p>On wireless links, bit error rates are thousands of times higher (<span class="math-inline">10^{-3}</span> to <span class="math-inline">10^{-5}</span>) due to RF noise, multipath fading, and handovers. When a packet is corrupted by radio noise:</p>
  <ul>
    <li>The network is <em>not congested at all</em>! The link has plenty of spare capacity.</li>
    <li>Yet TCP detects the loss, misinterprets it as severe congestion, slashes its congestion window <span class="math-inline">cwnd</span>, and drastically throttles its sending rate!</li>
    <li>Throughput plunges by 70% to 90% unnecessarily!</li>
  </ul>
</div>

<h3>6.8.1 Solutions to the Wireless TCP Dilemma</h3>
<p>Computer networking researchers and standards bodies have developed three primary architectural solutions:</p>

<div class="summary-grid" style="margin:1rem 0;">
  <div class="summary-card" style="border-top:3px solid #3b82f6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">1. Local Link-Layer Recovery</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Use fast Automatic Repeat reQuest (ARQ) and Forward Error Correction (FEC) at the wireless link layer (e.g., 802.11 retries and LTE HARQ). The link layer repairs corrupted frames locally before TCP's sender timeout timer expires, effectively hiding wireless losses from TCP.
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #10b981;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">2. TCP-Aware Link Layer (Snoop TCP)</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      The wireless base station snoops on passing TCP segments and caches copies locally. If duplicate ACKs arrive from the mobile host indicating a wireless loss, the base station immediately retransmits the lost packet locally and <em>suppresses the duplicate ACKs from reaching the wired sender</em>!
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #8b5cf6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">3. Split-Connection TCP (Split-TCP)</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      The base station acts as a proxy, splitting the end-to-end TCP connection into two separate connections: standard TCP over the stable wired Internet (Sender &leftrightarrow; Base Station) and a tuned, error-tolerant wireless protocol over the last hop (Base Station &leftrightarrow; Mobile Host).
    </p>
  </div>
</div>

<div class="callout callout-insight">
  <div class="callout-header">💡 Trade-Offs in Split-Connection TCP</div>
  While Split-TCP completely isolates the wired sender from wireless packet loss, it <strong>violates TCP end-to-end semantics</strong>: an ACK received by the sender only confirms that data reached the base station proxy, not that the mobile client has safely received it! If the base station crashes, acknowledged data can be lost.
</div>
""",
            "quiz": [
                {
                    "q": "Why does standard TCP perform poorly over wireless links when packets are lost due to RF radio noise?",
                    "opts": [
                        "TCP refuses to run over radio waves",
                        "TCP mistakenly assumes that all packet loss is caused by network congestion, cutting cwnd and throttling throughput when no congestion exists",
                        "TCP headers are too large for wireless antennas",
                        "Radio noise changes the TCP sequence number length"
                    ],
                    "ans": 1,
                    "exp": "Standard TCP assumes packet loss implies buffer overflow congestion, inappropriately slashing cwnd upon wireless channel bit errors (§6.8)."
                },
                {
                    "q": "What is the architectural drawback of using Split-Connection TCP at a wireless base station?",
                    "opts": [
                        "It requires all packets to use UDP",
                        "It breaks TCP's end-to-end reliability semantics, because the sender receives ACKs before data has actually reached the mobile host",
                        "It cannot support web browsing (HTTP)",
                        "It increases packet sizes beyond MTU limits"
                    ],
                    "ans": 1,
                    "exp": "In Split-TCP, the base station ACKs packets to the sender before delivering them to the mobile host, violating true end-to-end acknowledgment guarantees (§6.8.1)."
                }
            ]
        },
        {
            "id": "ch6-9",
            "num": "6.9",
            "title": "Chapter 6 Summary & Worked Problems",
            "subtitle": "Comprehensive wireless/mobile review and step-by-step worked calculations",
            "content": r"""
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 1: CDMA Orthogonality & Decoding</div>
    <span class="interactive-badge">P5 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Suppose two CDMA transmitters have the following 8-bit chip sequences:
    <br>&emsp;User 1: <span class="math-inline">\mathbf{c}_1 = (+1, +1, +1, -1, +1, -1, -1, -1)</span>
    <br>&emsp;User 2: <span class="math-inline">\mathbf{c}_2 = (+1, -1, +1, +1, -1, -1, +1, -1)</span>
  </p>
  <p>(a) Prove that <span class="math-inline">\mathbf{c}_1</span> and <span class="math-inline">\mathbf{c}_2</span> are strictly orthogonal.</p>
  <p>(b) If User 1 sends data bit <span class="math-inline">d_1 = +1</span> and User 2 sends data bit <span class="math-inline">d_2 = -1</span>, compute the combined channel signal vector <span class="math-inline">\mathbf{S}</span>.</p>
  <p>(c) Show mathematically how the receiver decodes User 1's transmitted bit from <span class="math-inline">\mathbf{S}</span>.</p>

  <button class="btn-secondary" onclick="toggleSolution('ch6-prob1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch6-prob1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Check orthogonality via inner dot product:
      <div class="math-display">
        \mathbf{c}_1 \cdot \mathbf{c}_2 = (1)(1) + (1)(-1) + (1)(1) + (-1)(1) + (1)(-1) + (-1)(-1) + (-1)(1) + (-1)(-1)
      </div>
      <div class="math-display">
        = 1 - 1 + 1 - 1 - 1 + 1 - 1 + 1 = 0
      </div>
      Since <span class="math-inline">\frac{1}{8} (\mathbf{c}_1 \cdot \mathbf{c}_2) = 0</span>, the codes are strictly orthogonal!
    </div>
    <div class="calc-step">Step 2: Compute transmitted chip vectors:
      <br>&emsp;User 1: <span class="math-inline">d_1 \times \mathbf{c}_1 = (+1) \times (+1, +1, +1, -1, +1, -1, -1, -1) = (+1, +1, +1, -1, +1, -1, -1, -1)</span>
      <br>&emsp;User 2: <span class="math-inline">d_2 \times \mathbf{c}_2 = (-1) \times (+1, -1, +1, +1, -1, -1, +1, -1) = (-1, +1, -1, -1, +1, +1, -1, +1)</span>
    </div>
    <div class="calc-step">Step 3: Compute composite channel vector <span class="math-inline">\mathbf{S} = d_1 \mathbf{c}_1 + d_2 \mathbf{c}_2</span>:
      <div class="math-display">
        \mathbf{S} = (1-1,\ 1+1,\ 1-1,\ -1-1,\ 1+1,\ -1+1,\ -1-1,\ -1+1) = (0,\ 2,\ 0,\ -2,\ 2,\ 0,\ -2,\ 0)
      </div>
    </div>
    <div class="calc-step">Step 4: Decode User 1 at receiver:
      <div class="math-display">
        \mathbf{S} \cdot \mathbf{c}_1 = (0)(1) + (2)(1) + (0)(1) + (-2)(-1) + (2)(1) + (0)(-1) + (-2)(-1) + (0)(-1)
      </div>
      <div class="math-display">
        = 0 + 2 + 0 + 2 + 2 + 0 + 2 + 0 = 8
      </div>
      <div class="math-display">
        d_1 = \frac{1}{8} (\mathbf{S} \cdot \mathbf{c}_1) = \frac{8}{8} = +1
      </div>
    </div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
      Final Answer: The extracted data bit is <strong>+1 (binary 1)</strong>! User 2's interference was completely canceled out.
    </div>
  </div>
</div>

<div class="interactive-card" style="margin-top:1.5rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 2: 802.11 RTS/CTS Timing Budget & Efficiency</div>
    <span class="interactive-badge">P9 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Suppose an 802.11b station transmits a 1000-byte data frame using the RTS/CTS exchange at transmission rate <span class="math-inline">R = 11\text{ Mbps}</span>. Frame parameters:
    <br>&emsp;&bull; RTS frame = 20 bytes, CTS frame = 14 bytes, ACK frame = 14 bytes
    <br>&emsp;&bull; SIFS = <span class="math-inline">10\ \mu\text{s}</span>, DIFS = <span class="math-inline">50\ \mu\text{s}</span>, Propagation delay = <span class="math-inline">1\ \mu\text{s}</span> per hop
    <br>&emsp;&bull; Control frames (RTS, CTS, ACK) are sent at base rate <span class="math-inline">2\text{ Mbps}</span>; DATA is sent at <span class="math-inline">11\text{ Mbps}</span>.
    <br>Find the total time required to successfully transmit the frame (assuming zero backoff).
  </p>

  <button class="btn-secondary" onclick="toggleSolution('ch6-prob2-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch6-prob2-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Calculate transmission times for each frame:
      <br>&emsp;&bull; <span class="math-inline">t_{\text{RTS}} = (20 \times 8\text{ bits}) / (2 \times 10^6\text{ bps}) = 160 / 2 = 80\ \mu\text{s}</span>
      <br>&emsp;&bull; <span class="math-inline">t_{\text{CTS}} = (14 \times 8\text{ bits}) / (2 \times 10^6\text{ bps}) = 112 / 2 = 56\ \mu\text{s}</span>
      <br>&emsp;&bull; <span class="math-inline">t_{\text{DATA}} = (1000 \times 8\text{ bits}) / (11 \times 10^6\text{ bps}) = 8000 / 11 \approx 727.27\ \mu\text{s}</span>
      <br>&emsp;&bull; <span class="math-inline">t_{\text{ACK}} = (14 \times 8\text{ bits}) / (2 \times 10^6\text{ bps}) = 112 / 2 = 56\ \mu\text{s}</span>
    </div>
    <div class="calc-step">Step 2: Sum all components in the CSMA/CA sequence:
      <div class="math-display">
        T_{\text{total}} = \text{DIFS} + t_{\text{RTS}} + \text{prop} + \text{SIFS} + t_{\text{CTS}} + \text{prop} + \text{SIFS} + t_{\text{DATA}} + \text{prop} + \text{SIFS} + t_{\text{ACK}} + \text{prop}
      </div>
      <div class="math-display">
        T_{\text{total}} = 50 + 80 + 1 + 10 + 56 + 1 + 10 + 727.27 + 1 + 10 + 56 + 1
      </div>
      <div class="math-display">
        T_{\text{total}} = 50 + 80 + 56 + 727.27 + 56 + (3 \times 10) + (4 \times 1) = 969.27 + 30 + 4 = 1003.27\ \mu\text{s} \approx 1.003\text{ ms}
      </div>
    </div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
      Final Answer: Total elapsed time is <strong>1003.27 &mu;s (~1.003 ms)</strong>! Pure payload transmission accounts for ~72.5% of channel time; the rest is CSMA/CA coordination overhead.
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the primary trade-off of using the RTS/CTS reservation exchange in 802.11?",
                    "opts": [
                        "It consumes extra channel overhead for small packets, but saves massive channel time for large data packets by preventing catastrophic collisions caused by hidden terminals",
                        "It disables all wireless encryption",
                        "It requires all hosts to switch to 60 GHz microwave bands",
                        "It permanently doubles the transmission rate"
                    ],
                    "ans": 0,
                    "exp": "For short packets, the 4-way RTS/CTS overhead exceeds the packet size; for large frames, reserving the medium prevents devastating collisions and wasted airtime (§6.3.3)."
                }
            ]
        }
    ]
}
