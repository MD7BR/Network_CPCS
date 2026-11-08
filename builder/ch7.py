"""Chapter 7 Data: Multimedia Networking (Kurose & Ross 6th Ed.)
Comprehensive, textbook-grade expansion covering all subsections, inline SVGs, 
worked problems, and interactive simulators.
"""

CH7_DATA = {
    "id": "ch7",
    "num": 7,
    "title": "Multimedia Networking",
    "subtitle": "Streaming Video, DASH, CDNs, Voice-over-IP (VoIP), RTP/SIP, and QoS Token Bucket Scheduling",
    "layer": "Multimedia & QoS",
    "color": "#ec4899",
    "objectives": [
        "Contrast video/audio properties: spatial vs temporal compression, I/P/B frames, and CBR vs VBR",
        "Analyze digital audio sampling via Pulse Code Modulation (PCM) and calculate bitrates for speech vs CD audio",
        "Formulate client playout buffering dynamics (fill vs drain) and Dynamic Adaptive Streaming over HTTP (DASH)",
        "Differentiate CDN deployment strategies (Enter Deep vs Bring Home) and trace DNS-based cluster redirection",
        "Calculate Voice-over-IP (VoIP) adaptive playout delay to mitigate network jitter",
        "Apply packet loss recovery in real-time audio: XOR FEC, Piggybacked low-bitrate FEC, and Interleaving",
        "Dissect the Real-Time Transport Protocol (RTP) packet header and trace Session Initiation Protocol (SIP) signaling",
        "Evaluate link scheduling disciplines: FIFO, Priority Queuing, Round Robin, and Weighted Fair Queuing (WFQ)",
        "Formulate Token Bucket traffic policing (rate r, burst b) and calculate maximum permissible bursts (b + rt)"
    ],
    "sections": [
        {
            "id": "ch7-1",
            "num": "7.1",
            "title": "Multimedia Networking Applications",
            "subtitle": "Properties of video/audio, compression techniques, and application classes",
            "content": r"""
<p>Multimedia applications (streaming video, video conferencing, audio streaming) now account for over 70% of total Internet traffic. Unlike traditional text and web browsing applications (which demand 100% loss-free transmission but tolerate variable delays), multimedia applications exhibit unique transmission characteristics:</p>
<ul>
  <li><strong>High Bandwidth Demand:</strong> High-definition video streams require hundreds of kilobits to multiple megabits per second.</li>
  <li><strong>Delay Sensitivity:</strong> Interactive speech cannot tolerate round-trip delays exceeding <strong>150–200 ms</strong> without human conversation breaking down.</li>
  <li><strong>Loss Tolerance:</strong> Occasional packet loss (1% to 5%) can be concealed by decompression algorithms or human perceptual limits, meaning strict retransmission is often unnecessary or even harmful.</li>
</ul>

<h3>7.1.1 Digital Audio Characteristics and PCM Sampling</h3>
<p>An analog audio signal is a continuous pressure wave. To transmit audio over digital networks, it must be digitized using <strong>Pulse Code Modulation (PCM)</strong>:</p>
<ol>
  <li><strong>Sampling:</strong> The continuous analog wave is sampled at regular discrete time intervals. According to the Nyquist theorem, to capture frequencies up to <span class="math-inline">B\text{ Hz}</span>, the sampling rate must be at least <span class="math-inline">2B\text{ samples/second}</span>.</li>
  <li><strong>Quantization:</strong> The amplitude of each sample is rounded to the nearest discrete quantization level, encoded as an <span class="math-inline">n</span>-bit integer (<span class="math-inline">2^n</span> quantization levels).</li>
</ol>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Audio Bitrate Calculations (§7.1.1)</div>
  <ul>
    <li><strong>Standard Telephone Speech (PCM):</strong> Sampled at 8,000 samples/sec with 8 bits per sample (256 discrete amplitude levels).
      <div class="math-display">
        \text{Bitrate} = 8,000\text{ samples/s} \times 8\text{ bits/sample} = \mathbf{64\text{ kbps}}
      </div>
    </li>
    <li><strong>Compact Disc (CD) Music Audio:</strong> Sampled at 44,100 samples/sec with 16 bits per sample, in stereo (2 channels).
      <div class="math-display">
        \text{Bitrate} = 44,100 \times 16 \times 2 = \mathbf{1.411\text{ Mbps}}
      </div>
    </li>
    <li><strong>Compressed Audio (MP3 / AAC):</strong> Advanced psychoacoustic compression eliminates frequencies inaudible to human ears, compressing CD-quality audio down to <strong>128 kbps</strong> or <strong>256 kbps</strong> (a ~10:1 compression ratio!).</li>
  </ul>
</div>

<h3>7.1.2 Digital Video Characteristics and Compression</h3>
<p>A digital video is a sequence of discrete images (frames) displayed at 24 to 60 frames per second. An uncompressed high-definition video frame (<span class="math-inline">1920 \times 1080</span> pixels, 24 bits per pixel at 30 fps) requires a staggering <span class="math-inline">1920 \times 1080 \times 24 \times 30 \approx \mathbf{1.5\text{ Gbps}}</span>! Transmission across standard consumer broadband is impossible without video compression.</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Spatial vs. Temporal Video Compression (MPEG / H.264 / H.265)</div>
  Video compression exploits two distinct forms of redundancy:
  <ul>
    <li><strong>Spatial Redundancy (Intra-Frame):</strong> Redundancy within a single static image frame. For example, a picture of a clear blue sky contains thousands of adjacent pixels with almost identical color values. Instead of transmitting each pixel individually, the encoder transmits a compact mathematical description of the uniform region.</li>
    <li><strong>Temporal Redundancy (Inter-Frame):</strong> Redundancy across consecutive frames in time. In a scene where a person talks while sitting in a room, the background walls and furniture do not move from frame to frame. Instead of retransmitting the entire image, the encoder transmits only the <em>motion vectors and difference values</em> between frames!</li>
  </ul>
</div>

<h4>Frame Types in MPEG / H.264:</h4>
<ul>
  <li><strong>I-Frames (Intra-coded):</strong> Completely self-contained images encoded with spatial compression only. No other frames are needed to decode an I-frame. I-frames serve as anchor points for random seeking and recovery from errors.</li>
  <li><strong>P-Frames (Predictive):</strong> Encoded using motion prediction relative to the preceding I-frame or P-frame. Contains only the changes and motion vectors (much smaller than I-frames).</li>
  <li><strong>B-Frames (Bi-directional Predictive):</strong> Encoded using prediction from both the preceding <em>and following</em> reference frames, achieving the highest compression ratio.</li>
</ul>

<h3>7.1.3 The Three Classes of Multimedia Applications</h3>
<table class="data-table" style="margin:1rem 0;">
  <thead>
    <tr>
      <th>Application Class</th>
      <th>Key Examples</th>
      <th>Delay Tolerance</th>
      <th>Buffering & Seeking</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:700; color:var(--primary);">Streaming Stored Video</td>
      <td>YouTube, Netflix, Hulu</td>
      <td>Tolerant: 2 to 5 seconds initial startup delay is acceptable.</td>
      <td>Extensive client buffering (10–60 seconds). Allows pause, rewind, fast-forward seeking.</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:var(--accent-text);">Conversational Voice & Video</td>
      <td>Skype, Zoom, FaceTime, WebRTC</td>
      <td>Strictly intolerant: &le; 150–200 ms end-to-end delay; &gt; 400 ms is catastrophic.</td>
      <td>Minimal buffering (tens of milliseconds). Interactive; no pausing or seeking.</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:#8b5cf6;">Streaming Live Audio & Video</td>
      <td>Twitch, Live sports broadcasts</td>
      <td>Intermediate: 10 to 30 seconds delay acceptable.</td>
      <td>Client buffering to smooth jitter, but forward seeking is impossible.</td>
    </tr>
  </tbody>
</table>
""",
            "quiz": [
                {
                    "q": "What is the bitrate of standard uncompressed digital telephone voice sampled via PCM at 8,000 samples/second with 8 bits per sample?",
                    "opts": [
                        "8 kbps",
                        "64 kbps",
                        "128 kbps",
                        "1.411 Mbps"
                    ],
                    "ans": 1,
                    "exp": "8,000 samples/sec * 8 bits/sample = 64,000 bps = 64 kbps (§7.1.1)."
                },
                {
                    "q": "What type of video compression eliminates redundancy by transmitting only the motion vectors and pixel differences between consecutive frames over time?",
                    "opts": [
                        "Spatial redundancy compression",
                        "Temporal redundancy compression (inter-frame)",
                        "Pulse code modulation",
                        "Parity bit interleaving"
                    ],
                    "ans": 1,
                    "exp": "Temporal redundancy exploits the fact that successive video frames contain mostly identical background content, sending only differences between frames (§7.1.2)."
                }
            ]
        },
        {
            "id": "ch7-2",
            "num": "7.2",
            "title": "Streaming Stored Video",
            "subtitle": "HTTP streaming, client playout buffers, DASH, and Content Distribution Networks (CDNs)",
            "content": r"""
<p>Early video streaming architectures used proprietary UDP-based streaming servers (e.g. RealNetworks RTSP). Today, virtually all commercial video streaming operates over <strong>standard HTTP/TCP</strong>. HTTP streaming traverses enterprise firewalls and NATs effortlessly without requiring specialized server software.</p>

<h3>7.2.1 Client Playout Buffering Dynamics</h3>
<p>Over a packet-switched Internet, the rate at which video bytes are delivered to the client fluctuates unpredictably due to changing network congestion and TCP congestion control window adjustments. To deliver smooth, uninterrupted video playback, the client media player implements a <strong>playout buffer</strong>:</p>

<!-- INLINE SVG: Figure 7.1 Playout Buffer Dynamics -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 260" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Server Box -->
      <rect x="30" y="40" width="120" height="60" rx="8" fill="#8b5cf6"/>
      <text x="90" y="68" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">Video Server</text>
      <text x="90" y="85" font-size="9" fill="#ede9fe" text-anchor="middle">Stored Video File</text>

      <!-- Network Pipe -->
      <rect x="180" y="55" width="200" height="30" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="280" y="74" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">Variable Rate r_in(t)</text>
      <line x1="150" y1="70" x2="180" y2="70" stroke="#8b5cf6" stroke-width="3"/>
      <line x1="380" y1="70" x2="420" y2="70" stroke="#0284c7" stroke-width="3"/>

      <!-- Client Playout Buffer Box -->
      <rect x="420" y="30" width="200" height="180" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="2"/>
      <text x="520" y="52" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Client Playout Buffer</text>

      <!-- Buffer Liquid Level -->
      <rect x="440" y="90" width="160" height="100" rx="4" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="440" y="130" width="160" height="60" rx="4" fill="#38bdf8" fill-opacity="0.6"/>
      <text x="520" y="165" font-size="11" font-weight="800" fill="#0369a1" text-anchor="middle">Buffered Video</text>
      <text x="520" y="112" font-size="9" fill="#0284c7" text-anchor="middle">Fill Rate r_in &gt; Drain Rate r_out</text>

      <!-- Drain Arrow to Display -->
      <line x1="620" y1="160" x2="680" y2="160" stroke="#10b981" stroke-width="3"/>
      <text x="650" y="152" font-size="9" font-weight="600" fill="#059669">r_out (Fixed)</text>

      <!-- Video Display Screen -->
      <rect x="680" y="115" width="130" height="90" rx="6" fill="#1e293b"/>
      <text x="745" y="155" font-size="18" fill="#fff" text-anchor="middle">▶ 📺</text>
      <text x="745" y="180" font-size="10" font-weight="700" fill="#38bdf8" text-anchor="middle">Smooth Playback</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 7.1 — Client Playout Buffer Dynamics: Video arrives at fluctuating network rate r_in(t) and is drained at constant playback rate r_out (§7.2.1).</div>
</div>

<div class="callout callout-insight">
  <div class="callout-header">💡 Playout Buffer States: Freezing vs. Startup Delay</div>
  <ul>
    <li><strong>Initial Startup Delay:</strong> The client delays playback by a few seconds (<span class="math-inline">t_{\text{play}} - t_0</span>) until a predefined threshold of video data has accumulated in the buffer.</li>
    <li><strong>Buffer Starvation (Freeze / Rebuffering):</strong> If network throughput drops below the video consumption rate (<span class="math-inline">r_{\text{in}} < r_{\text{out}}</span>) for an extended duration, the buffer drains to empty. Video playback freezes, producing a frustrating rebuffering spinner!</li>
  </ul>
</div>

<h3>7.2.2 Dynamic Adaptive Streaming over HTTP (DASH)</h3>
<p>In standard HTTP streaming, all clients receive the exact same video file regardless of whether they are on a high-speed fiber connection or a congested 3G mobile link. To overcome this limitation, the industry developed <strong>DASH (Dynamic Adaptive Streaming over HTTP)</strong>:</p>

<ol>
  <li><strong>Multi-Bitrate Encoding:</strong> The content provider encodes the video into several different quality levels (e.g. 240p at 300 kbps, 480p at 1 Mbps, 720p at 2.5 Mbps, 1080p at 5 Mbps, and 4K at 15 Mbps).</li>
  <li><strong>Chunk Partitioning:</strong> Each version of the video is sliced into small chunks of equal playback duration (typically 2 to 10 seconds).</li>
  <li><strong>Media Presentation Description (MPD / Manifest):</strong> The server creates an XML manifest file listing the URL and bitrates of every chunk.</li>
  <li><strong>Client-Driven Rate Adaptation:</strong> The intelligence resides entirely in the <strong>client player</strong>:
    <br>&bull; The client downloads the MPD manifest file.
    <br>&bull; For each chunk, the client measures its recent download throughput and checks its current buffer level.
    <br>&bull; If bandwidth is ample and the buffer is full, the client requests the next chunk at a higher bitrate (e.g. 1080p).
    <br>&bull; If bandwidth plummets and the buffer is depleting, the client smoothly drops down to a lower bitrate chunk (e.g. 480p) to avoid stalling!
  </li>
</ol>

<!-- EMBEDDED INTERACTIVE: DASH BITRATE ADAPTATION SIMULATOR -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">📺 Interactive DASH Bitrate Adaptation & Playout Buffer</div>
    <span class="interactive-badge">Dynamic Adaptation</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Simulate bandwidth changes to observe how DASH automatically adapts video chunk quality and maintains buffer health:
  </p>
  <div class="fig-controls" style="margin-bottom:1rem;">
    <button class="btn-secondary" onclick="setSec7BW(1000)">Drop to 1 Mbps (Mobile 3G)</button>
    <button class="btn-secondary" onclick="setSec7BW(2500)">Set to 2.5 Mbps (DSL)</button>
    <button class="btn-secondary" onclick="setSec7BW(5000)">Set to 5 Mbps (Cable)</button>
    <button class="btn-primary" onclick="setSec7BW(15000)">Boost to 15 Mbps (Fiber)</button>
  </div>
  <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1.25rem;">
    <div style="font-size:0.85rem; font-weight:700; margin-bottom:0.35rem;">Client Playout Buffer Level:</div>
    <div style="width:100%; height:22px; background:var(--bg-secondary); border-radius:11px; overflow:hidden; border:1px solid var(--border); margin-bottom:0.75rem;">
      <div id="sec7-dash-buffer-fill" style="width:60%; height:100%; background:#3b82f6; transition:width 0.4s ease, background 0.4s ease;"></div>
    </div>
    <div class="calc-grid">
      <div class="calc-field">
        <label class="calc-label">Available Bandwidth</label>
        <div id="sec7-dash-bw" style="font-weight:700; color:var(--text-primary); font-size:1.1rem;">2,500 kbps</div>
      </div>
      <div class="calc-field">
        <label class="calc-label">Selected DASH Video Resolution</label>
        <div id="sec7-dash-res" style="font-weight:700; color:var(--primary); font-size:1.1rem;">720p HD</div>
      </div>
      <div class="calc-field">
        <label class="calc-label">Buffered Media Duration</label>
        <div id="sec7-dash-buffer" style="font-weight:700; color:var(--accent-text); font-size:1.1rem;">18.0s (60% buffer capacity)</div>
      </div>
    </div>
  </div>
</div>

<h3>7.2.3 Content Distribution Networks (CDNs)</h3>
<p>Serving millions of concurrent video streams from a single central mega-datacenter is fundamentally flawed: packets traverse dozens of transit ISPs (causing high delay and packet loss), the server link becomes a massive bottleneck, and the datacenter represents a single point of failure. To solve this, providers deploy <strong>Content Distribution Networks (CDNs)</strong>.</p>

<h4>CDN Server Placement Philosophies:</h4>
<ul>
  <li><strong>Enter Deep (Akamai approach):</strong> Deploy clusters of CDN servers inside access ISPs all over the world, placing servers in thousands of ISP networks close to end users. Minimizes latency and hop count, but increases maintenance complexity.</li>
  <li><strong>Bring Home (Limelight approach):</strong> Build larger server clusters in a smaller number (tens) of critical Internet Exchange Points (IXPs) and interconnect them with high-speed private fiber. Lower maintenance costs, but slightly higher latency to users.</li>
</ul>

<h4>DNS-Based Cluster Redirection in CDNs:</h4>
<p>When a user types <code>video.netflix.com</code>, how is the request steered to the optimal local CDN server?</p>

<!-- INLINE SVG: Figure 7.2 CDN DNS Redirection Flow -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 260" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Client Host -->
      <rect x="40" y="40" width="100" height="45" rx="6" fill="#3b82f6"/>
      <text x="90" y="64" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Client Host</text>
      <text x="90" y="77" font-size="8" fill="#dbeafe" text-anchor="middle">Jeddah</text>

      <!-- Local DNS Server -->
      <rect x="220" y="40" width="110" height="45" rx="6" fill="#0284c7"/>
      <text x="275" y="64" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Local DNS (LDNS)</text>
      <text x="275" y="77" font-size="8" fill="#e0f2fe" text-anchor="middle">ISP Server</text>

      <!-- Origin Authoritative DNS -->
      <rect x="420" y="40" width="130" height="45" rx="6" fill="#8b5cf6"/>
      <text x="485" y="64" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">Origin Auth DNS</text>
      <text x="485" y="77" font-size="8" fill="#ede9fe" text-anchor="middle">netflix.com</text>

      <!-- CDN Authoritative DNS -->
      <rect x="640" y="40" width="130" height="45" rx="6" fill="#10b981"/>
      <text x="705" y="64" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">CDN Auth DNS</text>
      <text x="705" y="77" font-size="8" fill="#d1fae5" text-anchor="middle">akamai.com</text>

      <!-- Closest CDN Video Cache Server -->
      <rect x="420" y="170" width="150" height="60" rx="8" fill="#059669"/>
      <text x="495" y="198" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">Closest CDN Server</text>
      <text x="495" y="215" font-size="9" fill="#a7f3d0" text-anchor="middle">Local Riyadh/Jeddah Node</text>

      <!-- Arrow 1: Client to LDNS -->
      <line x1="140" y1="55" x2="220" y2="55" stroke="#3b82f6" stroke-width="2.5"/>
      <text x="180" y="47" font-size="8" font-weight="700" fill="#1d4ed8" text-anchor="middle">1. Query video.com</text>

      <!-- Arrow 2: LDNS to Origin DNS -->
      <line x1="330" y1="55" x2="420" y2="55" stroke="#0284c7" stroke-width="2.5"/>
      <text x="375" y="47" font-size="8" font-weight="700" fill="#0369a1" text-anchor="middle">2. Query</text>

      <!-- Arrow 3: Origin returns CNAME -->
      <line x1="420" y1="70" x2="330" y2="70" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="4 3"/>
      <text x="375" y="83" font-size="8" fill="#6d28d9" text-anchor="middle">3. CNAME cdn.com</text>

      <!-- Arrow 4: LDNS to CDN DNS -->
      <path d="M 275 85 Q 480 130 685 85" stroke="#10b981" stroke-width="2.5" fill="none"/>
      <text x="480" y="125" font-size="8" font-weight="700" fill="#047857" text-anchor="middle">4. Query CNAME to CDN DNS</text>

      <!-- Arrow 5: CDN DNS returns Best IP -->
      <path d="M 660 85 Q 480 100 310 85" stroke="#10b981" stroke-width="2" fill="none" stroke-dasharray="4 3"/>
      <text x="480" y="103" font-size="8" fill="#047857" text-anchor="middle">5. Returns closest CDN IP</text>

      <!-- Arrow 6: Client streams directly from CDN Server -->
      <path d="M 90 85 Q 90 200 420 200" stroke="#f59e0b" stroke-width="3.5" fill="none"/>
      <text x="250" y="190" font-size="10" font-weight="800" fill="#b45309" text-anchor="middle">6. Direct HTTP GET & Streaming Video Payload</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 7.2 — CDN DNS Redirection 6-Step Resolution Dance Steering Client to the Optimal Local Edge Server (§7.2.3).</div>
</div>
""",
            "quiz": [
                {
                    "q": "What mechanism enables a Content Distribution Network (CDN) to intercept a user request and transparently route it to the nearest edge server?",
                    "opts": [
                        "BGP route poisoning",
                        "DNS CNAME (canonical name) referral to the CDN's authoritative DNS server, which inspects the client's Local DNS IP to select the closest cluster",
                        "TCP SYN flood attacks",
                        "IP multicast tunneling"
                    ],
                    "ans": 1,
                    "exp": "The origin server returns a CNAME pointing to the CDN. The CDN authoritative DNS inspects the requesting client's Local DNS IP to return the IP address of the closest edge cluster (§7.2.3)."
                },
                {
                    "q": "What is the primary difference between the 'Enter Deep' and 'Bring Home' CDN server placement philosophies?",
                    "opts": [
                        "Enter Deep places servers inside access ISPs close to users; Bring Home places larger clusters at a smaller number of Internet Exchange Points (IXPs)",
                        "Enter Deep uses optical cables, while Bring Home uses copper",
                        "Enter Deep only works for audio, while Bring Home is for video",
                        "There is no difference"
                    ],
                    "ans": 0,
                    "exp": "Enter Deep (Akamai) deploys thousands of small clusters directly inside access networks; Bring Home builds fewer, larger clusters at major IXPs (§7.2.3)."
                }
            ]
        },
        {
            "id": "ch7-3",
            "num": "7.3",
            "title": "Voice-over-IP (VoIP)",
            "subtitle": "Jitter removal via adaptive playout delay, and packet loss recovery (FEC & Interleaving)",
            "content": r"""
<p>Conversational Voice-over-IP (VoIP) operates under strict real-time constraints: human conversation degrades noticeably if one-way end-to-end delay exceeds <strong>150 ms</strong>, and becomes completely unusable if delay exceeds <strong>400 ms</strong>.</p>

<h3>7.3.1 Eliminating Jitter: Adaptive Playout Delay</h3>
<p>Because IP packets travel across shared routers with variable queuing, the inter-arrival times between consecutive packets vary widely (known as <strong>packet jitter</strong>). If a receiver plays packets the instant they arrive, the speech sounds choppy and distorted.</p>
<p>The receiver smooths jitter by holding received packets in a playout buffer before converting them to audio. In <strong>Adaptive Playout Delay</strong>, the playout delay is dynamically adjusted at the beginning of each speech <strong>talkspurt</strong> (periods of speech separated by silent pauses):</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Adaptive Playout Delay Equations (§7.3.2)</div>
  <p>Let <span class="math-inline">t_i</span> be the sender timestamp of packet <span class="math-inline">i</span>, and <span class="math-inline">r_i</span> be the arrival time at the receiver. The individual packet delay is <span class="math-inline">r_i - t_i</span>.</p>
  <p>The receiver calculates an Exponentially Weighted Moving Average (EWMA) of delay <span class="math-inline">d_i</span> and delay variation <span class="math-inline">v_i</span>:</p>
  <div class="math-display">
    d_i = (1 - \alpha) d_{i-1} + \alpha (r_i - t_i) \quad (\text{typically } \alpha = 0.1)
  </div>
  <div class="math-display">
    v_i = (1 - \beta) v_{i-1} + \beta |r_i - t_i - d_i| \quad (\text{typically } \beta = 0.1)
  </div>
  <p>For the first packet of a new talkspurt, the playout time <span class="math-inline">p_i</span> is set to:</p>
  <div class="math-display">
    p_i = t_i + d_i + K \cdot v_i
  </div>
  <p>where <span class="math-inline">K</span> is a safety factor (typically <span class="math-inline">K = 4</span>). All subsequent packets in the same talkspurt are played out at intervals matching their original sender timestamps!</p>
</div>

<h3>7.3.2 Packet Loss Recovery in VoIP: FEC vs. Interleaving</h3>
<p>Because VoIP runs over UDP without retransmissions (a retransmitted packet would arrive far too late for real-time conversation), loss must be repaired using proactive loss recovery:</p>

<div class="summary-grid" style="margin:1rem 0;">
  <div class="summary-card" style="border-top:3px solid #3b82f6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">1. Piggybacked Low-Bitrate FEC</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      The sender transmits the current audio chunk at primary high quality (e.g. 64 kbps G.711) and piggybacks a redundant lower-quality copy of the <em>previous</em> chunk (e.g. 13 kbps GSM) onto the packet. If packet <span class="math-inline">n</span> is lost, the receiver reconstructs chunk <span class="math-inline">n</span> from packet <span class="math-inline">n+1</span>!
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #10b981;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">2. Parity / XOR FEC</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      For every group of <span class="math-inline">n</span> chunks, the sender computes an exclusive-OR (XOR) parity chunk and transmits it as an extra packet. The receiver can reconstruct <em>any single lost packet</em> in the group by XORing the remaining <span class="math-inline">n-1</span> packets with the parity packet.
    </p>
  </div>
  <div class="summary-card" style="border-top:3px solid #8b5cf6;">
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">3. Interleaving</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
      The sender breaks audio chunks into small 5 ms units and disperses them across multiple transmitted packets. If a packet is lost, it creates small, imperceptible sub-millisecond gaps across multiple chunks rather than an entire missing word! <strong>Key advantage: adds ZERO transmission bandwidth overhead!</strong>
    </p>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the primary advantage of Interleaving over Forward Error Correction (FEC) for voice loss recovery?",
                    "opts": [
                        "Interleaving does not increase transmission bit rate or bandwidth consumption",
                        "Interleaving adds zero latency",
                        "Interleaving guarantees 100% loss recovery",
                        "Interleaving eliminates the need for UDP checksums"
                    ],
                    "ans": 0,
                    "exp": "Unlike FEC which transmits redundant bits, interleaving reorders samples across packets with zero bandwidth overhead (at the cost of small playout latency) (§7.3.3)."
                },
                {
                    "q": "Why does adaptive playout delay adjust the playout delay ONLY at the beginning of a talkspurt rather than in the middle of active speech?",
                    "opts": [
                        "Because adjusting delay during active speech would unpleasantly compress or expand the audio, creating noticeable pitch and voice distortion",
                        "Because routers drop packets during pauses",
                        "Because UDP sockets only open during speech",
                        "To force the client to renegotiate SIP credentials"
                    ],
                    "ans": 0,
                    "exp": "Changing playout delays during continuous speech would compress or elongate phonemes, causing jarring voice distortion. Adjusting during silent gaps is imperceptible to listeners (§7.3.2)."
                }
            ]
        },
        {
            "id": "ch7-4",
            "num": "7.4",
            "title": "Protocols for Real-Time Conversational Applications",
            "subtitle": "RTP packet format, RTCP quality feedback, and SIP call setup signaling",
            "content": r"""
<p>Conversational multimedia requires two distinct protocols operating in parallel: a <strong>transport protocol</strong> for streaming media payloads (RTP) and a <strong>signaling protocol</strong> for establishing and tearing down calls (SIP).</p>

<h3>7.4.1 Real-Time Transport Protocol (RTP, RFC 3550)</h3>
<p>RTP runs over UDP (typically on an even port number). It standardizes packet header fields needed by real-time multimedia:</p>

<!-- INLINE SVG: Figure 7.3 Bit-Accurate RTP Header -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 180" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Row 1: Bits 0 to 31 -->
      <rect x="20" y="30" width="70" height="45" fill="#f8fafc" stroke="#475569" stroke-width="1.5" rx="3"/>
      <text x="55" y="52" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">V=2 | P | X</text>
      <text x="55" y="66" font-size="8" fill="#64748b" text-anchor="middle">CC (4b)</text>

      <rect x="90" y="30" width="50" height="45" fill="#f8fafc" stroke="#475569" stroke-width="1.5" rx="3"/>
      <text x="115" y="52" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">M (1b)</text>
      <text x="115" y="66" font-size="8" fill="#64748b" text-anchor="middle">Marker</text>

      <rect x="140" y="30" width="130" height="45" fill="#eff6ff" stroke="#3b82f6" stroke-width="2" rx="3"/>
      <text x="205" y="52" font-size="11" font-weight="800" fill="#1d4ed8" text-anchor="middle">Payload Type (7 bits)</text>
      <text x="205" y="66" font-size="8" fill="#2563eb" text-anchor="middle">Audio/Video Encoding ID</text>

      <rect x="270" y="30" width="220" height="45" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="3"/>
      <text x="380" y="52" font-size="11" font-weight="800" fill="#047857" text-anchor="middle">Sequence Number (16 bits)</text>
      <text x="380" y="66" font-size="8" fill="#059669" text-anchor="middle">Packet Loss Detection & In-Order Reordering</text>

      <!-- Row 2: Timestamp (32 bits) -->
      <rect x="20" y="80" width="470" height="40" fill="#fdf4ff" stroke="#c084fc" stroke-width="2" rx="3"/>
      <text x="255" y="100" font-size="11" font-weight="800" fill="#7e22ce" text-anchor="middle">Timestamp (32 bits)</text>
      <text x="255" y="113" font-size="8" fill="#9333ea" text-anchor="middle">Sampling Instant of First Audio Sample in Packet (Jitter Removal)</text>

      <!-- Row 3: SSRC (32 bits) -->
      <rect x="20" y="125" width="470" height="40" fill="#fff7ed" stroke="#f97316" stroke-width="2" rx="3"/>
      <text x="255" y="145" font-size="11" font-weight="800" fill="#c2410c" text-anchor="middle">Synchronization Source Identifier — SSRC (32 bits)</text>
      <text x="255" y="158" font-size="8" fill="#ea580c" text-anchor="middle">Unique ID of the Transmitting Source Stream</text>

      <!-- Payload Data Block -->
      <rect x="510" y="30" width="310" height="135" rx="8" fill="#f1f5f9" stroke="#334155" stroke-width="1.5"/>
      <text x="665" y="90" font-size="14" font-weight="800" fill="#0f172a" text-anchor="middle">Audio / Video Payload</text>
      <text x="665" y="110" font-size="10" fill="#475569" text-anchor="middle">e.g. 160 Bytes of PCM Audio (20 ms at 64 kbps)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 7.3 — Complete Bit-Accurate Real-Time Transport Protocol (RTP) Header Format (§7.4.1).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 Key Fields in the RTP Header</div>
  <ul>
    <li><strong>Payload Type (7 bits):</strong> Identifies the media compression codec (e.g. Type 0 = PCM &mu;-law 64 kbps; Type 26 = Motion JPEG; Type 33 = MPEG2 video). Allows receiver to dynamically change decoders.</li>
    <li><strong>Sequence Number (16 bits):</strong> Increments by 1 for each RTP packet sent. Used by receiver to detect dropped packets and restore original packet order.</li>
    <li><strong>Timestamp (32 bits):</strong> Reflects the sampling instant of the first audio sample in the packet. Allows the receiver to eliminate jitter and synchronize audio playout with video.</li>
    <li><strong>SSRC (32 bits):</strong> A randomly assigned identifier that distinguishes different streams in a multimedia conference.</li>
  </ul>
</div>

<h3>7.4.2 Session Initiation Protocol (SIP, RFC 3261)</h3>
<p>While RTP carries media data, <strong>SIP</strong> is the application-layer signaling protocol that establishes, modifies, and terminates calls. Key properties:</p>
<ul>
  <li>Text-based protocol heavily inspired by HTTP and SMTP (uses human-readable methods like <code>INVITE</code>, <code>ACK</code>, <code>BYE</code>, and response codes like <code>200 OK</code>).</li>
  <li>Uses <strong>SIP URIs</strong> resembling email addresses: <code>sip:bob@domain.com</code>.</li>
  <li>Negotiates media codecs and port numbers using embedded <strong>SDP (Session Description Protocol)</strong>.</li>
  <li><strong>SIP Registrars & Proxies:</strong> When Bob connects his SIP phone, it sends a <code>REGISTER</code> message to his home registrar. When Alice calls Bob, her local SIP proxy routes the <code>INVITE</code> to Bob's current IP address!</li>
</ul>

<!-- INLINE SVG: Figure 7.4 SIP Call Flow -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 840 240" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px;">
      <!-- Alice Timeline -->
      <line x1="150" y1="30" x2="150" y2="220" stroke="#3b82f6" stroke-width="2"/>
      <text x="150" y="20" font-size="11" font-weight="700" fill="#3b82f6" text-anchor="middle">Alice (Caller)</text>

      <!-- Bob Timeline -->
      <line x1="690" y1="30" x2="690" y2="220" stroke="#10b981" stroke-width="2"/>
      <text x="690" y="20" font-size="11" font-weight="700" fill="#10b981" text-anchor="middle">Bob (Callee)</text>

      <!-- 1. INVITE -->
      <line x1="150" y1="50" x2="690" y2="70" stroke="#3b82f6" stroke-width="2.5"/>
      <text x="420" y="52" font-size="9" font-weight="700" fill="#1d4ed8" text-anchor="middle">1. INVITE (Port 5060, SDP: audio port 51234, PCM)</text>

      <!-- 2. 180 Ringing -->
      <line x1="690" y1="85" x2="150" y2="105" stroke="#10b981" stroke-width="2" stroke-dasharray="4 3"/>
      <text x="420" y="88" font-size="9" fill="#047857" text-anchor="middle">2. 180 Ringing (Bob's phone is ringing)</text>

      <!-- 3. 200 OK -->
      <line x1="690" y1="120" x2="150" y2="140" stroke="#10b981" stroke-width="2.5"/>
      <text x="420" y="123" font-size="9" font-weight="700" fill="#047857" text-anchor="middle">3. 200 OK (Bob picked up! SDP: audio port 61234)</text>

      <!-- 4. ACK -->
      <line x1="150" y1="150" x2="690" y2="170" stroke="#3b82f6" stroke-width="2.5"/>
      <text x="420" y="153" font-size="9" font-weight="700" fill="#1d4ed8" text-anchor="middle">4. ACK (Signaling Complete)</text>

      <!-- Bidirectional RTP Media Flow -->
      <rect x="250" y="180" width="340" height="24" rx="4" fill="#fdf4ff" stroke="#c084fc" stroke-width="1.5"/>
      <text x="420" y="196" font-size="10" font-weight="800" fill="#7e22ce" text-anchor="middle">&harr; Bidirectional Audio Payload via RTP/UDP &harr;</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 7.4 — Basic SIP Direct Call Setup and Signaling Sequence (§7.4.2).</div>
</div>
""",
            "quiz": [
                {
                    "q": "What information does the Payload Type field in the RTP header communicate to the receiver?",
                    "opts": [
                        "The TCP window size",
                        "The audio or video encoding format (e.g. PCM, GSM, MPEG) used to compress the payload",
                        "The IP address of the SIP proxy",
                        "The duration of the talkspurt"
                    ],
                    "ans": 1,
                    "exp": "The 7-bit Payload Type identifies the media compression encoding so the receiver can decode the audio or video bits (§7.4.1)."
                },
                {
                    "q": "Which protocol is responsible for initiating, ringing, and terminating VoIP calls between end users?",
                    "opts": [
                        "RTP",
                        "SIP (Session Initiation Protocol)",
                        "OSPF",
                        "ARP"
                    ],
                    "ans": 1,
                    "exp": "SIP is the signaling protocol that manages session setup, ringing, and teardown; RTP transmits the actual audio payload (§7.4.2)."
                }
            ]
        },
        {
            "id": "ch7-5",
            "num": "7.5",
            "title": "Network Support for Multimedia: Scheduling and Policing",
            "subtitle": "FIFO, Priority Queuing, Round Robin, WFQ, and Token Bucket traffic policing",
            "content": r"""
<p>To provide Quality of Service (QoS) guarantees to real-time multimedia flows sharing routers with bursty web traffic, router output ports implement <strong>packet scheduling disciplines</strong> and <strong>traffic policing mechanisms</strong>.</p>

<h3>7.5.1 Packet Scheduling Disciplines</h3>
<ul>
  <li><strong>First-In-First-Out (FIFO):</strong> Packets are transmitted strictly in the order they arrive. If the queue is full, incoming packets are dropped (Tail Drop). Offers zero QoS isolation between flows.</li>
  <li><strong>Priority Queuing:</strong> Packets are classified into priority classes (e.g. VoIP has High Priority; email has Low Priority). The router <em>never transmits a low-priority packet if any high-priority packet is waiting in queue</em>!
    <br><span style="color:var(--danger-text); font-weight:700;">Fatal Flaw (Starvation):</span> A continuous stream of high-priority packets will completely starve low-priority traffic!
  </li>
  <li><strong>Round Robin:</strong> The scheduler cycles between packet classes: transmits one packet from Class 1, then one packet from Class 2, and so on. Prevents starvation, but treats all classes with equal weight regardless of packet size.</li>
  <li><strong>Weighted Fair Queuing (WFQ):</strong> The generalized, ideal round-robin scheduler. Each class <span class="math-inline">i</span> is assigned a weight <span class="math-inline">w_i</span>. Each class is guaranteed a minimum fraction of link transmission capacity <span class="math-inline">R</span>:
    <div class="math-display">
      \text{Guaranteed Throughput for Class } i = R \times \left( \frac{w_i}{\sum_j w_j} \right)
    </div>
  </li>
</ul>

<h3>7.5.2 Traffic Policing: The Token Bucket Mechanism</h3>
<p>A network cannot guarantee delay bounds to a flow unless the flow's traffic is <strong>policed</strong> (bounded). The standard mechanism is the <strong>Token Bucket</strong>:</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 Token Bucket (r, b) Parameters (§7.5.2)</div>
  <p>A token bucket has two parameters:</p>
  <ul>
    <li><strong>Token Generation Rate <span class="math-inline">r</span> (tokens/sec):</strong> Tokens are deposited into the bucket at a constant rate of <span class="math-inline">r</span> tokens per second. (Limits the long-term average transmission rate).</li>
    <li><strong>Bucket Capacity <span class="math-inline">b</span> (tokens):</strong> The bucket can hold at most <span class="math-inline">b</span> tokens. Excess tokens overflow and are discarded. (Limits the maximum burst size).</li>
  </ul>
  <p><strong>Transmission Rule:</strong> Before a packet of size <span class="math-inline">L</span> bits can be transmitted onto the link, it must remove <span class="math-inline">L</span> tokens from the bucket. If fewer than <span class="math-inline">L</span> tokens are present, the packet must wait or be marked as non-conformant.</p>
  <p><strong>Maximum Burst Constraint:</strong> Over any time interval of length <span class="math-inline">t</span>, the maximum number of bits that can be admitted into the network is strictly bounded by:</p>
  <div class="math-display">
    \text{Max Bits in Interval } t = b + r \cdot t
  </div>
</div>

<!-- EMBEDDED INTERACTIVE: TOKEN BUCKET CALCULATOR -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🚰 Interactive Token Bucket Traffic Policing Calculator</div>
    <span class="interactive-badge">QoS Policing Tool</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:1rem;">
    Calculate the maximum burst transmission permitted under token generation rate r and bucket depth b:
  </p>
  <div class="calc-grid">
    <div class="calc-field">
      <label class="calc-label">Bucket Capacity b (kbits)</label>
      <input type="number" id="sec7-tb-b" class="calc-input" value="1000" min="10" max="50000" oninput="calcSec7TokenBucket()">
    </div>
    <div class="calc-field">
      <label class="calc-label">Token Rate r (kbps)</label>
      <input type="number" id="sec7-tb-r" class="calc-input" value="100" min="1" max="10000" oninput="calcSec7TokenBucket()">
    </div>
    <div class="calc-field">
      <label class="calc-label">Burst Duration t (seconds)</label>
      <input type="number" id="sec7-tb-t" class="calc-input" value="5" min="0.1" max="60" step="0.5" oninput="calcSec7TokenBucket()">
    </div>
  </div>
  <div id="sec7-tb-result" class="calc-result-box" style="margin-top:1rem;">
    <!-- Computed live -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What is the maximum number of bits a Token Bucket with capacity b = 500 kbits and rate r = 100 kbps can transmit in an interval of t = 10 seconds?",
                    "opts": [
                        "500 kbits",
                        "1,000 kbits",
                        "1,500 kbits",
                        "5,000 kbits"
                    ],
                    "ans": 2,
                    "exp": "Max bits = b + r * t = 500 + (100 * 10) = 500 + 1000 = 1,500 kbits (§7.5.2)."
                },
                {
                    "q": "In a Weighted Fair Queuing (WFQ) scheduler with link capacity R = 10 Mbps, Class 1 has weight 1 and Class 2 has weight 3. What is the guaranteed throughput for Class 1?",
                    "opts": [
                        "1 Mbps",
                        "2.5 Mbps",
                        "3.33 Mbps",
                        "7.5 Mbps"
                    ],
                    "ans": 1,
                    "exp": "Guaranteed rate = R * (w1 / (w1 + w2)) = 10 Mbps * (1 / (1 + 3)) = 10 / 4 = 2.5 Mbps (§7.5.1)."
                }
            ]
        },
        {
            "id": "ch7-6",
            "num": "7.6",
            "title": "Chapter 7 Summary & Worked Problems",
            "subtitle": "Comprehensive multimedia review and worked QoS calculation",
            "content": r"""
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 7: Token Bucket & WFQ Delay Guarantee</div>
    <span class="interactive-badge">P12 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Consider a 10 Mbps link shared by two traffic flows using Weighted Fair Queuing (WFQ). Flow 1 has weight <span class="math-inline">w_1 = 1</span> and is policed by a Token Bucket with capacity <span class="math-inline">b = 100\text{ kbits}</span> and rate <span class="math-inline">r = 1\text{ Mbps}</span>. Flow 2 has weight <span class="math-inline">w_2 = 1</span>.
    <br>Find the maximum queuing delay experienced by any packet in Flow 1.
  </p>

  <button class="btn-secondary" onclick="toggleSolution('ch7-prob1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch7-prob1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Calculate the guaranteed transmission service rate for Flow 1:
      <div class="math-display">
        R_1 = R \times \left( \frac{w_1}{w_1 + w_2} \right) = 10\text{ Mbps} \times \left( \frac{1}{1 + 1} \right) = 5\text{ Mbps}
      </div>
    </div>
    <div class="calc-step">Step 2: Determine worst-case queuing delay:
      <br>&emsp;The worst-case queuing delay occurs when the bucket is full (<span class="math-inline">b = 100\text{ kbits}</span>) and transmits an immediate maximum burst of <span class="math-inline">b</span> bits while the link services Flow 1 at its minimum guaranteed rate <span class="math-inline">R_1 = 5\text{ Mbps}</span>.
      <div class="math-display">
        d_{\text{max}} = \frac{b}{R_1} = \frac{100\text{ kbits}}{5\text{ Mbps}} = \frac{100 \times 10^3\text{ bits}}{5 \times 10^6\text{ bps}} = \frac{1}{50}\text{ s} = 0.020\text{ s} = \mathbf{20\text{ ms}}
      </div>
    </div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">
      Final Answer: The maximum queuing delay is strictly bounded to <strong>20 ms</strong>! Combining a Token Bucket with Weighted Fair Queuing provides deterministic delay bounds.
    </div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "What happens if a token bucket's capacity b is reached and tokens continue to be generated at rate r?",
                    "opts": [
                        "The router buffer overflows and crashes",
                        "The extra tokens overflow and are discarded without increasing bucket capacity",
                        "The link transmission rate doubles automatically",
                        "TCP enters slow start"
                    ],
                    "ans": 1,
                    "exp": "Tokens generated when the bucket is full simply overflow and are discarded, preventing infinite burst accumulation (§7.5.2)."
                }
            ]
        }
    ]
}
