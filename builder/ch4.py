"""Chapter 4 Data: The Network Layer (Kurose & Ross 6th Ed.)
Completely expanded to full textbook depth: Data Plane vs Control Plane, Router Architectures,
Switching Fabrics, HOL Blocking, Bit-accurate IPv4 & IPv6 headers, Fragmentation, Subnetting/CIDR,
DHCP DORA, NAT translation tables, ICMP, Dijkstra trace, Bellman-Ford Count-to-Infinity & Poisoned Reverse,
OSPF Areas, BGP policy, Multicast RPF, and 3 comprehensive worked homework problems.
"""

CH4_DATA = {
    "id": "ch4",
    "num": 4,
    "title": "The Network Layer",
    "subtitle": "Data & Control Planes, Router Architectures, IPv4, Subnetting, NAT, DHCP, IPv6 & Routing Algorithms",
    "layer": "Network Layer",
    "color": "#10b981",
    "objectives": [
        "Distinguish between Forwarding (data plane, hardware) and Routing (control plane, software)",
        "Analyze Router architecture: Input ports, Switching fabrics (memory, bus, crossbar), Output queuing & HOL blocking",
        "Perform IPv4 packet fragmentation and reassembly calculations (Offset in 8-byte units, MF flag)",
        "Calculate IPv4 Subnetting & CIDR ranges: Network, Broadcast, First/Last Usable Host, Total Hosts",
        "Trace DHCP 4-step DORA exchange and NAT address/port translation tables",
        "Contrast IPv4 vs IPv6 headers and explain dual-stack & tunneling migration strategies",
        "Execute Dijkstra's Link-State algorithm step-by-step and construct the routing table",
        "Formulate Bellman-Ford Distance Vector equations and explain Count-to-Infinity and Poisoned Reverse",
        "Evaluate Internet routing protocols: RIP (DV), OSPF (LS/Areas), and BGP (Path Vector/Policy)",
        "Understand broadcast and multicast routing: Reverse Path Forwarding (RPF), Spanning Trees, and IGMP/PIM"
    ],
    "sections": [
        {
            "id": "ch4-1",
            "num": "4.1",
            "title": "Introduction to the Network Layer",
            "subtitle": "Forwarding vs Routing, Data Plane vs Control Plane, and Network Service Models",
            "content": r"""
<p>The network layer is responsible for transporting packets from a sending host to a receiving host across the network core. Unlike the transport layer, which runs solely in the end systems, the network layer protocol runs in <strong>every host and router</strong> in the network.</p>

<p>To move a packet from sending host to receiving host, two vital network-layer functions are required:</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Forwarding vs Routing: The Data Plane vs Control Plane</div>
  <ul>
    <li><strong>Forwarding (Data Plane):</strong> The router's local action of transferring a packet from an incoming link interface to the appropriate outgoing link interface. Forwarding takes place at extremely fast timescales (typically nanoseconds) and is almost universally implemented directly in specialized hardware (ASICs/TCAM).</li>
    <li><strong>Routing (Control Plane):</strong> The network-wide process that determines the end-to-end paths that packets take from source to destination. Routing takes place on longer timescales (typically seconds) and is usually implemented in software executed by the router's routing processor.</li>
  </ul>
</div>

<p>A helpful analogy from Kurose & Ross is taking a road trip:</p>
<ul>
  <li><strong>Routing</strong> is analogous to consulting a map or GPS navigation system before and during the trip to plan the sequence of cities and interstate highways to take from New York to Los Angeles.</li>
  <li><strong>Forwarding</strong> is analogous to driving through a single interchange or roundabout: choosing which specific exit ramp to take to continue along the planned path.</li>
</ul>

<!-- FIGURE 4.1: FORWARDING VS ROUTING INTERPLAY -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 280" xmlns="http://www.w3.org/2000/svg">
      <!-- Control plane zone -->
      <rect x="30" y="20" width="680" height="90" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4 4"/>
      <text x="50" y="42" font-size="12" font-weight="700" fill="#1e40af">CONTROL PLANE (Software &bull; Milliseconds to Seconds)</text>
      <rect x="220" y="48" width="300" height="45" rx="6" fill="#3b82f6"/>
      <text x="370" y="75" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">Routing Algorithm (OSPF, BGP)</text>

      <!-- Arrow down to data plane -->
      <path d="M 370 93 L 370 140" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
      <text x="385" y="120" font-size="11" font-weight="600" fill="#0284c7">Computes & Installs Forwarding Table</text>

      <!-- Data plane zone -->
      <rect x="30" y="145" width="680" height="115" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
      <text x="50" y="167" font-size="12" font-weight="700" fill="#047857">DATA PLANE (Hardware &bull; Nanoseconds per packet)</text>

      <!-- Arriving packet -->
      <rect x="50" y="185" width="90" height="36" rx="4" fill="#3b82f6"/>
      <text x="95" y="207" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Header [Dest IP]</text>
      <line x1="140" y1="203" x2="210" y2="203" stroke="#10b981" stroke-width="3"/>

      <!-- Forwarding table box -->
      <rect x="210" y="172" width="220" height="65" rx="6" fill="#ffffff" stroke="#10b981" stroke-width="2"/>
      <text x="320" y="192" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Local Forwarding Table</text>
      <text x="320" y="210" font-size="9.5" fill="#64748b" text-anchor="middle">Dest Prefix &rarr; Output Link 3</text>
      <text x="320" y="224" font-size="9" fill="#10b981" text-anchor="middle">Hardware Lookup (TCAM)</text>

      <!-- Switching fabric -->
      <line x1="430" y1="203" x2="520" y2="203" stroke="#10b981" stroke-width="3"/>
      <rect x="520" y="175" width="90" height="58" rx="6" fill="#10b981"/>
      <text x="565" y="200" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Switching</text>
      <text x="565" y="216" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Fabric</text>

      <!-- Outgoing link -->
      <line x1="610" y1="203" x2="680" y2="203" stroke="#10b981" stroke-width="3"/>
      <text x="645" y="195" font-size="10" font-weight="700" fill="#047857">Output 3</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.1 — Interplay between Routing (Control Plane) and Forwarding (Data Plane) inside a router (§4.1.1).</div>
</div>

<h3>Network Service Models</h3>
<p>What service guarantees does a network architecture provide to packets transported from source to destination? Possible guarantees include guaranteed delivery, guaranteed delivery with bounded delay, in-order packet delivery, guaranteed minimum bandwidth, and security encryption.</p>

<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.88rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px 10px;">Network Architecture</th>
      <th style="padding:8px 10px;">Service Model</th>
      <th style="padding:8px 10px;">Bandwidth Guarantee</th>
      <th style="padding:8px 10px;">Loss Guarantee</th>
      <th style="padding:8px 10px;">Timing / Delay</th>
      <th style="padding:8px 10px;">Congestion Feedback</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light); background:var(--bg-card);">
      <td style="padding:8px 10px; font-weight:700; color:var(--accent-text);">Internet IP</td>
      <td style="padding:8px 10px; font-weight:600;">Best Effort</td>
      <td style="padding:8px 10px; color:var(--danger-text);">None</td>
      <td style="padding:8px 10px; color:var(--danger-text);">None (packets may drop)</td>
      <td style="padding:8px 10px; color:var(--danger-text);">None (variable delay)</td>
      <td style="padding:8px 10px;">None (indirect loss)</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">ATM CBR</td>
      <td style="padding:8px 10px;">Constant Bit Rate</td>
      <td style="padding:8px 10px; color:#10b981; font-weight:600;">Constant rate</td>
      <td style="padding:8px 10px; color:#10b981;">Guaranteed no loss</td>
      <td style="padding:8px 10px; color:#10b981;">Strict bounded delay</td>
      <td style="padding:8px 10px;">No congestion</td>
    </tr>
    <tr>
      <td style="padding:8px 10px; font-weight:700;">ATM ABR</td>
      <td style="padding:8px 10px;">Available Bit Rate</td>
      <td style="padding:8px 10px; color:#0284c7;">Guaranteed minimum</td>
      <td style="padding:8px 10px; color:var(--danger-text);">None</td>
      <td style="padding:8px 10px; color:var(--danger-text);">None</td>
      <td style="padding:8px 10px; color:#10b981; font-weight:600;">Explicit feedback (RM cells)</td>
    </tr>
  </tbody>
</table>

<div class="callout callout-insight">
  <div class="callout-header">💡 Why Best-Effort Won the Networking Revolution</div>
  Despite offering zero QoS guarantees, the Internet's <strong>Best-Effort model</strong> triumphed worldwide over complex circuit-like architectures like ATM because:
  <ol>
    <li>Simplicity at the core allowed routers to be built with ultra-high throughput and modest costs.</li>
    <li>Adequate link bandwidth provisioning frequently eliminated delay and congestion in practice.</li>
    <li>Intelligence was placed in end systems (TCP congestion control, adaptive application codecs), making the core protocol agnostic to application types.</li>
  </ol>
</div>
""",
            "quiz": [
                {
                    "q": "Which action operates at nanosecond timescales and is implemented directly in router hardware?",
                    "opts": [
                        "Dijkstra's Link-State routing algorithm",
                        "Forwarding (transferring a packet from input link to output link)",
                        "BGP inter-AS route advertisement",
                        "OSPF link-state advertisement flooding"
                    ],
                    "ans": 1,
                    "exp": "Forwarding is the data plane action performed locally by router hardware at nanosecond speeds (§4.1.1)."
                },
                {
                    "q": "What service guarantees does the Internet's IPv4 network layer provide for end-to-end packet delivery?",
                    "opts": [
                        "Guaranteed delivery with bounded delay",
                        "In-order packet delivery with guaranteed minimum bandwidth",
                        "Best effort: no guarantees on loss, delay, bandwidth, or ordering",
                        "Guaranteed error-free transmission via ATM-like virtual circuits"
                    ],
                    "ans": 2,
                    "exp": "The Internet network layer provides only Best-Effort service with zero guarantees on delivery, delay, jitter, or order (§4.1.2)."
                }
            ]
        },
        {
            "id": "ch4-2",
            "num": "4.2",
            "title": "Virtual Circuit and Datagram Networks",
            "subtitle": "Connection-oriented VC networks vs connectionless datagram networks and Longest Prefix Match",
            "content": r"""
<p>Just as the transport layer can offer connection-oriented (TCP) or connectionless (UDP) services to applications, the network layer can offer connection-oriented or connectionless service between host end systems. However, there are fundamental differences:</p>
<ul>
  <li>In the network layer, connection service is provided <strong>host-to-host</strong> (across all routers along the path), not process-to-process.</li>
  <li>In the transport layer, connection state is kept only in end systems. In a network-layer connection-oriented network, <strong>every intermediate core router maintains connection state!</strong></li>
</ul>

<h3>4.2.1 Virtual-Circuit (VC) Networks</h3>
<p>A <strong>Virtual Circuit (VC)</strong> consists of: (1) a path (series of links and routers) between source and destination, (2) VC numbers for each link along the path, and (3) entries in the forwarding table in each router along that path.</p>

<p>When a packet traverses a link, it carries a <strong>VC Number</strong> in its header rather than a full destination address. Crucially, a packet does <em>not</em> maintain the same VC number on each link; instead, each router replaces the VC number with a new one using its local VC translation table!</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Why Replace VC Numbers on Each Link?</div>
  <ol>
    <li>Replacing the number reduces the required header size (VC number field needs to index only active connections on that single link, rather than across the entire global network).</li>
    <li>Simplifies VC setup: routers choose available VC numbers locally without global synchronization.</li>
  </ol>
</div>

<p>A VC network operates in three distinct phases: <strong>VC Setup</strong> (signaling messages establish state), <strong>Data Transfer</strong> (packets flow with VC numbers), and <strong>VC Teardown</strong> (signaling terminates state). Examples: ATM, Frame Relay, X.25.</p>

<h3>4.2.2 Datagram Networks and Longest Prefix Matching</h3>
<p>In a <strong>datagram network</strong>, each time an end system wants to send a packet, it stamps the packet with the destination host's full 32-bit IP address. Routers maintain <strong>no connection state</strong> for active conversations. Each packet is routed independently!</p>

<p>Because there are over 4 billion 32-bit IPv4 addresses, a router cannot maintain a table with 4 billion entries. Instead, the router aggregates addresses into <strong>prefixes</strong> and matches them using <strong>Longest Prefix Matching (LPM)</strong>:</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Longest Prefix Matching (LPM) Rule</div>
  When a router looks up a destination address in its forwarding table, it searches for the table entry with the <strong>longest matching address prefix</strong> (the most specific match) and forwards the packet out the link interface associated with that longest match.
</div>

<p>Consider the forwarding table below:</p>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.88rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:6px 10px;">Prefix Match</th>
      <th style="padding:6px 10px;">Link Interface</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-family:monospace;">11001000 00010111 00010*** ******** (200.23.16.0/21)</td>
      <td style="padding:6px 10px; font-weight:700; color:#3b82f6;">Link 0</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-family:monospace;">11001000 00010111 00011000 ******** (200.23.24.0/24)</td>
      <td style="padding:6px 10px; font-weight:700; color:#10b981;">Link 1</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-family:monospace;">11001000 00010111 00011*** ******** (200.23.24.0/21)</td>
      <td style="padding:6px 10px; font-weight:700; color:#f59e0b;">Link 2</td>
    </tr>
    <tr>
      <td style="padding:6px 10px; font-family:monospace;">Otherwise (Default Route 0.0.0.0/0)</td>
      <td style="padding:6px 10px; font-weight:700; color:#8b5cf6;">Link 3</td>
    </tr>
  </tbody>
</table>

<p>Example: Destination Address <code>11001000 00010111 00011000 10101010</code>.</p>
<ul>
  <li>Matches prefix 2 (21 bits) &rarr; Link 2</li>
  <li>Matches prefix 1 (24 bits) &rarr; Link 1</li>
  <li>By Longest Prefix Matching, the router chooses <strong>Link 1</strong> because 24 bits is longer than 21 bits!</li>
</ul>
""",
            "quiz": [
                {
                    "q": "Why do virtual-circuit routers swap VC numbers on every link along a path instead of keeping a single global VC number?",
                    "opts": [
                        "To prevent eavesdropping attacks by malicious routers",
                        "Because swapping VC numbers keeps the VC field small and allows routers to allocate numbers locally without global coordination",
                        "Because IP header checksums require varying VC IDs",
                        "To ensure TCP flow control remains synchronized"
                    ],
                    "ans": 1,
                    "exp": "Local VC number swapping minimizes the header bits needed to identify circuits and eliminates the need for global VC number coordination (§4.2.1)."
                },
                {
                    "q": "Under Longest Prefix Matching, if an incoming packet matches both a /16 prefix and a /24 prefix in the routing table, which interface is chosen?",
                    "opts": [
                        "The /16 interface because it covers a larger address range",
                        "The /24 interface because it is the longest, most specific matching prefix",
                        "The router drops the packet due to ambiguous forwarding",
                        "The interface with the lower physical link cost"
                    ],
                    "ans": 1,
                    "exp": "Longest Prefix Matching dictates choosing the most specific prefix (the one with the largest number of matching leading bits, /24 > /16) (§4.2.2)."
                }
            ]
        },
        {
            "id": "ch4-3",
            "num": "4.3",
            "title": "What's Inside a Router?",
            "subtitle": "Input processing, switching fabrics, output processing, and Head-of-Line (HOL) blocking",
            "content": r"""
<p>A high-performance router consists of four primary structural components:</p>
<ol>
  <li><strong>Input Ports:</strong> Terminate incoming physical links, decapsulate link-layer frames, perform decentralized lookup in the Forwarding Information Base (FIB) to determine the output port, and queue packets if necessary.</li>
  <li><strong>Switching Fabric:</strong> The physical network that connects the router's input ports to its output ports.</li>
  <li><strong>Output Ports:</strong> Store packets received from the switching fabric and transmit them over outgoing physical links.</li>
  <li><strong>Routing Processor:</strong> Executes traditional control-plane routing protocols (OSPF, RIP, BGP), maintains routing tables, and computes forwarding tables installed into input ports.</li>
</ol>

<!-- FIGURE 4.2: ROUTER ARCHITECTURE OVERVIEW -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 270" xmlns="http://www.w3.org/2000/svg">
      <!-- Routing processor at top -->
      <rect x="250" y="15" width="240" height="42" rx="6" fill="#3b82f6"/>
      <text x="370" y="41" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">Routing Processor (Control Plane)</text>
      <line x1="370" y1="57" x2="370" y2="85" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>

      <!-- Central Switching Fabric -->
      <rect x="270" y="85" width="200" height="165" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>
      <text x="370" y="160" font-size="14" font-weight="800" fill="#334155" text-anchor="middle">High-Speed</text>
      <text x="370" y="180" font-size="14" font-weight="800" fill="#334155" text-anchor="middle">Switching Fabric</text>

      <!-- Input Ports on Left -->
      <rect x="30" y="90" width="180" height="38" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
      <text x="120" y="114" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Input Port 1 (Lookup FIB)</text>
      <line x1="210" y1="109" x2="270" y2="109" stroke="#10b981" stroke-width="2"/>

      <rect x="30" y="150" width="180" height="38" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
      <text x="120" y="174" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Input Port 2 (Lookup FIB)</text>
      <line x1="210" y1="169" x2="270" y2="169" stroke="#10b981" stroke-width="2"/>

      <rect x="30" y="210" width="180" height="38" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
      <text x="120" y="234" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Input Port 3 (Lookup FIB)</text>
      <line x1="210" y1="229" x2="270" y2="229" stroke="#10b981" stroke-width="2"/>

      <!-- Output Ports on Right -->
      <line x1="470" y1="109" x2="530" y2="109" stroke="#3b82f6" stroke-width="2"/>
      <rect x="530" y="90" width="180" height="38" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
      <text x="620" y="114" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Output Port 1 (Buffer/Tx)</text>

      <line x1="470" y1="169" x2="530" y2="169" stroke="#3b82f6" stroke-width="2"/>
      <rect x="530" y="150" width="180" height="38" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
      <text x="620" y="174" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Output Port 2 (Buffer/Tx)</text>

      <line x1="470" y1="229" x2="530" y2="229" stroke="#3b82f6" stroke-width="2"/>
      <rect x="530" y="210" width="180" height="38" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
      <text x="620" y="234" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Output Port 3 (Buffer/Tx)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.2 — Router Architecture Overview: Input Ports, Switching Fabric, Output Ports, and Routing Processor (§4.3).</div>
</div>

<h3>4.3.2 The Three Types of Switching Fabrics</h3>
<p>The switching fabric is at the heart of the router. Three major architectures exist:</p>

<!-- FIGURE 4.3: THREE SWITCHING FABRICS -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 220" xmlns="http://www.w3.org/2000/svg">
      <!-- (a) Memory -->
      <rect x="20" y="20" width="220" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="130" y="42" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">(a) Switching via Memory</text>
      <rect x="50" y="60" width="160" height="30" rx="4" fill="#dbeafe" stroke="#3b82f6"/>
      <text x="130" y="80" font-size="11" font-weight="600" fill="#1e40af" text-anchor="middle">System Memory (RAM)</text>
      <path d="M 50 140 L 100 90 M 160 90 L 210 140" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)"/>
      <text x="130" y="160" font-size="10" fill="#64748b" text-anchor="middle">CPU copies packet twice</text>
      <text x="130" y="175" font-size="9.5" fill="#ef4444" text-anchor="middle">Speed limited by memory bus</text>

      <!-- (b) Bus -->
      <rect x="260" y="20" width="220" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="370" y="42" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">(b) Switching via Bus</text>
      <line x1="280" y1="105" x2="460" y2="105" stroke="#f59e0b" stroke-width="6"/>
      <text x="370" y="95" font-size="10.5" font-weight="700" fill="#d97706" text-anchor="middle">Shared Internal Bus</text>
      <line x1="300" y1="140" x2="300" y2="108" stroke="#10b981" stroke-width="2"/>
      <line x1="440" y1="108" x2="440" y2="140" stroke="#3b82f6" stroke-width="2"/>
      <text x="370" y="160" font-size="10" fill="#64748b" text-anchor="middle">Direct bus transfer</text>
      <text x="370" y="175" font-size="9.5" fill="#ef4444" text-anchor="middle">Limited by bus contention (1 pkt)</text>

      <!-- (c) Crossbar Interconnection -->
      <rect x="500" y="20" width="220" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="610" y="42" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">(c) Switching via Crossbar</text>
      <!-- Horizontal lines -->
      <line x1="530" y1="75" x2="690" y2="75" stroke="#10b981" stroke-width="2"/>
      <line x1="530" y1="110" x2="690" y2="110" stroke="#10b981" stroke-width="2"/>
      <line x1="530" y1="145" x2="690" y2="145" stroke="#10b981" stroke-width="2"/>
      <!-- Vertical lines -->
      <line x1="560" y1="55" x2="560" y2="165" stroke="#3b82f6" stroke-width="2"/>
      <line x1="610" y1="55" x2="610" y2="165" stroke="#3b82f6" stroke-width="2"/>
      <line x1="660" y1="55" x2="660" y2="165" stroke="#3b82f6" stroke-width="2"/>
      <!-- Crosspoints -->
      <circle cx="610" cy="75" r="4" fill="#ef4444"/>
      <circle cx="560" cy="145" r="4" fill="#ef4444"/>
      <text x="610" y="182" font-size="10" font-weight="700" fill="#10b981" text-anchor="middle">Non-blocking parallel switching</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.3 — The Three Types of Switching Fabrics: Memory, Bus, and Crossbar Interconnection Network (§4.3.2).</div>
</div>

<ol>
  <li><strong>Switching via Memory:</strong> Early routers were traditional computers. An incoming packet signaled an interrupt, causing the CPU to copy the packet across the system bus into main memory. The CPU extracted the destination address from the header, looked up the output port, and copied the packet across the bus to the output port. Throughput is strictly limited by memory bus bandwidth (at most <span class="math-inline"><i>B</i> / 2</span> if bus speed is <span class="math-inline"><i>B</i></span>).</li>
  <li><strong>Switching via a Bus:</strong> Input ports transfer packets directly to output ports over a shared internal bus without routing processor intervention. Because the bus is shared, <strong>only one packet can cross the bus at a time</strong>. All other arriving packets must wait in input queues. Modern bus routers achieve switching speeds of gigabits per second, but are bottlenecked for terabit-scale core routers.</li>
  <li><strong>Switching via an Interconnection Network (Crossbar):</strong> A crossbar switch consists of an <span class="math-inline">2<i>n</i></span> bus matrix connecting <span class="math-inline"><i>n</i></span> input ports to <span class="math-inline"><i>n</i></span> output ports. Crosspoints can be dynamically opened and closed by the switch fabric controller. Multiple packets can be forwarded <strong>in parallel</strong> as long as their destinations are different! Crossbar switches are non-blocking and form the backbone of modern terabit routers.</li>
</ol>

<h3>4.3.4 Queuing and Head-of-Line (HOL) Blocking</h3>
<p>Where does packet queuing occur inside a router? Queues can form at both the <strong>input ports</strong> and the <strong>output ports</strong>:</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Head-of-Line (HOL) Blocking in Input Queues</div>
  In an input-queued switch with a crossbar fabric, <strong>Head-of-Line (HOL) blocking</strong> occurs when a packet at the front of an input queue is blocked from moving through the fabric because its destination output port is currently busy, which in turn <strong>blocks all other packets queued behind it</strong> &mdash; even if those subsequent packets are destined to completely idle output ports!
</div>

<!-- FIGURE 4.4: HOL BLOCKING -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 210" xmlns="http://www.w3.org/2000/svg">
      <!-- Input Queues -->
      <rect x="40" y="30" width="220" height="60" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="50" y="48" font-size="10.5" font-weight="700" fill="#334155">Input Queue 1</text>
      <!-- Pkt A at head (red) -->
      <rect x="180" y="55" width="60" height="26" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
      <text x="210" y="72" font-size="10" font-weight="700" fill="#991b1b" text-anchor="middle">&rarr; Out 1</text>
      <!-- Pkt B behind (green) -->
      <rect x="110" y="55" width="60" height="26" rx="3" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="140" y="72" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">&rarr; Out 2</text>

      <rect x="40" y="110" width="220" height="60" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="50" y="128" font-size="10.5" font-weight="700" fill="#334155">Input Queue 2</text>
      <!-- Pkt C at head (red) -->
      <rect x="180" y="135" width="60" height="26" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
      <text x="210" y="152" font-size="10" font-weight="700" fill="#991b1b" text-anchor="middle">&rarr; Out 1</text>

      <!-- Contention Banner -->
      <path d="M 245 68 L 330 100 M 245 148 L 330 100" stroke="#ef4444" stroke-width="2"/>
      <circle cx="330" cy="100" r="14" fill="#ef4444"/>
      <text x="330" y="105" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">!</text>
      <text x="330" y="130" font-size="10" font-weight="700" fill="#ef4444" text-anchor="middle">Contention!</text>

      <!-- Switching fabric & Output Ports -->
      <rect x="430" y="45" width="160" height="45" rx="4" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
      <text x="510" y="72" font-size="11" font-weight="700" fill="#991b1b" text-anchor="middle">Output Port 1 (BUSY)</text>

      <rect x="430" y="120" width="160" height="45" rx="4" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="510" y="147" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Output Port 2 (IDLE!)</text>

      <!-- Explanation label -->
      <rect x="600" y="50" width="125" height="110" rx="4" fill="#f1f5f9"/>
      <text x="662" y="72" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle">HOL Effect:</text>
      <text x="662" y="90" font-size="9" fill="#64748b" text-anchor="middle">Green packet &rarr; Out 2</text>
      <text x="662" y="105" font-size="9" fill="#ef4444" text-anchor="middle">is BLOCKED behind</text>
      <text x="662" y="120" font-size="9" fill="#ef4444" text-anchor="middle">contending red packet,</text>
      <text x="662" y="135" font-size="9" fill="#047857" text-anchor="middle">even though Out 2</text>
      <text x="662" y="150" font-size="9" fill="#047857" text-anchor="middle">is totally free!</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.4 — Head-of-Line (HOL) Blocking in an Input-Queued Router (§4.3.4).</div>
</div>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Rule-of-Thumb for Router Buffer Sizing</div>
  For decades, the standard rule of thumb for sizing router output buffers was:
  <div class="math-display">
    <i>B</i> = RTT &times; <i>C</i>
  </div>
  where RTT is average round-trip time (e.g. 250 ms) and <span class="math-inline"><i>C</i></span> is link capacity.
  <br>However, recent measurements for large numbers of TCP flows (<span class="math-inline"><i>N</i></span>) show that buffer requirements drop dramatically due to statistical desynchronization:
  <div class="math-display">
    <i>B</i> = <span class="math-frac"><span class="math-num">RTT &times; <i>C</i></span><span class="math-denom">&radic;<i>N</i></span></span>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What causes Head-of-Line (HOL) blocking in an input-queued router?",
                    "opts": [
                        "A packet at the head of an input queue waiting for a busy output port prevents other packets behind it from reaching idle output ports",
                        "The routing processor CPU runs out of memory for OSPF calculations",
                        "TCP receiver window drops to zero",
                        "Output port scheduler uses strict priority instead of round robin"
                    ],
                    "ans": 0,
                    "exp": "HOL blocking occurs when an unblocked packet behind the head of an input queue is forced to wait because the packet in front of it is contending for a different, busy output port (§4.3.4)."
                },
                {
                    "q": "If 100 independent TCP flows traverse a router link with RTT = 200 ms and C = 10 Gbps, how does the modernized buffer sizing formula B = (RTT * C) / sqrt(N) compare to the classic rule?",
                    "opts": [
                        "It requires 10 times more buffering",
                        "It requires 10 times less buffering (divided by sqrt(100) = 10)",
                        "It requires the exact same 2 Gb buffer",
                        "Buffer sizing becomes zero"
                    ],
                    "ans": 1,
                    "exp": "Because N = 100 flows desynchronize, the required buffer size is divided by sqrt(100) = 10, needing only 1/10th the memory of the classic rule (§4.3.4)."
                }
            ]
        },
        {
            "id": "ch4-4",
            "num": "4.4",
            "title": "The Internet Protocol (IP)",
            "subtitle": "IPv4 datagram format, fragmentation, CIDR addressing, DHCP, NAT, ICMP & IPv6",
            "content": r"""
<p>The Internet Protocol is the unifying glue of the entire Internet. We begin with IPv4 (RFC 791) and its 20-byte base header layout:</p>

<!-- FIGURE 4.5: BIT-ACCURATE IPV4 HEADER SVG -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 760 210" xmlns="http://www.w3.org/2000/svg">
      <text x="30" y="20" font-size="10" fill="#64748b">Bit 0</text>
      <text x="110" y="20" font-size="10" fill="#64748b">3 4</text>
      <text x="190" y="20" font-size="10" fill="#64748b">7 8</text>
      <text x="370" y="20" font-size="10" fill="#64748b">15 16</text>
      <text x="730" y="20" font-size="10" fill="#64748b">31</text>
      <line x1="30" y1="25" x2="730" y2="25" stroke="#cbd5e1" stroke-width="1"/>

      <!-- Row 1: Version, IHL, TOS, Total Length -->
      <rect x="30" y="30" width="85" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="72" y="50" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Ver (4b)</text>

      <rect x="115" y="30" width="85" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="157" y="50" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">IHL (4b)</text>

      <rect x="200" y="30" width="170" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="285" y="50" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">TOS / Diffserv (8 bits)</text>

      <rect x="370" y="30" width="360" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="550" y="50" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Total Datagram Length in Bytes (16 bits)</text>

      <!-- Row 2: ID, Flags, Frag Offset -->
      <rect x="30" y="62" width="340" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="200" y="82" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">16-bit Identification (Packet ID)</text>

      <rect x="370" y="62" width="70" height="32" fill="#fed7aa" stroke="#f97316" stroke-width="1.5"/>
      <text x="405" y="82" font-size="10" font-weight="700" fill="#9a3412" text-anchor="middle">Flags (3b)</text>

      <rect x="440" y="62" width="290" height="32" fill="#fed7aa" stroke="#f97316" stroke-width="1.5"/>
      <text x="585" y="82" font-size="10" font-weight="700" fill="#9a3412" text-anchor="middle">Fragment Offset (13b in 8-Byte Units)</text>

      <!-- Row 3: TTL, Protocol, Checksum -->
      <rect x="30" y="94" width="170" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="115" y="114" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Time-to-Live (TTL 8b)</text>

      <rect x="200" y="94" width="170" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="285" y="114" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Protocol (TCP=6, UDP=17)</text>

      <rect x="370" y="94" width="360" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="550" y="114" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Header Checksum (16 bits)</text>

      <!-- Row 4: Source IP Address -->
      <rect x="30" y="126" width="700" height="32" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="380" y="146" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">32-bit Source IP Address</text>

      <!-- Row 5: Destination IP Address -->
      <rect x="30" y="158" width="700" height="32" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="380" y="178" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">32-bit Destination IP Address</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.5 — Bit-accurate IPv4 20-byte base header layout (§4.4.1).</div>
</div>

<h3>4.4.1 IPv4 Datagram Fragmentation</h3>
<p>Different link-layer protocols have different Maximum Transmission Units (MTUs). Ethernet has an MTU of 1500 bytes. When an IP datagram arrives at a router and its length exceeds the MTU of the outgoing link, the router must <strong>fragment</strong> the datagram into multiple smaller datagrams.</p>

<p>Crucially, <strong>reassembly of fragments is performed exclusively at the destination end system</strong>, never by intermediate routers! Three header fields govern fragmentation:</p>
<ul>
  <li><strong>Identification (16 bits):</strong> Copied into all fragments of the same original datagram so the receiver knows they belong together.</li>
  <li><strong>Flags (3 bits):</strong> Includes <strong>DF</strong> (Don't Fragment) and <strong>MF</strong> (More Fragments: 1 if more fragments follow, 0 for the last fragment).</li>
  <li><strong>Fragment Offset (13 bits):</strong> Specifies where in the original datagram this fragment's data begins, measured in <strong>units of 8-byte (64-bit) chunks</strong>.</li>
</ul>

<!-- EMBEDDED INTERACTIVE: LIVE FRAGMENTATION CALCULATOR -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🧩 Live IPv4 Datagram Fragmentation Calculator</div>
    <span class="interactive-badge">RFC 791 Math</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Calculate exact fragment lengths, 8-byte offsets, and More-Fragment flags for any datagram and link MTU.
  </p>
  <div class="grid-2">
    <div class="form-group">
      <label class="form-label">Total Datagram Size (Bytes, incl 20B header):</label>
      <input type="number" id="calc-frag-total" class="form-input" value="4000" min="60" max="65535" oninput="computeFragmentation()">
    </div>
    <div class="form-group">
      <label class="form-label">Outgoing Link MTU (Bytes):</label>
      <input type="number" id="calc-frag-mtu" class="form-input" value="1500" min="68" max="9000" oninput="computeFragmentation()">
    </div>
  </div>
  <div id="calc-frag-result" class="calc-result-box" style="margin-top:0.75rem;"></div>
</div>

<h3>4.4.2 IPv4 Addressing, Subnets, and CIDR</h3>
<p>An IPv4 address is 32 bits (4 bytes) long, represented in dotted-decimal notation (e.g., <code>192.168.1.1</code>). In IP addressing, a <strong>subnet</strong> is a network interconnecting host interfaces and router interfaces that can physically reach each other without an intervening router.</p>

<p>The Internet uses <strong>Classless Inter-Domain Routing (CIDR, RFC 4632)</strong>, where an address prefix is represented as <code>a.b.c.d/x</code>, where <span class="math-inline"><i>x</i></span> is the prefix length (the subnet mask length in bits):</p>
<ul>
  <li>Subnet portion = <span class="math-inline"><i>x</i></span> leading bits.</li>
  <li>Host portion = <span class="math-inline">32 &minus; <i>x</i></span> remaining bits.</li>
  <li>Total IP addresses in subnet = <span class="math-inline">2<sup>32 &minus; <i>x</i></sup></span>.</li>
  <li>Usable host IP addresses = <span class="math-inline">2<sup>32 &minus; <i>x</i></sup> &minus; 2</span> (all zeros host is the Network Address; all ones host is the Directed Broadcast Address).</li>
</ul>

<!-- EMBEDDED INTERACTIVE: LIVE CIDR SUBNET CALCULATOR -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🧮 Live IPv4 Subnet / CIDR Planner</div>
    <span class="interactive-badge">Address Planner</span>
  </div>
  <div class="grid-2">
    <div class="form-group">
      <label class="form-label">IP Address:</label>
      <input type="text" id="sec4-ip" class="form-input" value="192.168.1.130" oninput="calcSec4CIDR()">
    </div>
    <div class="form-group">
      <label class="form-label">Prefix Length (/x):</label>
      <input type="number" id="sec4-prefix" class="form-input" value="26" min="1" max="30" oninput="calcSec4CIDR()">
    </div>
  </div>
  <div id="sec4-cidr-result" class="calc-result-box" style="margin-top:0.75rem;"></div>
</div>

<h3>4.4.3 Dynamic Host Configuration Protocol (DHCP)</h3>
<p>DHCP (RFC 2131) automates the configuration of host IP addresses, subnet masks, default gateway router, and local DNS server. It is a client-server protocol running over UDP (client port 68, server port 67) using the 4-step <strong>DORA</strong> exchange:</p>
<ol>
  <li><strong>DHCP Discover:</strong> Newly arrived host broadcasts <code>src: 0.0.0.0:68 &rarr; dst: 255.255.255.255:67</code> asking "Are there any DHCP servers?"</li>
  <li><strong>DHCP Offer:</strong> Server broadcasts an offer containing proposed IP (<code>yiaddr</code>: your IP address), subnet mask, lease time, and server IP.</li>
  <li><strong>DHCP Request:</strong> Client broadcasts confirmation selecting one offer and echoing server ID: <code>dst: 255.255.255.255:67</code>.</li>
  <li><strong>DHCP ACK:</strong> Server acknowledges and confirms lease parameters.</li>
</ol>

<h3>4.4.4 Network Address Translation (NAT)</h3>
<p>Because IPv4 addresses are scarce, private networks use private address blocks (RFC 1918: <code>10.0.0.0/8</code>, <code>172.16.0.0/12</code>, <code>192.168.0.0/16</code>). Core Internet routers never route these private addresses!</p>
<p>To communicate with the global Internet, a <strong>NAT-enabled router</strong> maps multiple private internal host IP/port combinations to a single public IP address using a 16-bit port translation table:</p>

<!-- FIGURE 4.6: NAT OPERATION & TRANSLATION TABLE -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 230" xmlns="http://www.w3.org/2000/svg">
      <!-- Home network zone -->
      <rect x="20" y="20" width="220" height="190" rx="6" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
      <text x="130" y="42" font-size="11.5" font-weight="700" fill="#047857" text-anchor="middle">Private Home Subnet 192.168.1.0/24</text>
      <!-- Host 1 -->
      <rect x="40" y="60" width="180" height="40" rx="4" fill="#ffffff" stroke="#10b981"/>
      <text x="130" y="84" font-size="10.5" font-weight="600" fill="#065f46" text-anchor="middle">Host: 192.168.1.100 : 3345</text>
      <!-- Host 2 -->
      <rect x="40" y="115" width="180" height="40" rx="4" fill="#ffffff" stroke="#10b981"/>
      <text x="130" y="139" font-size="10.5" font-weight="600" fill="#065f46" text-anchor="middle">Host: 192.168.1.101 : 3345</text>

      <!-- NAT Router -->
      <rect x="280" y="35" width="180" height="160" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="370" y="60" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">NAT Router</text>
      <text x="370" y="78" font-size="10" fill="#1d4ed8" text-anchor="middle">LAN IP: 192.168.1.1</text>
      <text x="370" y="94" font-size="10" font-weight="700" fill="#b91c1c" text-anchor="middle">WAN IP: 138.76.29.7</text>

      <!-- NAT Table Mini Box -->
      <rect x="295" y="105" width="150" height="75" rx="4" fill="#ffffff" stroke="#93c5fd"/>
      <text x="370" y="122" font-size="9" font-weight="700" fill="#1e40af" text-anchor="middle">NAT Translation Table</text>
      <text x="370" y="140" font-size="8.5" fill="#334155" text-anchor="middle">WAN Side &harr; LAN Side</text>
      <text x="370" y="156" font-size="8" font-family="monospace" fill="#047857" text-anchor="middle">138.76.29.7:5001 &harr; .100:3345</text>
      <text x="370" y="170" font-size="8" font-family="monospace" fill="#047857" text-anchor="middle">138.76.29.7:5002 &harr; .101:3345</text>

      <!-- Internet & Remote Web Server -->
      <rect x="520" y="45" width="190" height="140" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>
      <text x="615" y="75" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">Public Internet</text>
      <rect x="540" y="95" width="150" height="65" rx="4" fill="#ffffff" stroke="#64748b"/>
      <text x="615" y="120" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">Origin Web Server</text>
      <text x="615" y="140" font-size="10" font-family="monospace" fill="#2563eb" text-anchor="middle">128.119.40.186 : 80</text>

      <!-- Connection Lines -->
      <line x1="220" y1="80" x2="280" y2="80" stroke="#10b981" stroke-width="2"/>
      <line x1="460" y1="80" x2="520" y2="80" stroke="#ef4444" stroke-width="2"/>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.6 — Network Address Translation (NAT) operation and port mapping table (§4.4.4).</div>
</div>

<h3>4.4.5 ICMP (Internet Control Message Protocol)</h3>
<p>ICMP (RFC 792) is used by hosts and routers to communicate network-layer information, typically for error reporting (e.g. "Destination host unreachable") or operational diagnostics (e.g. <code>ping</code> and <code>traceroute</code>).</p>
<p>ICMP messages are carried inside IP datagrams (IP protocol field = 1). Common types:</p>
<table style="width:100%; border-collapse:collapse; margin:0.75rem 0; font-size:0.85rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:6px 10px;">Type</th>
      <th style="padding:6px 10px;">Code</th>
      <th style="padding:6px 10px;">Description</th>
      <th style="padding:6px 10px;">Used by</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 10px;">0</td><td style="padding:6px 10px;">0</td><td style="padding:6px 10px;">Echo Reply</td><td style="padding:6px 10px;"><code>ping</code> response</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 10px;">3</td><td style="padding:6px 10px;">0</td><td style="padding:6px 10px;">Destination Network Unreachable</td><td style="padding:6px 10px;">Router error</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 10px;">3</td><td style="padding:6px 10px;">1</td><td style="padding:6px 10px;">Destination Host Unreachable</td><td style="padding:6px 10px;">Router error</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 10px;">3</td><td style="padding:6px 10px;">3</td><td style="padding:6px 10px;">Destination Port Unreachable</td><td style="padding:6px 10px;"><code>traceroute</code> destination termination</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 10px;">8</td><td style="padding:6px 10px;">0</td><td style="padding:6px 10px;">Echo Request</td><td style="padding:6px 10px;"><code>ping</code> query</td></tr>
    <tr><td style="padding:6px 10px;">11</td><td style="padding:6px 10px;">0</td><td style="padding:6px 10px;">TTL Expired in Transit</td><td style="padding:6px 10px;"><code>traceroute</code> hop discovery</td></tr>
  </tbody>
</table>

<h3>4.4.6 IPv6</h3>
<p>To overcome IPv4 address exhaustion, IPv6 was introduced (RFC 2460). Key improvements:</p>
<ul>
  <li><strong>Expanded 128-Bit Addressing:</strong> <span class="math-inline">2<sup>128</sup> &approx; 3.4 &times; 10<sup>38</sup></span> addresses (enough to assign billions of addresses to every grain of sand on Earth).</li>
  <li><strong>Streamlined 40-Byte Fixed Base Header:</strong> Fixed size accelerates hardware processing.</li>
  <li><strong>No Header Checksum:</strong> Checksum eliminated completely to speed up forwarding (transport and link layers already perform checksums).</li>
  <li><strong>No Router Fragmentation:</strong> Intermediate routers NEVER fragment packets! If a packet is too large, router drops it and sends back ICMPv6 "Packet Too Big".</li>
</ul>

<!-- FIGURE 4.7: BIT-ACCURATE IPV6 HEADER SVG -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 760 210" xmlns="http://www.w3.org/2000/svg">
      <text x="30" y="20" font-size="10" fill="#64748b">Bit 0</text>
      <text x="110" y="20" font-size="10" fill="#64748b">3 4</text>
      <text x="210" y="20" font-size="10" fill="#64748b">11 12</text>
      <text x="730" y="20" font-size="10" fill="#64748b">31</text>
      <line x1="30" y1="25" x2="730" y2="25" stroke="#cbd5e1" stroke-width="1"/>

      <!-- Row 1: Ver (4b), Traffic Class (8b), Flow Label (20b) -->
      <rect x="30" y="30" width="85" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="72" y="50" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Ver (4b)</text>

      <rect x="115" y="30" width="160" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="195" y="50" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Traffic Class (8b)</text>

      <rect x="275" y="30" width="455" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="502" y="50" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Flow Label (20 bits)</text>

      <!-- Row 2: Payload Length (16b), Next Header (8b), Hop Limit (8b) -->
      <rect x="30" y="62" width="350" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="205" y="82" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Payload Length in Bytes (16 bits)</text>

      <rect x="380" y="62" width="170" height="32" fill="#fbcfe8" stroke="#db2777" stroke-width="1.5"/>
      <text x="465" y="82" font-size="10" font-weight="700" fill="#9d174d" text-anchor="middle">Next Header (8b)</text>

      <rect x="550" y="62" width="180" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="640" y="82" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Hop Limit (8b)</text>

      <!-- Row 3 & 4: Source 128-bit IPv6 Address -->
      <rect x="30" y="94" width="700" height="42" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="380" y="119" font-size="11.5" font-weight="700" fill="#1e40af" text-anchor="middle">128-bit Source IPv6 Address (16 bytes)</text>

      <!-- Row 5 & 6: Dest 128-bit IPv6 Address -->
      <rect x="30" y="136" width="700" height="42" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="380" y="161" font-size="11.5" font-weight="700" fill="#1e40af" text-anchor="middle">128-bit Destination IPv6 Address (16 bytes)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.7 — Bit-accurate IPv6 40-byte streamlined base header layout (§4.4.6).</div>
</div>

<h3>IPv6 Transition: Tunneling</h3>
<p>Because the billions of IPv4 routers cannot be upgraded simultaneously, the primary migration mechanism is <strong>Tunneling (RFC 4213)</strong>. An IPv6 datagram is encapsulated as the complete payload of an IPv4 datagram (with IPv4 Protocol field = 41). The IPv4 core routes the packet normally between dual-stack routers at the tunnel endpoints.</p>
""",
            "quiz": [
                {
                    "q": "Which field present in the IPv4 header was completely removed from the IPv6 base header to streamline router processing?",
                    "opts": [
                        "Hop Limit",
                        "Header Checksum",
                        "Next Header",
                        "Flow Label"
                    ],
                    "ans": 1,
                    "exp": "IPv6 eliminated the Header Checksum to eliminate per-hop recomputation, relying on transport and link-layer error checks (§4.4.6)."
                },
                {
                    "q": "How does an IPv6 packet traverse an intermediate network containing only legacy IPv4 routers?",
                    "opts": [
                        "The IPv6 packet is converted to ATM cells",
                        "The entire IPv6 datagram is encapsulated inside the payload of a standard IPv4 datagram (Tunneling)",
                        "The IPv4 routers drop the packet and issue an ICMP redirect",
                        "The IPv6 address is truncated to 32 bits"
                    ],
                    "ans": 1,
                    "exp": "Tunneling encapsulates the IPv6 datagram inside an IPv4 datagram between dual-stack border routers (§4.4.6)."
                }
            ]
        },
        {
            "id": "ch4-5",
            "num": "4.5",
            "title": "Routing Algorithms",
            "subtitle": "Link-State (Dijkstra) vs Distance-Vector (Bellman-Ford), Count-to-Infinity & Hierarchical Routing",
            "content": r"""
<p>The goal of routing algorithms is to determine good paths (least-cost paths) through the network of routers from senders to receivers.</p>

<h3>4.5.1 The Link-State (LS) Routing Algorithm: Dijkstra</h3>
<p>In a <strong>Link-State algorithm</strong>, the network topology and all link costs are known to all nodes. This is accomplished by having each node broadcast link-state packets (LSAs) to all other nodes (link-state flooding). Dijkstra's algorithm computes the least-cost path from one node (the source, <span class="math-inline"><i>u</i></span>) to all other nodes in the network.</p>

<!-- FIGURE 4.8: 6-NODE TOPOLOGY FOR DIJKSTRA -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 230" xmlns="http://www.w3.org/2000/svg">
      <!-- Node u (source) -->
      <circle cx="90" cy="115" r="24" fill="#3b82f6"/>
      <text x="90" y="122" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">u</text>

      <!-- Node v -->
      <circle cx="250" cy="50" r="22" fill="#10b981"/>
      <text x="250" y="56" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">v</text>

      <!-- Node x -->
      <circle cx="250" cy="180" r="22" fill="#10b981"/>
      <text x="250" y="186" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">x</text>

      <!-- Node w -->
      <circle cx="490" cy="50" r="22" fill="#10b981"/>
      <text x="490" y="56" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">w</text>

      <!-- Node y -->
      <circle cx="490" cy="180" r="22" fill="#10b981"/>
      <text x="490" y="186" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">y</text>

      <!-- Node z -->
      <circle cx="650" cy="115" r="24" fill="#8b5cf6"/>
      <text x="650" y="122" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">z</text>

      <!-- Links and Costs -->
      <!-- u to v -->
      <line x1="112" y1="106" x2="228" y2="59" stroke="#64748b" stroke-width="2"/>
      <rect x="160" y="70" width="22" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="171" y="83" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">2</text>

      <!-- u to x -->
      <line x1="112" y1="124" x2="228" y2="171" stroke="#64748b" stroke-width="2"/>
      <rect x="160" y="140" width="22" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="171" y="153" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">1</text>

      <!-- u to w -->
      <line x1="114" y1="115" x2="466" y2="52" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3 3"/>
      <text x="290" y="75" font-size="11" font-weight="700" fill="#94a3b8">cost = 5</text>

      <!-- v to x -->
      <line x1="250" y1="72" x2="250" y2="158" stroke="#64748b" stroke-width="2"/>
      <rect x="240" y="105" width="20" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="250" y="118" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">2</text>

      <!-- v to w -->
      <line x1="272" y1="50" x2="468" y2="50" stroke="#64748b" stroke-width="2"/>
      <rect x="360" y="41" width="20" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="370" y="54" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">3</text>

      <!-- x to w -->
      <line x1="270" y1="168" x2="470" y2="62" stroke="#64748b" stroke-width="2"/>
      <rect x="360" y="105" width="20" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="370" y="118" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">3</text>

      <!-- x to y -->
      <line x1="272" y1="180" x2="468" y2="180" stroke="#64748b" stroke-width="2"/>
      <rect x="360" y="171" width="20" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="370" y="184" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">1</text>

      <!-- w to y -->
      <line x1="490" y1="72" x2="490" y2="158" stroke="#64748b" stroke-width="2"/>
      <rect x="480" y="105" width="20" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="490" y="118" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">1</text>

      <!-- w to z -->
      <line x1="512" y1="59" x2="628" y2="106" stroke="#64748b" stroke-width="2"/>
      <rect x="565" y="70" width="22" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="576" y="83" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">5</text>

      <!-- y to z -->
      <line x1="512" y1="171" x2="628" y2="124" stroke="#64748b" stroke-width="2"/>
      <rect x="565" y="140" width="22" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="576" y="153" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">2</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.8 — 6-Node Network Topology for Dijkstra's Link-State Algorithm (Kurose & Ross Table 4.3 network).</div>
</div>

<p>Table 4.3 from Kurose & Ross: Step-by-step trace of Dijkstra's algorithm for source node <span class="math-inline"><i>u</i></span>:</p>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.85rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:6px 8px;">Step</th>
      <th style="padding:6px 8px;"><i>N'</i></th>
      <th style="padding:6px 8px;"><i>D</i>(<i>v</i>), <i>p</i>(<i>v</i>)</th>
      <th style="padding:6px 8px;"><i>D</i>(<i>w</i>), <i>p</i>(<i>w</i>)</th>
      <th style="padding:6px 8px;"><i>D</i>(<i>x</i>), <i>p</i>(<i>x</i>)</th>
      <th style="padding:6px 8px;"><i>D</i>(<i>y</i>), <i>p</i>(<i>y</i>)</th>
      <th style="padding:6px 8px;"><i>D</i>(<i>z</i>), <i>p</i>(<i>z</i>)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 8px; font-weight:700;">0</td><td>{u}</td><td>2, u</td><td>5, u</td><td style="background:#dcfce7; font-weight:700;">1, u</td><td>&infin;</td><td>&infin;</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 8px; font-weight:700;">1</td><td>{u, x}</td><td style="background:#dcfce7; font-weight:700;">2, u</td><td>min(5, 1+3) = 4, x</td><td>&mdash;</td><td style="background:#dcfce7; font-weight:700;">min(&infin;, 1+1) = 2, x</td><td>&infin;</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 8px; font-weight:700;">2</td><td>{u, x, y}</td><td style="background:#dcfce7; font-weight:700;">2, u</td><td style="background:#dcfce7; font-weight:700;">min(4, 2+1) = 3, y</td><td>&mdash;</td><td>&mdash;</td><td>min(&infin;, 2+2) = 4, y</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 8px; font-weight:700;">3</td><td>{u, x, y, v}</td><td>&mdash;</td><td style="background:#dcfce7; font-weight:700;">3, y</td><td>&mdash;</td><td>&mdash;</td><td>4, y</td></tr>
    <tr style="border-bottom:1px solid var(--border-light);"><td style="padding:6px 8px; font-weight:700;">4</td><td>{u, x, y, v, w}</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td><td style="background:#dcfce7; font-weight:700;">min(4, 3+5) = 4, y</td></tr>
    <tr><td style="padding:6px 8px; font-weight:700;">5</td><td>{u, x, y, v, w, z}</td><td colspan="5">All nodes visited! Final forwarding table: v &rarr; (u,v); x &rarr; (u,x); y &rarr; (u,x); w &rarr; (u,x); z &rarr; (u,x).</td></tr>
  </tbody>
</table>

<!-- EMBEDDED INTERACTIVE: DIJKSTRA STEPPER -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🗺️ Interactive Dijkstra's Algorithm Step-Through</div>
    <span class="interactive-badge">Table Trace</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Source Node <strong>u</strong> computing least-cost paths to nodes (v, x, w, y, z) following Table 4.3.
  </p>
  <div class="sim-viewport" style="align-items:flex-start; min-height:120px;">
    <div style="font-family:monospace; font-size:0.88rem; line-height:1.6; width:100%;">
      <div id="sec4-dijkstra-step" style="font-weight:700; color:var(--accent-text); margin-bottom:0.35rem;">[Ready] Click 'Next Dijkstra Step'</div>
      <div id="sec4-dijkstra-info" style="color:var(--text-secondary);">Trace shortest path calculation step by step.</div>
    </div>
  </div>
  <div class="sim-controls">
    <button class="btn-primary" onclick="stepSec4Dijkstra()">⏭ Next Dijkstra Step</button>
    <button class="btn-secondary" onclick="resetSec4Dijkstra()">🔄 Reset</button>
  </div>
</div>

<h3>4.5.2 The Distance-Vector (DV) Routing Algorithm: Bellman-Ford</h3>
<p>While the LS algorithm uses global information, the <strong>Distance-Vector (DV) algorithm</strong> is <em>iterative</em>, <em>asynchronous</em>, and <em>distributed</em>. Each node receives information only from its directly connected neighbors, performs calculation, and distributes its results back to its neighbors.</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 The Bellman-Ford Equation</div>
  Let <span class="math-inline"><i>d<sub>x</sub></i>(<i>y</i>)</span> be the cost of the least-cost path from node <span class="math-inline"><i>x</i></span> to node <span class="math-inline"><i>y</i></span>:
  <div class="math-display">
    <i>d<sub>x</sub></i>(<i>y</i>) = min<sub><i>v</i></sub> { <i>c</i>(<i>x</i>, <i>v</i>) + <i>d<sub>v</sub></i>(<i>y</i>) }
  </div>
  where the min is taken over all neighbors <span class="math-inline"><i>v</i></span> of <span class="math-inline"><i>x</i></span>.
</div>

<h3>The Count-to-Infinity Problem & Poisoned Reverse</h3>
<p>When a link cost increases or a link breaks, Distance Vector can suffer from routing loops and the notorious <strong>Count-to-Infinity problem</strong>:</p>
<ul>
  <li>"Good news travels fast": When link cost decreases, convergence is rapid (1 to 2 iterations).</li>
  <li>"Bad news travels slow": When link cost jumps (e.g. from 4 to 60), nodes bounce routing loops back and forth (e.g., node <span class="math-inline">y</span> thinks it can reach <span class="math-inline">x</span> through <span class="math-inline">z</span> with cost 5, and <span class="math-inline">z</span> thinks it can reach <span class="math-inline">x</span> through <span class="math-inline">y</span> with cost 6...). The loop counts up: 4 &rarr; 5 &rarr; 6 &rarr; ... until it exceeds the link cost or infinity threshold!</li>
</ul>

<div class="callout callout-def">
  <div class="callout-header">📘 Poisoned Reverse Solution</div>
  If node <span class="math-inline"><i>z</i></span> routes through node <span class="math-inline"><i>y</i></span> to get to destination <span class="math-inline"><i>x</i></span>, node <span class="math-inline"><i>z</i></span> advertises to <span class="math-inline"><i>y</i></span> that its distance to <span class="math-inline"><i>x</i></span> is <strong>infinity</strong>:
  <div class="math-display"><i>d<sub>z</sub></i>(<i>x</i>) = &infin; &emsp; (advertised strictly to <i>y</i>)</div>
  This prevents <span class="math-inline"><i>y</i></span> from ever attempting to route back through <span class="math-inline"><i>z</i></span> to reach <span class="math-inline"><i>x</i></span>!
  <br><em>Important Limitation: Poisoned reverse completely eliminates 2-node loops, but does NOT prevent loops involving 3 or more nodes!</em>
</div>
""",
            "quiz": [
                {
                    "q": "What is the primary operational difference between Link-State (Dijkstra) and Distance-Vector (Bellman-Ford) routing?",
                    "opts": [
                        "Link-state uses global network topology broadcast to all nodes, while distance-vector communicates only with direct neighbors asynchronously",
                        "Link-state runs only over UDP, while distance-vector runs over TCP",
                        "Distance-vector is immune to routing loops, while link-state is not",
                        "Link-state has O(N^3) time complexity while distance-vector is O(1)"
                    ],
                    "ans": 0,
                    "exp": "Link-state requires complete global topology via flooding, whereas distance-vector is decentralized and exchanges vectors only with immediate neighbors (§4.5)."
                },
                {
                    "q": "Does Poisoned Reverse solve the Count-to-Infinity problem for all possible routing loops?",
                    "opts": [
                        "Yes, it eliminates loops of any size completely",
                        "No, it solves 2-node loops, but loops involving 3 or more nodes can still count to infinity",
                        "No, it only works if link costs are integers less than 15",
                        "Yes, but only when used alongside OSPF areas"
                    ],
                    "ans": 1,
                    "exp": "Poisoned reverse prevents 2-node loops; loops involving 3 or more nodes cannot be detected by simple poisoned reverse (§4.5.2)."
                }
            ]
        },
        {
            "id": "ch4-6",
            "num": "4.6",
            "title": "Routing in the Internet",
            "subtitle": "Intra-AS routing (RIP, OSPF) and Inter-AS routing (BGP)",
            "content": r"""
<p>To scale to tens of thousands of ISPs and billions of hosts, the Internet organizes routers into <strong>Autonomous Systems (ASs)</strong>, each under unified administrative and technical control.</p>

<h3>Intra-AS Routing (Interior Gateway Protocols)</h3>
<ul>
  <li><strong>RIP (Routing Information Protocol, RFC 2453):</strong> Distance-vector protocol. Metric is <strong>hop count</strong> (each link has cost 1). Maximum path cost is 15 hops (16 = infinity). Advertisements sent every 30 seconds via UDP port 520.</li>
  <li><strong>OSPF (Open Shortest Path First, RFC 2328):</strong> Modern link-state protocol using Dijkstra's algorithm. OSPF messages are carried directly over IP (protocol 89). Features:
    <ol>
      <li><strong>Security:</strong> All OSPF exchanges can be authenticated (MD5/HMAC).</li>
      <li><strong>Multiple Same-Cost Paths (ECMP):</strong> Permits load balancing across multiple equal-cost paths.</li>
      <li><strong>Hierarchical Structure:</strong> An AS can be partitioned into <strong>Areas</strong>, coordinated by a <strong>Backbone Area (Area 0)</strong>.</li>
    </ol>
  </li>
</ul>

<!-- FIGURE 4.9: HIERARCHICAL OSPF -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 220" xmlns="http://www.w3.org/2000/svg">
      <!-- Area 0 Backbone -->
      <rect x="230" y="20" width="280" height="90" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
      <text x="370" y="42" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">OSPF Area 0 (Backbone Area)</text>
      <!-- Backbone Routers -->
      <circle cx="280" cy="72" r="16" fill="#3b82f6"/>
      <text x="280" y="76" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">ABR1</text>
      <circle cx="370" cy="72" r="16" fill="#1e40af"/>
      <text x="370" y="76" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">BBR</text>
      <circle cx="460" cy="72" r="16" fill="#3b82f6"/>
      <text x="460" y="76" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">ABR2</text>
      <line x1="296" y1="72" x2="354" y2="72" stroke="#3b82f6" stroke-width="2"/>
      <line x1="386" y1="72" x2="444" y2="72" stroke="#3b82f6" stroke-width="2"/>

      <!-- Area 1 on Left -->
      <rect x="30" y="125" width="200" height="80" rx="6" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
      <text x="130" y="145" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Area 1 (Local Area)</text>
      <circle cx="70" cy="175" r="14" fill="#10b981"/>
      <text x="70" y="179" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">R1</text>
      <circle cx="150" cy="175" r="14" fill="#10b981"/>
      <text x="150" y="179" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">R2</text>
      <line x1="84" y1="175" x2="136" y2="175" stroke="#10b981" stroke-width="2"/>
      <line x1="164" y1="175" x2="270" y2="84" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3"/>

      <!-- Area 2 on Right -->
      <rect x="510" y="125" width="200" height="80" rx="6" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
      <text x="610" y="145" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Area 2 (Local Area)</text>
      <circle cx="560" cy="175" r="14" fill="#10b981"/>
      <text x="560" y="179" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">R3</text>
      <circle cx="640" cy="175" r="14" fill="#10b981"/>
      <text x="640" y="179" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">R4</text>
      <line x1="574" y1="175" x2="626" y2="175" stroke="#10b981" stroke-width="2"/>
      <line x1="560" y1="161" x2="470" y2="84" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3"/>

      <!-- ASBR Gateway to outside -->
      <circle cx="370" cy="175" r="16" fill="#ef4444"/>
      <text x="370" y="179" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">ASBR</text>
      <line x1="370" y1="88" x2="370" y2="159" stroke="#ef4444" stroke-width="2"/>
      <text x="370" y="202" font-size="9" font-weight="700" fill="#991b1b" text-anchor="middle">To other ASs (BGP)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 4.9 — Hierarchical OSPF: Backbone Area 0, Area Border Routers (ABRs), and AS Boundary Router (ASBR) (§4.6.2).</div>
</div>

<h3>Inter-AS Routing: BGP (Border Gateway Protocol, BGP-4)</h3>
<p>BGP (RFC 4271) is the glue that holds the Internet together. It is a <strong>Path-Vector protocol</strong> running reliably over <strong>TCP port 179</strong>.</p>
<ul>
  <li><strong>eBGP (External BGP):</strong> Exchanges prefix reachability between gateway routers in <em>different</em> Autonomous Systems.</li>
  <li><strong>iBGP (Internal BGP):</strong> Propagates exterior prefix reachability to all routers <em>inside the same</em> Autonomous System.</li>
</ul>

<div class="callout callout-def">
  <div class="callout-header">📘 Key BGP Attributes: AS-PATH & NEXT-HOP</div>
  When a router advertises a prefix across a BGP session, it includes BGP attributes:
  <ul>
    <li><strong><code>AS-PATH</code>:</strong> Contains the list of ASs through which the prefix advertisement has passed. Crucially used for <strong>loop detection</strong>: if a router sees its own AS number in an incoming <code>AS-PATH</code>, it rejects the advertisement immediately!</li>
    <li><strong><code>NEXT-HOP</code>:</strong> The IP address of the router interface that begins the <code>AS-PATH</code>.</li>
  </ul>
</div>

<h3>BGP Route Selection Algorithm</h3>
<p>If a router learns multiple paths to the same destination prefix, it applies the following priority rules sequentially:</p>
<ol>
  <li><strong>Local Preference:</strong> Policy-assigned value; route with highest local preference is chosen.</li>
  <li><strong>Shortest AS-PATH:</strong> Route with fewest AS hops is preferred.</li>
  <li><strong>Closest NEXT-HOP Router (Hot-Potato Routing):</strong> Choose the route with the smallest internal intra-AS cost (get the packet out of your own network as quickly as possible!).</li>
  <li><strong>BGP Identifiers:</strong> Lowest router ID tiebreaker.</li>
</ol>
""",
            "quiz": [
                {
                    "q": "What transport-layer protocol and port does BGP use for establishing peering sessions between routers?",
                    "opts": [
                        "UDP port 520",
                        "TCP port 179",
                        "Directly over IP protocol 89",
                        "ICMP type 11"
                    ],
                    "ans": 1,
                    "exp": "BGP establishes reliable peering sessions over TCP port 179 (§4.6.3)."
                },
                {
                    "q": "How does BGP detect and prevent routing loops between autonomous systems?",
                    "opts": [
                        "Using the 16-bit UDP checksum",
                        "By inspecting the AS-PATH attribute: if an AS sees its own AS number in the list, it rejects the advertisement",
                        "By enforcing a 15-hop limit like RIP",
                        "Through TCP 3-way handshake sequence synchronization"
                    ],
                    "ans": 1,
                    "exp": "The AS-PATH attribute lists all traversed ASs; if an AS sees its own ASN in the AS-PATH, it drops the route to prevent loops (§4.6.3)."
                }
            ]
        },
        {
            "id": "ch4-7",
            "num": "4.7",
            "title": "Broadcast and Multicast Routing",
            "subtitle": "Flooding, Reverse Path Forwarding (RPF), Spanning Tree, and Multicast IGMP/PIM",
            "content": r"""
<p>In <strong>broadcast routing</strong>, the network layer delivers a packet from a source to <em>all</em> nodes in the network. In <strong>multicast routing</strong>, a packet is delivered to a <em>selected group</em> of nodes (a multicast group).</p>

<h3>Broadcast Routing: Reverse Path Forwarding (RPF)</h3>
<p>Simple flooding causes <strong>broadcast storms</strong> (infinite duplicate loops). <strong>Reverse Path Forwarding (RPF)</strong> provides elegant, loop-free flooding without requiring routers to know the entire spanning tree:</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 The Reverse Path Forwarding (RPF) Rule</div>
  When a router receives a broadcast packet from source <span class="math-inline"><i>S</i></span>:
  <ol>
    <li>Check if the packet arrived on the interface that this router would use to send unicast traffic <strong>back to source <span class="math-inline"><i>S</i></span></strong> (along its shortest path).</li>
    <li>If <strong>YES</strong>: The router transmits copies of the packet out onto all other outgoing interfaces.</li>
    <li>If <strong>NO</strong>: The router <strong>drops the packet immediately</strong>!</li>
  </ol>
</div>

<h3>Multicast Routing</h3>
<p>Multicast packets are addressed to a Class D multicast IP group (<code>224.0.0.0</code> to <code>239.255.255.255</code>). Two protocols cooperate:</p>
<ul>
  <li><strong>IGMP (Internet Group Management Protocol, RFC 3376):</strong> Runs between a host and its directly attached local router, allowing hosts to join or leave multicast groups.</li>
  <li><strong>Multicast Routing Protocols:</strong> Build delivery trees across routers:
    <ol>
      <li><strong>Source-Based Trees (e.g. DVMRP, PIM-DM):</strong> Constructs a unique shortest-path tree rooted at each sender using Reverse Path Multicasting with <em>prune messages</em>.</li>
      <li><strong>Group-Shared Trees (e.g. PIM-SM):</strong> All senders send to a central <strong>Rendezvous Point (RP)</strong>, and receivers join a shared tree rooted at the RP.</li>
    </ol>
  </li>
</ul>
""",
            "quiz": [
                {
                    "q": "Under Reverse Path Forwarding (RPF), when does a router forward an arriving broadcast packet?",
                    "opts": [
                        "Always on all interfaces",
                        "Only if the packet arrived on the interface that the router uses to reach the source along its shortest path",
                        "Only if the packet contains an IGMP membership query",
                        "Only if the packet TTL is equal to 1"
                    ],
                    "ans": 1,
                    "exp": "Under RPF, a packet is accepted and forwarded only if it arrives on the ingress interface corresponding to the shortest path back to the sender (§4.7.1)."
                }
            ]
        },
        {
            "id": "ch4-8",
            "num": "4.8",
            "title": "Chapter 4 Summary & Worked Problems",
            "subtitle": "Comprehensive worked problems: Subnetting, IPv4 Fragmentation, and Dijkstra's Algorithm",
            "content": r"""
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 1: Subnetting Breakdown</div>
    <span class="interactive-badge">P12 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Consider the subnet prefix <code>128.119.40.128/26</code>.</p>
  <p>(a) What is the subnet mask in dotted-decimal notation?</p>
  <p>(b) How many total IP addresses are in this subnet?</p>
  <p>(c) How many usable host IP addresses are available?</p>
  <p>(d) What is the broadcast address for this subnet?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch4-prob1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch4-prob1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Prefix is /26 &rarr; 26 ones followed by 6 zeros in binary: <code>11111111.11111111.11111111.11000000</code>.</div>
    <div class="calc-step">Step 2: Subnet Mask = <code>255.255.255.192</code>.</div>
    <div class="calc-step">Step 3: Host bits <span class="math-inline"><i>h</i> = 32 &minus; 26 = 6</span>. Total addresses = <span class="math-inline">2<sup>6</sup> = <strong>64</strong></span>.</div>
    <div class="calc-step">Step 4: Usable host addresses = <span class="math-inline">2<sup>6</sup> &minus; 2 = 64 &minus; 2 = <strong>62 hosts</strong></span>.</div>
    <div class="calc-step">Step 5: Subnet starts at <code>128.119.40.128</code>. Adding 63 (binary 111111):</div>
    <div class="calc-step">Final Answer: Broadcast address is <code>128.119.40.191</code>. Usable range: <code>128.119.40.129</code> to <code>128.119.40.190</code>.</div>
  </div>
</div>

<div class="interactive-card" style="margin-top:1.5rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 2: IPv4 Datagram Fragmentation</div>
    <span class="interactive-badge">P19 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> A 4000-byte IPv4 datagram (20 bytes IP header + 3980 bytes payload) arrives at a router and must be forwarded over a link with MTU = 1500 bytes.</p>
  <p>Compute the total length, payload data length, identification, fragment offset, and More-Fragments (MF) flag for each fragment generated.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch4-prob2-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch4-prob2-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Maximum IP payload per fragment = MTU &minus; 20 = 1500 &minus; 20 = 1480 bytes.</div>
    <div class="calc-step">Notice: 1480 is divisible by 8 (<span class="math-inline">1480 / 8 = 185</span>), which satisfies the 8-byte offset rule.</div>
    <div class="calc-step"><strong>Fragment 1:</strong> Total Length = 1500 B (20B header + 1480B data). Data bytes 0 to 1479. Offset = <span class="math-inline">0 / 8 = 0</span>. MF = 1.</div>
    <div class="calc-step"><strong>Fragment 2:</strong> Total Length = 1500 B (20B header + 1480B data). Data bytes 1480 to 2959. Offset = <span class="math-inline">1480 / 8 = <strong>185</strong></span>. MF = 1.</div>
    <div class="calc-step"><strong>Fragment 3:</strong> Remaining payload = <span class="math-inline">3980 &minus; 2960 = 1020</span> bytes. Total Length = <span class="math-inline">1020 + 20 = 1040</span> bytes. Data bytes 2960 to 3979. Offset = <span class="math-inline">2960 / 8 = <strong>370</strong></span>. MF = 0 (last fragment!).</div>
    <div class="calc-step">Final Answer: 3 fragments generated with offsets 0, 185, 370 and MF flags 1, 1, 0.</div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "For an IPv4 datagram fragmented across an MTU of 1500 bytes, what is the Fragment Offset of the 3rd fragment if each prior fragment carried 1480 bytes of data?",
                    "opts": [
                        "185",
                        "2960",
                        "370",
                        "740"
                    ],
                    "ans": 2,
                    "exp": "Prior data bytes = 1480 * 2 = 2960 bytes. Offset = 2960 / 8 = 370 (§4.4.1)."
                }
            ]
        }
    ]
}
