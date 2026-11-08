"""Chapter 9 Data: Network Management (Kurose & Ross 6th Ed.)
Comprehensive, textbook-grade expansion covering all subsections, inline SVGs, 
worked problems, and interactive simulators.
"""

CH9_DATA = {
    "id": "ch9",
    "num": 9,
    "title": "Network Management",
    "subtitle": "ISO FCAPS, SNMP Infrastructure, SMI / MIB Object Trees, and ASN.1 / BER TLV Encoding",
    "layer": "Network Management",
    "color": "#475569",
    "objectives": [
        "Deconstruct the 5 ISO network management functional areas (FCAPS): Fault, Configuration, Accounting, Performance, and Security",
        "Analyze the Internet Network Management Architecture: Managing Entity, Managed Devices, Management Agents, MIB, and SNMP",
        "Navigate the Structure of Management Information (SMI) hierarchical OID tree under iso.org.dod.internet.mgmt.mib-2 (1.3.6.1.2.1)",
        "Differentiate all 7 SNMP PDU operations: GetRequest, GetNextRequest, GetBulkRequest, SetRequest, Response, Trap, and InformRequest",
        "Contrast polling over UDP port 161 with asynchronous event traps over UDP port 162",
        "Evaluate SNMPv3 security enhancements: User-Based Security Model (USM) and View-Based Access Control Model (VACM)",
        "Execute ASN.1 Basic Encoding Rules (BER) Tag-Length-Value (TLV) byte conversions for integers and strings"
    ],
    "sections": [
        {
            "id": "ch9-1",
            "num": "9.1",
            "title": "What Is Network Management?",
            "subtitle": "Definition, operational challenges, and the ISO FCAPS management framework",
            "content": r"""
<p>Modern enterprise and telecommunications networks contain thousands of routers, switches, optical transceivers, wireless access points, firewalls, and server farms. <strong>Network management</strong> encompasses the deployment, integration, and coordination of hardware, software, and human elements to monitor, test, poll, configure, analyze, evaluate, and control network resources to meet real-time operational and Quality of Service requirements.</p>

<h3>9.1.1 The ISO Network Management Functional Areas (FCAPS)</h3>
<p>The International Organization for Standardization (ISO) categorized network management into five distinct functional areas, widely known by the acronym <strong>FCAPS</strong>:</p>

<!-- INLINE SVG: Figure 9.1 ISO FCAPS Framework -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 220" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Fault Card -->
      <rect x="25" y="40" width="145" height="150" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
      <text x="97" y="70" font-size="24" text-anchor="middle">🚨</text>
      <text x="97" y="98" font-size="12" font-weight="800" fill="#991b1b" text-anchor="middle">Fault (F)</text>
      <text x="97" y="120" font-size="9" fill="#b91c1c" text-anchor="middle">Detect, isolate, log</text>
      <text x="97" y="135" font-size="9" fill="#b91c1c" text-anchor="middle">& resolve failures</text>
      <text x="97" y="150" font-size="8" fill="#7f1d1d" text-anchor="middle">(link down, alarms)</text>

      <!-- Configuration Card -->
      <rect x="185" y="40" width="145" height="150" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
      <text x="257" y="70" font-size="24" text-anchor="middle">⚙️</text>
      <text x="257" y="98" font-size="12" font-weight="800" fill="#1e40af" text-anchor="middle">Config (C)</text>
      <text x="257" y="120" font-size="9" fill="#1d4ed8" text-anchor="middle">Track device state,</text>
      <text x="257" y="135" font-size="9" fill="#1d4ed8" text-anchor="middle">OS versions & update</text>
      <text x="257" y="150" font-size="8" fill="#1e3a8a" text-anchor="middle">router parameters</text>

      <!-- Accounting Card -->
      <rect x="345" y="40" width="145" height="150" rx="8" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="417" y="70" font-size="24" text-anchor="middle">📊</text>
      <text x="417" y="98" font-size="12" font-weight="800" fill="#7e22ce" text-anchor="middle">Account (A)</text>
      <text x="417" y="120" font-size="9" fill="#9333ea" text-anchor="middle">Measure resource</text>
      <text x="417" y="135" font-size="9" fill="#9333ea" text-anchor="middle">usage for billing</text>
      <text x="417" y="150" font-size="8" fill="#581c87" text-anchor="middle">& quota control</text>

      <!-- Performance Card -->
      <rect x="505" y="40" width="145" height="150" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
      <text x="577" y="70" font-size="24" text-anchor="middle">📈</text>
      <text x="577" y="98" font-size="12" font-weight="800" fill="#047857" text-anchor="middle">Perform (P)</text>
      <text x="577" y="120" font-size="9" fill="#059669" text-anchor="middle">Monitor throughput,</text>
      <text x="577" y="135" font-size="9" fill="#059669" text-anchor="middle">latency, loss & jitter</text>
      <text x="577" y="150" font-size="8" fill="#064e3b" text-anchor="middle">to maintain SLAs</text>

      <!-- Security Card -->
      <rect x="665" y="40" width="145" height="150" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="2"/>
      <text x="737" y="70" font-size="24" text-anchor="middle">🔒</text>
      <text x="737" y="98" font-size="12" font-weight="800" fill="#c2410c" text-anchor="middle">Security (S)</text>
      <text x="737" y="120" font-size="9" fill="#ea580c" text-anchor="middle">Control admin</text>
      <text x="737" y="135" font-size="9" fill="#ea580c" text-anchor="middle">access, ACLs &</text>
      <text x="737" y="150" font-size="8" fill="#7c2d12" text-anchor="middle">audit intrusion logs</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 9.1 — The 5 ISO Network Management Functional Areas (FCAPS) (§9.1.1).</div>
</div>

<ol>
  <li><strong>Fault Management:</strong> The immediate detection, isolation, logging, and resolution of network anomalies and equipment failures (e.g., an optical fiber cut, interface link down, power supply failure). It includes automated alarm correlation and root-cause analysis.</li>
  <li><strong>Configuration Management:</strong> Tracking hardware serial numbers, firmware revisions, and network interface settings. Orchestrating synchronized configuration updates across switches and routers to prevent routing loops or configuration drift.</li>
  <li><strong>Accounting Management:</strong> Monitoring resource consumption (megabytes transmitted, peak bandwidth utilized) per user, department, or customer for billing, chargeback, or quota enforcement.</li>
  <li><strong>Performance Management:</strong> Continuous quantitative assessment of network Key Performance Indicators (KPIs): throughput, interface utilization, packet discard rates, queuing delay, and round-trip times to maintain Service Level Agreements (SLAs).</li>
  <li><strong>Security Management:</strong> Authorizing administrative access, managing RADIUS/TACACS+ credentials, distributing cryptographic keys (IPsec/SSH), configuring firewall ACL rules, and auditing intrusion alert logs.</li>
</ol>
""",
            "quiz": [
                {
                    "q": "What does the 'A' represent in the ISO FCAPS network management framework?",
                    "opts": [
                        "Authentication",
                        "Accounting Management (tracking resource consumption and billing)",
                        "Access Control",
                        "Automation"
                    ],
                    "ans": 1,
                    "exp": "In ISO FCAPS, 'A' stands for Accounting Management (§9.1.1)."
                },
                {
                    "q": "Tracking router OS firmware revisions and updating interface MTU parameters falls under which FCAPS functional area?",
                    "opts": [
                        "Fault Management",
                        "Configuration Management",
                        "Accounting Management",
                        "Security Management"
                    ],
                    "ans": 1,
                    "exp": "Managing hardware/software versions and updating operational parameters is Configuration Management (§9.1.1)."
                }
            ]
        },
        {
            "id": "ch9-2",
            "num": "9.2",
            "title": "The Infrastructure for Network Management",
            "subtitle": "Managing Entity, Managed Devices, Agents, MIB, and SNMP",
            "content": r"""
<p>The Internet-standard management framework is composed of five interconnected components:</p>

<!-- INLINE SVG: Figure 9.2 Network Management Architecture -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 260" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Managing Entity (NOC) Box -->
      <rect x="30" y="30" width="220" height="200" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
      <text x="140" y="58" font-size="12" font-weight="800" fill="#1e40af" text-anchor="middle">Managing Entity (Manager)</text>
      <rect x="50" y="75" width="180" height="50" rx="6" fill="#3b82f6"/>
      <text x="140" y="98" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">NMS Management Console</text>
      <text x="140" y="112" font-size="9" fill="#dbeafe" text-anchor="middle">Network Operations Center (NOC)</text>
      <text x="140" y="150" font-size="9" fill="#1e40af" text-anchor="middle">&bull; Issues SNMP Polls (Port 161)</text>
      <text x="140" y="168" font-size="9" fill="#1e40af" text-anchor="middle">&bull; Listens for Traps (Port 162)</text>
      <text x="140" y="186" font-size="9" fill="#1e40af" text-anchor="middle">&bull; Analyzes KPIs & Displays Alarms</text>

      <!-- Network Clouds / Communication -->
      <line x1="250" y1="90" x2="480" y2="90" stroke="#0284c7" stroke-width="3"/>
      <polygon points="480,90 470,85 472,95" fill="#0284c7"/>
      <text x="365" y="82" font-size="9" font-weight="700" fill="#0284c7" text-anchor="middle">SNMP Request (Get/Set, Port 161)</text>

      <line x1="480" y1="120" x2="250" y2="120" stroke="#0284c7" stroke-width="2" stroke-dasharray="4 3"/>
      <polygon points="250,120 260,115 258,125" fill="#0284c7"/>
      <text x="365" y="113" font-size="9" fill="#0284c7" text-anchor="middle">SNMP Response (Port 161)</text>

      <line x1="480" y1="155" x2="250" y2="155" stroke="#ef4444" stroke-width="2.5"/>
      <polygon points="250,155 260,150 258,160" fill="#ef4444"/>
      <text x="365" y="172" font-size="9" font-weight="700" fill="#b91c1c" text-anchor="middle">Unsolicited Trap / Inform (Port 162)</text>

      <!-- Managed Device Box -->
      <rect x="480" y="30" width="330" height="200" rx="10" fill="#f8fafc" stroke="#10b981" stroke-width="2"/>
      <text x="645" y="58" font-size="12" font-weight="800" fill="#065f46" text-anchor="middle">Managed Device (Router / Switch)</text>

      <!-- Management Agent -->
      <rect x="500" y="75" width="130" height="50" rx="6" fill="#10b981"/>
      <text x="565" y="98" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">SNMP Agent</text>
      <text x="565" y="112" font-size="9" fill="#d1fae5" text-anchor="middle">Software Daemon</text>

      <!-- MIB (Management Information Base) -->
      <rect x="660" y="75" width="130" height="135" rx="6" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="725" y="98" font-size="11" font-weight="800" fill="#7e22ce" text-anchor="middle">MIB (Database)</text>
      <text x="725" y="118" font-size="8" fill="#64748b" text-anchor="middle">&bull; sysUpTime</text>
      <text x="725" y="133" font-size="8" fill="#64748b" text-anchor="middle">&bull; ifInOctets</text>
      <text x="725" y="148" font-size="8" fill="#64748b" text-anchor="middle">&bull; ifOutOctets</text>
      <text x="725" y="163" font-size="8" fill="#64748b" text-anchor="middle">&bull; ipInDiscards</text>
      <text x="725" y="178" font-size="8" fill="#64748b" text-anchor="middle">&bull; tcpCurrEstab</text>

      <!-- Internal Device Line Agent <-> MIB -->
      <line x1="630" y1="100" x2="660" y2="100" stroke="#8b5cf6" stroke-width="3"/>
      <text x="565" y="160" font-size="8" fill="#475569" text-anchor="middle">Interacts with local OS</text>
      <text x="565" y="175" font-size="8" fill="#475569" text-anchor="middle">hardware counters</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 9.2 — Internet Network Management Architecture: Managing Entity, Managed Device, SNMP Agent, MIB, and Protocol Interactions (§9.2).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 The 5 Pillars of Network Management Infrastructure</div>
  <ul>
    <li><strong>Managing Entity (Manager):</strong> A network management application running on a server in the Network Operations Center (NOC). The human operator interacts with this console to visualize network topology, execute diagnostic polling, and receive alarm notifications.</li>
    <li><strong>Managed Device:</strong> Any piece of network equipment on the managed network (routers, switches, firewalls, middleboxes, servers, access points).</li>
    <li><strong>Management Agent:</strong> A software process (daemon) executing directly on the managed device. The agent translates SNMP requests into internal operating system function calls, reads hardware counters, and formats responses.</li>
    <li><strong>Management Information Base (MIB):</strong> A virtual database residing on each managed device containing structured operational status data (e.g., number of bytes received, packets discarded due to buffer overflow).</li>
    <li><strong>Network Management Protocol (SNMP):</strong> The protocol that coordinates communication between the manager and the agents.</li>
  </ul>
</div>
""",
            "quiz": [
                {
                    "q": "Where does the Management Agent software process reside and execute?",
                    "opts": [
                        "Exclusively on the central managing server in the NOC",
                        "Directly on each managed device (routers, switches, firewalls)",
                        "Inside root DNS servers",
                        "In the client's web browser"
                    ],
                    "ans": 1,
                    "exp": "A management agent is an embedded software process running locally on each managed device, collecting local MIB data (§9.2)."
                }
            ]
        },
        {
            "id": "ch9-3",
            "num": "9.3",
            "title": "The Internet-Standard Management Framework",
            "subtitle": "SMI, MIB-2 Object Trees (OIDs), SNMP PDUs, and SNMPv3 security",
            "content": r"""
<p>The Internet-standard management framework is defined by three coordinated RFC specifications: the <strong>Structure of Management Information (SMI)</strong>, the <strong>Management Information Base (MIB-2)</strong>, and the <strong>Simple Network Management Protocol (SNMP)</strong>.</p>

<h3>9.3.1 Structure of Management Information (SMIv2)</h3>
<p>SMI defines the data types, constructors, and naming structure used to describe MIB objects. To maintain vendor independence, every MIB object is assigned a universally unique <strong>Object Identifier (OID)</strong> arranged in an inverted hierarchical tree:</p>

<!-- INLINE SVG: Figure 9.3 MIB-2 OID Tree -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 260" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Root Node -->
      <circle cx="420" cy="25" r="14" fill="#64748b"/>
      <text x="420" y="29" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">root</text>

      <!-- iso(1) -->
      <line x1="420" y1="39" x2="420" y2="65" stroke="#94a3b8" stroke-width="2"/>
      <circle cx="420" cy="75" r="14" fill="#475569"/>
      <text x="420" y="79" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">iso(1)</text>

      <!-- org(3) -->
      <line x1="420" y1="89" x2="420" y2="110" stroke="#94a3b8" stroke-width="2"/>
      <circle cx="420" cy="120" r="14" fill="#334155"/>
      <text x="420" y="124" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">org(3)</text>

      <!-- dod(6) -->
      <line x1="420" y1="134" x2="420" y2="155" stroke="#94a3b8" stroke-width="2"/>
      <circle cx="420" cy="165" r="14" fill="#1e293b"/>
      <text x="420" y="169" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">dod(6)</text>

      <!-- internet(1) -->
      <line x1="420" y1="179" x2="420" y2="200" stroke="#94a3b8" stroke-width="2"/>
      <circle cx="420" cy="210" r="15" fill="#3b82f6"/>
      <text x="420" y="214" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">internet(1)</text>

      <!-- mgmt(2) Branch from internet -->
      <line x1="435" y1="210" x2="520" y2="210" stroke="#3b82f6" stroke-width="2"/>
      <circle cx="535" cy="210" r="15" fill="#0284c7"/>
      <text x="535" y="214" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">mgmt(2)</text>

      <!-- mib-2(1) Branch from mgmt -->
      <line x1="550" y1="210" x2="630" y2="210" stroke="#0284c7" stroke-width="2"/>
      <circle cx="645" cy="210" r="16" fill="#10b981"/>
      <text x="645" y="214" font-size="8" font-weight="800" fill="#fff" text-anchor="middle">mib-2(1)</text>

      <!-- Subtree bracket underneath mib-2 -->
      <text x="740" y="195" font-size="9" font-weight="700" fill="#047857">&bull; system(1)</text>
      <text x="740" y="210" font-size="9" font-weight="700" fill="#047857">&bull; interfaces(2)</text>
      <text x="740" y="225" font-size="9" font-weight="700" fill="#047857">&bull; ip(4) | tcp(6) | udp(7)</text>

      <!-- Prefix label callout -->
      <rect x="50" y="185" width="230" height="50" rx="6" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5"/>
      <text x="165" y="205" font-size="10" font-weight="700" fill="#1e40af" text-anchor="middle">Standard MIB-2 Prefix:</text>
      <text x="165" y="222" font-size="12" font-weight="800" fill="#0284c7" text-anchor="middle">1.3.6.1.2.1</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 9.3 — The SMI MIB-2 Hierarchical Object Identifier (OID) Namespace Tree Leading to 1.3.6.1.2.1 (§9.3.1).</div>
</div>

<h3>9.3.2 Standard MIB-2 Groups</h3>
<ul>
  <li><code>1.3.6.1.2.1.1</code> (<strong>system</strong>): General hardware description, system uptime (<code>sysUpTime</code>), and administrative contact.</li>
  <li><code>1.3.6.1.2.1.2</code> (<strong>interfaces</strong>): Interface table tracking physical network interfaces, MTU, speed, and in/out octet byte counters (used to calculate link utilization!).</li>
  <li><code>1.3.6.1.2.1.4</code> (<strong>ip</strong>): IP layer status, including datagrams received, discards due to lack of buffers (<code>ipInDiscards</code>), and routing table entries.</li>
  <li><code>1.3.6.1.2.1.6</code> (<strong>tcp</strong>): TCP connection table, current connections in ESTABLISHED state (<code>tcpCurrEstab</code>), and retransmitted segments.</li>
  <li><code>1.3.6.1.2.1.7</code> (<strong>udp</strong>): Total UDP datagrams delivered and dropped due to unassigned ports (<code>udpNoPorts</code>).</li>
</ul>

<!-- Interactive MIB-2 Tree Explorer -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🌳 Interactive MIB-2 OID Tree Navigator</div>
    <span class="interactive-badge">Hierarchical SMI Explorer</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Click on any MIB-2 group to inspect its OID number, description, and managed variables:
  </p>
  <div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem;">
    <button class="btn-primary" id="sec9-mib-system" onclick="inspectMibNode('system')">system (1.3.6.1.2.1.1)</button>
    <button class="btn-secondary" id="sec9-mib-interfaces" onclick="inspectMibNode('interfaces')">interfaces (1.3.6.1.2.1.2)</button>
    <button class="btn-secondary" id="sec9-mib-ip" onclick="inspectMibNode('ip')">ip (1.3.6.1.2.1.4)</button>
    <button class="btn-secondary" id="sec9-mib-tcp" onclick="inspectMibNode('tcp')">tcp (1.3.6.1.2.1.6)</button>
    <button class="btn-secondary" id="sec9-mib-udp" onclick="inspectMibNode('udp')">udp (1.3.6.1.2.1.7)</button>
  </div>
  <div id="sec9-mib-display" style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1.25rem;">
    <!-- Filled dynamically -->
  </div>
</div>

<h3>9.3.3 SNMP Protocol Operations (PDUs)</h3>
<p>SNMP operates over <strong>UDP port 161</strong> for manager-initiated queries and responses, and <strong>UDP port 162</strong> for asynchronous agent-initiated event notifications.</p>

<table class="data-table" style="margin:1rem 0;">
  <thead>
    <tr>
      <th>PDU Type</th>
      <th>Direction</th>
      <th>Function & Operational Mechanics</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:700; color:var(--primary);">GetRequest</td>
      <td>Manager &rarr; Agent</td>
      <td>Queries the agent for the values of one or more specified MIB object instances.</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--primary);">GetNextRequest</td>
      <td>Manager &rarr; Agent</td>
      <td>Retrieves the value of the <em>lexicographically next</em> object in the MIB tree (used to walk tables of unknown size).</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--primary);">GetBulkRequest</td>
      <td>Manager &rarr; Agent</td>
      <td>(Introduced in SNMPv2) Efficiently retrieves large blocks of tabular data in a single UDP segment without repeated round trips.</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--primary);">SetRequest</td>
      <td>Manager &rarr; Agent</td>
      <td>Sets or modifies the value of a MIB object variable on the managed device (used for configuration management).</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--accent-text);">Response</td>
      <td>Agent &rarr; Manager</td>
      <td>Returns the requested MIB values or an error status code to the manager.</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--danger-text);">Trap</td>
      <td>Agent &rarr; Manager</td>
      <td><strong>Asynchronous & unsolicited:</strong> Sent to UDP port 162 when an unexpected event occurs (e.g., interface link down, power supply failure). Unconfirmed (fire-and-forget).</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--danger-text);">InformRequest</td>
      <td>Manager &harr; Manager / Agent</td>
      <td>(Introduced in SNMPv2) An asynchronous notification that <strong>requires an explicit acknowledgment</strong> from the receiving manager.</td>
    </tr>
  </tbody>
</table>

<h3>9.3.4 SNMPv3 Security Architecture</h3>
<p>SNMPv1 and SNMPv2c used cleartext <strong>"community strings"</strong> (essentially cleartext passwords sent in every UDP datagram) that were trivial for adversaries to sniff on the wire. <strong>SNMPv3</strong> introduced robust cryptographic protection:</p>
<ul>
  <li><strong>USM (User-Based Security Model):</strong> Provides message authentication (HMAC-MD5 or HMAC-SHA) and encryption (DES or AES-128) using pre-shared secret keys.</li>
  <li><strong>VACM (View-Based Access Control Model):</strong> Defines fine-grained access policies determining which administrative users can read or write specific MIB subtrees.</li>
</ul>
""",
            "quiz": [
                {
                    "q": "What UDP port is used by a managed device agent to send an unsolicited SNMP Trap notification to the management station?",
                    "opts": [
                        "UDP port 53",
                        "UDP port 161",
                        "UDP port 162",
                        "TCP port 179"
                    ],
                    "ans": 2,
                    "exp": "SNMP queries use UDP port 161 on the agent, while asynchronous SNMP Traps are sent to UDP port 162 on the management station (§9.3.3)."
                },
                {
                    "q": "What is the primary operational improvement of InformRequest over the traditional SNMP Trap?",
                    "opts": [
                        "InformRequest requires zero UDP checksums",
                        "InformRequest requires an explicit acknowledgment from the recipient manager, guaranteeing reliable delivery of critical alarms",
                        "InformRequest only runs over optical fiber",
                        "InformRequest changes the OID prefix"
                    ],
                    "ans": 1,
                    "exp": "Traps are unacknowledged and can be lost on congested links. InformRequest requires an acknowledgment, providing reliable alarm delivery (§9.3.3)."
                }
            ]
        },
        {
            "id": "ch9-4",
            "num": "9.4",
            "title": "ASN.1 and Basic Encoding Rules (BER)",
            "subtitle": "Tag-Length-Value (TLV) encoding format and byte representations",
            "content": r"""
<p>Because managed devices have different processor architectures (big-endian vs little-endian, 32-bit vs 64-bit), SNMP uses <strong>ASN.1 (Abstract Syntax Notation One)</strong> to define data types and <strong>BER (Basic Encoding Rules)</strong> to serialize data into an architecture-independent byte stream.</p>

<h3>9.4.1 The Tag-Length-Value (TLV) Principle</h3>
<p>Every serialized ASN.1 data item is transmitted as three consecutive fields:</p>
<ol>
  <li><strong>Tag (Type):</strong> A 1-byte field specifying the data type. Common ASN.1 BER tags:
    <br>&bull; <code>0x02</code>: <strong>INTEGER</strong>
    <br>&bull; <code>0x04</code>: <strong>OCTET STRING</strong> (raw byte array or ASCII text)
    <br>&bull; <code>0x05</code>: <strong>NULL</strong>
    <br>&bull; <code>0x06</code>: <strong>OBJECT IDENTIFIER (OID)</strong>
    <br>&bull; <code>0x30</code>: <strong>SEQUENCE</strong> (constructor for ordered lists of items)
  </li>
  <li><strong>Length:</strong> One or more bytes specifying the exact number of bytes in the following Value field. If the length is &le; 127 bytes, it is encoded in a single byte.</li>
  <li><strong>Value:</strong> The raw binary payload of the data item (integers are encoded in big-endian two's complement).</li>
</ol>

<!-- INLINE SVG: Figure 9.4 BER TLV Structure -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 150" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Tag Block -->
      <rect x="60" y="40" width="160" height="65" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
      <text x="140" y="68" font-size="12" font-weight="800" fill="#1d4ed8" text-anchor="middle">Tag (Type)</text>
      <text x="140" y="85" font-size="9" fill="#2563eb" text-anchor="middle">1 Byte (e.g. 0x02 = INTEGER)</text>

      <!-- Length Block -->
      <rect x="235" y="40" width="160" height="65" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
      <text x="315" y="68" font-size="12" font-weight="800" fill="#047857" text-anchor="middle">Length (L)</text>
      <text x="315" y="85" font-size="9" fill="#059669" text-anchor="middle">&ge; 1 Byte (Number of Value Bytes)</text>

      <!-- Value Block -->
      <rect x="410" y="40" width="370" height="65" rx="6" fill="#fdf4ff" stroke="#c084fc" stroke-width="2"/>
      <text x="595" y="68" font-size="12" font-weight="800" fill="#7e22ce" text-anchor="middle">Value Payload</text>
      <text x="595" y="85" font-size="9" fill="#9333ea" text-anchor="middle">L Bytes (Big-Endian Binary Data / ASCII)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 9.4 — ASN.1 Basic Encoding Rules (BER) Tag-Length-Value (TLV) Triplet Serialization (§9.4.1).</div>
</div>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Worked BER TLV Example: Encoding INTEGER 257</div>
  <ol>
    <li><strong>Tag:</strong> The tag for ASN.1 INTEGER is fixed at <code>0x02</code>.</li>
    <li><strong>Value in Hex:</strong> <span class="math-inline">257 = 256 + 1 = 1 \times 256^1 + 1 \times 256^0 = \mathbf{0x0101}</span> (requires 2 bytes).</li>
    <li><strong>Length:</strong> Because the value requires 2 bytes, the Length byte is <code>0x02</code>.</li>
    <li><strong>Final Serialized Byte Stream:</strong>
      <div class="math-display">
        \mathbf{02\ 02\ 01\ 01} \quad \text{(4 bytes total)}
      </div>
    </li>
  </ol>
</div>

<!-- Interactive ASN.1 BER TLV Encoder -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🔢 Live ASN.1 BER Tag-Length-Value (TLV) Byte Encoder</div>
    <span class="interactive-badge">Encoding Tool</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:1rem;">
    Enter a data type and value to see the exact byte serialization generated by Basic Encoding Rules:
  </p>
  <div class="calc-grid">
    <div class="calc-field">
      <label class="calc-label">ASN.1 Data Type</label>
      <select id="tlv-type-input" class="calc-input" onchange="calcSec9TLV()">
        <option value="int" selected>INTEGER (Tag 0x02)</option>
        <option value="str">OCTET STRING (Tag 0x04)</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">Value to Encode</label>
      <input type="text" id="tlv-val-input" class="calc-input" value="257" oninput="calcSec9TLV()">
    </div>
  </div>
  <div id="tlv-result-box" class="calc-result-box" style="margin-top:1rem;">
    <!-- Rendered dynamically -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In ASN.1 BER encoding, what is the complete hexadecimal TLV byte sequence for the INTEGER value 5?",
                    "opts": [
                        "02 01 05",
                        "04 01 05",
                        "05 02 01",
                        "00 05 01"
                    ],
                    "ans": 0,
                    "exp": "Tag for INTEGER is 02. Length is 01 (1 byte). Value is 05. Serialized string: 02 01 05 (§9.4.1)."
                },
                {
                    "q": "Why does ASN.1 BER use Tag-Length-Value (TLV) rather than fixed-length offsets?",
                    "opts": [
                        "To force all packets to be 1500 bytes",
                        "To enable architecture-independent decoding of variable-length fields (strings, OIDs, integers) across heterogeneous computing platforms",
                        "Because UDP requires TLV",
                        "To prevent buffer overflows automatically"
                    ],
                    "ans": 1,
                    "exp": "TLV encoding allows receivers on any hardware architecture to parse arbitrary variable-length fields without prior compiled offset knowledge (§9.4)."
                }
            ]
        },
        {
            "id": "ch9-5",
            "num": "9.5",
            "title": "Chapter 9 Summary & Review Problems",
            "subtitle": "Comprehensive network management review and ASN.1 encoding problem",
            "content": r"""
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 9: ASN.1 BER TLV String Encoding</div>
    <span class="interactive-badge">P8 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Show the exact BER TLV hexadecimal byte encoding for the ASCII string <code>"KAU"</code> (OCTET STRING tag is <code>0x04</code>). ASCII values: 'K' = 0x4B, 'A' = 0x41, 'U' = 0x55.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch9-prob1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch9-prob1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Tag byte for OCTET STRING = <span class="math-inline">\mathbf{0x04}</span>.</div>
    <div class="calc-step">Step 2: Length of string "KAU" is 3 characters = 3 bytes = <span class="math-inline">\mathbf{0x03}</span>.</div>
    <div class="calc-step">Step 3: Hexadecimal values of characters:
      <br>&emsp;&bull; 'K' = <span class="math-inline">0x4B</span>
      <br>&emsp;&bull; 'A' = <span class="math-inline">0x41</span>
      <br>&emsp;&bull; 'U' = <span class="math-inline">0x55</span>
    </div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
      Final Answer: The complete BER TLV byte sequence is <strong><code>04 03 4B 41 55</code></strong> (5 bytes total).
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the standard OID prefix for all Internet MIB-2 management objects?",
                    "opts": [
                        "1.2.3.4.5.6",
                        "1.3.6.1.2.1",
                        "0.0.0.0.1",
                        "255.255.255.0"
                    ],
                    "ans": 1,
                    "exp": "The prefix 1.3.6.1.2.1 corresponds to iso.org.dod.internet.mgmt.mib-2 (§9.3.1)."
                }
            ]
        }
    ]
}
