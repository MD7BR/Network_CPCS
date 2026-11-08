"""Chapter 2 Data: Application Layer (Kurose & Ross 6th & 8th Ed.)
Exhaustive textbook depth, Midterm Study Guide integration (P9-P16), bit-accurate diagrams,
and fully functional interactive calculators and steppers.
"""

CH2_DATA = {
    "id": "ch2",
    "num": 2,
    "title": "Application Layer",
    "subtitle": "Network Applications, HTTP, Email, DNS, P2P, Video Streaming, CDNs & Sockets",
    "layer": "Application Layer",
    "color": "#8b5cf6",
    "objectives": [
        "Compare the Client-Server and Peer-to-Peer (P2P) network application paradigms",
        "Explain processes, sockets, and how a process is addressed (IP address + port number)",
        "List the four things an application-layer protocol defines (types, syntax, semantics, rules)",
        "Match applications to their transport service requirements (data loss, throughput, timing)",
        "Compare TCP and UDP service models and explain what TLS adds at the application layer",
        "Dissect HTTP request and response messages, header lines, and HTTP status codes",
        "Compare non-persistent and persistent HTTP and compute response times (2 RTT + L/R)",
        "Explain the four components of cookies and describe user session tracking",
        "Analyze Web caching, proxy server delay improvements, and Conditional GET",
        "Explain Head-of-Line (HOL) blocking and how HTTP/2 and HTTP/3 mitigate latency",
        "Describe email components, SMTP transfer commands, and mail access protocols (POP3, IMAP)",
        "Trace the DNS hierarchy, iterated vs recursive queries, caching, and Resource Records (A, NS, CNAME, MX)",
        "Explain BitTorrent mechanisms: chunks, tracker, churn, rarest-first, and tit-for-tat incentives",
        "Formulate video encoding, continuous playout buffering, DASH, and CDN placement philosophies"
    ],
    "sections": [
        {
            "id": "ch2-1",
            "num": "2.1",
            "title": "Principles of Network Applications",
            "subtitle": "Application architectures, communicating processes, sockets, and transport requirements",
            "content": r"""
<p>At the core of network application development is writing programs that run on different end systems and communicate with each other over the network. Crucially, application software runs <strong>strictly on end systems</strong>; you do not write software that executes inside network-core packet switches or routers.</p>

<h3>2.1.1 Application Architectures: Client-Server vs P2P</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.88rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px 10px;">Dimension</th>
      <th style="padding:8px 10px;">Client-Server Paradigm</th>
      <th style="padding:8px 10px;">Peer-to-Peer (P2P) Architecture</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">Server Characteristics</td>
      <td style="padding:8px 10px;">Always-on host with a fixed, well-known IP address. Scalability requires massive data centers.</td>
      <td style="padding:8px 10px; color:var(--text-secondary);">No dedicated central server. Arbitrary pairs of connected end systems communicate directly.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">Client / Peer Role</td>
      <td style="padding:8px 10px;">Clients do not communicate directly with each other; they only contact the server.</td>
      <td style="padding:8px 10px; color:var(--primary-text); font-weight:600;">Peers are both consumers and suppliers of service. A peer is a client when downloading, and a server when uploading.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:8px 10px; font-weight:700;">Scalability</td>
      <td style="padding:8px 10px; color:var(--danger-text);">Server bandwidth bottleneck as clients grow; high infrastructure cost.</td>
      <td style="padding:8px 10px; color:var(--accent-text); font-weight:700;"><strong>Self-Scalability:</strong> Each new peer brings new upload capacity as well as new service demand.</td>
    </tr>
    <tr>
      <td style="padding:8px 10px; font-weight:700;">Host Connectivity</td>
      <td style="padding:8px 10px;">Server has fixed IP, 24/7 uptime; clients have dynamic IPs and intermittent connectivity.</td>
      <td style="padding:8px 10px;">Peers are intermittently connected and change IP addresses dynamically (high <strong>churn</strong>).</td>
    </tr>
  </tbody>
</table>

<h3>2.1.2 Processes Communicating Across the Network</h3>
<p>In operating systems terminology, an executing program is a <strong>process</strong>. When two processes communicate across different hosts, they do so by exchanging messages through a software interface called a <strong>socket</strong>.</p>

<div class="callout callout-def">
  <div class="callout-header">🚪 The Socket Interface (The Door Analogy)</div>
  A <strong>socket</strong> is the software interface between an application-layer process and the underlying transport-layer protocol stack.
  <ul>
    <li>A process is analogous to a house, and its socket is analogous to its front door. When a process wants to send a message to another process, it pushes the message out its door into the network.</li>
    <li><strong>Control boundary:</strong> The application developer controls everything on the <em>application-layer side</em> of the socket (message format, timing, application logic). The developer has very little control over the <em>transport-layer side</em>, limited only to: (1) choosing TCP or UDP, and (2) setting a few transport parameters such as buffer sizes and maximum segment sizes.</li>
  </ul>
</div>

<h3>Addressing Communicating Processes</h3>
<p>To deliver a message to a specific process running on a remote host, the sending host requires two pieces of addressing information:</p>
<ol>
  <li><strong>IP Address (32-bit in IPv4):</strong> Identifies the specific destination host across the global Internet.</li>
  <li><strong>Port Number (16-bit integer, 0–65535):</strong> Identifies the specific receiving process / socket on that destination host. Why is the IP address alone not enough? Because a single host runs dozens of network processes simultaneously (web server, email server, SSH daemon, browser)!</li>
</ol>

<h3>2.1.3 What Does an Application-Layer Protocol Define?</h3>
<p>An application-layer protocol defines how application processes running on different end systems pass messages to each other:</p>
<ol>
  <li><strong>Types of messages exchanged:</strong> (e.g. request messages and response messages).</li>
  <li><strong>Syntax of message fields:</strong> How fields are delineated and formatted (e.g. ASCII strings terminated by CRLF).</li>
  <li><strong>Semantics of the fields:</strong> The meaning of the information contained in the fields.</li>
  <li><strong>Rules:</strong> Determining when and how a process sends messages and responds to messages.</li>
</ol>
<p>Protocols defined in RFCs (such as HTTP, SMTP, DNS) are <strong>open protocols</strong> that guarantee interoperability between different software vendors. In contrast, proprietary protocols (like Skype or Zoom) use closed formats.</p>

<h3>2.1.4 Transport Service Needs of Network Applications</h3>
<p>Different applications have vastly different transport requirements along three dimensions:</p>
<ul>
  <li><strong>Data Loss:</strong> Some applications (file transfer, Web, email, banking) require <strong>100% reliable data transfer</strong> (zero loss tolerated). Multimedia applications (conversational audio/video, live streaming) are <strong>loss-tolerant</strong> (a dropped packet produces only minor visual or audio glitch).</li>
  <li><strong>Throughput:</strong> <em>Bandwidth-sensitive applications</em> (video streaming, VoIP) require a minimum guaranteed throughput to be effective. <em>Elastic applications</em> (email, file download, Web browsing) can utilize whatever throughput is available without failing.</li>
  <li><strong>Timing / Delay:</strong> Interactive real-time applications (Internet telephony, video conferencing, multiplayer games) require low latency (tens to hundreds of milliseconds) to feel conversational. Delay is non-critical for elastic file transfers.</li>
</ul>

<div class="callout callout-exam">
  <div class="callout-header">🎯 Transport Service Requirements Table (Kurose & Ross Table 2.1 / Study Guide P10)</div>
  <table style="width:100%; border-collapse:collapse; margin-top:0.5rem; font-size:0.85rem;">
    <tr style="border-bottom:2px solid var(--border); font-weight:700;">
      <td style="padding:6px 8px;">Application</td>
      <td style="padding:6px 8px;">Data Loss?</td>
      <td style="padding:6px 8px;">Throughput Guarantee?</td>
      <td style="padding:6px 8px;">Time Sensitive?</td>
      <td style="padding:6px 8px;">Typical Transport Protocol</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 8px; font-weight:600;">File Transfer / Download</td>
      <td style="padding:6px 8px; color:var(--danger-text);">No loss tolerated</td>
      <td style="padding:6px 8px;">Elastic</td>
      <td style="padding:6px 8px;">No</td>
      <td style="padding:6px 8px; font-weight:700; color:var(--primary-text);">TCP</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 8px; font-weight:600;">Web Browsing</td>
      <td style="padding:6px 8px; color:var(--danger-text);">No loss tolerated</td>
      <td style="padding:6px 8px;">Elastic</td>
      <td style="padding:6px 8px;">No (few seconds)</td>
      <td style="padding:6px 8px; font-weight:700; color:var(--primary-text);">TCP</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 8px; font-weight:600;">E-Mail</td>
      <td style="padding:6px 8px; color:var(--danger-text);">No loss tolerated</td>
      <td style="padding:6px 8px;">Elastic</td>
      <td style="padding:6px 8px;">No</td>
      <td style="padding:6px 8px; font-weight:700; color:var(--primary-text);">TCP</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 8px; font-weight:600;">Internet Telephony (VoIP)</td>
      <td style="padding:6px 8px; color:var(--accent-text);">Loss-tolerant</td>
      <td style="padding:6px 8px;">Audio: 64–128 kbps</td>
      <td style="padding:6px 8px; color:var(--danger-text); font-weight:700;">Yes: 10's–150 ms</td>
      <td style="padding:6px 8px; font-weight:700;">UDP or TCP</td>
    </tr>
    <tr>
      <td style="padding:6px 8px; font-weight:600;">Interactive Real-Time Games</td>
      <td style="padding:6px 8px; color:var(--accent-text);">Loss-tolerant</td>
      <td style="padding:6px 8px;">Few kbps–100 kbps</td>
      <td style="padding:6px 8px; color:var(--danger-text); font-weight:700;">Yes: 10's–100 ms</td>
      <td style="padding:6px 8px; font-weight:700;">UDP or TCP</td>
    </tr>
  </table>
</div>

<h3>2.1.5 TCP vs UDP Services and What TLS Adds</h3>
<ul>
  <li><strong>TCP Service Model:</strong> Connection-oriented (3-way handshake), 100% reliable in-order byte stream, flow control (prevents sender overflowing receiver buffer), and congestion control (throttles sender when network core is congested). <em>Does NOT provide: timing guarantees, delay guarantees, or throughput minimums.</em></li>
  <li><strong>UDP Service Model:</strong> Connectionless (no handshake), lightweight, unreliable best-effort data delivery. No flow control, no congestion control. Allows applications to pump bits as fast as desired.</li>
  <li><strong>Securing TCP with TLS (Transport Layer Security):</strong> Neither TCP nor UDP provides any encryption; cleartext passwords sent over standard TCP are vulnerable to packet sniffing. <strong>TLS/SSL</strong> is implemented at the <strong>Application layer</strong> (using TCP underneath) to provide end-to-end encryption, message integrity, and endpoint authentication.</li>
</ul>
""",
            "quiz": [
                {
                    "q": "Why is a destination host's IP address not sufficient to identify the destination receiving process?",
                    "opts": [
                        "Because IP addresses change dynamically",
                        "Because a single host may run many network processes concurrently; the 16-bit port number is needed to demultiplex messages to the specific socket",
                        "Because IP addresses are only used at Layer 2",
                        "Because routers mask IP addresses"
                    ],
                    "ans": 1,
                    "exp": "The 32-bit IP address identifies the machine, while the 16-bit port number identifies the specific application process/socket running on that machine (§2.1.2 / P9c)."
                },
                {
                    "q": "At which layer of the Internet protocol stack is TLS (Transport Layer Security) actually implemented?",
                    "opts": [
                        "Network Layer",
                        "Link Layer",
                        "Application Layer (using TCP socket services)",
                        "Physical Layer"
                    ],
                    "ans": 2,
                    "exp": "TLS is an application-layer enhancement. Application code links to TLS libraries (like OpenSSL), which encrypt data before passing it to the standard TCP transport socket (§2.1.5)."
                }
            ]
        },
        {
            "id": "ch2-2",
            "num": "2.2",
            "title": "The Web and HTTP",
            "subtitle": "HTTP message formats, persistent connections, cookies, web caching, and HTTP/2 & 3",
            "content": r"""
<p>The <strong>Hypertext Transfer Protocol (HTTP)</strong> is the Web's application-layer protocol (RFC 1945 for HTTP/1.0, RFC 2616 for HTTP/1.1, RFC 7540 for HTTP/2, RFC 9114 for HTTP/3). A Web page consists of <strong>objects</strong> (base HTML file, JPEG images, CSS stylesheets, JavaScript files) addressable by a <strong>Uniform Resource Locator (URL)</strong>:</p>
<div class="math-display">
  \underbrace{\text{http://www.someschool.edu}}_{\text{Host name}} \ / \ \underbrace{\text{someDepartment/home.index}}_{\text{Path name}}
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 HTTP is a Stateless Protocol</div>
  An HTTP server maintains <strong>no state</strong> about past client requests. If a client requests the same object twice in a few seconds, the server resends the entire object from scratch without remembering the previous request.
</div>

<h3>2.2.2 Non-Persistent vs Persistent HTTP Connections</h3>
<ul>
  <li><strong>Non-Persistent Connections (HTTP/1.0 default):</strong> Each TCP connection is closed immediately after the server sends the requested object. Fetching a page with 1 base HTML file and 10 JPEG images requires <strong>11 separate TCP connections</strong>!
    <div class="math-display">
      \text{Response Time per Object} = 2 \times \text{RTT} + d_{\text{trans}}
    </div>
    (1 RTT for TCP 3-way handshake + 1 RTT for HTTP GET request and first bytes of response).
  </li>
  <li><strong>Persistent Connections (HTTP/1.1 default):</strong> The server leaves the TCP connection open after sending a response. Subsequent requests and responses between the same client and server can be sent over the same ongoing TCP connection.
    <br>&bull; <em>Persistent with Pipelining:</em> The client sends requests as soon as it parses referenced objects, back-to-back without waiting for prior responses. All referenced objects can be retrieved in roughly <strong>1 RTT</strong> total!
  </li>
</ul>

<!-- FIGURE 2.1: INTERACTIVE HTTP TIMELINE -->
<div class="svg-figure">
  <div class="svg-container">
    <svg id="http-timeline-svg" viewBox="0 0 760 270" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <text x="140" y="30" font-size="12" font-weight="700" fill="#2563eb" text-anchor="middle">Client (Web Browser)</text>
      <text x="620" y="30" font-size="12" font-weight="700" fill="#8b5cf6" text-anchor="middle">Origin Web Server</text>

      <line x1="140" y1="45" x2="140" y2="250" stroke="#94a3b8" stroke-width="2"/>
      <line x1="620" y1="45" x2="620" y2="250" stroke="#94a3b8" stroke-width="2"/>
      <text x="380" y="42" font-size="10" fill="#64748b" text-anchor="middle">&darr; Time flows downwards &darr;</text>

      <!-- TCP Handshake: 1 RTT -->
      <line x1="140" y1="65" x2="620" y2="95" stroke="#3b82f6" stroke-width="2"/>
      <text x="380" y="75" font-size="10" fill="#1e40af" text-anchor="middle">1. TCP SYN (Connection Request)</text>

      <line x1="620" y1="95" x2="140" y2="125" stroke="#3b82f6" stroke-width="2"/>
      <text x="380" y="105" font-size="10" fill="#1e40af" text-anchor="middle">2. TCP SYN-ACK &bull; 1 RTT Elapsed</text>

      <!-- Base HTML GET: 2 RTT -->
      <line x1="140" y1="125" x2="620" y2="155" stroke="#10b981" stroke-width="2"/>
      <text x="380" y="135" font-size="10" fill="#047857" text-anchor="middle">3. HTTP GET index.html (ACK piggybacked)</text>

      <line x1="620" y1="155" x2="140" y2="185" stroke="#10b981" stroke-width="2"/>
      <text x="380" y="165" font-size="10" fill="#047857" text-anchor="middle">4. HTTP 200 OK (index.html payload) &bull; 2 RTT + L/R Elapsed</text>

      <!-- Persistent Reuse: 1 extra RTT -->
      <line x1="140" y1="190" x2="620" y2="220" stroke="#8b5cf6" stroke-width="2"/>
      <text x="380" y="200" font-size="10" fill="#6d28d9" text-anchor="middle">5. HTTP GET image.png (over SAME open persistent TCP connection!)</text>

      <line x1="620" y1="220" x2="140" y2="250" stroke="#8b5cf6" stroke-width="2"/>
      <text x="380" y="230" font-size="10" fill="#6d28d9" text-anchor="middle">6. HTTP 200 OK (image.png) &bull; Only 1 additional RTT!</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 2.1 — Timeline of TCP 3-Way Handshake followed by HTTP/1.1 persistent request/response exchanges (§2.2.2).</div>
</div>

<h3>2.2.3 HTTP Message Formats (Command-Line Dissection)</h3>
<p>HTTP messages are human-readable ASCII text strings. There are two types: request and response.</p>

<div class="callout callout-exam">
  <div class="callout-header">🎯 High-Yield Exam Dissection: HTTP Request Message Format</div>
  <pre style="background:var(--bg-secondary); border:1px solid var(--border); padding:0.85rem; border-radius:6px; font-size:0.85rem; line-height:1.6; overflow-x:auto;">
<code>GET /cpcs371/notes/ch2.html HTTP/1.1\r\n
Host: www.example.edu\r\n
Connection: keep-alive\r\n
Keep-Alive: timeout=5, max=100\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n
Accept-Language: en-US,en;q=0.9,ar;q=0.8\r\n
\r\n</code></pre>
  <ul>
    <li><strong>Request Line (Line 1):</strong> Has three fields:
      <ol>
        <li><strong>Method:</strong> <code>GET</code> (requests an object). Other methods: <code>POST</code> (uploads user form data in the entity body), <code>HEAD</code> (requests identical headers without the body, used for debugging), <code>PUT</code> (uploads an object to the specified path), <code>DELETE</code> (removes an object).</li>
        <li><strong>URL Path:</strong> <code>/cpcs371/notes/ch2.html</code> (path on server disk).</li>
        <li><strong>HTTP Version:</strong> <code>HTTP/1.1</code>.</li>
      </ol>
    </li>
    <li><strong><code>Host: www.example.edu</code>:</strong> <strong>Mandatory in HTTP/1.1!</strong> Required for Web proxy caches and <em>virtual hosting</em>, where multiple domain names share the same physical server and public IP address.</li>
    <li><strong><code>Connection: keep-alive</code>:</strong> Informs the server that the client wants a persistent connection. (Set to <code>close</code> if non-persistent).</li>
    <li><strong><code>Keep-Alive: timeout=5, max=100</code>:</strong> The server should close the idle connection after 5 seconds of inactivity, and service at most 100 requests over this single connection.</li>
    <li><strong><code>User-Agent:</code>:</strong> Identifies client browser and OS (used for server content negotiation).</li>
    <li><strong>Empty Line (<code>\r\n</code>):</strong> Marks the end of the header section.</li>
  </ul>
</div>

<div class="callout callout-exam">
  <div class="callout-header">🎯 High-Yield Exam Dissection: HTTP Response Message Format</div>
  <pre style="background:var(--bg-secondary); border:1px solid var(--border); padding:0.85rem; border-radius:6px; font-size:0.85rem; line-height:1.6; overflow-x:auto;">
<code>HTTP/1.1 200 OK\r\n
Date: Thu, 05 Nov 2026 07:31:00 GMT\r\n
Server: Apache/2.4.52 (Ubuntu)\r\n
Last-Modified: Wed, 21 Oct 2026 07:28:00 GMT\r\n
Content-Length: 6821\r\n
Content-Type: text/html; charset=UTF-8\r\n
\r\n
&lt;html&gt;&lt;head&gt;...&lt;/html&gt; (Entity Body)</code></pre>
  <ul>
    <li><strong>Status Line:</strong> Protocol version (<code>HTTP/1.1</code>), 3-digit status code (<code>200</code>), and phrase (<code>OK</code>).</li>
    <li><strong>Common HTTP Status Codes:</strong>
      <ul>
        <li><code>200 OK</code>: Request succeeded and requested object is in entity body.</li>
        <li><code>301 Moved Permanently</code>: Requested object relocated; new URL specified in <code>Location:</code> header.</li>
        <li><code>304 Not Modified</code>: Conditional GET response; cached copy is up to date, entity body is empty!</li>
        <li><code>400 Bad Request</code>: Generic error code; server could not understand request.</li>
        <li><code>404 Not Found</code>: The requested document does not exist on this server.</li>
        <li><code>505 HTTP Version Not Supported</code>: Server cannot speak the requested HTTP protocol version.</li>
      </ul>
    </li>
    <li><strong><code>Date:</code>:</strong> Time the server created and transmitted this response (NOT when file was last edited).</li>
    <li><strong><code>Last-Modified:</code>:</strong> Timestamp when the object was created or last modified on server disk. Critical for caching!</li>
    <li><strong><code>Content-Length:</code>:</strong> Size of entity body in bytes (tells persistent connections where object ends).</li>
    <li><strong><code>Content-Type:</code>:</strong> MIME type of payload (e.g. <code>text/html</code>, <code>image/jpeg</code>).</li>
  </ul>
</div>

<h3>2.2.4 User-Server Interaction: Cookies</h3>
<p>Because HTTP is stateless, websites use <strong>cookies</strong> to track user state (shopping carts, user identity, recommendations). The cookie technology has <strong>four components</strong>:</p>
<ol>
  <li>A cookie header line in the HTTP response message: <code>Set-Cookie: 167845</code>.</li>
  <li>A cookie header line in subsequent HTTP request messages: <code>Cookie: 167845</code>.</li>
  <li>A cookie file stored on the user's host and managed by the browser.</li>
  <li>A back-end database at the website mapping cookie IDs to user session history and preferences.</li>
</ol>

<h3>2.2.5 & 2.2.6 Web Caching and the Conditional GET</h3>
<p>A <strong>Web cache</strong> (or <strong>proxy server</strong>) satisfies HTTP requests on behalf of origin Web servers. It has its own local storage, keeping copies of recently requested objects.</p>

<div class="callout callout-exam">
  <div class="callout-header">🎯 Classic Exam Calculation: Web Caching Delay Improvement (Slides Worked Example)</div>
  Suppose average object size is <span class="math-inline">L = 100\text{ Kbits}</span>, request rate is 15 req/s. Access link is <span class="math-inline">R = 1.54\text{ Mbps}</span>, and RTT from edge router to origin server is 2 seconds.
  <ul>
    <li>Average arrival rate of bits: <span class="math-inline">15 \times 100\text{ Kbits} = 1.50\text{ Mbps}</span>.</li>
    <li>Access link utilization without cache:
      <div class="math-display">\text{Utilization} = \frac{1.50\text{ Mbps}}{1.54\text{ Mbps}} = \mathbf{0.974} \ (97.4\%)</div>
      Queuing delay is in minutes/seconds; total response time is enormous.
    </li>
    <li>Now install an institutional Web cache with hit rate <span class="math-inline">h = 0.40</span> (40%):
      <br>&bull; 40% of requests are satisfied locally over LAN in &lt; 10 ms.
      <br>&bull; Traffic on the 1.54 Mbps access link drops by 40%: new arrival rate = <span class="math-inline">0.60 \times 1.50 = 0.90\text{ Mbps}</span>.
      <br>&bull; New access link utilization: <span class="math-inline">\frac{0.90}{1.54} = \mathbf{0.584} \ (58.4\%)</span>.
      <br>&bull; Average end-to-end response time drops from multiple seconds to:
      <div class="math-display">d_{\text{avg}} = 0.4 \times (0.01\text{ s}) + 0.6 \times (2.01\text{ s}) \approx \mathbf{1.2\text{ seconds}}</div>
      A dramatic improvement without buying expensive link bandwidth!
    </li>
  </ul>
</div>

<p>To prevent serving stale data, the cache issues a <strong>Conditional GET</strong>:</p>
<ol>
  <li>The cache sends a GET request containing: <code>If-Modified-Since: Wed, 21 Oct 2026 07:28:00 GMT</code>.</li>
  <li>If the object has not changed, the server replies: <strong><code>HTTP/1.1 304 Not Modified</code></strong> with an <strong>empty entity body</strong>, saving link bandwidth!</li>
</ol>

<h3>2.2.7 HTTP/2 and HTTP/3</h3>
<ul>
  <li><strong>HTTP/1.1 HOL Blocking:</strong> If a large or slow object is at the head of a pipelined connection, all following objects are delayed behind it.</li>
  <li><strong>HTTP/2:</strong> Eliminates application-layer Head-of-Line (HOL) blocking by dividing messages into independent <strong>binary frames</strong> and <strong>multiplexing</strong> multiple bidirectional request/response streams over a single TCP connection. Also adds server push and stream prioritization.</li>
  <li><strong>HTTP/3:</strong> While HTTP/2 solved application HOL blocking, TCP packet loss still stalled all multiplexed streams at the transport layer. HTTP/3 runs over <strong>QUIC</strong> (built on top of <strong>UDP</strong>), providing independent per-stream loss recovery and zero-RTT connection establishment.</li>
</ul>
""",
            "quiz": [
                {
                    "q": "What is the primary role of the 'Host:' header in an HTTP/1.1 request message?",
                    "opts": [
                        "It specifies the client host's MAC address",
                        "It is mandatory for virtual hosting and caching, allowing one physical server with one IP address to host multiple domain names",
                        "It sets the TCP port number",
                        "It prevents SQL injection attacks"
                    ],
                    "ans": 1,
                    "exp": "Without the Host: header, a web server hosting multiple domains on the same IP address cannot tell which virtual website the client is requesting (§2.2.3 / P11a)."
                },
                {
                    "q": "What HTTP status code is returned by a web server when an object has NOT been modified since the timestamp in 'If-Modified-Since'?",
                    "opts": [
                        "200 OK",
                        "301 Moved Permanently",
                        "304 Not Modified (with empty entity body)",
                        "404 Not Found"
                    ],
                    "ans": 2,
                    "exp": "The server sends '304 Not Modified' with no body, telling the client/cache to use its stored copy (§2.2.6)."
                }
            ]
        },
        {
            "id": "ch2-3",
            "num": "2.3",
            "title": "File Transfer: FTP",
            "subtitle": "Out-of-band control on port 21 vs data transfer on port 20",
            "content": r"""
<p>The <strong>File Transfer Protocol (FTP, RFC 959)</strong> transfers files between a client host and a remote server. While both HTTP and FTP transfer files, FTP operates under a unique architectural design:</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Out-of-Band Control: Port 21 vs Port 20</div>
  FTP uses two parallel TCP connections:
  <ol>
    <li><strong>Control Connection (TCP Port 21):</strong> Used for sending user identification, password, directory commands, and file transfer commands. Remains open throughout the entire multi-file user session.</li>
    <li><strong>Data Connection (TCP Port 20):</strong> Created anew for every single file transfer. When the transfer of a file (or directory listing) completes, the data connection is immediately closed.</li>
  </ol>
  Because FTP sends its control information over a completely separate connection from its data, FTP control is called <strong>out-of-band</strong> (in contrast to HTTP, which is <strong>in-band</strong> because request headers and file payloads share the exact same connection).
</div>

<h3>FTP Session State</h3>
<p>Unlike stateless HTTP, an FTP server is <strong>stateful</strong>. The server maintains state about the client: current working directory, authenticated user identity, and active data port bindings.</p>

<div class="callout callout-exam">
  <div class="callout-header">🎯 Common FTP Commands and Status Replies</div>
  <ul>
    <li><code>USER username</code>: Sends username. Server replies <code>331 User name okay, need password</code>.</li>
    <li><code>PASS password</code>: Sends password. Server replies <code>230 User logged in, proceed</code>.</li>
    <li><code>LIST</code>: Requests directory listing (sent over a new data connection).</li>
    <li><code>RETR filename</code>: Retrieves (downloads) a file from server.</li>
    <li><code>STOR filename</code>: Stores (uploads) a file onto server.</li>
  </ul>
</div>
""",
            "quiz": [
                {
                    "q": "Why is FTP's control connection described as 'out-of-band'?",
                    "opts": [
                        "It uses UDP instead of TCP",
                        "It uses a separate TCP connection (port 21) from the data transfer connection (port 20)",
                        "It bypasses operating system sockets",
                        "It only works on wireless networks"
                    ],
                    "ans": 1,
                    "exp": "FTP sends control commands over TCP port 21 and data over a separate TCP connection on port 20. Because control info does not travel in the data connection, it is 'out-of-band' (§2.3)."
                }
            ]
        },
        {
            "id": "ch2-4",
            "num": "2.4",
            "title": "Electronic Mail in the Internet",
            "subtitle": "SMTP protocol exchange, mail message formats, and mail access (POP3 vs IMAP vs Webmail)",
            "content": r"""
<p>Internet email consists of three major architectural components: <strong>user agents</strong>, <strong>mail servers</strong>, and the <strong>Simple Mail Transfer Protocol (SMTP, RFC 5321)</strong>.</p>

<h3>2.4.1 SMTP and the 6-Step Alice-to-Bob Mail Path</h3>
<p>Suppose Alice wants to send an email to Bob:</p>
<ol>
  <li>Alice composes a message in her user agent and clicks Send.</li>
  <li>Alice's user agent sends the message to her <strong>sender mail server</strong> over SMTP (or HTTP), where it is placed in the message queue.</li>
  <li>The client side of SMTP running on Alice's mail server opens a <strong>TCP connection to Bob's mail server on port 25</strong>.</li>
  <li>After an initial SMTP handshake, Alice's mail server transmits the message over the TCP connection.</li>
  <li>Bob's mail server deposits the arriving message into Bob's <strong>mailbox</strong> on disk.</li>
  <li>Bob retrieves the message from his mailbox using a mail access protocol (POP3, IMAP, or HTTP).</li>
</ol>

<div class="callout callout-exam">
  <div class="callout-header">🎯 SMTP Command Exchange Protocol Trace (Study Guide P13)</div>
  SMTP command phases occur in a strict, prescribed sequence:
  <ol>
    <li><strong>Handshaking Phase:</strong>
      <br>&bull; Server: <code>220 mail.bob.com ESMTP ready</code>
      <br>&bull; Client: <code>HELO mail.alice.com</code>
      <br>&bull; Server: <code>250 Hello mail.alice.com, pleased to meet you</code>
    </li>
    <li><strong>Transfer Phase:</strong>
      <br>&bull; Client: <code>MAIL FROM: &lt;alice@alice.com&gt;</code> &rarr; Server: <code>250 Sender OK</code>
      <br>&bull; Client: <code>RCPT TO: &lt;bob@bob.com&gt;</code> &rarr; Server: <code>250 Recipient OK</code>
      <br>&bull; Client: <code>DATA</code> &rarr; Server: <code>354 Start mail input; end with &lt;CRLF&gt;.&lt;CRLF&gt;</code>
      <br>&bull; Client transmits header lines (<code>To:</code>, <code>From:</code>, <code>Subject:</code>) and message body lines.
      <br>&bull; Client transmits: <strong><code>.</code></strong> (a single line containing only a period) to mark end of message!
      <br>&bull; Server: <code>250 Message accepted for delivery</code>
    </li>
    <li><strong>Closure Phase:</strong>
      <br>&bull; Client: <code>QUIT</code> &rarr; Server: <code>221 mail.bob.com closing connection</code>
    </li>
  </ol>
</div>

<div class="callout callout-def">
  <div class="callout-header">⚖️ SMTP vs HTTP Comparison</div>
  <ul>
    <li><strong>Push vs Pull:</strong> HTTP is mainly a <strong>pull protocol</strong> (users pull web pages from server). SMTP is fundamentally a <strong>push protocol</strong> (sending mail server pushes mail to receiving mail server).</li>
    <li><strong>Character Encoding:</strong> SMTP requires all messages to be in <strong>7-bit ASCII</strong> format (binary attachments must be encoded via Base64/MIME). HTTP allows arbitrary binary data.</li>
    <li><strong>Handling Multiple Objects:</strong> HTTP encapsulates each object in its own response message. SMTP places all text and attachments into a <strong>single multipart message</strong>.</li>
  </ul>
</div>

<h3>2.4.4 Mail Access Protocols: POP3 vs IMAP vs Webmail</h3>
<ul>
  <li><strong>POP3 (Post Office Protocol 3, TCP Port 110):</strong> Simple. Client downloads messages from mailbox. Can operate in <em>download-and-delete</em> (messages deleted from server after download) or <em>download-and-keep</em>. Does not preserve folder states across multiple devices.</li>
  <li><strong>IMAP (Internet Mail Access Protocol, TCP Port 143):</strong> Advanced. Associates each message with a folder on the server. Maintains folder hierarchy and state across multiple devices (phone, laptop, desktop). Allows partial message download (e.g. headers only).</li>
  <li><strong>Webmail (HTTP/HTTPS, Port 443):</strong> Browser communicates with user's mail server via HTTP; the mail server communicates with remote mail servers via SMTP.</li>
</ul>
""",
            "quiz": [
                {
                    "q": "Which sequence correctly orders the phases and commands of an SMTP mail transfer?",
                    "opts": [
                        "HELO → DATA → QUIT → MAIL FROM: → RCPT TO: → .",
                        "HELO (handshaking) → MAIL FROM: → RCPT TO: → DATA → message body → . (end message) → QUIT (closure)",
                        "MAIL FROM: → RCPT TO: → HELO → QUIT → DATA",
                        "DATA → HELO → MAIL FROM: → ."
                    ],
                    "ans": 1,
                    "exp": "SMTP order: Handshaking (HELO) → Envelope sender (MAIL FROM:) → Envelope recipient (RCPT TO:) → Message content (DATA) → Terminating period (.) → Connection teardown (QUIT) (§2.4 / P13)."
                },
                {
                    "q": "Why can SMTP NOT be used by Bob's smartphone to retrieve emails from his own mail server?",
                    "opts": [
                        "SMTP does not support passwords",
                        "SMTP is strictly a push protocol, whereas retrieving messages requires a pull protocol like POP3, IMAP, or HTTP",
                        "SMTP operates over UDP",
                        "Bob's smartphone does not have an IP address"
                    ],
                    "ans": 1,
                    "exp": "SMTP pushes messages from sender to receiver. Pulling messages from a server mailbox requires a pull protocol such as POP3, IMAP, or Webmail (§2.4.4)."
                }
            ]
        },
        {
            "id": "ch2-5",
            "num": "2.5",
            "title": "DNS—The Internet's Directory Service",
            "subtitle": "Hierarchical architecture, iterative vs recursive queries, caching, and Resource Records",
            "content": r"""
<p>While humans prefer mnemonic names like <code>www.kau.edu.sa</code>, network routers identify destination interfaces using 32-bit IP addresses like <code>212.111.45.10</code>. The <strong>Domain Name System (DNS, RFC 1034/1035)</strong> is the Internet's distributed, hierarchical directory service that translates hostnames to IP addresses. DNS runs over <strong>UDP port 53</strong>.</p>

<h3>2.5.1 Services Provided by DNS</h3>
<ol>
  <li><strong>Hostname-to-IP Translation:</strong> Translates human-friendly hostnames to IP addresses.</li>
  <li><strong>Host Aliasing:</strong> A host with a complex canonical name (e.g. <code>server-east-01.cdn.kau.edu.sa</code>) can have one or more alias names (e.g. <code>www.kau.edu.sa</code>).</li>
  <li><strong>Mail Server Aliasing:</strong> Enables clean email addresses (e.g. <code>student@kau.edu.sa</code>) by mapping the domain to the canonical mail server host (e.g. <code>mail.kau.edu.sa</code>).</li>
  <li><strong>Load Distribution:</strong> Busy sites replicate across multiple server IP addresses. DNS rotates the order of returned IP addresses (round-robin DNS) to balance traffic.</li>
</ol>

<div class="callout callout-insight">
  <div class="callout-header">💡 Why Is DNS Distributed Instead of Centralized?</div>
  A single centralized DNS server would suffer from fatal limitations:
  <ul>
    <li><strong>Single Point of Failure:</strong> If the central server crashes, the entire global Internet stops working!</li>
    <li><strong>Traffic Volume:</strong> A single server would have to handle hundreds of billions of queries per second.</li>
    <li><strong>Distant Centralized Database:</strong> Queries from across the globe would experience enormous propagation delays.</li>
    <li><strong>Maintenance:</strong> Storing and updating all global records on one machine is administratively impossible.</li>
  </ul>
</div>

<h3>2.5.2 The DNS Hierarchy</h3>
<ul>
  <li><strong>Root DNS Servers:</strong> 13 logical root server IP addresses worldwide (named A through M), managed by 12 distinct organizations. Each logical address is replicated across hundreds of physical servers using anycast routing.</li>
  <li><strong>Top-Level Domain (TLD) Servers:</strong> Responsible for generic top-level domains (<code>.com</code>, <code>.org</code>, <code>.edu</code>, <code>.gov</code>) and country code domains (<code>.sa</code>, <code>.uk</code>, <code>.jp</code>).</li>
  <li><strong>Authoritative DNS Servers:</strong> Every organization with publicly accessible hosts must provide authoritative DNS records mapping its hostnames to IPs.</li>
  <li><strong>Local DNS Server (Default Resolver):</strong> Does not strictly belong to the hierarchy. Each ISP or university operates a local DNS server (e.g. via DHCP). When a host issues a DNS query, the query is sent directly to its local DNS server, which acts as a proxy to query the hierarchy.</li>
</ul>

<!-- EMBEDDED INTERACTIVE: DNS RESOLUTION WALKTHROUGH -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">🌳 Interactive Iterated DNS Resolution Trace (8 Messages)</div>
    <span class="interactive-badge">Study Guide P14 Trace</span>
  </div>
  <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Trace how a client at <code>engineering.nyu.edu</code> resolves <code>gaia.cs.umass.edu</code> using standard <strong>iterative queries</strong>:
  </p>
  <div class="sim-viewport" style="align-items:flex-start; min-height:130px;">
    <div style="width:100%;">
      <div id="sec2-dns-step" style="font-weight:700; color:var(--primary-text); font-size:1rem; margin-bottom:0.35rem;">
        Step 1: Host to Local DNS Server
      </div>
      <div id="sec2-dns-desc" style="font-size:0.85rem; color:var(--text-secondary); line-height:1.6;">
        Client host at <code>engineering.nyu.edu</code> queries its Local DNS Server (<code>dns.nyu.edu</code>) for <code>gaia.cs.umass.edu</code>. This query is <strong>recursive</strong> (local DNS takes responsibility to resolve it).
      </div>
    </div>
  </div>
  <div class="sim-controls">
    <button class="btn-primary" onclick="stepSec2DNS()">⏭ Next DNS Query Step</button>
    <button class="btn-secondary" onclick="resetSec2DNS()">🔄 Reset</button>
  </div>
</div>

<h3>2.5.3 DNS Resource Records (RR)</h3>
<p>DNS servers store <strong>Resource Records (RRs)</strong>, which are 4-tuples: <span class="math-inline">(\text{Name}, \text{Value}, \text{Type}, \text{TTL})</span>.</p>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:0.85rem;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:6px 10px;">RR Type</th>
      <th style="padding:6px 10px;">Name Field</th>
      <th style="padding:6px 10px;">Value Field</th>
      <th style="padding:6px 10px;">Description & Example</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700; color:var(--primary-text);">Type A</td>
      <td style="padding:6px 10px;">Hostname</td>
      <td style="padding:6px 10px;">IPv4 Address</td>
      <td style="padding:6px 10px;">Standard hostname-to-IP mapping: <code>(dns1.abc.com, 10.1.2.3, A)</code></td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700; color:var(--accent-text);">Type NS</td>
      <td style="padding:6px 10px;">Domain Name</td>
      <td style="padding:6px 10px;">Authoritative Hostname</td>
      <td style="padding:6px 10px;">Identifies authoritative name server for domain: <code>(abc.com, dns1.abc.com, NS)</code></td>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:6px 10px; font-weight:700; color:var(--warning-text);">Type CNAME</td>
      <td style="padding:6px 10px;">Alias Hostname</td>
      <td style="padding:6px 10px;">Canonical Hostname</td>
      <td style="padding:6px 10px;">Canonical name for an alias: <code>(shop.xyz.com, east7.backup.xyz.com, CNAME)</code></td>
    </tr>
    <tr>
      <td style="padding:6px 10px; font-weight:700; color:#8b5cf6;">Type MX</td>
      <td style="padding:6px 10px;">Domain Name</td>
      <td style="padding:6px 10px;">Mail Server Hostname</td>
      <td style="padding:6px 10px;">Specifies mail server for domain: <code>(abc.com, mail.abc.com, MX)</code></td>
    </tr>
  </tbody>
</table>

<div class="callout callout-def">
  <div class="callout-header">📘 DNS Caching & TTL</div>
  When a local DNS server resolves a query, it <strong>caches</strong> the mapping locally. If another query for the same host arrives, it answers immediately from cache without querying root or TLD servers! Each record carries a <strong>TTL (Time-To-Live)</strong> determining when it must be purged. If a host changes its IP address before TTL expires, cached mappings are temporarily out of date (DNS provides best-effort consistency).
</div>
""",
            "quiz": [
                {
                    "q": "What is the record Type of the DNS Resource Record (shop.xyz.com, east7.backup.xyz.com, ?)?",
                    "opts": [
                        "Type A",
                        "Type NS",
                        "Type CNAME",
                        "Type MX"
                    ],
                    "ans": 2,
                    "exp": "This record maps an alias hostname (shop.xyz.com) to a canonical hostname (east7.backup.xyz.com). This is a Type CNAME record (§2.5.3 / P14b)."
                },
                {
                    "q": "In iterated DNS query resolution for a non-cached domain, how many total DNS messages are exchanged between the host, local DNS, Root, TLD, and Authoritative servers?",
                    "opts": [
                        "2 messages",
                        "4 messages",
                        "8 messages",
                        "16 messages"
                    ],
                    "ans": 2,
                    "exp": "8 messages: (1) Host → Local, (2) Local → Root, (3) Root → Local referral, (4) Local → TLD, (5) TLD → Local referral, (6) Local → Authoritative, (7) Authoritative → Local answer, (8) Local → Host answer (§2.5.2 / P14a)."
                }
            ]
        },
        {
            "id": "ch2-6",
            "num": "2.6",
            "title": "Peer-to-Peer Applications & Video Streaming",
            "subtitle": "P2P file distribution time equations, BitTorrent, DASH, and CDN architectures",
            "content": r"""
<p>Peer-to-Peer (P2P) systems leverage user end systems to distribute data directly without requiring dedicated server infrastructure.</p>

<h3>2.6.1 File Distribution Time: Client-Server vs P2P</h3>
<p>Consider distributing a file of size <span class="math-inline">F</span> bits to <span class="math-inline">N</span> peers. Let <span class="math-inline">u_s</span> be the server upload rate, <span class="math-inline">d_{\min} = \min_i d_i</span> be the minimum peer download rate, and <span class="math-inline">u_i</span> be peer <span class="math-inline">i</span>'s upload rate:</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Minimum Distribution Time Formulas (§2.6.1)</div>
  <strong>Client-Server Architecture:</strong>
  <div class="math-display">
    D_{\text{CS}} \ge \max\left( \frac{N \cdot F}{u_s}, \ \frac{F}{d_{\min}} \right)
  </div>
  <em>As <span class="math-inline">N</span> increases, server upload capacity is fixed at <span class="math-inline">u_s</span>; distribution time grows linearly with <span class="math-inline">N</span>!</em>
  <br><br>
  <strong>Peer-to-Peer Architecture:</strong>
  <div class="math-display">
    D_{\text{P2P}} \ge \max\left( \frac{F}{u_s}, \ \frac{F}{d_{\min}}, \ \frac{N \cdot F}{u_s + \sum_{i=1}^N u_i} \right)
  </div>
  <em>P2P is <strong>self-scaling</strong>: each new peer brings its own upload capacity <span class="math-inline">u_i</span>. As <span class="math-inline">N \to \infty</span>, <span class="math-inline">D_{\text{P2P}}</span> approaches a constant bound!</em>
</div>

<!-- EMBEDDED INTERACTIVE: LIVE P2P VS CLIENT-SERVER CALCULATOR -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">⚡ Interactive P2P vs Client-Server Distribution Calculator</div>
    <span class="interactive-badge">Live Math Comparison</span>
  </div>
  <div class="grid-3">
    <div class="form-group">
      <label class="form-label">File Size F (Mbits):</label>
      <input type="number" id="sec2-p2p-f" class="form-input" value="1000" oninput="calcSec2P2P()">
    </div>
    <div class="form-group">
      <label class="form-label">Server Upload u_s (Mbps):</label>
      <input type="number" id="sec2-p2p-us" class="form-input" value="30" oninput="calcSec2P2P()">
    </div>
    <div class="form-group">
      <label class="form-label">Number of Peers N:</label>
      <input type="number" id="sec2-p2p-n" class="form-input" value="10" oninput="calcSec2P2P()">
    </div>
    <div class="form-group">
      <label class="form-label">Min Download d_min (Mbps):</label>
      <input type="number" id="sec2-p2p-dmin" class="form-input" value="2" oninput="calcSec2P2P()">
    </div>
    <div class="form-group">
      <label class="form-label">Peer Upload u_peer (Mbps):</label>
      <input type="number" id="sec2-p2p-upeer" class="form-input" value="1" oninput="calcSec2P2P()">
    </div>
  </div>
  <div id="sec2-p2p-result" class="calc-result-box" style="margin-top:1rem;">
    <!-- Computed live by calcSec2P2P() -->
  </div>
</div>

<h3>2.6.2 BitTorrent Architecture</h3>
<ul>
  <li><strong>Torrent:</strong> The collection of all peers participating in the distribution of a particular file.</li>
  <li><strong>Tracker:</strong> An infrastructure node that tracks active peers in the swarm and returns peer IP addresses to newcomers.</li>
  <li><strong>Chunks:</strong> The file is split into equal-size chunks (typically 256 KBytes).</li>
  <li><strong>Churn:</strong> Peers join and leave the torrent intermittently.</li>
  <li><strong>Rarest-First Strategy:</strong> A peer queries its neighbors to determine which chunk is least common among them, and requests that chunk first to equalize chunk distribution.</li>
  <li><strong>Tit-for-Tat Incentive (Unchoking):</strong> A peer measures download rates and sends chunks to the <strong>top 4 peers</strong> that provide data at the highest rate (evaluated every 10 seconds).</li>
  <li><strong>Optimistic Unchoking:</strong> Every 30 seconds, a peer randomly selects one additional peer to unchoke, giving newcomers a chance to earn a top-4 spot!</li>
</ul>

<h3>2.6.3 Video Streaming and DASH</h3>
<p>Video accounts for over 70% of Internet traffic. Video is a sequence of images displayed at a constant rate (e.g. 24 or 30 frames/sec).</p>
<ul>
  <li><strong>Continuous Playout Constraint:</strong> Once playout begins, frames must be displayed continuously according to original video timing. If network delay varies (<strong>jitter</strong>) and a frame arrives late, playout freezes (buffering stall!).</li>
  <li><strong>Client Playout Buffer & Delay:</strong> The client stores incoming video chunks in a local buffer for a few seconds before beginning playout. This buffer absorbs variations in packet delay.</li>
  <li><strong>DASH (Dynamic Adaptive Streaming over HTTP):</strong>
    <ul>
      <li>Video is encoded at multiple different bitrates (e.g. 240p, 720p, 1080p, 4K) and divided into multi-second chunks.</li>
      <li>The server provides a <strong>Manifest File</strong> (MPD) listing the URLs and bitrates for all chunks.</li>
      <li>The client measures available bandwidth and dynamically requests chunks at the highest possible quality without stalling.</li>
    </ul>
  </li>
</ul>

<h3>2.6.4 Content Distribution Networks (CDNs)</h3>
<p>Why can a single massive "mega-server" not stream video to millions of global users? (1) Single point of failure; (2) Network congestion around the server's access link; (3) Long propagation paths to distant users; (4) Redundant copies of the same video repeatedly cross the same transit links.</p>
<p>A <strong>Content Distribution Network (CDN)</strong> distributes server copies across geographically distributed nodes:</p>
<ol>
  <li><strong>Enter Deep (Akamai Philosophy):</strong> Deploy thousands of server clusters inside thousands of access ISPs around the world, getting as close to users as possible.</li>
  <li><strong>Bring Home (Limelight Philosophy):</strong> Build fewer, larger clusters located at Internet Exchange Points (IXPs) and private peering points.</li>
  <li><strong>DNS CNAME Redirection:</strong> When a user requests <code>video.netcinema.com</code>, NetCinema's authoritative DNS server returns a <code>CNAME</code> pointing to <code>kingcdn.com</code>, and KingCDN's name server directs the user to the nearest server cluster!</li>
</ol>
""",
            "quiz": [
                {
                    "q": "What is the purpose of a DASH manifest file?",
                    "opts": [
                        "It contains the cryptographic SSL private keys",
                        "It lists the URLs of video chunks available encoded at various bitrates, allowing the client to adapt quality dynamically",
                        "It acts as a BitTorrent tracker",
                        "It stores user cookie passwords"
                    ],
                    "ans": 1,
                    "exp": "The DASH manifest file provides URLs and bitrate specifications for all video segments, enabling the client player to request optimal quality chunks based on measured bandwidth (§2.6.3 / P16b)."
                },
                {
                    "q": "Why does a video streaming client buffer data before starting playback?",
                    "opts": [
                        "To prevent TCP SYN flood attacks",
                        "Because network delay varies (jitter); the playout buffer absorbs delay variations to satisfy the continuous playout constraint",
                        "To compress video from 4K to 240p",
                        "To calculate the 16-bit Internet checksum"
                    ],
                    "ans": 1,
                    "exp": "Video must be displayed at constant rate. The playout buffer absorbs packet delay variations (jitter) so playback does not stall (§2.6.3 / P16a)."
                }
            ]
        },
        {
            "id": "ch2-7",
            "num": "2.7",
            "title": "Socket Programming: Building Network Applications",
            "subtitle": "Building Python network clients and servers with UDP and TCP",
            "content": r"""
<p>We examine the standard Python socket API for creating networked applications. A network application consists of a pair of programs (a client program and a server program) residing on two different end systems.</p>

<h3>2.7.1 Socket Programming with UDP (Connectionless)</h3>
<p>In UDP, there is no initial handshake. The sender attaches the destination IP address and port number to every datagram:</p>

<div class="grid-2">
  <div>
    <div style="font-weight:700; color:var(--primary-text); margin-bottom:0.25rem;">UDPClient.py</div>
    <pre style="background:var(--bg-secondary); border:1px solid var(--border); padding:0.75rem; border-radius:6px; font-size:0.8rem; overflow-x:auto;">
<code>from socket import *
serverName = '192.168.1.50'
serverPort = 12000
# Create UDP socket (AF_INET = IPv4, SOCK_DGRAM = UDP)
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence: ')
# Send datagram with attached destination address
clientSocket.sendto(message.encode(), (serverName, serverPort))
# Read response datagram and server address
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()</code></pre>
  </div>
  <div>
    <div style="font-weight:700; color:var(--primary-text); margin-bottom:0.25rem;">UDPServer.py</div>
    <pre style="background:var(--bg-secondary); border:1px solid var(--border); padding:0.75rem; border-radius:6px; font-size:0.8rem; overflow-x:auto;">
<code>from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Bind socket to local port 12000
serverSocket.bind(('', serverPort))
print('UDP Server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)</code></pre>
  </div>
</div>

<h3>2.7.2 Socket Programming with TCP (Connection-Oriented)</h3>
<p>In TCP, client and server perform a 3-way handshake before transmitting data. The TCP server employs <strong>two distinct sockets</strong>:</p>
<ol>
  <li><strong>Welcoming Socket:</strong> Listens for incoming connection requests on a well-known port (e.g. 12000).</li>
  <li><strong>Connection Socket:</strong> Created anew by <code>serverSocket.accept()</code> specifically for that individual client connection!</li>
</ol>

<div class="grid-2" style="margin-top:1rem;">
  <div>
    <div style="font-weight:700; color:var(--primary-text); margin-bottom:0.25rem;">TCPClient.py</div>
    <pre style="background:var(--bg-secondary); border:1px solid var(--border); padding:0.75rem; border-radius:6px; font-size:0.8rem; overflow-x:auto;">
<code>from socket import *
serverName = '192.168.1.50'
serverPort = 12000
# Create TCP socket (SOCK_STREAM = TCP)
clientSocket = socket(AF_INET, SOCK_STREAM)
# Initiate 3-way handshake
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence: ')
# Send byte stream (no destination address needed!)
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode())
clientSocket.close()</code></pre>
  </div>
  <div>
    <div style="font-weight:700; color:var(--primary-text); margin-bottom:0.25rem;">TCPServer.py</div>
    <pre style="background:var(--bg-secondary); border:1px solid var(--border); padding:0.75rem; border-radius:6px; font-size:0.8rem; overflow-x:auto;">
<code>from socket import *
serverPort = 12000
# Create welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1) # Listen for connections
print('TCP Server is ready to receive')
while True:
    # Accept creates dedicated connection socket!
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()</code></pre>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In TCP socket programming, what is the role of the welcoming socket vs the connection socket?",
                    "opts": [
                        "The welcoming socket performs encryption while the connection socket sends plaintext",
                        "The welcoming socket remains listening on the known port for connection requests, while accept() spawns a dedicated connection socket for that specific client",
                        "The welcoming socket runs on the client and the connection socket runs on the server",
                        "The welcoming socket uses UDP and the connection socket uses TCP"
                    ],
                    "ans": 1,
                    "exp": "The welcoming socket listens for new incoming TCP handshakes. When accept() returns, it creates a new dedicated connection socket to handle that client's byte stream (§2.7.2)."
                }
            ]
        },
        {
            "id": "ch2-8",
            "num": "2.8",
            "title": "Chapter 2 Summary & Exam Practice Problems (P9–P16)",
            "subtitle": "Complete worked solutions to all 8 Midterm Study Guide Practice Problems plus Textbook Problems",
            "content": r"""
<p>Master these 8 practice problems from the official CPCS-371 Midterm Study Guide covering Chapter 2:</p>

<!-- PROBLEM P9 -->
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P9: Architectures and Processes</div>
    <span class="interactive-badge">Study Guide P9</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) Give two properties of the server in the client-server paradigm and two properties of peers in a P2P architecture.<br>
     (b) In a P2P file-sharing session, which process is the client and which is the server?<br>
     (c) Why is a host's IP address not enough to identify the receiving process?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p9-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p9-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) <strong>Server properties:</strong> Always on; fixed permanent IP address; typically housed in dedicated data centers.
      <br><strong>Peer properties:</strong> Arbitrary end systems communicate directly; no dedicated central server; self-scalable (peers provide service capacity as well as demand); intermittently connected with changing IP addresses.
    </div>
    <div class="calc-step">(b) The peer that initiates contact and downloads chunks is the <strong>client process</strong>; the peer that receives the request and uploads chunks is the <strong>server process</strong>.</div>
    <div class="calc-step">(c) A single host may run multiple network applications simultaneously (e.g. web server, email client, SSH session). The 32-bit IP address identifies only the physical host; the <strong>16-bit port number</strong> is required to identify the specific process/socket.</div>
  </div>
</div>

<!-- PROBLEM P10 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P10: Transport Service Needs Matching</div>
    <span class="interactive-badge">Study Guide P10</span>
  </div>
  <p><strong>Problem:</strong> For (i) file download, (ii) Internet telephony, (iii) e-mail, and (iv) an interactive online game, state whether the application tolerates data loss, whether it is time-sensitive, and which transport protocol it typically uses.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p10-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p10-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">&bull; <strong>(i) File Download:</strong> No loss tolerated; not time-sensitive; uses <strong>TCP</strong>.</div>
    <div class="calc-step">&bull; <strong>(ii) Internet Telephony (VoIP):</strong> Loss-tolerant; time-sensitive (10's–150 ms); uses <strong>UDP</strong> (or TCP).</div>
    <div class="calc-step">&bull; <strong>(iii) E-mail:</strong> No loss tolerated; not time-sensitive; uses <strong>TCP</strong>.</div>
    <div class="calc-step">&bull; <strong>(iv) Interactive Game:</strong> Loss-tolerant; time-sensitive (10's–100 ms); uses <strong>UDP</strong> (or TCP).</div>
  </div>
</div>

<!-- PROBLEM P11 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P11: Dissecting HTTP Request Headers</div>
    <span class="interactive-badge">Study Guide P11</span>
  </div>
  <p><strong>Problem:</strong> A web browser transmits the following request:</p>
  <pre style="background:var(--bg-secondary); padding:0.5rem; border-radius:4px; font-size:0.82rem;"><code>GET /cpcs371/notes/ch2.html HTTP/1.1
Host: www.example.edu
Connection: keep-alive</code></pre>
  <p>(a) What is the full URL of the requested object?<br>
     (b) What does <code>Connection: keep-alive</code> indicate?<br>
     (c) The server replies <code>HTTP/1.1 404 Not Found</code>. What does this mean?<br>
     (d) Which HTTP method sends form input in the entity body, and which method requests only headers?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p11-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p11-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) <strong>Full URL:</strong> <code>http://www.example.edu/cpcs371/notes/ch2.html</code> (Host name + Path name).</div>
    <div class="calc-step">(b) <strong><code>Connection: keep-alive</code>:</strong> The client requests a <strong>persistent HTTP connection</strong>; the server should keep the underlying TCP connection open for subsequent requests.</div>
    <div class="calc-step">(c) <strong><code>404 Not Found</code>:</strong> The server successfully received the request, but the requested document does not exist at the specified path on the server.</div>
    <div class="calc-step">(d) <strong><code>POST</code></strong> sends form input in the entity body; <strong><code>HEAD</code></strong> requests only the response header lines without the entity body.</div>
  </div>
</div>

<!-- PROBLEM P12 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P12: Non-Persistent Response Time & Cookies</div>
    <span class="interactive-badge">Study Guide P12</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) The RTT between client and server is 60 ms and transmitting an object takes 15 ms. With non-persistent HTTP, how long does it take to receive one object from the moment the client starts opening the connection?<br>
     (b) HTTP is stateless. Describe how the four cookie components let an online bookstore recognize a returning customer one week later.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p12-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p12-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a): With non-persistent HTTP:
      <div class="math-display">d_{\text{response}} = 2 \times \text{RTT} + d_{\text{trans}} = (2 \times 60\text{ ms}) + 15\text{ ms} = 120 + 15 = \mathbf{135\text{ ms}}</div>
      (1 RTT to open TCP connection + 1 RTT for HTTP request/response header + 15 ms transmission).
    </div>
    <div class="calc-step">Part (b):
      <ol>
        <li>On the first visit, the server creates a unique user identification number and creates a matching entry in its back-end database.</li>
        <li>The server includes the header <code>Set-Cookie: ID</code> in its HTTP response message.</li>
        <li>The client browser saves the cookie ID line in its local cookie file.</li>
        <li>One week later, every request from that browser to the site automatically includes the header <code>Cookie: ID</code>. The server looks up the ID in its database, retrieving the user's shopping cart and preferences!</li>
      </ol>
    </div>
  </div>
</div>

<!-- PROBLEM P13 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P13: Ordering SMTP Commands</div>
    <span class="interactive-badge">Study Guide P13</span>
  </div>
  <p><strong>Problem:</strong> Put the following SMTP items in correct sequential order and state which phase of the transfer each belongs to: <code>DATA</code>, <code>HELO</code>, <code>QUIT</code>, <code>RCPT TO:</code>, <code>MAIL FROM:</code>, a line containing only <code>.</code>.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p13-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p13-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step"><strong>1. <code>HELO</code></strong> &rarr; Handshaking Phase (client introduces its domain to server).</div>
    <div class="calc-step"><strong>2. <code>MAIL FROM:</code></strong> &rarr; Transfer Phase (identifies sender mailbox).</div>
    <div class="calc-step"><strong>3. <code>RCPT TO:</code></strong> &rarr; Transfer Phase (identifies recipient mailbox).</div>
    <div class="calc-step"><strong>4. <code>DATA</code></strong> &rarr; Transfer Phase (initiates message body text).</div>
    <div class="calc-step"><strong>5. <code>.</code> (single period line)</strong> &rarr; Transfer Phase (terminates message input).</div>
    <div class="calc-step"><strong>6. <code>QUIT</code></strong> &rarr; Closure Phase (terminates TCP connection).</div>
  </div>
</div>

<!-- PROBLEM P14 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P14: DNS Resolution & Resource Records</div>
    <span class="interactive-badge">Study Guide P14</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) A host at <code>engineering.nyu.edu</code> needs the IP of <code>gaia.cs.umass.edu</code>. With an iterated query and empty cache, list the 8 DNS messages exchanged.<br>
     (b) State the Resource Record Type for each:
     <br>&emsp;• <code>(dns1.abc.com, 10.1.2.3, ?)</code>
     <br>&emsp;• <code>(abc.com, dns1.abc.com, ?)</code>
     <br>&emsp;• <code>(shop.xyz.com, east7.backup.xyz.com, ?)</code>
     <br>&emsp;• <code>(abc.com, mail.abc.com, ?)</code><br>
     (c) Why can a cached mapping be out of date, and what limits how long it stays cached?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p14-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p14-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Part (a): 8 messages:
      <ol>
        <li>Host &rarr; Local DNS server (query <code>gaia.cs.umass.edu</code>)</li>
        <li>Local DNS &rarr; Root DNS server</li>
        <li>Root DNS &rarr; Local DNS (referral to <code>.edu</code> TLD server)</li>
        <li>Local DNS &rarr; <code>.edu</code> TLD server</li>
        <li>TLD server &rarr; Local DNS (referral to <code>umass.edu</code> authoritative server)</li>
        <li>Local DNS &rarr; <code>umass.edu</code> authoritative server</li>
        <li>Authoritative server &rarr; Local DNS (returns IP address of <code>gaia.cs.umass.edu</code>)</li>
        <li>Local DNS &rarr; Host (delivers IP address)</li>
      </ol>
    </div>
    <div class="calc-step">Part (b):
      <br>&bull; <code>(dns1.abc.com, 10.1.2.3, A)</code> &rarr; <strong>Type A</strong> (Hostname to IPv4).
      <br>&bull; <code>(abc.com, dns1.abc.com, NS)</code> &rarr; <strong>Type NS</strong> (Authoritative name server for domain).
      <br>&bull; <code>(shop.xyz.com, east7.backup.xyz.com, CNAME)</code> &rarr; <strong>Type CNAME</strong> (Canonical name for alias).
      <br>&bull; <code>(abc.com, mail.abc.com, MX)</code> &rarr; <strong>Type MX</strong> (Mail server for domain).
    </div>
    <div class="calc-step">Part (c): Name servers cache records to reduce latency. If a host changes its IP address, the cache does not know until the <strong>TTL (Time-To-Live)</strong> timer expires. DNS provides best-effort consistency.</div>
  </div>
</div>

<!-- PROBLEM P15 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P15: P2P and BitTorrent Mechanisms</div>
    <span class="interactive-badge">Study Guide P15</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) What does "self-scalability" mean in P2P?<br>
     (b) What is a torrent, and what is churn?<br>
     (c) How does tit-for-tat reward peers that upload?</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p15-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p15-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) <strong>Self-scalability:</strong> Each new peer that joins the system brings new service demand (downloading), but also contributes new service capacity (uploading). Therefore, total system capacity grows proportionally with the number of users.</div>
    <div class="calc-step">(b) A <strong>torrent</strong> is the group of all peers participating in the distribution of a particular file. <strong>Churn</strong> refers to the frequent, unpredictable joining and leaving of peers.</div>
    <div class="calc-step">(c) Under <strong>tit-for-tat</strong>, a peer unchokes (sends data to) the top 4 peers that provide data to it at the highest upload rate. Thus, peers that upload generously to others are rewarded by becoming top partners of others and receiving chunks at high rates in return.</div>
  </div>
</div>

<!-- PROBLEM P16 -->
<div class="interactive-card" style="margin-top:1.25rem;">
  <div class="interactive-header">
    <div class="interactive-title">📝 Practice Problem P16: Video Streaming, DASH, and CDNs</div>
    <span class="interactive-badge">Study Guide P16</span>
  </div>
  <p><strong>Problem:</strong></p>
  <p>(a) Why does a video client buffer data before starting playout?<br>
     (b) What does a DASH manifest file contain?<br>
     (c) Give three reasons why one huge "mega-server" cannot stream to millions of users.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch2-p16-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch2-p16-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">(a) Network packet delay varies dynamically (<strong>jitter</strong>), but video playback must adhere to the <strong>continuous playout constraint</strong>. A client-side buffer absorbs delay variations so the video does not freeze.</div>
    <div class="calc-step">(b) A DASH manifest file (MPD) contains the <strong>URLs of video chunks</strong>, each encoded at various bitrates and resolutions.</div>
    <div class="calc-step">(c) Any three of:
      <ol>
        <li><strong>Single point of failure:</strong> If the mega-server or its data center fails, the entire service goes down.</li>
        <li><strong>Network congestion bottleneck:</strong> The access links leading to the mega-server become severely congested.</li>
        <li><strong>Long propagation paths:</strong> Distant international users experience high latency and packet loss.</li>
        <li><strong>Wasted transit bandwidth:</strong> Redundant copies of the exact same video stream repeatedly cross the same transit links.</li>
      </ol>
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the primary difference between POP3 and IMAP mail access protocols?",
                    "opts": [
                        "POP3 uses UDP while IMAP uses TCP",
                        "IMAP maintains message folders and read/unread state on the server across multiple devices, whereas POP3 is a simple download protocol that does not maintain server state",
                        "POP3 encrypts messages while IMAP sends plaintext",
                        "IMAP is used to send mail while POP3 is used to receive mail"
                    ],
                    "ans": 1,
                    "exp": "IMAP keeps all user folders and message states on the mail server, allowing synchronized access across multiple devices (phones, laptops). POP3 downloads messages locally (§2.4.4)."
                }
            ]
        }
    ]
}
