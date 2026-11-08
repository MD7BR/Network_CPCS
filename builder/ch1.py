"""Chapter 1 Data: Computer Networks and the Internet (Kurose & Ross 6th & 8th Ed.)
Exhaustive textbook depth, Midterm Study Guide integration (P1-P8), bit-accurate SVG diagrams,
and fully functional interactive calculators and steppers.
"""

CH1_DATA = {
    "id": "ch1",
    "num": 1,
    "title": "Computer Networks and the Internet",
    "subtitle": "Network Edge, Core, Delay/Loss/Throughput, Protocol Layering, Security & History",
    "layer": "Overview & Foundation",
    "color": "#64748b",
    "objectives": [
        "Describe the Internet from both the 'nuts-and-bolts' view and the 'service' view",
        "Define what a protocol is (format, order of messages, and actions taken)",
        "Compare access networks: DSL, Cable (HFC), FTTH (PON/AON), Enterprise, WiFi, and Cellular",
        "Compare guided (twisted pair, coax, fiber) and unguided (radio, satellite) physical media",
        "Explain packet switching, store-and-forward delay, queuing, and buffer overflow loss",
        "Distinguish routing (control plane) from forwarding (data plane)",
        "Compare packet switching with circuit switching (FDM and TDM) and calculate user capacity",
        "Describe the hierarchical 'network of networks' structure (Tier-1, IXPs, Regional ISPs, Content Providers)",
        "Calculate the 4 components of nodal delay: processing, queuing, transmission (L/R), and propagation (d/s)",
        "Use traffic intensity (La/R) to evaluate queuing delay and predict packet loss",
        "Calculate path throughput and identify the bottleneck link",
        "Describe security threats: malware (viruses vs worms), DoS/DDoS, packet sniffing, and IP spoofing",
        "Name the 5 layers of the Internet stack, their PDUs, and compare with the 7-layer OSI model",
        "Trace packet encapsulation and decapsulation across hosts, switches, and routers"
    ],
    "sections": [
        {
            "id": "ch1-1",
            "num": "1.1",
            "title": "What Is the Internet?",
            "subtitle": "Nuts-and-bolts view, services view, RFCs, and protocol definitions",
            "content": r"""
<p>To understand the Internet, we examine it from two complementary perspectives: the <strong>nuts-and-bolts view</strong> (the physical hardware and software components) and the <strong>services view</strong> (the communication infrastructure enabling distributed applications).</p>

<div class="summary-grid" style="margin:1rem 0;">
  <div class="summary-card" style="border-top:3px solid #3b82f6;">
    <div style="font-size:1.4rem; margin-bottom:0.25rem;">🔩</div>
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">1. Nuts-and-Bolts View</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      The Internet is an interconnected system of billions of computing devices called <strong>hosts</strong> or <strong>end systems</strong>. Hosts connect via a fabric of <strong>communication links</strong> (fiber, copper, radio, satellite) and <strong>packet switches</strong> (routers and link-layer switches).
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #10b981;">
    <div style="font-size:1.4rem; margin-bottom:0.25rem;">🌐</div>
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">2. Services View</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      The Internet is an infrastructure that provides services to distributed applications (Web, email, video streaming, games, social networks) through an <strong>Application Programming Interface (API)</strong> specifying how programs request data delivery from the network.
    </p>
  </div>
</div>

<h3>1.1.1 End Systems, Communication Links, and Packet Switches</h3>
<ul>
  <li><strong>End Systems (Hosts):</strong> Devices that sit at the network edge and run application programs. These include traditional PCs, workstations, and servers in data centers, as well as modern smartphones, tablets, TVs, gaming consoles, webcams, smart watches, and billions of Internet of Things (IoT) sensors. Hosts are divided into <em>clients</em> (e.g. mobile browsers) and <em>servers</em> (powerful machines in data centers).</li>
  <li><strong>Transmission Rate (Bandwidth):</strong> The speed at which a communication link pushes bits into the medium, measured in <em>bits per second</em> (bps, Kbps, Mbps, Gbps).</li>
  <li><strong>Packets:</strong> When an end system sends data, it breaks it into chunks and prefixes each chunk with header bytes. These formatted packages are called <strong>packets</strong>.</li>
  <li><strong>Packet Switches:</strong> Intermediate nodes that take an arriving packet on an incoming link and forward it onto an outgoing link. The two dominant types are:
    <ul>
      <li><strong>Routers:</strong> Layer-3 switches typically used in the network core that read IP addresses to route packets between networks.</li>
      <li><strong>Link-Layer Switches:</strong> Layer-2 switches typically used in access networks that forward frames using MAC addresses.</li>
    </ul>
  </li>
  <li><strong>Route / Path:</strong> The sequence of communication links and packet switches traversed by a packet from sender to receiver.</li>
  <li><strong>Internet Standards & RFCs:</strong> Internet standards are developed by the <strong>IETF (Internet Engineering Task Force)</strong> and published as <strong>RFCs (Request for Comments)</strong>. Examples include RFC 791 (IPv4), RFC 793 (TCP), and RFC 2616 (HTTP/1.1). Other standards bodies include the IEEE 802 committee (Ethernet, WiFi) and the W3C (Web standards).</li>
</ul>

<!-- FIGURE 1.1: INTERACTIVE ARCHITECTURE OF THE INTERNET -->
<div class="svg-figure">
  <div class="svg-container">
    <svg id="fig1-1-svg" viewBox="0 0 920 360" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:12px; width:100%;">
      <defs>
        <linearGradient id="grad-host" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#3b82f6"/>
          <stop offset="100%" stop-color="#1d4ed8"/>
        </linearGradient>
        <linearGradient id="grad-switch" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#475569"/>
        </linearGradient>
        <linearGradient id="grad-router" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#10b981"/>
          <stop offset="100%" stop-color="#047857"/>
        </linearGradient>
        <linearGradient id="grad-server" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#8b5cf6"/>
          <stop offset="100%" stop-color="#6d28d9"/>
        </linearGradient>
        <filter id="glow-pkt" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="4" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      <!-- Shaded Zones -->
      <rect x="20" y="20" width="240" height="320" rx="10" fill="#eff6ff" fill-opacity="0.45" stroke="#bfdbfe" stroke-dasharray="4 4"/>
      <text x="140" y="42" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">NETWORK EDGE (Hosts & Access)</text>

      <rect x="280" y="20" width="370" height="320" rx="10" fill="#ecfdf5" fill-opacity="0.45" stroke="#a7f3d0" stroke-dasharray="4 4"/>
      <text x="465" y="42" font-size="12" font-weight="700" fill="#065f46" text-anchor="middle">NETWORK CORE (Mesh of Routers)</text>

      <rect x="670" y="20" width="230" height="320" rx="10" fill="#f5f3ff" fill-opacity="0.45" stroke="#ddd6fe" stroke-dasharray="4 4"/>
      <text x="785" y="42" font-size="12" font-weight="700" fill="#5b21b6" text-anchor="middle">SERVERS & DATA CENTERS</text>

      <!-- Edge Links -->
      <line x1="120" y1="95" x2="200" y2="180" stroke="#93c5fd" stroke-width="3"/>
      <line x1="120" y1="180" x2="200" y2="180" stroke="#93c5fd" stroke-width="3"/>
      <line x1="120" y1="265" x2="200" y2="180" stroke="#93c5fd" stroke-width="3"/>

      <!-- Access to Core -->
      <line x1="240" y1="180" x2="350" y2="120" stroke="#94a3b8" stroke-width="3"/>
      <line x1="240" y1="180" x2="350" y2="240" stroke="#94a3b8" stroke-width="3"/>

      <!-- Core Mesh -->
      <line x1="375" y1="120" x2="550" y2="120" stroke="#10b981" stroke-width="4"/>
      <line x1="375" y1="240" x2="550" y2="240" stroke="#10b981" stroke-width="4"/>
      <line x1="375" y1="120" x2="550" y2="240" stroke="#6ee7b7" stroke-width="3"/>
      <line x1="375" y1="240" x2="550" y2="120" stroke="#6ee7b7" stroke-width="3"/>
      <line x1="375" y1="120" x2="375" y2="240" stroke="#10b981" stroke-width="3"/>
      <line x1="550" y1="120" x2="550" y2="240" stroke="#10b981" stroke-width="3"/>

      <!-- Core to Data Center -->
      <line x1="575" y1="120" x2="730" y2="180" stroke="#c084fc" stroke-width="4"/>
      <line x1="575" y1="240" x2="730" y2="180" stroke="#c084fc" stroke-width="4"/>

      <!-- Nodes: Edge -->
      <g id="node-host1" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Client Laptop', 'End system running web browser (IP: 192.168.1.105, Port: 53210)')">
        <rect x="40" y="70" width="80" height="50" rx="8" fill="url(#grad-host)"/>
        <text x="80" y="94" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">💻 Laptop</text>
        <text x="80" y="110" font-size="9" fill="#bfdbfe" text-anchor="middle">Client Host</text>
      </g>
      <g id="node-host2" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Smartphone', 'Mobile end system streaming audio over 802.11 WiFi')">
        <rect x="40" y="155" width="80" height="50" rx="8" fill="url(#grad-host)"/>
        <text x="80" y="179" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">📱 Phone</text>
        <text x="80" y="195" font-size="9" fill="#bfdbfe" text-anchor="middle">Mobile Host</text>
      </g>
      <g id="node-host3" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('IoT Sensor', 'Smart embedded camera transmitting UDP telemetry')">
        <rect x="40" y="240" width="80" height="50" rx="8" fill="url(#grad-host)"/>
        <text x="80" y="264" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">📷 IoT Cam</text>
        <text x="80" y="280" font-size="9" fill="#bfdbfe" text-anchor="middle">Smart Device</text>
      </g>

      <!-- Access Switch -->
      <g id="node-switch" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Access Switch / Base Station', 'Layer-2 switch forwarding Ethernet frames based on 48-bit MAC addresses')">
        <rect x="200" y="155" width="55" height="50" rx="6" fill="url(#grad-switch)"/>
        <text x="227" y="179" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Switch</text>
        <text x="227" y="194" font-size="8" fill="#cbd5e1" text-anchor="middle">Access Node</text>
      </g>

      <!-- Routers in Core -->
      <g id="node-r1" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Edge Router R1', 'First-hop router; examines IP destination address and forwards over shortest path')">
        <circle cx="375" cy="120" r="26" fill="url(#grad-router)"/>
        <text x="375" y="117" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">R1</text>
        <path d="M 363 125 L 387 125 M 375 120 L 375 130" stroke="#ffffff" stroke-width="2"/>
        <text x="375" y="160" font-size="9" font-weight="600" fill="#065f46" text-anchor="middle">Router 1</text>
      </g>
      <g id="node-r2" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Core Router R2', 'High-throughput backbone router running OSPF/BGP')">
        <circle cx="375" cy="240" r="26" fill="url(#grad-router)"/>
        <text x="375" y="237" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">R2</text>
        <path d="M 363 245 L 387 245 M 375 240 L 375 250" stroke="#ffffff" stroke-width="2"/>
        <text x="375" y="280" font-size="9" font-weight="600" fill="#065f46" text-anchor="middle">Router 2</text>
      </g>
      <g id="node-r3" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Core Router R3', 'Interconnects regional ISPs via Tier-1 transit backbone and peering points (IXP)')">
        <circle cx="550" cy="120" r="26" fill="url(#grad-router)"/>
        <text x="550" y="117" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">R3</text>
        <path d="M 538 125 L 562 125 M 550 120 L 550 130" stroke="#ffffff" stroke-width="2"/>
        <text x="550" y="160" font-size="9" font-weight="600" fill="#065f46" text-anchor="middle">Router 3</text>
      </g>
      <g id="node-r4" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Edge Router R4', 'Gateway to the data center network, enforcing firewall ACLs and BGP route policies')">
        <circle cx="550" cy="240" r="26" fill="url(#grad-router)"/>
        <text x="550" y="237" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">R4</text>
        <path d="M 538 245 L 562 245 M 550 240 L 550 250" stroke="#ffffff" stroke-width="2"/>
        <text x="550" y="280" font-size="9" font-weight="600" fill="#065f46" text-anchor="middle">Router 4</text>
      </g>

      <!-- Server / Data Center -->
      <g id="node-server" class="diagram-node" style="cursor:pointer;" onclick="inspectNode('Web Server Farm', 'Data center hosting HTTP origin servers and cloud databases (IP: 142.250.190.46, Port: 80/443)')">
        <rect x="730" y="140" width="115" height="80" rx="8" fill="url(#grad-server)"/>
        <line x1="740" y1="160" x2="835" y2="160" stroke="#ddd6fe" stroke-width="2"/>
        <line x1="740" y1="180" x2="835" y2="180" stroke="#ddd6fe" stroke-width="2"/>
        <line x1="740" y1="200" x2="835" y2="200" stroke="#ddd6fe" stroke-width="2"/>
        <circle cx="750" cy="150" r="2.5" fill="#a7f3d0"/>
        <circle cx="750" cy="170" r="2.5" fill="#a7f3d0"/>
        <circle cx="750" cy="190" r="2.5" fill="#a7f3d0"/>
        <text x="785" y="153" font-size="11" font-weight="700" fill="#ffffff">Web Server</text>
        <text x="785" y="173" font-size="9" fill="#ddd6fe">Data Center</text>
        <text x="785" y="212" font-size="8" fill="#a7f3d0">Online (200 OK)</text>
      </g>

      <!-- Animated Traveling Packet -->
      <circle id="anim-packet-circle" cx="80" cy="95" r="9" fill="#ef4444" filter="url(#glow-pkt)" opacity="0"/>
      <text id="anim-packet-label" x="80" y="80" font-size="10" font-weight="800" fill="#ef4444" text-anchor="middle" opacity="0">Packet</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 1.1 — Overall Architecture of the Internet: Edge Hosts, Access Networks, Core Packet Switches, and Data Centers (§1.1.1).</div>
  <div class="figure-notice">💡 Click any device node above to inspect its role. Use the controls below to animate a packet journey through the network!</div>
  <div class="fig-controls">
    <button class="btn-primary" onclick="animateFigure1Packet()">▶ Send Packet (Laptop → Server)</button>
    <button class="btn-secondary" onclick="resetFigure1Packet()">🔄 Reset</button>
    <div id="fig1-info" class="fig-step-badge" style="color:var(--primary-text);">Status: Ready. Click 'Send Packet' to trace packet flow.</div>
  </div>
</div>

<h3>1.1.2 What Is a Protocol?</h3>
<div class="callout callout-def">
  <div class="callout-header">📘 Definition: Network Protocol (Kurose & Ross §1.1.2)</div>
  A <strong>protocol</strong> defines the <em>format</em> and the <em>order</em> of messages exchanged between two or more communicating entities, as well as the <em>actions taken</em> on the transmission and/or receipt of a message or other event.
</div>

<p>Every activity in the Internet is governed by protocols. For example, hardware protocols in network interface cards control bit transmission on copper or fiber; congestion control protocols in end systems regulate transmission rates; routing protocols in core switches construct forwarding tables.</p>

<!-- FIGURE 1.2: HUMAN VS NETWORK PROTOCOL TIMELINE -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <!-- Left side: Human Protocol -->
      <text x="180" y="25" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">Human Protocol Analogy</text>
      <line x1="80" y1="40" x2="80" y2="200" stroke="#94a3b8" stroke-width="2"/>
      <line x1="280" y1="40" x2="280" y2="200" stroke="#94a3b8" stroke-width="2"/>
      <text x="80" y="38" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Alice</text>
      <text x="280" y="38" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Bob</text>

      <line x1="80" y1="65" x2="280" y2="85" stroke="#3b82f6" stroke-width="2"/>
      <text x="180" y="70" font-size="10" fill="#1d4ed8" text-anchor="middle">"Hi"</text>

      <line x1="280" y1="95" x2="80" y2="115" stroke="#3b82f6" stroke-width="2"/>
      <text x="180" y="100" font-size="10" fill="#1d4ed8" text-anchor="middle">"Hi"</text>

      <line x1="80" y1="125" x2="280" y2="145" stroke="#10b981" stroke-width="2"/>
      <text x="180" y="130" font-size="10" fill="#047857" text-anchor="middle">"Got the time?"</text>

      <line x1="280" y1="155" x2="80" y2="175" stroke="#10b981" stroke-width="2"/>
      <text x="180" y="160" font-size="10" fill="#047857" text-anchor="middle">"2:00"</text>

      <!-- Center Divider -->
      <line x1="380" y1="20" x2="380" y2="210" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="4 4"/>

      <!-- Right side: Network Protocol -->
      <text x="570" y="25" font-size="12" font-weight="700" fill="#7c3aed" text-anchor="middle">Network Protocol (TCP Connection)</text>
      <line x1="470" y1="40" x2="470" y2="200" stroke="#94a3b8" stroke-width="2"/>
      <line x1="670" y1="40" x2="670" y2="200" stroke="#94a3b8" stroke-width="2"/>
      <text x="470" y="38" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Client</text>
      <text x="670" y="38" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Server</text>

      <line x1="470" y1="65" x2="670" y2="85" stroke="#8b5cf6" stroke-width="2"/>
      <text x="570" y="70" font-size="10" fill="#6d28d9" text-anchor="middle">TCP SYN (req_conn)</text>

      <line x1="670" y1="95" x2="470" y2="115" stroke="#8b5cf6" stroke-width="2"/>
      <text x="570" y="100" font-size="10" fill="#6d28d9" text-anchor="middle">TCP SYN-ACK (ack_conn)</text>

      <line x1="470" y1="125" x2="670" y2="145" stroke="#10b981" stroke-width="2"/>
      <text x="570" y="130" font-size="10" fill="#047857" text-anchor="middle">HTTP GET /index.html</text>

      <line x1="670" y1="155" x2="470" y2="175" stroke="#10b981" stroke-width="2"/>
      <text x="570" y="160" font-size="10" fill="#047857" text-anchor="middle">HTTP 200 OK &lt;data&gt;</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 1.2 — A human protocol vs a computer network protocol exchange (§1.1.2).</div>
</div>
""",
            "quiz": [
                {
                    "q": "What are the three essential components of a protocol definition according to Kurose & Ross?",
                    "opts": [
                        "Bandwidth, latency, and packet loss",
                        "Format of messages, order of messages, and actions taken upon transmission/receipt",
                        "IP addresses, MAC addresses, and port numbers",
                        "Encryption, compression, and error correction"
                    ],
                    "ans": 1,
                    "exp": "A protocol defines the format, the order of messages exchanged between two or more communicating entities, and the actions taken on the transmission and/or receipt of a message or other event (§1.1.2)."
                },
                {
                    "q": "Which of the following devices is classified as an End System (Host)?",
                    "opts": [
                        "Link-layer switch",
                        "Core backbone router",
                        "Smartphone streaming video",
                        "Fiber-optic repeater"
                    ],
                    "ans": 2,
                    "exp": "End systems sit at the network edge and run applications (PCs, phones, webcams, servers). Switches and routers are packet switches in the network core (§1.1.1)."
                }
            ]
        },
        {
            "id": "ch1-2",
            "num": "1.2",
            "title": "The Network Edge: Access Networks & Physical Media",
            "subtitle": "DSL, Cable HFC, FTTH, Enterprise/Home networks, Wireless, and Transmission Media",
            "content": r"""
<p>The <strong>network edge</strong> consists of end systems that initiate and terminate data. An <strong>access network</strong> physically connects an end system to the first router (the <strong>edge router</strong>) on the path to any other end system.</p>

<h3>1.2.1 Access Networks Comparison</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.88rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px 10px;">Access Technology</th>
      <th style="padding:8px 10px;">Physical Medium</th>
      <th style="padding:8px 10px;">Architecture & Medium Type</th>
      <th style="padding:8px 10px;">Typical Bandwidth</th>
      <th style="padding:8px 10px;">Key Characteristics</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">DSL (Digital Subscriber Line)</td>
      <td style="padding:8px 10px;">Telephone copper twisted pair</td>
      <td style="padding:8px 10px; color:var(--primary-text); font-weight:600;">Dedicated line to CO</td>
      <td style="padding:8px 10px;">Up to 24–52 Mbps down, 3.5–16 Mbps up</td>
      <td style="padding:8px 10px;">Uses FDM over copper: 0–4 kHz voice, 4–50 kHz upstream data, 50 kHz–1 MHz downstream data. Splitter separates voice/data at home; DSLAM multiplexes at Telco Central Office (CO). Speed independent of neighbors.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">Cable Internet (HFC)</td>
      <td style="padding:8px 10px;">Fiber to neighborhood + Coaxial to homes</td>
      <td style="padding:8px 10px; color:var(--warning-text); font-weight:600;">Shared broadcast medium</td>
      <td style="padding:8px 10px;">Up to 1.2 Gbps down, 30–100 Mbps up (DOCSIS 3.1)</td>
      <td style="padding:8px 10px;">Hybrid Fiber-Coaxial (HFC). Cable Modem Termination System (CMTS) at cable headend. <strong>Shared medium:</strong> multiple homes share the coaxial channel; heavy neighborhood downloads reduce available throughput.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">FTTH (Fiber to the Home)</td>
      <td style="padding:8px 10px;">Optical fiber</td>
      <td style="padding:8px 10px; color:var(--accent-text); font-weight:600;">Dedicated optical fiber</td>
      <td style="padding:8px 10px;">1 Gbps – 10 Gbps symmetric</td>
      <td style="padding:8px 10px;">Two architectures: AON (Active Optical Network, switched Ethernet) and <strong>PON (Passive Optical Network)</strong>. PON uses an Optical Line Terminator (OLT) at CO, passive unpowered optical splitters in the neighborhood, and an Optical Network Terminator (ONT) at each home.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">Enterprise LAN (Ethernet & WiFi)</td>
      <td style="padding:8px 10px;">Cat 5e/6 UTP copper + 2.4/5 GHz radio</td>
      <td style="padding:8px 10px;">Star topology to Ethernet switch</td>
      <td style="padding:8px 10px;">100 Mbps, 1 Gbps, 10 Gbps wired; 100–1000 Mbps WiFi</td>
      <td style="padding:8px 10px;">Hosts connect to an Ethernet switch via twisted pair. Wireless laptops and phones connect to an Access Point (AP) which wires into the enterprise switch.</td>
    </tr>
    <tr>
      <td style="padding:8px 10px; font-weight:700;">Wide-Area Wireless (Cellular 4G/5G)</td>
      <td style="padding:8px 10px;">Electromagnetic radio spectrum</td>
      <td style="padding:8px 10px;">Cellular tower base stations</td>
      <td style="padding:8px 10px;">10–100 Mbps (4G LTE), 100 Mbps–1 Gbps (5G)</td>
      <td style="padding:8px 10px;">Connects mobile devices within tens of kilometers to cellular base stations operated by telecommunication providers.</td>
    </tr>
  </tbody>
</table>

<div class="callout callout-exam">
  <div class="callout-header">🎯 Exam Focus: Home Network Architecture</div>
  A typical home network connects multiple devices through a single integrated device (the "home router/combo box") that combines:
  <ol>
    <li>An <strong>802.11 Wireless Access Point (AP)</strong> for wireless phones and laptops.</li>
    <li>A <strong>100 Mbps / 1 Gbps Ethernet Switch</strong> for wired devices (TVs, desktop PCs).</li>
    <li>A <strong>Network Router</strong> implementing IP forwarding and NAT (Network Address Translation) to share a single public IP.</li>
    <li>A <strong>Cable Modem or DSL Modem</strong> converting digital packets into analog signals on the access medium.</li>
  </ol>
</div>

<h3>1.2.2 Physical Transmission Media</h3>
<p>Bits travel across a physical medium as electromagnetic waves or optical pulses. Media are classified into two broad categories:</p>

<div class="grid-2">
  <div class="interactive-card" style="margin:0;">
    <div style="font-weight:700; color:var(--primary-text); margin-bottom:0.5rem;">📡 Guided Media (Signals wave-guided in solid medium)</div>
    <ul style="font-size:0.85rem; line-height:1.6; margin:0; padding-left:1.2rem;">
      <li><strong>Unshielded Twisted Pair (UTP):</strong> Two insulated copper wires twisted together to reduce electromagnetic interference. Cat 5e (100 Mbps / 1 Gbps up to 100m), Cat 6/6a (10 Gbps). Most prevalent in LANs.</li>
      <li><strong>Coaxial Cable:</strong> Concentric copper conductors separated by insulation. Offers higher data rates than twisted pair, used in cable TV networks and HFC broadband. Can function as a shared broadcast medium.</li>
      <li><strong>Fiber Optic Cable:</strong> Thin flexible strands of glass that conduct pulses of light (photons). Extremely high bandwidth (tens to hundreds of Gbps), low attenuation over tens of kilometers, and <strong>immune to electromagnetic interference</strong>. The backbone of core and transoceanic links.</li>
    </ul>
  </div>

  <div class="interactive-card" style="margin:0;">
    <div style="font-weight:700; color:var(--primary-text); margin-bottom:0.5rem;">📻 Unguided Media (Signals propagate freely through atmosphere/outer space)</div>
    <ul style="font-size:0.85rem; line-height:1.6; margin:0; padding-left:1.2rem;">
      <li><strong>Terrestrial Radio:</strong> Electromagnetic spectrum carrying signals via line-of-sight or reflection. Subject to path loss, multipath fading, and interference (WiFi 802.11, cellular 4G/5G, Bluetooth).</li>
      <li><strong>Satellite Radio:</strong> Relays signals between terrestrial ground stations:
        <ul>
          <li><strong>Geostationary (GEO):</strong> Orbit at 36,000 km above equator. Stationary relative to Earth. Round-trip propagation delay is substantial (~280 ms one-way, ~560 ms round-trip).</li>
          <li><strong>Low Earth Orbit (LEO):</strong> Orbit at 500–1,500 km (e.g. Starlink). Much lower propagation delay (~10–30 ms) but constellations require hundreds of satellites because they move rapidly across the sky.</li>
        </ul>
      </li>
    </ul>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "Why does high neighborhood network activity degrade download speeds on Cable Internet (HFC) but not on DSL?",
                    "opts": [
                        "DSL uses fiber-optic cables whereas Cable Internet uses copper twisted pairs",
                        "Cable Internet is a shared broadcast coaxial medium among neighborhood homes, whereas DSL provides a dedicated local loop to the telco Central Office",
                        "DSL operates at Layer 3 while Cable operates at Layer 1",
                        "Cable modems do not perform store-and-forward transmission"
                    ],
                    "ans": 1,
                    "exp": "On an HFC cable network, multiple residences share the same coaxial cable trunk back to the fiber node. In contrast, DSL gives each subscriber an individual, dedicated copper pair to the Central Office (§1.2.1)."
                },
                {
                    "q": "Which transmission medium is completely immune to electromagnetic interference (EMI)?",
                    "opts": [
                        "Category 6 UTP copper",
                        "Coaxial cable",
                        "Optical fiber",
                        "Terrestrial microwave radio"
                    ],
                    "ans": 2,
                    "exp": "Optical fiber transmits light pulses (photons) through silica glass and is completely immune to electromagnetic interference, electrical noise, and cross-talk (§1.2.2)."
                }
            ]
        },
        {
            "id": "ch1-3",
            "num": "1.3",
            "title": "The Network Core: Packet Switching & Circuit Switching",
            "subtitle": "Store-and-forward, queuing delay, FDM vs TDM, and the hierarchical network of networks",
            "content": r"""
<p>The <strong>network core</strong> is the interconnected mesh of packet switches and communication links that transports data between end systems. There are two fundamental architectural paradigms for transporting data through a network of links and switches:</p>

<h3>1.3.1 Packet Switching</h3>
<p>End systems segment long messages into smaller chunks called <strong>packets</strong> of length <span class="math-inline">L</span> bits. Each packet is transmitted across a communication link of transmission rate <span class="math-inline">R</span> bits/second.</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Definition: Store-and-Forward Transmission</div>
  Most packet switches use <strong>store-and-forward transmission</strong> at link inputs. A switch must receive the <em>entire packet</em> (all <span class="math-inline">L</span> bits) before it can begin transmitting the first bit onto the outbound link.
</div>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Store-and-Forward Transmission Delay Equations</div>
  Transmitting 1 packet of <span class="math-inline">L</span> bits across a path of <span class="math-inline">N</span> identical links of rate <span class="math-inline">R</span> (separated by <span class="math-inline">N - 1</span> routers, ignoring propagation/processing):
  <div class="math-display">
    d_{\text{end-to-end}} = N \cdot \frac{L}{R}
  </div>
  Transmitting <span class="math-inline">P</span> packets back-to-back across <span class="math-inline">N</span> links in a pipelined fashion:
  <div class="math-display">
    d_{\text{total}} = (N + P - 1) \cdot \frac{L}{R}
  </div>
</div>

<!-- EMBEDDED INTERACTIVE: STORE-AND-FORWARD PIPELINE -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">⚡ Interactive Store-and-Forward Pipeline Simulator</div>
    <span class="interactive-badge">P3 Pipeline Trace</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Observe how <span class="math-inline">P = 3</span> packets traverse <span class="math-inline">N = 2</span> links separated by 1 router. Notice how packet pipelining allows link 1 and link 2 to transmit simultaneously!
  </p>
  <div class="sim-viewport">
    <svg viewBox="0 0 720 140" style="width:100%; max-width:700px;">
      <!-- Sender A -->
      <rect x="20" y="40" width="90" height="50" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="65" y="70" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Sender Host</text>
      <!-- Link 1 -->
      <line x1="110" y1="65" x2="300" y2="65" stroke="#94a3b8" stroke-width="4"/>
      <text x="205" y="55" font-size="9" fill="#64748b" text-anchor="middle">Link 1 (Rate R = 1 Mbps)</text>
      <!-- Router -->
      <circle cx="330" cy="65" r="28" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
      <text x="330" y="69" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Router</text>
      <!-- Link 2 -->
      <line x1="360" y1="65" x2="560" y2="65" stroke="#94a3b8" stroke-width="4"/>
      <text x="460" y="55" font-size="9" fill="#64748b" text-anchor="middle">Link 2 (Rate R = 1 Mbps)</text>
      <!-- Receiver B -->
      <rect x="560" y="40" width="90" height="50" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="605" y="70" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Receiver Host</text>

      <!-- Packets State Badges -->
      <g transform="translate(140, 95)">
        <rect id="sec1-sf-p1" x="0" y="0" width="80" height="26" rx="4" fill="var(--bg-secondary)" stroke="var(--border)"/>
        <text x="40" y="17" font-size="9.5" font-weight="600" fill="var(--text-primary)" text-anchor="middle">Packet 1</text>
      </g>
      <g transform="translate(240, 95)">
        <rect id="sec1-sf-p2" x="0" y="0" width="80" height="26" rx="4" fill="var(--bg-secondary)" stroke="var(--border)"/>
        <text x="40" y="17" font-size="9.5" font-weight="600" fill="var(--text-primary)" text-anchor="middle">Packet 2</text>
      </g>
      <g transform="translate(340, 95)">
        <rect id="sec1-sf-p3" x="0" y="0" width="80" height="26" rx="4" fill="var(--bg-secondary)" stroke="var(--border)"/>
        <text x="40" y="17" font-size="9.5" font-weight="600" fill="var(--text-primary)" text-anchor="middle">Packet 3</text>
      </g>
    </svg>
    <div id="sec1-sf-status" style="font-size:0.88rem; font-weight:600; color:var(--primary-text); margin-top:0.75rem; min-height:1.4rem;">
      Ready. Click 'Next Pipeline Step' to step through transmission.
    </div>
  </div>
  <div class="sim-controls">
    <button class="btn-primary" onclick="stepSec1SF()">⏭ Next Pipeline Step</button>
    <button class="btn-secondary" onclick="resetSec1SF()">🔄 Reset</button>
  </div>
</div>

<h3>Queuing Delay and Packet Loss</h3>
<p>Each packet switch has multiple links. For each link, the switch maintains an <strong>output buffer</strong> (also called an output queue). If a packet arrives when the outbound link is busy transmitting another packet, the newly arrived packet must wait in the output buffer (<strong>queuing delay</strong>). If the buffer memory becomes completely full, newly arriving packets have nowhere to be stored and are dropped (<strong>packet loss</strong>).</p>

<h3>Forwarding vs Routing</h3>
<ul>
  <li><strong>Forwarding (Data Plane):</strong> The router's local hardware action of transferring a packet from an input link interface to the appropriate output link interface based on inspecting the packet's destination header and looking up the <strong>forwarding table</strong>. Occurs in nanoseconds.</li>
  <li><strong>Routing (Control Plane):</strong> The network-wide collaborative process that determines the end-to-end paths packets take from source to destination. Routers execute <strong>routing protocols</strong> (e.g. OSPF, BGP) to compute the values placed into forwarding tables. Occurs in seconds/minutes.</li>
</ul>

<h3>1.3.2 Circuit Switching: FDM vs TDM</h3>
<p>In <strong>circuit-switched networks</strong> (e.g. traditional telephone networks), the resources needed along a path (buffers, link transmission rate) are <em>reserved</em> for the duration of the communication session. Dedicated transmission rate is guaranteed; no queuing delay occurs once connected.</p>
<ul>
  <li><strong>Frequency-Division Multiplexing (FDM):</strong> The frequency spectrum of a link is divided among connections; each circuit receives a dedicated frequency band continuously.</li>
  <li><strong>Time-Division Multiplexing (TDM):</strong> Time is divided into recurring frames of fixed duration, each frame split into a fixed number of time slots. Each connection receives a dedicated time slot in each recurring frame.</li>
</ul>

<div class="callout callout-exam">
  <div class="callout-header">🎯 Classic Exam Calculation: Packet Switching vs Circuit Switching Capacity</div>
  Suppose users share a <strong>1 Mbps link</strong>, and each user generates <strong>100 kbps</strong> when transmitting, but is active only <strong>10% of the time</strong> (<span class="math-inline">p = 0.10</span>).
  <ul>
    <li><strong>Circuit switching:</strong> Link capacity is partitioned into fixed 100 kbps slots:
      <div class="math-display">\text{Max Users} = \frac{1000\text{ kbps}}{100\text{ kbps}} = \mathbf{10\text{ users}}</div>
      It can support at most 10 simultaneous users, even if all 10 are completely idle 90% of the time!
    </li>
    <li><strong>Packet switching:</strong> With <strong>35 users</strong>, the probability that 11 or more users transmit simultaneously (causing queuing) is computed by the binomial distribution:
      <div class="math-display">
        P(X \ge 11) = \sum_{k=11}^{35} \binom{35}{k} (0.10)^k (0.90)^{35-k} \approx \mathbf{0.0004} \ (0.04\%)
      </div>
      Packet switching supports <strong>3.5× more users</strong> with less than a 0.04% probability of experiencing any queuing delay!
    </li>
  </ul>
</div>

<h3>1.3.3 A Network of Networks: The Internet ISP Hierarchy</h3>
<p>End systems connect to access ISPs. How do access ISPs connect to one another? The global Internet is structured as a five-tier hierarchy:</p>
<ol>
  <li><strong>Access ISPs:</strong> Local and regional cable, DSL, or cellular companies connecting residential homes and enterprises.</li>
  <li><strong>Regional ISPs:</strong> Intermediate networks connecting access ISPs to large backbone transit providers.</li>
  <li><strong>Tier-1 ISPs:</strong> Global commercial transit backbones (e.g. AT&T, Lumen/Level 3, NTT, Verizon) that span continents with high-speed fiber trunks. Tier-1 ISPs connect directly to every other Tier-1 ISP without paying transit fees (peering).</li>
  <li><strong>Points of Presence (PoPs):</strong> A group of routers in an ISP's network where customer ISPs can connect into the provider ISP.</li>
  <li><strong>Multi-Homing:</strong> An ISP or enterprise connects to two or more provider ISPs to guarantee connectivity if one provider fails.</li>
  <li><strong>Internet Exchange Points (IXPs):</strong> Third-party meeting points with high-speed switches where multiple ISPs peer directly with each other to exchange traffic free of transit charges.</li>
  <li><strong>Content Provider Networks (e.g. Google, Akamai, Microsoft):</strong> Private networks that bypass the commercial public Internet by connecting their own private data centers directly to lower-tier ISPs via IXPs and peering.</li>
</ol>
""",
            "quiz": [
                {
                    "q": "What is the primary difference between routing and forwarding in a router?",
                    "opts": [
                        "Routing uses hardware while forwarding uses software",
                        "Forwarding is the router's local action of transferring a packet from input to output interface; routing is the network-wide process that determines end-to-end paths",
                        "Routing is used in circuit switching while forwarding is used in packet switching",
                        "Forwarding happens over minutes while routing happens in nanoseconds"
                    ],
                    "ans": 1,
                    "exp": "Forwarding is the data-plane action of moving a packet from input port to output port using the forwarding table. Routing is the control-plane process that computes the paths and populates the table (§1.3.1)."
                },
                {
                    "q": "A 2.048 Mbps link uses TDM with 32 slots. At what dedicated transmission rate does each circuit transmit?",
                    "opts": [
                        "32 kbps",
                        "64 kbps",
                        "128 kbps",
                        "2048 kbps"
                    ],
                    "ans": 1,
                    "exp": "Rate per circuit = Link rate / Number of slots = 2.048 Mbps / 32 = 2048 kbps / 32 = 64 kbps (§1.3.2 / P7)."
                }
            ]
        },
        {
            "id": "ch1-4",
            "num": "1.4",
            "title": "Delay, Loss, and Throughput in Packet Networks",
            "subtitle": "The 4 components of nodal delay, the Caravan Analogy, queuing intensity, and bottleneck links",
            "content": r"""
<p>As a packet travels from source to destination across a network, it encounters four distinct delay components at every single node:</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Total Nodal Delay Equation (§1.4.1)</div>
  <div class="math-display">
    d_{\text{nodal}} = d_{\text{proc}} + d_{\text{queue}} + d_{\text{trans}} + d_{\text{prop}}
  </div>
  <ul>
    <li><strong>Processing Delay (<span class="math-inline">d_{\text{proc}}</span>):</strong> Time required by the router processor to examine the packet header, check for bit-level errors using checksums, and look up the forwarding table. Typically microseconds (<span class="math-inline">\mu\text{s}</span>).</li>
    <li><strong>Queuing Delay (<span class="math-inline">d_{\text{queue}}</span>):</strong> Time the packet waits in the output buffer queue before transmission begins. Depends on traffic intensity and preceding packets. Ranges from microseconds to hundreds of milliseconds.</li>
    <li><strong>Transmission Delay (<span class="math-inline">d_{\text{trans}} = \frac{L}{R}</span>):</strong> Time required to push all <span class="math-inline">L</span> bits of the packet onto the physical link at transmission rate <span class="math-inline">R</span> bps. Depends strictly on packet size <span class="math-inline">L</span> and link rate <span class="math-inline">R</span> (independent of distance!).</li>
    <li><strong>Propagation Delay (<span class="math-inline">d_{\text{prop}} = \frac{d}{s}</span>):</strong> Time required for a single physical bit to propagate across the physical medium of distance <span class="math-inline">d</span> meters at propagation speed <span class="math-inline">s</span> (<span class="math-inline">s \approx 2 \times 10^8\text{ m/s}</span> in fiber/copper, <span class="math-inline">3 \times 10^8\text{ m/s}</span> in free space). Depends strictly on distance and physical speed of light (independent of packet size or link bandwidth!).</li>
  </ul>
</div>

<div class="callout callout-def">
  <div class="callout-header">📏 Networking Units & Conversion Rules (Study Guide Page 20)</div>
  <ul>
    <li><strong>Data Size vs Rates:</strong> In networking, prefixes are powers of 10: <span class="math-inline">1\text{ Kbps} = 10^3\text{ bps}</span>, <span class="math-inline">1\text{ Mbps} = 10^6\text{ bps}</span>, <span class="math-inline">1\text{ Gbps} = 10^9\text{ bps}</span>.</li>
    <li><strong>Bytes to Bits:</strong> Always multiply by 8! <span class="math-inline">1\text{ Byte} = 8\text{ bits}</span>; <span class="math-inline">1\text{ MB} = 10^6\text{ Bytes} = 8 \times 10^6\text{ bits}</span>.</li>
    <li><strong>Time Units:</strong> <span class="math-inline">1\text{ s} = 1,000\text{ ms} = 1,000,000\ \mu\text{s}</span>; <span class="math-inline">1\text{ ms} = 10^{-3}\text{ s}</span>; <span class="math-inline">1\ \mu\text{s} = 10^{-6}\text{ s}</span>.</li>
    <li><strong>Distance Units:</strong> Convert km to meters before dividing by <span class="math-inline">s</span>: <span class="math-inline">d = 4,000\text{ km} = 4 \times 10^6\text{ m}</span>.</li>
  </ul>
</div>

<div class="callout callout-insight">
  <div class="callout-header">💡 The Tollbooth Caravan Analogy (Kurose & Ross §1.4.1 / Study Guide P4)</div>
  To intuitively differentiate transmission delay from propagation delay, consider a caravan of cars passing through highway tollbooths separated by a long highway:
  <ul>
    <li><strong>Cars = Bits; Caravan = Packet; Tollbooth service rate = Link transmission rate (<span class="math-inline">R</span>); Highway = Link physical medium; Speed of car = Propagation speed (<span class="math-inline">s</span>).</strong></li>
  </ul>
  <strong>Scenario 1 (Study Guide P4a):</strong> 8-car caravan, tollbooths 150 km apart. Each booth needs 15 s per car, cars travel at 100 km/h.
  <ul>
    <li>Time to push all 8 cars through first booth (<span class="math-inline">d_{\text{trans}}</span>): <span class="math-inline">8 \times 15\text{ s} = 120\text{ s} = \mathbf{2\text{ minutes}}</span>.</li>
    <li>Time for the last car to travel 150 km at 100 km/h (<span class="math-inline">d_{\text{prop}}</span>): <span class="math-inline">150 / 100 = 1.5\text{ hours} = \mathbf{90\text{ minutes}}</span>.</li>
    <li>Total time for entire caravan to line up before booth 2: <span class="math-inline">2\text{ min} + 90\text{ min} = \mathbf{92\text{ minutes}}</span>.</li>
  </ul>
  <strong>Scenario 2 (Study Guide P4b - Superfast Cars):</strong> Cars travel at 1,000 km/h and a booth needs 1 minute per car.
  <ul>
    <li>First car leaves booth 1 at <span class="math-inline">t = 1\text{ minute}</span>. Travel time to booth 2 = <span class="math-inline">150 / 1000\text{ h} = 0.15\text{ h} = 9\text{ minutes}</span>. First car arrives at booth 2 at <span class="math-inline">t = 1 + 9 = \mathbf{10\text{ minutes}}</span>.</li>
    <li>Meanwhile, the 8th car leaves booth 1 at <span class="math-inline">t = 8 \times 1 = \mathbf{8\text{ minutes}}</span>.</li>
    <li><em>Does the first car reach booth 2 before the last car leaves booth 1?</em> <strong>No!</strong> All 8 cars have cleared booth 1 at minute 8, well before the first car arrives at booth 2 at minute 10!</li>
  </ul>
</div>

<!-- EMBEDDED INTERACTIVE: LIVE NODAL DELAY CALCULATOR -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🧮 Interactive Nodal Delay Breakdown Calculator</div>
    <span class="interactive-badge">Live Math & Slider</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Adjust the parameters to compute <span class="math-inline">d_{\text{trans}}</span>, <span class="math-inline">d_{\text{prop}}</span>, and total nodal delay in real time:
  </p>
  <div class="grid-3">
    <div class="form-group">
      <label class="form-label">Processing Delay (<span id="sec1-dproc-val">5 ms</span>):</label>
      <input type="range" id="sec1-dproc" min="0" max="50" value="5" step="1" oninput="calcSec1Delay()">
    </div>
    <div class="form-group">
      <label class="form-label">Queuing Delay (<span id="sec1-dqueue-val">10 ms</span>):</label>
      <input type="range" id="sec1-dqueue" min="0" max="100" value="10" step="1" oninput="calcSec1Delay()">
    </div>
    <div class="form-group">
      <label class="form-label">Packet Size L (<span id="sec1-pktlen-val">1,500 Bytes (12,000 bits)</span>):</label>
      <input type="range" id="sec1-pktlen" min="500" max="64000" value="12000" step="500" oninput="calcSec1Delay()">
    </div>
    <div class="form-group">
      <label class="form-label">Link Rate R (<span id="sec1-rate-val">100 Mbps</span>):</label>
      <input type="range" id="sec1-rate" min="1" max="1000" value="100" step="5" oninput="calcSec1Delay()">
    </div>
    <div class="form-group">
      <label class="form-label">Distance d (<span id="sec1-dist-val">1,000 km</span>):</label>
      <input type="range" id="sec1-dist" min="1" max="20000" value="1000" step="100" oninput="calcSec1Delay()">
    </div>
    <div class="form-group">
      <label class="form-label">Prop Speed s (<span id="sec1-propspeed-val">200,000 km/s</span>):</label>
      <input type="range" id="sec1-propspeed" min="100000" max="300000" value="200000" step="10000" oninput="calcSec1Delay()">
    </div>
  </div>
  <div id="sec1-delay-output" class="calc-result-box" style="margin-top:1rem;">
    <!-- Populated live by calcSec1Delay() -->
  </div>
</div>

<h3>Queuing Delay and Traffic Intensity (<span class="math-inline">\frac{L \cdot a}{R}</span>)</h3>
<p>Let <span class="math-inline">a</span> denote the average packet arrival rate (packets/second), <span class="math-inline">L</span> the packet length in bits, and <span class="math-inline">R</span> the transmission rate in bps. The dimensionless ratio:</p>
<div class="math-display">
  \text{Traffic Intensity} = \frac{L \cdot a}{R}
</div>
<ul>
  <li>If <span class="math-inline">\frac{La}{R} \approx 0</span>: Packets arrive rarely; average queuing delay is practically zero.</li>
  <li>As <span class="math-inline">\frac{La}{R} \to 1</span>: Packets arrive in bursts faster than the link can drain them; queuing delay increases exponentially.</li>
  <li>If <span class="math-inline">\frac{La}{R} > 1</span>: More bits arrive per second than the link can transmit. The queue grows without bound and <strong>packets are dropped (lost)</strong> when the router buffer overflows!</li>
</ul>

<h3>End-to-End Delay and <code>traceroute</code></h3>
<p>The program <code>traceroute</code> maps the route packets take between two Internet hosts:</p>
<ol>
  <li>The source sends 3 UDP or ICMP probes with <span class="math-inline">\text{TTL} = 1</span>. The first router decrements TTL to 0, drops the packet, and returns an <code>ICMP Time Exceeded</code> message (Type 11, Code 0) containing its IP address.</li>
  <li>The source records the round-trip time (RTT) for all 3 probes.</li>
  <li>The source increments TTL to 2, 3, 4, ... repeating the process until the destination host receives the probe and replies with <code>ICMP Port Unreachable</code> (Type 3, Code 3).</li>
  <li><em>Why can delay decrease between consecutive hops in traceroute?</em> Internet routing is dynamic (probes take different paths), or intermediate routers deprioritize ICMP generation!</li>
</ol>

<h3>Throughput and Bottleneck Link</h3>
<p><strong>Throughput</strong> is the rate (in bits/sec) at which bits are delivered to the destination. For an end-to-end path with server link <span class="math-inline">R_s</span> and client link <span class="math-inline">R_c</span>:</p>
<div class="math-display">
  \text{Throughput} = \min(R_s, R_c)
</div>
<p>The link on the end-to-end path that constrains the end-to-end throughput is called the <strong>bottleneck link</strong>. When <span class="math-inline">N</span> flows share a core link of capacity <span class="math-inline">R</span>:</p>
<div class="math-display">
  \text{Throughput} = \min\left(R_s, R_c, \frac{R}{N}\right)
</div>
""",
            "quiz": [
                {
                    "q": "A packet of size L = 1,000 Bytes is sent over a 20 Mbps link that is 4,000 km long (speed s = 2 * 10^8 m/s). Which delay dominates?",
                    "opts": [
                        "Transmission delay dominates (20 ms vs 0.4 ms)",
                        "Propagation delay dominates (d_prop = 20 ms vs d_trans = 0.4 ms)",
                        "Both delays are equal at 2 ms",
                        "Processing delay dominates"
                    ],
                    "ans": 1,
                    "exp": "d_trans = (1000 * 8) / (20 * 10^6) = 0.4 ms. d_prop = (4 * 10^6 m) / (2 * 10^8 m/s) = 0.02 s = 20 ms. Propagation delay is 50 times larger and completely dominates (§1.4 / P2)."
                },
                {
                    "q": "Packets of 500 Bytes arrive at an average rate of 300 packets/sec at a 1 Mbps router link. What is the traffic intensity?",
                    "opts": [
                        "0.15",
                        "0.60",
                        "1.20 (unstable, buffer overflows and packets lost)",
                        "1.50"
                    ],
                    "ans": 2,
                    "exp": "La / R = (500 * 8 * 300) / 1,000,000 = 1,200,000 / 1,000,000 = 1.2 > 1. Because intensity > 1, the queue grows infinitely and packets are lost (§1.4 / P5)."
                }
            ]
        },
        {
            "id": "ch1-5",
            "num": "1.5",
            "title": "Protocol Layers and Their Service Models",
            "subtitle": "The 5-layer Internet stack, 7-layer OSI model, and packet encapsulation",
            "content": r"""
<p>Computer networks are exceedingly complex, comprising billions of diverse hosts, switches, copper/fiber/radio links, applications, and operating systems. To manage this complexity, network designers organize communication protocols into <strong>layers</strong>.</p>

<div class="callout callout-insight">
  <div class="callout-header">✈️ The Airline Travel Analogy (Kurose & Ross §1.5)</div>
  Consider taking an international commercial flight:
  <ol>
    <li><strong>Ticket purchase:</strong> Ticket counter / online booking.</li>
    <li><strong>Baggage check:</strong> Checked baggage handlers.</li>
    <li><strong>Boarding gate:</strong> Boarding pass scan & gate departure.</li>
    <li><strong>Runway takeoff:</strong> Air traffic control runway clearance.</li>
    <li><strong>Airplane routing:</strong> Aircraft en route to destination.</li>
  </ol>
  Each step performs an action and relies on the layer beneath it. If the airline upgrades its baggage barcode system, it does not require changing how air traffic control directs airplanes! Modularity allows updates without system-wide rewrites.
</div>

<h3>The 5-Layer Internet Protocol Stack</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.88rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px 10px;">Layer</th>
      <th style="padding:8px 10px;">Packet Name (PDU)</th>
      <th style="padding:8px 10px;">Primary Function</th>
      <th style="padding:8px 10px;">Example Protocols</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700; color:var(--layer-app);">5. Application</td>
      <td style="padding:8px 10px; font-weight:700;">Message</td>
      <td style="padding:8px 10px;">Supports network applications; exchange of user messages between end systems</td>
      <td style="padding:8px 10px;">HTTP, SMTP, IMAP, DNS, FTP, BitTorrent</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700; color:var(--layer-trans);">4. Transport</td>
      <td style="padding:8px 10px; font-weight:700;">Segment</td>
      <td style="padding:8px 10px;">Process-to-process data delivery, multiplexing/demultiplexing, reliability, flow/congestion control</td>
      <td style="padding:8px 10px;">TCP, UDP</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700; color:var(--layer-net);">3. Network</td>
      <td style="padding:8px 10px; font-weight:700;">Datagram</td>
      <td style="padding:8px 10px;">Routing datagrams from source host to destination host across network core</td>
      <td style="padding:8px 10px;">IP (IPv4, IPv6), OSPF, BGP, ICMP</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700; color:var(--layer-link);">2. Link</td>
      <td style="padding:8px 10px; font-weight:700;">Frame</td>
      <td style="padding:8px 10px;">Data transfer between neighboring network elements over a single communication link</td>
      <td style="padding:8px 10px;">Ethernet (802.3), WiFi (802.11), PPP, DOCSIS</td>
    </tr>
    <tr>
      <td style="padding:8px 10px; font-weight:700; color:var(--layer-phy);">1. Physical</td>
      <td style="padding:8px 10px; font-weight:700;">Bits</td>
      <td style="padding:8px 10px;">Modulates bits onto electromagnetic or optical transmission media</td>
      <td style="padding:8px 10px;">1000BASE-T, DSL, 802.11a/b/g/n/ac PHY</td>
    </tr>
  </tbody>
</table>

<div class="callout callout-def">
  <div class="callout-header">📘 The 7-Layer ISO OSI Reference Model vs 5-Layer Internet Stack</div>
  In the late 1970s, ISO proposed the 7-Layer Open Systems Interconnection (OSI) model. It introduced two additional layers between Application and Transport:
  <ul>
    <li><strong>Presentation Layer (Layer 6):</strong> Interprets the meaning of exchanged data (data compression, encryption, character conversion like ASCII/EBCDIC).</li>
    <li><strong>Session Layer (Layer 5):</strong> Delimiting and synchronization of data exchanges, checkpointing, and recovery.</li>
  </ul>
  <em>Why does the Internet not have Presentation and Session layers?</em> In the Internet architecture, these services are implemented directly inside the <strong>Application layer</strong> by application developers if needed (e.g. TLS encryption in HTTPS)!
</div>

<h3>Packet Encapsulation and Device Layering</h3>
<p>As data moves down the protocol stack at the sending host, each layer adds its own protocol header (and sometimes a trailer) to the data received from the layer above:</p>
<div class="math-display">
  \text{Message } M \xrightarrow{+\ H_t} \text{Segment } (H_t + M) \xrightarrow{+\ H_n} \text{Datagram } (H_n + H_t + M) \xrightarrow{+\ H_l,\ T_l} \text{Frame } (H_l + H_n + H_t + M + T_l)
</div>

<!-- EMBEDDED INTERACTIVE: ENCAPSULATION / DECAPSULATION STEPPER -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📦 Interactive Protocol Encapsulation & Decapsulation</div>
    <span class="interactive-badge">Step-Through Animator</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Observe how headers are prepended on the way down the stack at the sender, and stripped away at the receiver:
  </p>
  <div id="sec1-encap-visual" style="background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:1.25rem; min-height:85px; display:flex; align-items:center; justify-content:center;">
    <!-- Rendered dynamically -->
  </div>
  <div style="margin-top:0.75rem; text-align:center;">
    <div id="sec1-encap-layer" style="font-weight:700; color:var(--primary-text); font-size:1rem;">1. Application Layer (Message M)</div>
    <div id="sec1-encap-info" style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.25rem;">
      The user application creates raw application data (e.g. an HTTP GET request message). PDU: Message.
    </div>
  </div>
  <div class="fig-controls" style="margin-top:1rem;">
    <button class="btn-primary" onclick="stepEncapDown()">⬇ Encapsulate (Move Down Stack)</button>
    <button class="btn-secondary" onclick="stepEncapUp()">⬆ Decapsulate (Move Up Stack)</button>
    <button class="btn-secondary" onclick="resetEncap()">🔄 Reset</button>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "Which layers are implemented in an intermediate packet switch: a link-layer switch vs a network core router?",
                    "opts": [
                        "Both implement all 5 layers",
                        "Link-layer switch implements layers 1 and 2 (Physical & Link); Router implements layers 1, 2, and 3 (Physical, Link, & Network)",
                        "Router implements only Layer 3; Switch implements only Layer 2",
                        "Switches implement Layer 4 while routers implement Layer 5"
                    ],
                    "ans": 1,
                    "exp": "A link-layer switch processes link and physical layers (1-2) to switch frames. A router processes physical, link, and network layers (1-3) to route datagrams (§1.5 / P8a)."
                },
                {
                    "q": "In the 5-layer Internet stack, what is the protocol data unit (PDU) at the Transport layer?",
                    "opts": [
                        "Message",
                        "Segment",
                        "Datagram",
                        "Frame"
                    ],
                    "ans": 1,
                    "exp": "Application = Message; Transport = Segment; Network = Datagram; Link = Frame; Physical = Bits (§1.5 / P8b)."
                }
            ]
        },
        {
            "id": "ch1-6",
            "num": "1.6",
            "title": "Networks Under Attack: Network Security Basics",
            "subtitle": "Malware (viruses vs worms), Denial of Service (DoS/DDoS), packet sniffing, and IP spoofing",
            "content": r"""
<p>The original ARPANET was designed among a small community of trusted academic and military researchers. As a result, mutual trust was assumed and security was omitted from the core architecture. Today, malicious actors exploit this foundational openness:</p>

<h3>1.6.1 Malware</h3>
<ul>
  <li><strong>Viruses:</strong> Malicious code that requires <strong>human user intervention</strong> to replicate and spread (e.g. opening an infected email attachment or executing a trojan program).</li>
  <li><strong>Worms:</strong> Self-replicating malware that spreads <strong>autonomously without any human action</strong>. A worm continuously scans the Internet for vulnerable hosts, injects itself into vulnerable processes over the network, and uses the newly infected hosts to scan and infect other hosts.</li>
  <li><strong>Spyware:</strong> Malware that secretly monitors user keystrokes, web browsing habits, and credentials, relaying them back to a collection server.</li>
  <li><strong>Botnets:</strong> A vast network of thousands or millions of compromised zombie hosts coordinated by a botmaster over IRC or P2P command-and-control (C&C) channels to launch coordinated attacks.</li>
</ul>

<h3>1.6.2 Denial-of-Service (DoS) and Distributed DoS (DDoS)</h3>
<p>A DoS attack renders a network, host, or service unavailable to legitimate users. Kurose & Ross categorize DoS into three types:</p>
<ol>
  <li><strong>Vulnerability Attacks:</strong> Sending a few delicately crafted malformed packets to a vulnerable application or operating system, causing the host to crash or freeze (e.g. Ping of Death).</li>
  <li><strong>Bandwidth Flooding:</strong> Flooding the victim's access link with an avalanche of bogus packets so that legitimate traffic cannot reach the server.</li>
  <li><strong>Connection Flooding:</strong> Opening thousands of half-open or fully-open TCP connections (e.g. TCP SYN flood), exhausting the victim's OS connection buffers.</li>
</ol>
<p>In a <strong>DDoS (Distributed Denial-of-Service)</strong> attack, the attacker harnesses a global botnet to blast traffic simultaneously from thousands of disparate IP addresses, making source filtering nearly impossible.</p>

<h3>1.6.3 Packet Sniffing & IP Spoofing</h3>
<ul>
  <li><strong>Packet Sniffing:</strong> A passive receiver placed on a shared broadcast medium (e.g. unencrypted WiFi, shared coaxial cable, hub Ethernet) puts its interface into <strong>promiscuous mode</strong>, recording a copy of every passing packet. Tools like Wireshark capture unencrypted passwords, credit card numbers, and emails. <em>Defense: Strong end-to-end cryptography (TLS/SSL, SSH, IPsec).</em></li>
  <li><strong>IP Spoofing:</strong> Injecting a packet into the Internet with a false, forged source IP address. The receiver believes the packet originated from the spoofed trusted host. <em>Defense: End-point authentication protocols (e.g. cryptographic nonces and digital signatures).</em></li>
</ul>
""",
            "quiz": [
                {
                    "q": "What is the critical technical distinction between a computer virus and a computer worm?",
                    "opts": [
                        "Viruses infect routers while worms infect PCs",
                        "A virus requires user intervention (e.g. executing an infected file) to replicate, whereas a worm replicates autonomously across the network without user action",
                        "Worms use encryption while viruses do not",
                        "A virus is hardware-based while a worm is software-based"
                    ],
                    "ans": 1,
                    "exp": "Viruses require user execution/interaction to propagate. Worms passively infect hosts over open network ports and replicate autonomously (§1.6 / P8c)."
                },
                {
                    "q": "Why are wireless networks and legacy shared Ethernet networks inherently vulnerable to packet sniffing?",
                    "opts": [
                        "Because packet switches drop all unencrypted packets",
                        "Because broadcast media deliver every physical signal to all nearby receivers; an interface in promiscuous mode can capture and log all passing traffic",
                        "Because IP addresses cannot be hidden",
                        "Because UDP lacks flow control"
                    ],
                    "ans": 1,
                    "exp": "On broadcast media, radio or electrical signals reach every antenna/interface in range. In promiscuous mode, the NIC processes all packets regardless of destination MAC (§1.6 / P8c)."
                }
            ]
        },
        {
            "id": "ch1-7",
            "num": "1.7",
            "title": "History of Computer Networking and the Internet",
            "subtitle": "Milestones: Kleinrock's packet switching, ARPANET, TCP/IP Flag Day, Web explosion, and mobile cloud",
            "content": r"""
<p>The Internet evolved over more than six decades across five distinct developmental eras:</p>

<div class="summary-grid" style="margin:1rem 0;">
  <div class="summary-card" style="border-top:3px solid #64748b;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.25rem;">1. 1961–1972: Early Packet Switching & ARPANET</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Leonard Kleinrock publishes the first paper on packet-switching queuing theory (1961). Paul Baran and Donald Davies independently conceptualize packet switching. First ARPANET node installed at UCLA (1969), connecting 4 universities via Interface Message Processors (IMPs). Ray Tomlinson writes first network email program (1972).
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #3b82f6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.25rem;">2. 1972–1980: Internetworking & TCP/IP</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Vinton Cerf and Robert Kahn release landmark paper (1974) outlining the TCP architecture for connecting disparate networks (DARPA Internetworking). Early network protocols (NCP) handled host communication.
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #10b981;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.25rem;">3. 1980–1990: Proliferation & Flag Day</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      <strong>January 1, 1983 (Flag Day):</strong> ARPANET officially cuts over from NCP to the TCP/IP protocol suite. Mockapetris invents the Domain Name System (DNS) in 1983. Van Jacobson creates TCP congestion control algorithms (1988) following catastrophic Internet congestion collapses.
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #8b5cf6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.25rem;">4. 1990s: The World Wide Web Explosion</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Tim Berners-Lee invents HTTP, HTML, and URL at CERN (1989–1991). Marc Andreessen develops Mosaic (1993) and Netscape Navigator. NSFNET commercializes in 1995, transferring the backbone to commercial ISPs.
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #e11d48;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.25rem;">5. 2000s–Present: Mobile, Cloud & CDNs</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      Broadband residential access (DSL/Cable/FTTH), ubiquitous 4G/5G mobile connectivity, hyperscale cloud data centers (AWS, Google Cloud, Azure), and Content Distribution Networks (CDNs) serving rich media to billions.
    </p>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "On what date did ARPANET officially adopt TCP/IP as its standard host protocol ('Flag Day')?",
                    "opts": [
                        "July 4, 1976",
                        "January 1, 1983",
                        "December 31, 1989",
                        "August 6, 1991"
                    ],
                    "ans": 1,
                    "exp": "January 1, 1983 marked the historic cutover date when all ARPANET hosts were required to transition from NCP to TCP/IP (§1.7)."
                }
            ]
        },
        {
            "id": "ch1-8",
            "num": "1.8",
            "title": "Chapter 1 Summary & Exam Practice Problems (P1–P8)",
            "subtitle": "Complete worked solutions to all 8 Midterm Study Guide Practice Problems plus Textbook Problems",
            "content": r"""
<p>Master these 8 practice problems from the official CPCS-371 Midterm Study Guide. Each question represents an exact exam pattern highlighted by the course instructors.</p>

<!-- PROBLEM P1 -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P1: Networking Units Warm-Up</div>
    <span class="interactive-badge">Study Guide P1</span>
  </div>
  <p><strong>Problem:</strong> Convert the following quantities:</p>
  <p>(a) Convert 3 MB to bits.<br>
     (b) Convert 2.5 Kbits to bytes.<br>
     (c) Convert 45 &mu;s to ms.<br>
     (d) Convert 600 Kbps to Mbps.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) In networking, <span class="math-inline">1\text{ MB} = 10^6\text{ bytes}</span> and <span class="math-inline">1\text{ byte} = 8\text{ bits}</span>:
      <div class="math-display">3 \times 10^6\text{ bytes} \times 8 = \mathbf{24,000,000\text{ bits}} \ (24\text{ Mbits})</div>
    </div>
    <div class="calc-step">(b) <span class="math-inline">2.5\text{ Kbits} = 2,500\text{ bits}</span>. Divide by 8 to convert to bytes:
      <div class="math-display">\frac{2,500}{8} = \mathbf{312.5\text{ bytes}}</div>
    </div>
    <div class="calc-step">(c) <span class="math-inline">1\text{ ms} = 1,000\ \mu\text{s}</span>:
      <div class="math-display">\frac{45}{1,000} = \mathbf{0.045\text{ ms}}</div>
    </div>
    <div class="calc-step">(d) <span class="math-inline">1\text{ Mbps} = 1,000\text{ Kbps}</span>:
      <div class="math-display">\frac{600}{1,000} = \mathbf{0.6\text{ Mbps}}</div>
    </div>
  </div>
</div>

<!-- PROBLEM P2 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P2: Transmission vs Propagation Delay</div>
    <span class="interactive-badge">Study Guide P2</span>
  </div>
  <p><strong>Problem:</strong> A 1,000-byte packet is sent over a 20 Mbps link that is 4,000 km long (<span class="math-inline">s = 2 \times 10^8\text{ m/s}</span>).</p>
  <p>(a) Compute the transmission delay and the propagation delay. Which one dominates?<br>
     (b) What is the propagation delay if the same link is only 400 m long? Which delay dominates now?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p2-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p2-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; Packet length in bits: <span class="math-inline">L = 1,000 \times 8 = 8,000\text{ bits}</span>.
      <br>&bull; Transmission delay:
      <div class="math-display">d_{\text{trans}} = \frac{L}{R} = \frac{8,000\text{ bits}}{20 \times 10^6\text{ bps}} = 0.0004\text{ s} = \mathbf{0.4\text{ ms}}</div>
      <br>&bull; Propagation delay (<span class="math-inline">d = 4,000\text{ km} = 4 \times 10^6\text{ m}</span>):
      <div class="math-display">d_{\text{prop}} = \frac{d}{s} = \frac{4 \times 10^6\text{ m}}{2 \times 10^8\text{ m/s}} = 0.02\text{ s} = \mathbf{20\text{ ms}}</div>
      <br>&bull; <strong>Verdict:</strong> Propagation delay (20 ms) is 50 times larger than transmission delay (0.4 ms) and <strong>heavily dominates</strong>!
    </div>
    <div class="calc-step">Part (b):
      <br>&bull; For <span class="math-inline">d = 400\text{ m}</span>:
      <div class="math-display">d_{\text{prop}} = \frac{400\text{ m}}{2 \times 10^8\text{ m/s}} = 2 \times 10^{-6}\text{ s} = \mathbf{2\ \mu\text{s}} \ (0.002\text{ ms})</div>
      <br>&bull; <strong>Verdict:</strong> Transmission delay (<span class="math-inline">0.4\text{ ms} = 400\ \mu\text{s}</span>) is now 200 times larger than propagation delay (<span class="math-inline">2\ \mu\text{s}</span>) and <strong>heavily dominates</strong>! The two delays depend on completely different physical factors.
    </div>
  </div>
</div>

<!-- PROBLEM P3 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P3: Store-and-Forward Pipelining</div>
    <span class="interactive-badge">Study Guide P3</span>
  </div>
  <p><strong>Problem:</strong> A host sends a 5,000-bit packet to a destination through one intermediate router. Both links have <span class="math-inline">R = 1\text{ Mbps}</span>. Ignore propagation, processing, and queuing delays.</p>
  <p>(a) How long until the destination has the entire packet?<br>
     (b) The host sends three such packets back-to-back. When does the last packet arrive?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p3-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p3-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a): Transmission time per link:
      <div class="math-display">\frac{L}{R} = \frac{5,000\text{ bits}}{10^6\text{ bps}} = 0.005\text{ s} = \mathbf{5\text{ ms}}</div>
      Because the router must store the entire packet before forwarding:
      <div class="math-display">d_{\text{total}} = 2 \times \frac{L}{R} = 2 \times 5\text{ ms} = \mathbf{10\text{ ms}}</div>
    </div>
    <div class="calc-step">Part (b): Pipelined transmission of <span class="math-inline">P = 3</span> packets over <span class="math-inline">N = 2</span> links:
      <br>&bull; Time <span class="math-inline">t = 0\text{ to }5\text{ ms}</span>: Host sends Packet 1 to router.
      <br>&bull; Time <span class="math-inline">t = 5\text{ to }10\text{ ms}</span>: Router forwards Packet 1 to destination; Host sends Packet 2 to router.
      <br>&bull; Time <span class="math-inline">t = 10\text{ to }15\text{ ms}</span>: Router forwards Packet 2 to destination; Host sends Packet 3 to router.
      <br>&bull; Time <span class="math-inline">t = 15\text{ to }20\text{ ms}</span>: Router forwards Packet 3 to destination.
      <div class="math-display">d_{\text{total}} = (N + P - 1) \cdot \frac{L}{R} = (2 + 3 - 1) \times 5\text{ ms} = 4 \times 5\text{ ms} = \mathbf{20\text{ ms}}</div>
    </div>
  </div>
</div>

<!-- PROBLEM P4 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P4: Tollbooth Caravan Analogy</div>
    <span class="interactive-badge">Study Guide P4</span>
  </div>
  <p><strong>Problem:</strong> An 8-car caravan travels between tollbooths 150 km apart. Each booth needs 15 s per car, and cars travel at 100 km/h.</p>
  <p>(a) How long after the caravan starts at the first booth is it lined up before the second booth?<br>
     (b) Now cars travel at 1,000 km/h and a booth needs 1 min per car. Does the first car reach the second booth before the last car has left the first booth?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p4-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p4-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; Transmission time for all 8 cars through first booth: <span class="math-inline">8 \times 15\text{ s} = 120\text{ s} = 2\text{ minutes}</span>.
      <br>&bull; Propagation time for the last car on the highway: <span class="math-inline">\frac{150\text{ km}}{100\text{ km/h}} = 1.5\text{ hours} = 90\text{ minutes}</span>.
      <br>&bull; Total time until caravan lines up at booth 2: <span class="math-inline">2\text{ min} + 90\text{ min} = \mathbf{92\text{ minutes}}</span>.
    </div>
    <div class="calc-step">Part (b):
      <br>&bull; The first car is serviced at booth 1 in 1 minute, departing at <span class="math-inline">t = 1\text{ min}</span>.
      <br>&bull; Travel time for the first car: <span class="math-inline">\frac{150\text{ km}}{1,000\text{ km/h}} = 0.15\text{ hours} = 9\text{ minutes}</span>.
      <br>&bull; The first car arrives at the second booth at <span class="math-inline">t = 1 + 9 = \mathbf{10\text{ minutes}}</span>.
      <br>&bull; Meanwhile, the 8th (last) car leaves booth 1 at <span class="math-inline">t = 8 \times 1\text{ min} = \mathbf{8\text{ minutes}}</span>.
      <br>&bull; <strong>Answer:</strong> <strong>No!</strong> All 8 cars have departed booth 1 by minute 8, which is 2 minutes before the first car reaches booth 2 at minute 10!
    </div>
  </div>
</div>

<!-- PROBLEM P5 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P5: Traffic Intensity and Queuing Loss</div>
    <span class="interactive-badge">Study Guide P5</span>
  </div>
  <p><strong>Problem:</strong> Packets of 500 bytes arrive at an average rate of 300 packets/sec at a router output link of 1 Mbps.</p>
  <p>(a) Compute the traffic intensity and describe what happens to the queue.<br>
     (b) What is the highest average arrival rate that keeps the traffic intensity at 0.5?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p5-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p5-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; Packet length in bits: <span class="math-inline">L = 500 \times 8 = 4,000\text{ bits}</span>.
      <br>&bull; Traffic intensity:
      <div class="math-display">I = \frac{L \cdot a}{R} = \frac{4,000\text{ bits} \times 300\text{ packets/s}}{10^6\text{ bps}} = \frac{1,200,000}{1,000,000} = \mathbf{1.2}</div>
      <br>&bull; <strong>Verdict:</strong> Because <span class="math-inline">I = 1.2 > 1</span>, more data arrives than the link can service. The queue buffer will fill up, queuing delay becomes unbounded, and newly arriving packets are <strong>dropped (packet loss)</strong>.
    </div>
    <div class="calc-step">Part (b): To achieve <span class="math-inline">I = 0.5</span>:
      <div class="math-display">a = \frac{0.5 \cdot R}{L} = \frac{0.5 \times 10^6\text{ bps}}{4,000\text{ bits}} = \mathbf{125\text{ packets/second}}</div>
    </div>
  </div>
</div>

<!-- PROBLEM P6 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P6: Path Throughput and Bottleneck Link</div>
    <span class="interactive-badge">Study Guide P6</span>
  </div>
  <p><strong>Problem:</strong> A server sends data to a client over a server link <span class="math-inline">R_s = 3\text{ Mbps}</span> and a client link <span class="math-inline">R_c = 8\text{ Mbps}</span>.</p>
  <p>(a) What is the end-to-end throughput, and which link is the bottleneck?<br>
     (b) The server link is upgraded to 12 Mbps. What is the new throughput and the new bottleneck?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p6-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p6-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <div class="math-display">\text{Throughput} = \min(R_s, R_c) = \min(3, 8) = \mathbf{3\text{ Mbps}}</div>
      The <strong>server link (<span class="math-inline">R_s</span>)</strong> is the bottleneck link.
    </div>
    <div class="calc-step">Part (b):
      <div class="math-display">\text{New Throughput} = \min(12, 8) = \mathbf{8\text{ Mbps}}</div>
      The <strong>client link (<span class="math-inline">R_c</span>)</strong> is now the new bottleneck link.
    </div>
  </div>
</div>

<!-- PROBLEM P7 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P7: Circuit Switching (TDM vs FDM)</div>
    <span class="interactive-badge">Study Guide P7</span>
  </div>
  <p><strong>Problem:</strong> All links have a rate of 2.048 Mbps and use TDM with 32 slots. Setting up an end-to-end circuit takes 250 ms.</p>
  <p>(a) How long does it take to send a 480,000-bit file over one circuit?<br>
     (b) If the links used FDM with 32 frequency bands instead, at what rate would each call transmit?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p7-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p7-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; Transmission rate per dedicated circuit:
      <div class="math-display">R_{\text{circuit}} = \frac{2.048\text{ Mbps}}{32} = \frac{2,048\text{ kbps}}{32} = \mathbf{64\text{ kbps}} = 64,000\text{ bps}</div>
      <br>&bull; Transmission time for the 480,000-bit file:
      <div class="math-display">d_{\text{trans}} = \frac{480,000\text{ bits}}{64,000\text{ bps}} = \mathbf{7.5\text{ seconds}}</div>
      <br>&bull; Total elapsed time including circuit set-up delay (250 ms = 0.25 s):
      <div class="math-display">d_{\text{total}} = 0.25\text{ s} + 7.5\text{ s} = \mathbf{7.75\text{ seconds}}</div>
    </div>
    <div class="calc-step">Part (b):
      With FDM with 32 bands, each call transmits at <span class="math-inline">\frac{2.048\text{ Mbps}}{32} = \mathbf{64\text{ kbps}}</span>. The difference is that in FDM, the 64 kbps bandwidth is available continuously, whereas in TDM it transmits in periodic time slots.
    </div>
  </div>
</div>

<!-- PROBLEM P8 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P8: Protocol Layering & Security Threats</div>
    <span class="interactive-badge">Study Guide P8</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) Which layers are implemented in an end system host, in a router, and in a link-layer switch?<br>
     (b) Give the official name of the packet (PDU) at the Transport, Network, and Link layers.<br>
     (c) Explain the difference between a virus and a worm, and explain why broadcast media are vulnerable to packet sniffing.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p8-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p8-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; <strong>Host:</strong> Implements all <strong>5 layers</strong> (Physical, Link, Network, Transport, Application).
      <br>&bull; <strong>Core Router:</strong> Implements <strong>layers 1–3</strong> (Physical, Link, Network).
      <br>&bull; <strong>Link-Layer Switch:</strong> Implements <strong>layers 1–2</strong> (Physical, Link).
    </div>
    <div class="calc-step">Part (b):
      <br>&bull; Transport layer: <strong>Segment</strong>.
      <br>&bull; Network layer: <strong>Datagram</strong>.
      <br>&bull; Link layer: <strong>Frame</strong>.
    </div>
    <div class="calc-step">Part (c):
      <br>&bull; <strong>Virus vs Worm:</strong> A computer virus requires human intervention (such as downloading and running an infected attachment or program) to replicate and execute. A worm is self-replicating and autonomously spreads across the network without user intervention.
      <br>&bull; <strong>Packet Sniffing Vulnerability:</strong> On a shared broadcast medium (such as wireless radio or shared coaxial cable), physical signals reach all interfaces in range. An adapter set to <strong>promiscuous mode</strong> can intercept, copy, and log all passing frames, capturing unencrypted data.
    </div>
  </div>
</div>

<!-- TEXTBOOK HOMEWORK PROBLEM P8 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Textbook Problem: Bandwidth-Delay Product & Reception Time</div>
    <span class="interactive-badge">Kurose & Ross P8</span>
  </div>
  <p><strong>Problem:</strong> Suppose two hosts, A and B, are separated by 20,000 kilometers and connected by a direct link of rate <span class="math-inline">R = 2\text{ Mbps}</span>. Propagation speed is <span class="math-inline">s = 2.5 \times 10^8\text{ m/s}</span>.</p>
  <p>(a) Calculate the bandwidth-delay product, <span class="math-inline">R \cdot d_{\text{prop}}</span>.<br>
     (b) Consider sending a file of 800,000 bits from A to B. How long until the first bit arrives at B? When is the file completely received?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch1-p-textbook-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch1-p-textbook-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Distance <span class="math-inline">d = 20,000\text{ km} = 2 \times 10^7\text{ m}</span>.
      <div class="math-display">d_{\text{prop}} = \frac{d}{s} = \frac{2 \times 10^7\text{ m}}{2.5 \times 10^8\text{ m/s}} = 0.08\text{ s} = \mathbf{80\text{ ms}}</div>
    </div>
    <div class="calc-step">Step 2: Bandwidth-Delay Product:
      <div class="math-display">\text{BDP} = R \times d_{\text{prop}} = (2 \times 10^6\text{ bps}) \times 0.08\text{ s} = \mathbf{160,000\text{ bits}}</div>
      <em>Physical significance:</em> The link "pipe" can hold up to 160,000 bits in transit simultaneously!
    </div>
    <div class="calc-step">Step 3: The first bit arrives at B after exactly <span class="math-inline">d_{\text{prop}} = \mathbf{80\text{ ms}}</span>.</div>
    <div class="calc-step">Step 4: Transmission delay:
      <div class="math-display">d_{\text{trans}} = \frac{L}{R} = \frac{800,000\text{ bits}}{2 \times 10^6\text{ bps}} = 0.4\text{ s} = \mathbf{400\text{ ms}}</div>
    </div>
    <div class="calc-step">Step 5: Total reception time until the last bit is received:
      <div class="math-display">d_{\text{total}} = d_{\text{trans}} + d_{\text{prop}} = 400\text{ ms} + 80\text{ ms} = \mathbf{480\text{ ms}} \ (0.48\text{ s})</div>
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the physical meaning of the Bandwidth-Delay Product (R * d_prop)?",
                    "opts": [
                        "The time it takes to push all packet bits into the link",
                        "The maximum number of bits that can be in flight simultaneously across the physical link",
                        "The total queuing capacity of the edge router",
                        "The round-trip delay divided by packet size"
                    ],
                    "ans": 1,
                    "exp": "The Bandwidth-Delay Product represents the volume of the communication link in bits — i.e. how many bits can fit 'in transit' on the physical medium at any instant (§1.4)."
                }
            ]
        }
    ]
}
