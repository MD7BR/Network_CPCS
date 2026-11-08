"""Chapter 3 Data: Transport Layer (Kurose & Ross 6th & 8th Ed.)
Exhaustive textbook depth, Midterm Study Guide integration (P17-P24), bit-accurate diagrams,
and fully functional interactive calculators and steppers.
"""

CH3_DATA = {
    "id": "ch3",
    "num": 3,
    "title": "Transport Layer",
    "subtitle": "Multiplexing/Demultiplexing, UDP, Reliable Data Transfer (rdt), TCP & Congestion Control",
    "layer": "Transport Layer",
    "color": "#2563eb",
    "objectives": [
        "Contrast transport-layer and network-layer services using the 12-kids household postal analogy",
        "Explain multiplexing and demultiplexing and compare 2-tuple (UDP) vs 4-tuple (TCP) demux",
        "Explain why UDP exists, deconstruct its 8-byte header, and compute the 16-bit Internet checksum",
        "Trace the evolution of RDT protocols: rdt 1.0 -> 2.0 -> 2.1 -> 2.2 -> 3.0",
        "Draw and analyze the 4 rdt 3.0 scenarios (no loss, packet loss, ACK loss, premature timeout)",
        "Compute stop-and-wait channel utilization and calculate required window size for pipelining",
        "Compare Go-Back-N (GBN) cumulative ACKs with Selective Repeat (SR) and resolve the SR dilemma",
        "Deconstruct the bit-accurate TCP segment header and explain all 6 control flags",
        "Trace multi-step TCP sequence numbers, cumulative ACKs, out-of-order gap buffering, and Telnet echo",
        "Calculate TCP EstimatedRTT, DevRTT, and TimeoutInterval (RTO) using EWMA formulas",
        "Analyze TCP Fast Retransmit on 3 duplicate ACKs and explain RFC 5681 receiver ACK generation",
        "Formulate TCP flow control (rwnd = RcvBuffer - buffered data) and explain 1-byte probing",
        "Explain why the 2-way handshake fails, trace the 3-way handshake, teardown (TIME_WAIT), and SYN cookies",
        "Simulate TCP Congestion Control: AIMD sawtooth, Slow Start, Congestion Avoidance, and Fast Recovery"
    ],
    "sections": [
        {
            "id": "ch3-1",
            "num": "3.1",
            "title": "Transport-Layer Services",
            "subtitle": "Relationship between Transport and Network Layers, and the Household Postal Analogy",
            "content": r"""
<p>A transport-layer protocol provides for <strong>logical communication</strong> between <em>application processes</em> running on different hosts. From an application process's perspective, it appears as if the hosts were directly connected, whereas in reality they may be on opposite sides of the planet connected by dozens of routers and diverse physical links.</p>

<p>Transport-layer protocols are implemented <strong>strictly in the end systems</strong> (hosts), not in network routers. Core routers inspect only network-layer fields (IP addresses); they do not inspect or modify transport-layer segments.</p>

<div class="callout callout-insight">
  <div class="callout-header">💡 The 12-Kids Household Postal Analogy (Kurose & Ross §3.1)</div>
  Consider two large family households: one on the East Coast with 12 kids (including cousin Ann), and one on the West Coast with 12 kids (including cousin Bill).
  <ul>
    <li>The kids write letters to each other every week (<strong>Application messages</strong>).</li>
    <li>In each house, one kid (Ann on East Coast, Bill on West Coast) collects letters from all siblings and distributes arriving letters to individual brothers and sisters (<strong>Transport-layer protocol: multiplexing & demultiplexing</strong>).</li>
    <li>The postal trucks and mail carriers transport mail bags between the two houses (<strong>Network-layer protocol: host-to-host delivery</strong>).</li>
  </ul>
  <em>Key take-away: Ann and Bill do not drive mail trucks between cities (they operate only inside the house), nor does the postal carrier deliver mail directly into the hands of a specific child in their bedroom! Transport protocols provide process-to-process communication on top of host-to-host network delivery.</em>
</div>

<!-- FIGURE 3.1: TRANSPORT VS NETWORK LAYER -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <!-- Host A -->
      <rect x="40" y="25" width="210" height="170" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="2"/>
      <text x="145" y="48" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">End System A (East Coast)</text>
      <!-- Processes -->
      <rect x="55" y="60" width="85" height="30" rx="4" fill="#ede9fe" stroke="#8b5cf6"/>
      <text x="97" y="79" font-size="9.5" font-weight="600" fill="#6d28d9" text-anchor="middle">Process P1</text>
      <rect x="150" y="60" width="85" height="30" rx="4" fill="#ede9fe" stroke="#8b5cf6"/>
      <text x="192" y="79" font-size="9.5" font-weight="600" fill="#6d28d9" text-anchor="middle">Process P2</text>
      <!-- Transport Layer -->
      <rect x="55" y="100" width="180" height="34" rx="4" fill="#dbeafe" stroke="#2563eb"/>
      <text x="145" y="121" font-size="10.5" font-weight="700" fill="#1e40af" text-anchor="middle">Transport Layer (Ann)</text>
      <!-- Network Layer -->
      <rect x="55" y="144" width="180" height="34" rx="4" fill="#d1fae5" stroke="#10b981"/>
      <text x="145" y="165" font-size="10.5" font-weight="700" fill="#047857" text-anchor="middle">Network Layer (IP)</text>

      <!-- Host B -->
      <rect x="510" y="25" width="210" height="170" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="2"/>
      <text x="615" y="48" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">End System B (West Coast)</text>
      <!-- Processes -->
      <rect x="525" y="60" width="85" height="30" rx="4" fill="#ede9fe" stroke="#8b5cf6"/>
      <text x="567" y="79" font-size="9.5" font-weight="600" fill="#6d28d9" text-anchor="middle">Process P3</text>
      <rect x="620" y="60" width="85" height="30" rx="4" fill="#ede9fe" stroke="#8b5cf6"/>
      <text x="662" y="79" font-size="9.5" font-weight="600" fill="#6d28d9" text-anchor="middle">Process P4</text>
      <!-- Transport Layer -->
      <rect x="525" y="100" width="180" height="34" rx="4" fill="#dbeafe" stroke="#2563eb"/>
      <text x="615" y="121" font-size="10.5" font-weight="700" fill="#1e40af" text-anchor="middle">Transport Layer (Bill)</text>
      <!-- Network Layer -->
      <rect x="525" y="144" width="180" height="34" rx="4" fill="#d1fae5" stroke="#10b981"/>
      <text x="615" y="165" font-size="10.5" font-weight="700" fill="#047857" text-anchor="middle">Network Layer (IP)</text>

      <!-- Logical Process-to-Process Communication Arrow -->
      <path d="M 235 117 L 525 117" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="5 5"/>
      <text x="380" y="108" font-size="11" font-weight="700" fill="#2563eb" text-anchor="middle">Logical Process-to-Process Communication</text>

      <!-- Physical Routers Core below -->
      <circle cx="320" cy="161" r="18" fill="#10b981"/>
      <text x="320" y="165" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">R1</text>
      <circle cx="440" cy="161" r="18" fill="#10b981"/>
      <text x="440" y="165" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">R2</text>
      <line x1="235" y1="161" x2="302" y2="161" stroke="#10b981" stroke-width="2"/>
      <line x1="338" y1="161" x2="422" y2="161" stroke="#10b981" stroke-width="2"/>
      <line x1="458" y1="161" x2="525" y2="161" stroke="#10b981" stroke-width="2"/>
      <text x="380" y="195" font-size="10" font-weight="600" fill="#047857" text-anchor="middle">Physical Host-to-Host Delivery (Network Layer)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 3.1 — Transport-layer process-to-process communication vs Network-layer host-to-host delivery (§3.1).</div>
</div>
""",
            "quiz": [
                {
                    "q": "In the 12-kids household postal analogy, what corresponds to the transport-layer protocol?",
                    "opts": [
                        "The letters written by the children",
                        "The postal carrier driving the truck between cities",
                        "Ann and Bill collecting and distributing letters within their respective houses",
                        "The envelope paper and ink"
                    ],
                    "ans": 2,
                    "exp": "Ann and Bill multiplex letters from siblings into mailbags and demultiplex arriving letters to individual kids. The postal service is the network layer (§3.1)."
                }
            ]
        },
        {
            "id": "ch3-2",
            "num": "3.2",
            "title": "Multiplexing and Demultiplexing",
            "subtitle": "Port numbers, 2-tuple connectionless demux vs 4-tuple connection-oriented demux",
            "content": r"""
<p>A destination host receives IP datagrams from the network layer. Each datagram carries a transport segment. Delivering the segment data to the correct application socket is called <strong>demultiplexing</strong>. Gathering data chunks from multiple application sockets at the source host, prefixing them with transport headers, and passing them to the network layer is called <strong>multiplexing</strong>.</p>

<h3>Port Numbers (RFC 1700)</h3>
<p>Port numbers are 16-bit integers ranging from 0 to 65535:</p>
<ul>
  <li><strong>Well-Known Ports (0 to 1023):</strong> Standard services (HTTP: 80, HTTPS: 443, DNS: 53, SMTP: 25, FTP: 20/21, SSH: 22). Restricted to privileged/root processes.</li>
  <li><strong>Registered Ports (1024 to 49151):</strong> Registered for vendor applications.</li>
  <li><strong>Dynamic / Private / Ephemeral Ports (49152 to 65535):</strong> Assigned automatically by the OS to client processes upon socket creation.</li>
</ul>

<div class="callout callout-def">
  <div class="callout-header">📘 Connectionless (UDP) Demultiplexing: 2-Tuple</div>
  A UDP socket is identified solely by a <strong>2-tuple</strong>:
  <div class="math-display">
    (\text{Destination IP Address}, \ \text{Destination Port Number})
  </div>
  If two UDP datagrams originate from completely different source IP addresses or different source port numbers, but have the <em>same</em> destination IP and destination port number, both datagrams will be directed to the <strong>exact same destination socket</strong>!
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 Connection-Oriented (TCP) Demultiplexing: 4-Tuple</div>
  A TCP socket is identified by a <strong>4-tuple</strong>:
  <div class="math-display">
    (\text{Source IP}, \ \text{Source Port}, \ \text{Destination IP}, \ \text{Destination Port})
  </div>
  When a TCP segment arrives at a host, the OS uses <strong>all four fields</strong> to demultiplex the segment to the specific connection socket.
  <br><em>Exam Example (Study Guide P17b):</em> A web server listens on port 80 (welcoming socket). Client A (IP: <code>192.168.1.10</code>, Port: <code>4001</code>) and Client B (IP: <code>192.168.1.20</code>, Port: <code>4001</code>) both connect to port 80. Although both clients chose source port 4001 and destination port 80, the server creates <strong>two separate connection sockets</strong> because their Source IP addresses differ!
</div>
""",
            "quiz": [
                {
                    "q": "Two UDP datagrams arrive at Host C on destination port 5353: one from (Host A, Port 4001) and one from (Host B, Port 4002). How many sockets at C receive them?",
                    "opts": [
                        "Two distinct sockets",
                        "One socket: UDP demultiplexes by destination port only, so both datagrams go to the same socket bound to 5353",
                        "Zero: the second packet is rejected as a duplicate",
                        "Four sockets"
                    ],
                    "ans": 1,
                    "exp": "UDP uses a 2-tuple (dst IP, dst port). Because both datagrams share the same destination port 5353 on Host C, both are delivered to the exact same UDP socket (§3.2 / P17a)."
                },
                {
                    "q": "Two TCP clients connect to a Web server on port 80: one from (Host A, Port 4001) and one from (Host B, Port 4001). How many connection sockets are created at the server?",
                    "opts": [
                        "One shared connection socket",
                        "Two connection sockets (plus the welcoming socket), because TCP uses the 4-tuple and their source IPs differ",
                        "Zero, because source ports clash",
                        "Three connection sockets"
                    ],
                    "ans": 1,
                    "exp": "TCP demultiplexes by 4-tuple (src IP, src port, dst IP, dst port). Since the source IPs differ, the server instantiates two separate connection sockets (§3.2 / P17b)."
                }
            ]
        },
        {
            "id": "ch3-3",
            "num": "3.3",
            "title": "Connectionless Transport: UDP",
            "subtitle": "UDP segment structure, advantages, and the 16-bit Internet Checksum algorithm",
            "content": r"""
<p><strong>UDP (User Datagram Protocol, RFC 768)</strong> is the minimal transport protocol. It takes application messages, attaches an 8-byte header, and hands the segment to the network layer.</p>

<h3>Why Would an Application Choose UDP over TCP?</h3>
<ol>
  <li><strong>Finer Application Control Over What Data Is Sent, and When:</strong> UDP does not throttle sending rates via congestion control. Real-time applications can pump data at a constant rate and tolerate minor packet loss.</li>
  <li><strong>No Connection Establishment Delay:</strong> UDP does not introduce any connection 3-way handshake delay. This is why DNS uses UDP (name lookup completes in 1 RTT).</li>
  <li><strong>No Connection State:</strong> TCP maintains receive/send buffers, congestion parameters, and sequence numbers. A server running UDP can support vastly more active clients simultaneously because it maintains zero state.</li>
  <li><strong>Small Header Overhead:</strong> UDP header is only <strong>8 bytes</strong>, whereas TCP's base header is <strong>20 bytes</strong>.</li>
</ol>

<!-- FIGURE 3.2: BIT-ACCURATE UDP HEADER -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 680 160" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <text x="30" y="20" font-size="10" fill="#64748b">Bit 0</text>
      <text x="335" y="20" font-size="10" fill="#64748b">15 16</text>
      <text x="640" y="20" font-size="10" fill="#64748b">31</text>
      <line x1="30" y1="25" x2="650" y2="25" stroke="#cbd5e1" stroke-width="1"/>

      <!-- Row 1: Source & Dest Port -->
      <rect x="30" y="30" width="310" height="35" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="185" y="52" font-size="12" font-weight="700" text-anchor="middle" fill="#1e40af">Source Port # (16 bits)</text>
      <rect x="340" y="30" width="310" height="35" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="495" y="52" font-size="12" font-weight="700" text-anchor="middle" fill="#1e40af">Destination Port # (16 bits)</text>

      <!-- Row 2: Length & Checksum -->
      <rect x="30" y="65" width="310" height="35" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="185" y="87" font-size="12" font-weight="700" text-anchor="middle" fill="#1e40af">Length in bytes (16 bits)</text>
      <rect x="340" y="65" width="310" height="35" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="495" y="87" font-size="12" font-weight="700" text-anchor="middle" fill="#1e40af">Checksum (16 bits)</text>

      <!-- Row 3: Application Data -->
      <rect x="30" y="100" width="620" height="40" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="340" y="125" font-size="12" font-weight="700" text-anchor="middle" fill="#6d28d9">Application Data (Payload)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 3.2 — Bit-accurate UDP Segment Header (8 bytes total overhead) (§3.3.1).</div>
</div>

<h3>The 16-Bit Internet Checksum Algorithm</h3>
<div class="callout callout-formula">
  <div class="callout-header">🧮 1's Complement Checksum Calculation Steps (Study Guide P18)</div>
  <ol>
    <li>Treat all 16-bit words in the segment (including header and pseudo-header) as unsigned 16-bit integers.</li>
    <li>Add them together using binary addition.</li>
    <li><strong>End-Around Carry (Wraparound):</strong> If a carry bit spills out of the 16th most significant bit, add it back to the least significant bit.</li>
    <li>Take the <strong>1's complement</strong> of the wrapped sum (invert every bit: flip 0s to 1s and 1s to 0s). This is the checksum stored in the header.</li>
    <li><strong>Receiver Verification:</strong> The receiver adds all 16-bit words <em>plus</em> the checksum. If no bits were corrupted, the result must be <strong>all 1s (<code>1111 1111 1111 1111</code> = <code>0xFFFF</code>)</strong>! If any single bit is 0, an error occurred.</li>
  </ol>
</div>

<!-- EMBEDDED INTERACTIVE: UDP CHECKSUM CALCULATOR -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🧮 Live 16-Bit Internet Checksum Calculator</div>
    <span class="interactive-badge">Study Guide P18 Worked Math</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Enter two 16-bit hex words (e.g. from P18: <code>5CA3</code> and <code>C675</code>) to see the live binary addition, wraparound carry, and bit inversion:
  </p>
  <div class="grid-2">
    <div class="form-group">
      <label class="form-label">16-bit Hex Word 1:</label>
      <input type="text" id="sec3-word1" class="form-input" value="5CA3" oninput="calcSec3Checksum()">
    </div>
    <div class="form-group">
      <label class="form-label">16-bit Hex Word 2:</label>
      <input type="text" id="sec3-word2" class="form-input" value="C675" oninput="calcSec3Checksum()">
    </div>
  </div>
  <div id="sec3-checksum-result" class="calc-result-box" style="margin-top:1rem;">
    <!-- Populated live by calcSec3Checksum() -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the total header size of a standard UDP datagram?",
                    "opts": [
                        "4 bytes",
                        "8 bytes (4 fields of 16 bits each)",
                        "20 bytes",
                        "32 bytes"
                    ],
                    "ans": 1,
                    "exp": "UDP header consists of 4 fields: source port, destination port, length, and checksum (each 16 bits = 2 bytes), totaling 8 bytes (§3.3)."
                },
                {
                    "q": "What binary result must the receiver obtain when adding all received 16-bit words plus the checksum if NO bit errors occurred?",
                    "opts": [
                        "All zeros (0x0000)",
                        "All ones (1111 1111 1111 1111 / 0xFFFF)",
                        "The original source port number",
                        "The IP address of the sender"
                    ],
                    "ans": 1,
                    "exp": "Because the checksum is the bit-inverted 1's complement of the sum, adding the sum to its inverted value must yield all 1s (0xFFFF). Any 0 indicates an error (§3.3 / P18)."
                }
            ]
        },
        {
            "id": "ch3-4",
            "num": "3.4",
            "title": "Principles of Reliable Data Transfer (RDT)",
            "subtitle": "Evolution from rdt 1.0 to 3.0, pipelined protocols, Go-Back-N, and Selective Repeat",
            "content": r"""
<p>The problem of reliable data transfer occurs not only at the transport layer, but also at the application and link layers. We trace the step-by-step design of reliable protocols over increasingly unreliable channels:</p>

<h3>Evolution of RDT Protocols</h3>
<ul>
  <li><strong>rdt 1.0 (Completely Reliable Channel):</strong> Underlying channel has zero bit errors and zero packet loss. Sender simply sends; receiver simply receives.</li>
  <li><strong>rdt 2.0 (Channel with Bit Errors):</strong> Employs <strong>stop-and-wait</strong>. Adds:
    <ol>
      <li><strong>Error detection:</strong> Checksum bits.</li>
      <li><strong>Receiver feedback:</strong> Positive ACKs (acknowledgments) and negative NAKs (negative acknowledgments).</li>
      <li><strong>Retransmission:</strong> Sender retransmits on NAK.</li>
    </ol>
    <span style="color:var(--danger-text); font-weight:700;">Fatal Flaw of rdt 2.0:</span> What if an ACK or NAK message itself gets corrupted on the return path? If the sender receives a corrupted ACK/NAK, it cannot know whether the packet was received correctly!
  </li>
  <li><strong>rdt 2.1 (Handling Corrupted ACKs/NAKs):</strong> Sender adds a <strong>1-bit sequence number</strong> (0 or 1) to each packet. If the receiver gets a duplicate packet with the sequence number it already received, it discards the duplicate data and re-sends an ACK.</li>
  <li><strong>rdt 2.2 (NAK-Free Protocol):</strong> Receiver sends duplicate ACKs instead of NAKs. The receiver ACKs the <em>last packet received correctly</em>, explicitly including the sequence number (e.g. <code>ACK 0</code>). An ACK for packet 0 received while waiting for packet 1 acts as an implicit NAK for packet 1!</li>
  <li><strong>rdt 3.0 (Channel with Errors and Packet Loss):</strong> Senders add a <strong>countdown timer</strong>. If no ACK arrives before the timer expires, the sender assumes the packet (or ACK) was lost and retransmits. Also known as the <em>alternating-bit protocol</em>.</li>
</ul>

<!-- FIGURE 3.3: THE 4 RDT 3.0 SCENARIOS -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 880 250" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <!-- Scenario A: No Loss -->
      <g transform="translate(15, 20)">
        <text x="95" y="15" font-size="11" font-weight="700" fill="#10b981" text-anchor="middle">(a) Operation with No Loss</text>
        <line x1="30" y1="30" x2="30" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="160" y1="30" x2="160" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="30" y1="50" x2="160" y2="75" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="60" font-size="8.5" fill="#1e40af" text-anchor="middle">pkt 0</text>
        <line x1="160" y1="75" x2="30" y2="100" stroke="#10b981" stroke-width="2"/>
        <text x="95" y="85" font-size="8.5" fill="#047857" text-anchor="middle">ack 0</text>
        <line x1="30" y1="110" x2="160" y2="135" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="120" font-size="8.5" fill="#1e40af" text-anchor="middle">pkt 1</text>
        <line x1="160" y1="135" x2="30" y2="160" stroke="#10b981" stroke-width="2"/>
        <text x="95" y="145" font-size="8.5" fill="#047857" text-anchor="middle">ack 1</text>
      </g>

      <!-- Scenario B: Packet Loss -->
      <g transform="translate(230, 20)">
        <text x="95" y="15" font-size="11" font-weight="700" fill="#ef4444" text-anchor="middle">(b) Packet Loss</text>
        <line x1="30" y1="30" x2="30" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="160" y1="30" x2="160" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <!-- Lost packet -->
        <line x1="30" y1="50" x2="100" y2="65" stroke="#ef4444" stroke-width="2"/>
        <text x="110" y="68" font-size="11" fill="#ef4444">❌</text>
        <text x="75" y="55" font-size="8.5" fill="#ef4444" text-anchor="middle">pkt 1 (lost!)</text>
        <!-- Timeout & retransmit -->
        <line x1="30" y1="120" x2="160" y2="145" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="130" font-size="8.5" fill="#1e40af" text-anchor="middle">pkt 1 (retransmit)</text>
        <line x1="160" y1="145" x2="30" y2="170" stroke="#10b981" stroke-width="2"/>
        <text x="95" y="155" font-size="8.5" fill="#047857" text-anchor="middle">ack 1</text>
      </g>

      <!-- Scenario C: ACK Loss -->
      <g transform="translate(445, 20)">
        <text x="95" y="15" font-size="11" font-weight="700" fill="#f59e0b" text-anchor="middle">(c) ACK Loss</text>
        <line x1="30" y1="30" x2="30" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="160" y1="30" x2="160" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="30" y1="50" x2="160" y2="75" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="60" font-size="8.5" fill="#1e40af" text-anchor="middle">pkt 1</text>
        <!-- Lost ACK -->
        <line x1="160" y1="75" x2="90" y2="90" stroke="#ef4444" stroke-width="2"/>
        <text x="80" y="93" font-size="11" fill="#ef4444">❌</text>
        <text x="125" y="80" font-size="8.5" fill="#ef4444" text-anchor="middle">ack 1 (lost!)</text>
        <!-- Timeout retransmits dup pkt -->
        <line x1="30" y1="125" x2="160" y2="150" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="135" font-size="8.5" fill="#1e40af" text-anchor="middle">pkt 1 (dup)</text>
        <line x1="160" y1="150" x2="30" y2="175" stroke="#10b981" stroke-width="2"/>
        <text x="95" y="160" font-size="8.5" fill="#047857" text-anchor="middle">ack 1 (resend)</text>
      </g>

      <!-- Scenario D: Premature Timeout -->
      <g transform="translate(660, 20)">
        <text x="95" y="15" font-size="11" font-weight="700" fill="#8b5cf6" text-anchor="middle">(d) Premature Timeout</text>
        <line x1="30" y1="30" x2="30" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="160" y1="30" x2="160" y2="200" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="30" y1="50" x2="160" y2="75" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="60" font-size="8.5" fill="#1e40af" text-anchor="middle">pkt 1</text>
        <!-- Premature timeout fires early -->
        <line x1="30" y1="95" x2="160" y2="120" stroke="#8b5cf6" stroke-width="2"/>
        <text x="95" y="105" font-size="8.5" fill="#6d28d9" text-anchor="middle">pkt 1 (premature)</text>
        <!-- Delayed ACK arrives -->
        <line x1="160" y1="75" x2="30" y2="135" stroke="#10b981" stroke-width="2"/>
        <text x="85" y="145" font-size="8.5" fill="#047857" text-anchor="middle">ack 1</text>
        <!-- Second ACK arrives -->
        <line x1="160" y1="120" x2="30" y2="175" stroke="#10b981" stroke-width="2"/>
        <text x="95" y="165" font-size="8.5" fill="#047857" text-anchor="middle">ack 1 (dup)</text>
      </g>
    </svg>
  </div>
  <div class="figure-caption">Figure 3.3 — The four rdt 3.0 operational scenarios: (a) No loss, (b) Packet loss, (c) ACK loss, (d) Premature timeout (§3.4.1).</div>
</div>

<h3>Pipelining and Channel Utilization</h3>
<p>In stop-and-wait protocols, the sender must wait an entire round-trip time before sending the next packet:</p>
<div class="math-display">
  U_{\text{sender}} = \frac{L / R}{\text{RTT} + (L / R)}
</div>
<p>On a 100 Mbps cross-country link (<span class="math-inline">\text{RTT} = 30\text{ ms}, L = 1,000\text{ bytes} = 8,000\text{ bits}</span>):</p>
<div class="math-display">
  d_{\text{trans}} = \frac{8,000}{10^8} = 0.08\text{ ms} \implies U_{\text{sender}} = \frac{0.08}{30 + 0.08} \approx \mathbf{0.0027} \ (0.27\%)
</div>
<p>The channel is idle 99.73% of the time! <strong>Pipelining</strong> solves this by allowing up to <span class="math-inline">N</span> packets to be in flight simultaneously:</p>
<div class="math-display">
  U_{\text{pipelined}} = \frac{N \cdot (L / R)}{\text{RTT} + (L / R)}
</div>

<h3>Go-Back-N (GBN) vs Selective Repeat (SR)</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.85rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:6px 10px;">Feature</th>
      <th style="padding:6px 10px;">Go-Back-N (GBN)</th>
      <th style="padding:6px 10px;">Selective Repeat (SR)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700;">ACK Strategy</td>
      <td style="padding:6px 10px;"><strong>Cumulative ACK:</strong> ACK <span class="math-inline">n</span> confirms all packets up to <span class="math-inline">n</span>.</td>
      <td style="padding:6px 10px;"><strong>Individual ACK:</strong> Each packet is individually acknowledged.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700;">Sender Timers</td>
      <td style="padding:6px 10px;">Single timer for the <em>oldest unacknowledged packet</em>.</td>
      <td style="padding:6px 10px;">Individual logical timer for <em>each unacknowledged packet</em>.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700;">Out-of-Order Packets</td>
      <td style="padding:6px 10px; color:var(--danger-text);"><strong>Discarded!</strong> Receiver maintains no buffer; re-ACKs highest in-order.</td>
      <td style="padding:6px 10px; color:var(--accent-text);"><strong>Buffered!</strong> Receiver buffers out-of-order packets until missing gap is filled.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700;">On Timeout</td>
      <td style="padding:6px 10px;">Retransmits <strong>all <span class="math-inline">N</span> packets</strong> in the current window!</td>
      <td style="padding:6px 10px;">Retransmits <strong>only the single timed-out packet</strong>.</td>
    </tr>
    <tr>
      <td style="padding:6px 10px; font-weight:700;">Window Size Constraint</td>
      <td style="padding:6px 10px;"><span class="math-inline">W \le 2^k - 1</span></td>
      <td style="padding:6px 10px;"><span class="math-inline">W \le 2^{k-1}</span> (Window size must be &le; half sequence space to prevent ambiguity).</td>
    </tr>
  </tbody>
</table>
""",
            "quiz": [
                {
                    "q": "What fatal flaw in rdt 2.0 motivated the introduction of sequence numbers in rdt 2.1?",
                    "opts": [
                        "rdt 2.0 lacked checksum error detection",
                        "If an ACK or NAK was corrupted, the sender could not tell whether the packet arrived; retransmitting caused duplicate packets that the receiver could not identify",
                        "rdt 2.0 did not support pipelining",
                        "rdt 2.0 timers were too short"
                    ],
                    "ans": 1,
                    "exp": "In rdt 2.0, corrupted feedback left the sender blind. Without sequence numbers, retransmitting resulted in undetected duplicate data at the receiver (§3.4 / P19a)."
                },
                {
                    "q": "If a protocol uses a 4-bit sequence number (range 0 to 15), what is the maximum permissible window size in Selective Repeat?",
                    "opts": [
                        "16",
                        "15",
                        "8 (half the sequence space: 2^(4-1) = 8)",
                        "4"
                    ],
                    "ans": 2,
                    "exp": "In Selective Repeat, window size W <= 2^(k-1) = 2^(4-1) = 8 to prevent window overlap ambiguity between old retransmissions and new packets (§3.4.4)."
                }
            ]
        },
        {
            "id": "ch3-5",
            "num": "3.5",
            "title": "Connection-Oriented Transport: TCP",
            "subtitle": "Segment structure, sequence/ACK numbers, RTT estimation, fast retransmit, flow control & handshakes",
            "content": r"""
<p><strong>TCP (Transmission Control Protocol, RFC 793)</strong> is the Internet's connection-oriented, reliable transport protocol. Key properties: point-to-point (single sender, single receiver), reliable in-order byte stream, full-duplex, pipelined, flow controlled, and congestion controlled.</p>

<!-- FIGURE 3.4: BIT-ACCURATE TCP HEADER -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 760 210" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <text x="30" y="20" font-size="10" fill="#64748b">Bit 0</text>
      <text x="370" y="20" font-size="10" fill="#64748b">15 16</text>
      <text x="730" y="20" font-size="10" fill="#64748b">31</text>
      <line x1="30" y1="25" x2="730" y2="25" stroke="#cbd5e1" stroke-width="1"/>

      <!-- Row 1: Source & Dest Port -->
      <rect x="30" y="30" width="350" height="32" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="205" y="50" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Source Port Number (16 bits)</text>
      <rect x="380" y="30" width="350" height="32" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="555" y="50" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Destination Port Number (16 bits)</text>

      <!-- Row 2: Sequence Number -->
      <rect x="30" y="62" width="700" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="380" y="82" font-size="11.5" font-weight="700" fill="#6d28d9" text-anchor="middle">Sequence Number (32 bits &bull; Byte-stream offset of first data byte)</text>

      <!-- Row 3: Acknowledgment Number -->
      <rect x="30" y="94" width="700" height="32" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="380" y="114" font-size="11.5" font-weight="700" fill="#6d28d9" text-anchor="middle">Acknowledgment Number (32 bits &bull; Next expected byte, cumulative)</text>

      <!-- Row 4: Header Len, Flags, Receive Window -->
      <rect x="30" y="126" width="90" height="32" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="75" y="146" font-size="9" font-weight="700" fill="#047857" text-anchor="middle">Data Offset (4b)</text>

      <rect x="120" y="126" width="90" height="32" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="165" y="146" font-size="9" font-weight="600" fill="#475569" text-anchor="middle">Reserved (6b)</text>

      <rect x="210" y="126" width="170" height="32" fill="#fed7aa" stroke="#f97316" stroke-width="1.5"/>
      <text x="295" y="146" font-size="9" font-weight="700" fill="#9a3412" text-anchor="middle">U A P R S F (6b Flags)</text>

      <rect x="380" y="126" width="350" height="32" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
      <text x="555" y="146" font-size="10.5" font-weight="700" fill="#b45309" text-anchor="middle">Receive Window rwnd (16 bits &bull; Flow Control)</text>

      <!-- Row 5: Checksum & Urgent Pointer -->
      <rect x="30" y="158" width="350" height="32" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="205" y="178" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Internet Checksum (16 bits)</text>
      <rect x="380" y="158" width="350" height="32" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="555" y="178" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">Urgent Pointer (16 bits)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 3.4 — Bit-accurate TCP 20-byte base header layout and 6 control flags (§3.5.2).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">🚩 TCP Control Flags Defined</div>
  <ul>
    <li><strong>SYN (Synchronize):</strong> Used exclusively during connection setup (3-way handshake).</li>
    <li><strong>ACK (Acknowledgment):</strong> Indicates that the Acknowledgment Number field contains valid data. Set in all segments after initial SYN.</li>
    <li><strong>FIN (Finish):</strong> Initiates graceful connection teardown.</li>
    <li><strong>RST (Reset):</strong> Rejects or aborts an invalid or crashed connection.</li>
    <li><strong>PSH (Push):</strong> Instructs receiver to push data immediately to application without waiting for buffer to fill.</li>
    <li><strong>URG (Urgent):</strong> Indicates urgent out-of-band data pointed to by Urgent Pointer.</li>
  </ul>
</div>

<div class="callout callout-exam">
  <div class="callout-header">🎯 High-Yield 3-Mark Exam Scenario: Tracing TCP Sequence & ACK Numbers (Study Guide P21)</div>
  TCP views data as an unstructured, ordered stream of bytes. Sequence numbers reflect <strong>byte offsets</strong> in the stream, not segment counts!
  <br><br>
  <strong>Scenario 1: Back-to-Back Segments (Study Guide P21):</strong>
  <br>Host A sends two segments back-to-back to Host B. Segment 1 has <span class="math-inline">\text{Seq} = 250</span> and carries 120 bytes; Segment 2 carries 80 bytes.
  <ol>
    <li><strong>Sequence number of Segment 2:</strong>
      <div class="math-display">\text{Seq}_2 = \text{Seq}_1 + \text{bytes}_1 = 250 + 120 = \mathbf{370}</div>
    </li>
    <li><strong>ACK numbers if both arrive in order:</strong>
      <br>&bull; After segment 1: B expects byte 370 &rarr; sends <span class="math-inline">\mathbf{ACK = 370}</span>.
      <br>&bull; After segment 2: B expects byte <span class="math-inline">370 + 80 = 450</span> &rarr; sends <span class="math-inline">\mathbf{ACK = 450}</span>.
    </li>
    <li><strong>If Segment 1 is lost and Segment 2 arrives:</strong>
      <br>&bull; B receives bytes 370–449 but is still missing bytes 250–369.
      <br>&bull; B sends a duplicate <span class="math-inline">\mathbf{ACK = 250}</span> (the next byte expected)!
    </li>
    <li><strong>A retransmits Segment 1 and it arrives (B buffered Segment 2):</strong>
      <br>&bull; The gap is filled! B now holds all continuous bytes from 250 through 449.
      <br>&bull; B sends a cumulative <span class="math-inline">\mathbf{ACK = 450}</span> (next byte expected)!
    </li>
  </ol>
  <strong>Scenario 2: Telnet Single-Character Echo (Kurose & Ross Figure 3.31):</strong>
  <br>&bull; Client sends typed character 'C' (1 byte data): <span class="math-inline">\text{Seq} = 42, \text{ACK} = 79, \text{Data} = \text{'C'}</span>.
  <br>&bull; Server echoes character 'C' and ACKs client's byte: <span class="math-inline">\text{Seq} = 79, \text{ACK} = 43, \text{Data} = \text{'C'}</span> (piggybacked ACK!).
  <br>&bull; Client confirms echo: <span class="math-inline">\text{Seq} = 43, \text{ACK} = 80, \text{Data} = \text{empty}</span>.
</div>

<h3>3.5.3 TCP Round-Trip Time (RTT) Estimation & Timeout</h3>
<p>TCP estimates RTT using an Exponentially Weighted Moving Average (EWMA):</p>
<div class="math-display">
  \text{EstimatedRTT} = (1 - \alpha) \cdot \text{EstimatedRTT} + \alpha \cdot \text{SampleRTT} \quad (\alpha = 0.125)
</div>
<p>RTT variation estimate:</p>
<div class="math-display">
  \text{DevRTT} = (1 - \beta) \cdot \text{DevRTT} + \beta \cdot |\text{SampleRTT} - \text{EstimatedRTT}| \quad (\beta = 0.25)
</div>
<div class="callout callout-formula">
  <div class="callout-header">🧮 TCP Retransmission Timeout Interval (RTO)</div>
  <div class="math-display">
    \text{TimeoutInterval} = \text{EstimatedRTT} + 4 \cdot \text{DevRTT}
  </div>
  <em>Study Guide Exam Note:</em> In the practice problems, update <span class="math-inline">\text{DevRTT}</span> using the <span class="math-inline">\text{EstimatedRTT}</span> value from <em>before</em> the new sample, then update <span class="math-inline">\text{EstimatedRTT}</span>!
  <br><strong>Karn's Algorithm:</strong> Do not measure <span class="math-inline">\text{SampleRTT}</span> for retransmitted segments. If a timeout occurs, double the timeout interval (exponential backoff).
</div>

<h3>Fast Retransmit & RFC 5681 ACK Generation</h3>
<p>Because timeouts are relatively long, TCP includes <strong>Fast Retransmit</strong>: if the sender receives <strong>3 duplicate ACKs</strong> for the same byte (meaning 4 identical ACKs total), the sender infers that the segment following the ACKed byte was lost and retransmits it immediately &mdash; before the timer expires!</p>

<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.85rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:6px 10px;">Event at TCP Receiver</th>
      <th style="padding:6px 10px;">TCP Receiver Action (RFC 5681)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px;">Arrival of in-order segment with expected Seq#. All earlier data acknowledged.</td>
      <td style="padding:6px 10px;">Delayed ACK. Wait up to 500 ms for next segment. If no next segment arrives, send ACK.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px;">Arrival of in-order segment with expected Seq#. One other segment waiting for ACK.</td>
      <td style="padding:6px 10px;">Immediately send single cumulative ACK, ACKing both in-order segments.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px;">Arrival of out-of-order segment with higher-than-expected Seq# (gap detected).</td>
      <td style="padding:6px 10px; color:var(--danger-text); font-weight:700;">Immediately send duplicate ACK, indicating Seq# of next expected byte.</td>
    </tr>
    <tr>
      <td style="padding:6px 10px;">Arrival of segment that partially or completely fills the gap.</td>
      <td style="padding:6px 10px; color:var(--accent-text); font-weight:700;">Immediately send cumulative ACK, provided segment starts at lower end of gap.</td>
    </tr>
  </tbody>
</table>

<h3>3.5.5 Flow Control</h3>
<p>TCP matches sending rate to receiving application drain rate via the <strong>Receive Window (<code>rwnd</code>)</strong> field in the TCP header:</p>
<div class="math-display">
  \text{rwnd} = \text{RcvBuffer} - [\text{LastByteRcvd} - \text{LastByteRead}]
</div>
<p>The sender guarantees: <span class="math-inline">\text{LastByteSent} - \text{LastByteAcked} \le \text{rwnd}</span>.</p>
<p><em>Edge Case:</em> If <span class="math-inline">\text{rwnd} = 0</span>, the sender continues sending 1-byte data probe segments so the receiver will reply with updated non-zero <code>rwnd</code> when the application drains the buffer.</p>

<h3>3.5.6 Connection Management: Handshake, Teardown & SYN Cookies</h3>
<div class="callout callout-def">
  <div class="callout-header">📘 Why Does a 2-Way Handshake Fail?</div>
  Variable network delays cause retransmitted connection requests and delayed duplicate data segments. In a 2-way handshake, the server allocates resources and opens a connection upon receiving a request. If an old delayed request arrives, the server opens a <strong>half-open connection</strong> and accepts duplicate data while the client has no idea!
</div>

<!-- EMBEDDED INTERACTIVE: TCP 3-WAY HANDSHAKE STEPPER -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🤝 Interactive TCP 3-Way Handshake & Connection Teardown</div>
    <span class="interactive-badge">State Transition Stepper</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Step through the 3-way handshake and 4-way teardown with TIME_WAIT:
  </p>
  <div class="sim-viewport" style="align-items:flex-start; min-height:100px;">
    <div style="width:100%;">
      <div id="sec3-tcp-step-badge" style="font-weight:700; color:var(--primary-text); font-size:1rem; margin-bottom:0.35rem;">
        Step 1: SYN
      </div>
      <div id="sec3-tcp-info" style="font-size:0.85rem; color:var(--text-secondary); line-height:1.6;">
        <strong>Client &rarr; Server:</strong> TCP SYN Segment (SYN=1, ACK=0, Seq=100). Client enters <code>SYN_SENT</code> state.
      </div>
    </div>
  </div>
  <div class="sim-controls">
    <button class="btn-primary" onclick="stepSec3TCPHandshake()">⏭ Next Handshake Step</button>
    <button class="btn-secondary" onclick="resetSec3TCPHandshake()">🔄 Reset</button>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "Host A sends two segments back-to-back: Segment 1 (Seq=250, 120 bytes) and Segment 2 (80 bytes). If Segment 1 is lost and Segment 2 arrives, what ACK does Host B return?",
                    "opts": [
                        "ACK = 370",
                        "ACK = 450",
                        "ACK = 250 (duplicate ACK for the next expected byte)",
                        "NAK = 1"
                    ],
                    "ans": 2,
                    "exp": "Because byte 250 is missing, receiver B buffers segment 2 and immediately sends a duplicate ACK for byte 250 (§3.5 / P21c)."
                },
                {
                    "q": "What is the formula for calculating TCP's Retransmission Timeout Interval (TimeoutInterval)?",
                    "opts": [
                        "EstimatedRTT / 2",
                        "EstimatedRTT + 4 * DevRTT",
                        "SampleRTT * 2",
                        "DevRTT + 4 * EstimatedRTT"
                    ],
                    "ans": 1,
                    "exp": "TimeoutInterval = EstimatedRTT + 4 * DevRTT. The 4*DevRTT term provides a safety margin that expands when sample variance is high (§3.5.3 / P22a)."
                }
            ]
        },
        {
            "id": "ch3-6",
            "num": "3.6",
            "title": "Principles of Congestion Control",
            "subtitle": "The three costs of congestion and network-assisted vs end-to-end approaches",
            "content": r"""
<p>Congestion occurs when too many packet sources transmit data at too high an aggregate rate for the network core links and switches to handle.</p>

<h3>The Three Costs of Network Congestion</h3>
<ol>
  <li><strong>Cost 1 (Huge Queuing Delays):</strong> As arrival rate approaches link transmission capacity (<span class="math-inline">La/R \to 1</span>), buffer queues grow towards infinity, causing massive end-to-end queuing delays.</li>
  <li><strong>Cost 2 (Wasted Transmissions from Retransmissions):</strong> Senders retransmit packets that were delayed but not lost, or packets dropped due to buffer overflow, wasting valuable link transmission bandwidth.</li>
  <li><strong>Cost 3 (Wasted Upstream Link Capacity):</strong> When a packet traverses multiple intermediate routers and is dropped far downstream at a congested router, all the transmission capacity and buffer resources consumed at every upstream router along the path were <strong>completely wasted</strong>!</li>
</ol>
""",
            "quiz": [
                {
                    "q": "Which scenario represents the most severe economic and bandwidth cost of network congestion?",
                    "opts": [
                        "A packet dropped at the sender's local interface",
                        "A packet traverses 10 upstream routers and is dropped at the 11th router, wasting all prior link capacity expended to carry it",
                        "A client opening multiple persistent TCP connections",
                        "A DNS cache hit"
                    ],
                    "ans": 1,
                    "exp": "Dropping a packet deep along an end-to-end path wastes all the upstream transmission bandwidth and router resources that were expended to carry the packet that far (§3.6.1)."
                }
            ]
        },
        {
            "id": "ch3-7",
            "num": "3.7",
            "title": "TCP Congestion Control",
            "subtitle": "AIMD sawtooth, Slow Start, Congestion Avoidance, Fast Recovery, and TCP Throughput",
            "content": r"""
<p>Because the IP layer provides no explicit congestion feedback, TCP uses <strong>end-to-end congestion control</strong>. Each TCP sender regulates its transmission rate by constraining its <strong>congestion window (<code>cwnd</code>)</strong>:</p>
<div class="math-display">
  \text{LastByteSent} - \text{LastByteAcked} \le \min(\text{cwnd}, \ \text{rwnd})
</div>

<h3>The Three Phases of TCP Congestion Control</h3>
<ol>
  <li><strong>Slow Start:</strong> Initial phase. <code>cwnd</code> starts at 1 MSS. For <em>every ACK received</em>, <code>cwnd</code> increases by 1 MSS. This results in an <strong>exponential doubling</strong> of <code>cwnd</code> every RTT (<span class="math-inline">1 \to 2 \to 4 \to 8 \to 16\text{ MSS}</span>) until:
    <ul>
      <li>A loss event occurs, or</li>
      <li><code>cwnd &ge; ssthresh</code> (slow start threshold), whereupon TCP transitions to Congestion Avoidance.</li>
    </ul>
  </li>
  <li><strong>Congestion Avoidance:</strong> Linear growth (Additive Increase). <code>cwnd</code> increases by <strong>1 MSS per RTT</strong>.</li>
  <li><strong>Fast Recovery:</strong>
    <ul>
      <li><strong>On 3 Duplicate ACKs (TCP Reno):</strong> Sets <span class="math-inline">\text{ssthresh} = \text{cwnd} / 2</span>, <span class="math-inline">\text{cwnd} = \text{ssthresh} + 3\text{ MSS}</span>, and resumes linear growth (Fast Recovery).</li>
      <li><strong>On Timeout (TCP Tahoe & Reno):</strong> Sets <span class="math-inline">\text{ssthresh} = \text{cwnd} / 2</span>, resets <span class="math-inline">\text{cwnd} = 1\text{ MSS}</span>, and falls back to Slow Start!</li>
    </ul>
  </li>
</ol>

<div class="callout callout-exam">
  <div class="callout-header">🎯 TCP Tahoe vs TCP Reno on Loss Events</div>
  <ul>
    <li><strong>TCP Tahoe:</strong> Unconditionally cuts <span class="math-inline">\text{cwnd} = 1\text{ MSS}</span> on ANY loss event (timeout OR 3 duplicate ACKs), always restarting from Slow Start.</li>
    <li><strong>TCP Reno:</strong> Distinguishes timeout (severe congestion &rarr; <span class="math-inline">\text{cwnd} = 1</span>) from 3 duplicate ACKs (mild congestion &rarr; cuts window in half, avoids slow start via Fast Recovery!).</li>
  </ul>
</div>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Macroscopic Model of TCP Throughput (§3.7)</div>
  During congestion avoidance, TCP's sawtooth cycles between <span class="math-inline">W / 2</span> and <span class="math-inline">W</span>. If <span class="math-inline">W</span> is the maximum window size in bytes and <span class="math-inline">L</span> is the packet loss rate:
  <div class="math-display">
    \text{Average Throughput} \approx \frac{1.22 \cdot \text{MSS}}{\text{RTT} \cdot \sqrt{L}}
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In TCP Reno, what is cwnd set to upon receiving 3 duplicate ACKs when cwnd = 24 MSS?",
                    "opts": [
                        "1 MSS",
                        "ssthresh + 3 MSS = 12 + 3 = 15 MSS (enters Fast Recovery)",
                        "24 MSS",
                        "48 MSS"
                    ],
                    "ans": 1,
                    "exp": "TCP Reno sets ssthresh = cwnd / 2 = 12 MSS, sets cwnd = ssthresh + 3 MSS = 15 MSS, and enters Fast Recovery (§3.7)."
                }
            ]
        },
        {
            "id": "ch3-8",
            "num": "3.8",
            "title": "Chapter 3 Summary & Exam Practice Problems (P17–P24)",
            "subtitle": "Complete worked solutions to all 8 Midterm Study Guide Practice Problems plus Textbook Problems",
            "content": r"""
<p>Master these 8 practice problems from the official CPCS-371 Midterm Study Guide covering Chapter 3:</p>

<!-- PROBLEM P17 -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P17: Transport Demultiplexing</div>
    <span class="interactive-badge">Study Guide P17</span>
  </div>
  <p><strong>Problem:</strong> Host C runs a UDP socket bound to port 5353 and a TCP server whose welcoming socket uses port 80.</p>
  <p>(a) Two UDP datagrams arrive with destination port 5353, from (Host A, port 4001) and (Host B, port 4002). How many sockets at C receive them?<br>
     (b) Two TCP clients connect to port 80: one from (A, 4001) and one from (B, 4001). How many connection sockets are created at C, and how does C tell their segments apart?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p17-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p17-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) <strong>One socket:</strong> UDP demultiplexes based on destination port only. Both datagrams share destination port 5353, so both go to the single socket bound to port 5353.</div>
    <div class="calc-step">(b) <strong>Two connection sockets</strong> (plus the welcoming socket). TCP demultiplexes using the 4-tuple: both connections have the same destination IP and destination port (C, 80) and same source port (4001), but have <strong>different source IP addresses</strong> (A vs B). Host C uses the distinct source IP addresses to demultiplex segments to their respective connection sockets.</div>
  </div>
</div>

<!-- PROBLEM P18 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P18: Computing & Verifying the Internet Checksum</div>
    <span class="interactive-badge">Study Guide P18</span>
  </div>
  <p><strong>Problem:</strong> Compute the 16-bit Internet checksum of the two words below, then show how the receiver verifies it:</p>
  <pre style="background:var(--bg-secondary); padding:0.5rem; border-radius:4px; font-size:0.85rem; font-family:monospace;">
Word 1: 0101 1100 1010 0011 (0x5CA3)
Word 2: 1100 0110 0111 0101 (0xC675)</pre>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p18-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p18-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Add the two 16-bit binary words:
      <pre style="font-family:monospace; margin:0.35rem 0;">
  0101 1100 1010 0011
+ 1100 0110 0111 0101
---------------------
1 0010 0011 0001 1000  (Notice the carry-out bit = 1!)</pre>
    </div>
    <div class="calc-step">Step 2: Add the wraparound carry bit back into the least significant bit:
      <pre style="font-family:monospace; margin:0.35rem 0;">
  0010 0011 0001 1000
+                   1
---------------------
  0010 0011 0001 1001  (Sum)</pre>
    </div>
    <div class="calc-step">Step 3: Take the 1's complement (invert all bits) to find the Checksum:
      <div class="math-display">\text{Checksum} = \mathbf{1101\ 1100\ 1110\ 0110} \ (0x\text{DCE6})</div>
    </div>
    <div class="calc-step">Step 4: <strong>Receiver Verification:</strong>
      <pre style="font-family:monospace; margin:0.35rem 0;">
  0010 0011 0001 1001  (Sum of received words)
+ 1101 1100 1110 0110  (Received checksum)
---------------------
  1111 1111 1111 1111  (All 1s &rarr; No error detected!)</pre>
      Any 0 bit in the result indicates that a bit error occurred!
    </div>
  </div>
</div>

<!-- PROBLEM P19 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P19: Reliable Data Transfer (rdt) Mechanics</div>
    <span class="interactive-badge">Study Guide P19</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) Why can rdt2.0 not cope with a corrupted ACK or NAK, and how does rdt2.1 fix it?<br>
     (b) How does rdt2.2 work without NAKs?<br>
     (c) What problem does rdt3.0 solve, and what new mechanism does it add?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p19-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p19-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) In rdt2.0, if an ACK/NAK is corrupted, the sender cannot determine whether the receiver successfully received the packet. If the sender blindly retransmits, it creates a duplicate packet that the receiver cannot identify. <strong>rdt2.1 fixes this by adding a sequence number (0 or 1)</strong> to each packet; if the receiver sees a duplicate sequence number, it discards the duplicate data and re-ACKs.</div>
    <div class="calc-step">(b) In rdt2.2, the receiver sends <strong>duplicate ACKs</strong> instead of NAKs. The receiver ACKs the last correctly received packet, explicitly including its sequence number. If the sender receives a duplicate ACK for the previous packet, it knows the current packet was corrupted and retransmits.</div>
    <div class="calc-step">(c) rdt3.0 handles <strong>packet loss</strong> (or lost ACKs) on an unreliable channel. It adds a <strong>countdown timer</strong> at the sender; if no ACK arrives before the timer expires, the sender assumes the packet was lost and retransmits.</div>
  </div>
</div>

<!-- PROBLEM P20 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P20: Channel Utilization in Stop-and-Wait vs Pipelining</div>
    <span class="interactive-badge">Study Guide P20</span>
  </div>
  <p><strong>Problem:</strong> A sender uses stop-and-wait on a 100 Mbps channel with RTT = 30 ms and 1,000-byte packets.</p>
  <p>(a) Compute <span class="math-inline">L/R</span> and the sender utilization.<br>
     (b) What is the utilization with 3-packet pipelining?<br>
     (c) How many packets would have to be in flight to keep the link fully busy (100% utilization)?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p20-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p20-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; Packet length in bits: <span class="math-inline">L = 1,000 \times 8 = 8,000\text{ bits}</span>.
      <div class="math-display">\frac{L}{R} = \frac{8,000\text{ bits}}{10^8\text{ bps}} = 0.00008\text{ s} = \mathbf{0.08\text{ ms}}</div>
      <br>&bull; Stop-and-wait utilization:
      <div class="math-display">U = \frac{L / R}{\text{RTT} + (L / R)} = \frac{0.08\text{ ms}}{30\text{ ms} + 0.08\text{ ms}} = \frac{0.08}{30.08} \approx \mathbf{0.00266} \ (0.27\%)</div>
    </div>
    <div class="calc-step">Part (b): With <span class="math-inline">N = 3</span> packet pipelining:
      <div class="math-display">U = \frac{3 \times 0.08}{30.08} \approx \mathbf{0.00798} \ (0.80\%)</div>
    </div>
    <div class="calc-step">Part (c): To achieve 100% utilization (<span class="math-inline">U = 1</span>):
      <div class="math-display">N \ge \frac{\text{RTT} + (L / R)}{L / R} = \frac{30.08\text{ ms}}{0.08\text{ ms}} = \mathbf{376\text{ packets in flight}}</div>
    </div>
  </div>
</div>

<!-- PROBLEM P21 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P21: TCP Sequence & Acknowledgment Numbers</div>
    <span class="interactive-badge">Study Guide P21</span>
  </div>
  <p><strong>Problem:</strong> Host A sends two segments back-to-back to Host B. The first segment has sequence number 250 and carries 120 bytes; the second segment carries 80 bytes.</p>
  <p>(a) What is the sequence number of the second segment?<br>
     (b) If both arrive in order, what ACK numbers does B send?<br>
     (c) If the first segment is lost and the second arrives, what ACK number does B send?<br>
     (d) A then retransmits the first segment and it arrives (B buffered the second). What ACK number does B send now?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p21-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p21-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) <span class="math-inline">\text{Seq}_2 = \text{Seq}_1 + \text{bytes}_1 = 250 + 120 = \mathbf{370}</span>.</div>
    <div class="calc-step">(b) After segment 1 arrives, B expects byte 370 &rarr; sends <span class="math-inline">\mathbf{ACK = 370}</span>. After segment 2 arrives, B expects byte <span class="math-inline">370 + 80 = \mathbf{450}</span> &rarr; sends <span class="math-inline">\mathbf{ACK = 450}</span>.</div>
    <div class="calc-step">(c) If segment 1 is lost, B receives bytes 370–449 but is still waiting for byte 250. B sends a duplicate <span class="math-inline">\mathbf{ACK = 250}</span> (the next expected byte!).</div>
    <div class="calc-step">(d) When the retransmitted first segment arrives, the gap is filled! B now has all bytes from 250 through 449. B sends a cumulative <span class="math-inline">\mathbf{ACK = 450}</span>!</div>
  </div>
</div>

<!-- PROBLEM P22 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P22: TCP RTT Estimation Trace</div>
    <span class="interactive-badge">Study Guide P22</span>
  </div>
  <p><strong>Problem:</strong> Currently <span class="math-inline">\text{EstimatedRTT} = 80\text{ ms}</span> and <span class="math-inline">\text{DevRTT} = 10\text{ ms}</span>. A new <span class="math-inline">\text{SampleRTT} = 120\text{ ms}</span> is measured (<span class="math-inline">\alpha = 0.125, \beta = 0.25</span>).</p>
  <p>(a) Compute the new DevRTT (using current EstimatedRTT), the new EstimatedRTT, and the new TimeoutInterval.<br>
     (b) Why is TimeoutInterval larger than EstimatedRTT?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p22-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p22-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a):
      <br>&bull; Step 1: Update DevRTT using the current EstimatedRTT (80 ms):
      <div class="math-display">\text{DevRTT} = (1 - 0.25) \times 10 + 0.25 \times |120 - 80| = 7.5 + (0.25 \times 40) = 7.5 + 10 = \mathbf{17.5\text{ ms}}</div>
      <br>&bull; Step 2: Update EstimatedRTT:
      <div class="math-display">\text{EstimatedRTT} = (1 - 0.125) \times 80 + 0.125 \times 120 = 70 + 15 = \mathbf{85\text{ ms}}</div>
      <br>&bull; Step 3: Compute TimeoutInterval:
      <div class="math-display">\text{TimeoutInterval} = \text{EstimatedRTT} + 4 \times \text{DevRTT} = 85 + (4 \times 17.5) = 85 + 70 = \mathbf{155\text{ ms}}</div>
    </div>
    <div class="calc-step">Part (b): Network RTT fluctuates due to queuing variations. The <span class="math-inline">4 \cdot \text{DevRTT}</span> safety margin prevents premature timeouts when delays spike.</div>
  </div>
</div>

<!-- PROBLEM P23 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P23: Flow Control vs Congestion Control</div>
    <span class="interactive-badge">Study Guide P23</span>
  </div>
  <p><strong>Problem:</strong> A receiver's <code>RcvBuffer</code> is 8,192 bytes, and 5,000 bytes are buffered but not yet read by the application.</p>
  <p>(a) What <code>rwnd</code> does it advertise, and what must the sender do with it?<br>
     (b) Explain the difference between flow control and congestion control.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p23-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p23-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) <span class="math-inline">\text{rwnd} = \text{RcvBuffer} - \text{buffered} = 8,192 - 5,000 = \mathbf{3,192\text{ bytes}}</span>. The sender must limit its unacknowledged in-flight data to &le; 3,192 bytes so the receiver buffer does not overflow.</div>
    <div class="calc-step">(b) <strong>Flow control</strong> protects the <em>receiver</em> from having its buffer overwhelmed by a fast sender (controlled by <code>rwnd</code>). <strong>Congestion control</strong> protects the <em>network core</em> from being overloaded by too many sources sending too much aggregate traffic (controlled by <code>cwnd</code>).</div>
  </div>
</div>

<!-- PROBLEM P24 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P24: TCP Teardown States & the FIN Bit</div>
    <span class="interactive-badge">Study Guide P24</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) Which header bit is used to close a TCP connection?<br>
     (b) List the client's states from <code>ESTABLISHED</code> to <code>CLOSED</code> when the client initiates closure, and describe what the client can and cannot do in <code>FIN_WAIT_1</code>.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch3-p24-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch3-p24-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) The <strong>FIN bit</strong> (Finish flag) in the TCP header.</div>
    <div class="calc-step">(b) <strong>State transitions:</strong>
      <div class="math-display">\text{ESTABLISHED} \longrightarrow \text{FIN\_WAIT\_1} \longrightarrow \text{FIN\_WAIT\_2} \longrightarrow \text{TIME\_WAIT} \ (2 \times \text{MSL}) \longrightarrow \text{CLOSED}</div>
      In <code>FIN_WAIT_1</code>, the client has sent its FIN and can <strong>no longer send new application data</strong>, but it <strong>can still receive incoming data</strong> sent by the server before the server closes!
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What state does the client TCP enter immediately after sending an ACK for the server's FIN segment during connection teardown?",
                    "opts": [
                        "CLOSED immediately",
                        "TIME_WAIT (waits 2 * MSL before closing)",
                        "CLOSE_WAIT",
                        "SYN_SENT"
                    ],
                    "ans": 1,
                    "exp": "The client enters TIME_WAIT (typically 30–120 seconds = 2*MSL) to ensure the server receives the final ACK in case it was lost in transit (§3.5.6 / P24b)."
                }
            ]
        }
    ]
}
