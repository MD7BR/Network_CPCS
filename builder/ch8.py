"""Chapter 8 Data: Security in Computer Networks (Kurose & Ross 6th & 8th Ed.)
Enhanced with bit-accurate SVG diagrams, interactive RSA calculator, ap1.0-ap4.0 stepper,
and stateful firewall ACL rule tester.
"""

CH8_DATA = {
    "id": "ch8",
    "num": 8,
    "title": "Security in Computer Networks",
    "subtitle": "Cryptography (DES, AES, RSA), Message Integrity, ap1.0–ap4.0, SSL/TLS, IPsec & Firewalls",
    "layer": "Security",
    "color": "#e11d48",
    "objectives": [
        "Define the 4 pillars of network security: Confidentiality, Integrity, Authentication, and Operational Security",
        "Contrast Symmetric Ciphers (AES, CBC mode) with Asymmetric Public-Key Cryptography (RSA)",
        "Execute RSA key generation, encryption (c = m^e mod n), and decryption (m = c^d mod n) with worked examples",
        "Differentiate Message Authentication Codes (MAC) from Public-Key Digital Signatures and CA Certificates",
        "Trace endpoint authentication protocol vulnerabilities: ap1.0 -> ap2.0 -> ap3.0 -> ap3.1 -> ap4.0 (Nonces)",
        "Analyze the SSL/TLS 1.2 handshake, 4-key derivation, and SSL record sequencing",
        "Evaluate IPsec in Tunnel Mode vs Transport Mode, AH vs ESP, and Security Associations (SAs)",
        "Construct Firewall Access Control Lists (ACLs) and contrast Stateless Filters with Stateful Inspection"
    ],
    "sections": [
        {
            "id": "ch8-1",
            "num": "8.1",
            "title": "What Is Network Security?",
            "subtitle": "The four pillars: Confidentiality, Integrity, Authentication, and Operational Security",
            "content": r"""
<p>In network security discussions, we refer to the communicating parties as <strong>Alice</strong> and <strong>Bob</strong>, and the malicious attacker as <strong>Trudy</strong> (intruder). Secure communication requires four fundamental pillars:</p>

<div class="summary-grid" style="margin:1rem 0;">
  <div class="summary-card" style="border-top:3px solid #3b82f6;">
    <div style="font-size:1.5rem; margin-bottom:0.25rem;">🔒</div>
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">1. Confidentiality</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">Only the sender and intended receiver should understand message contents. Intercepted ciphertext must be undecipherable without the decryption key.</p>
  </div>
  <div class="summary-card" style="border-top:3px solid #10b981;">
    <div style="font-size:1.5rem; margin-bottom:0.25rem;">🛡️</div>
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">2. Message Integrity</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">Communicating parties verify that transmitted data has not been modified, forged, or truncated by an adversary in transit (checked via MACs or digital signatures).</p>
  </div>
  <div class="summary-card" style="border-top:3px solid #8b5cf6;">
    <div style="font-size:1.5rem; margin-bottom:0.25rem;">🪪</div>
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">3. End-Point Authentication</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">Both sender and receiver confirm each other's true identity (proving Alice is genuinely Alice, defeating impersonation and spoofing).</p>
  </div>
  <div class="summary-card" style="border-top:3px solid #e11d48;">
    <div style="font-size:1.5rem; margin-bottom:0.25rem;">🧱</div>
    <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.35rem;">4. Operational Security</div>
    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">Protecting enterprise infrastructure from external threats, unauthorized access, and denial of service via packet filters, stateful firewalls, and IDSs.</p>
  </div>
</div>

<!-- FIGURE 8.1: THREAT MODEL SVG -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 760 180" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <!-- Alice -->
      <rect x="40" y="45" width="120" height="70" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="100" y="78" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">Alice</text>
      <text x="100" y="98" font-size="9" fill="#3b82f6" text-anchor="middle">Legitimate Sender</text>

      <!-- Channel Line -->
      <line x1="160" y1="80" x2="600" y2="80" stroke="#94a3b8" stroke-width="3"/>
      <text x="380" y="70" font-size="10" fill="#64748b" text-anchor="middle">Insecure Public Channel (Plaintext m &rarr; Ciphertext c)</text>

      <!-- Bob -->
      <rect x="600" y="45" width="120" height="70" rx="8" fill="#d1fae5" stroke="#10b981" stroke-width="2"/>
      <text x="660" y="78" font-size="12" font-weight="700" fill="#047857" text-anchor="middle">Bob</text>
      <text x="660" y="98" font-size="9" fill="#059669" text-anchor="middle">Intended Receiver</text>

      <!-- Trudy (Attacker) in Center Below -->
      <rect x="310" y="105" width="140" height="60" rx="8" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
      <text x="380" y="130" font-size="12" font-weight="800" fill="#b91c1c" text-anchor="middle">Trudy (Intruder)</text>
      <text x="380" y="148" font-size="8.5" fill="#dc2626" text-anchor="middle">Sniff, Tamper, Spoof, Replay</text>

      <!-- Threat Arrows -->
      <path d="M 380 80 L 380 105" stroke="#ef4444" stroke-width="2" stroke-dasharray="3 3"/>
      <path d="M 350 105 L 260 80" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 3"/>
      <path d="M 410 105 L 500 80" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 3"/>
    </svg>
  </div>
  <div class="figure-caption">Figure 8.1 — The Network Security Threat Model: Alice, Bob, and Trudy the Intruder (§8.1).</div>
</div>
""",
            "quiz": [
                {
                    "q": "Which security property ensures that a message has not been altered or tampered with in transit between sender and receiver?",
                    "opts": [
                        "Confidentiality",
                        "Message Integrity",
                        "Non-repudiation",
                        "High availability"
                    ],
                    "ans": 1,
                    "exp": "Message integrity guarantees that the recipient can detect whether transmitted data was modified, inserted, or deleted by an adversary (§8.1)."
                }
            ]
        },
        {
            "id": "ch8-2",
            "num": "8.2",
            "title": "Principles of Cryptography",
            "subtitle": "Symmetric key cryptography (DES, AES, CBC) and Public Key Cryptography (RSA)",
            "content": r"""
<p>Cryptography transforms plaintext <span class="math-inline">m</span> into ciphertext <span class="math-inline">c = K_A(m)</span>, and inverts ciphertext back: <span class="math-inline">m = K_B(c)</span>.</p>

<h3>Symmetric Key Cryptography</h3>
<p>Alice and Bob share the <strong>exact same secret key</strong> (<span class="math-inline">K_A = K_B</span>).</p>
<ul>
  <li><strong>Block Ciphers:</strong> Break data into blocks of <span class="math-inline">k</span> bits (64 bits in DES, 128 bits in AES with 128, 192, or 256-bit keys).
    <br>&bull; <strong>Electronic Codebook (ECB):</strong> Encrypts each block independently. <em>Flaw:</em> identical plaintext blocks produce identical ciphertext blocks!
    <br>&bull; <strong>Cipher Block Chaining (CBC):</strong> Generates a random Initialization Vector (IV). Before encrypting block <span class="math-inline">i</span>, it is XORed with ciphertext block <span class="math-inline">i - 1</span>:
    <div class="math-display">
      c_i = K_S(m_i \oplus c_{i-1}) \quad (\text{where } c_0 = \text{IV})
    </div>
  </li>
</ul>

<!-- FIGURE 8.2: CBC MODE SVG -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 160" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <!-- Block 1 -->
      <rect x="40" y="20" width="80" height="28" rx="4" fill="#ede9fe" stroke="#8b5cf6"/>
      <text x="80" y="38" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Plaintext m1</text>
      <circle cx="80" cy="70" r="10" fill="#fee2e2" stroke="#ef4444"/>
      <text x="80" y="74" font-size="12" font-weight="800" fill="#b91c1c" text-anchor="middle">&oplus;</text>
      <line x1="80" y1="48" x2="80" y2="60" stroke="#8b5cf6" stroke-width="1.5"/>
      <!-- IV -->
      <rect x="10" y="85" width="40" height="20" rx="3" fill="#fed7aa" stroke="#f97316"/>
      <text x="30" y="99" font-size="9" font-weight="700" fill="#9a3412" text-anchor="middle">IV</text>
      <line x1="50" y1="95" x2="72" y2="76" stroke="#f97316" stroke-width="1.5"/>
      <!-- AES Block 1 -->
      <rect x="50" y="95" width="60" height="26" rx="4" fill="#dbeafe" stroke="#2563eb"/>
      <text x="80" y="112" font-size="9.5" font-weight="700" fill="#1e40af" text-anchor="middle">AES (Ks)</text>
      <line x1="80" y1="80" x2="80" y2="95" stroke="#ef4444" stroke-width="1.5"/>
      <!-- Ciphertext 1 -->
      <rect x="40" y="130" width="80" height="25" rx="4" fill="#d1fae5" stroke="#10b981"/>
      <text x="80" y="147" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Cipher c1</text>
      <line x1="80" y1="121" x2="80" y2="130" stroke="#2563eb" stroke-width="1.5"/>

      <!-- Chain line to Block 2 -->
      <path d="M 120 142 L 230 142 L 230 76 L 250 72" fill="none" stroke="#10b981" stroke-width="1.5"/>

      <!-- Block 2 -->
      <rect x="220" y="20" width="80" height="28" rx="4" fill="#ede9fe" stroke="#8b5cf6"/>
      <text x="260" y="38" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Plaintext m2</text>
      <circle cx="260" cy="70" r="10" fill="#fee2e2" stroke="#ef4444"/>
      <text x="260" y="74" font-size="12" font-weight="800" fill="#b91c1c" text-anchor="middle">&oplus;</text>
      <line x1="260" y1="48" x2="260" y2="60" stroke="#8b5cf6" stroke-width="1.5"/>
      <rect x="230" y="95" width="60" height="26" rx="4" fill="#dbeafe" stroke="#2563eb"/>
      <text x="260" y="112" font-size="9.5" font-weight="700" fill="#1e40af" text-anchor="middle">AES (Ks)</text>
      <line x1="260" y1="80" x2="260" y2="95" stroke="#ef4444" stroke-width="1.5"/>
      <rect x="220" y="130" width="80" height="25" rx="4" fill="#d1fae5" stroke="#10b981"/>
      <text x="260" y="147" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Cipher c2</text>
      <line x1="260" y1="121" x2="260" y2="130" stroke="#2563eb" stroke-width="1.5"/>

      <!-- Explanation note -->
      <text x="450" y="65" font-size="11" font-weight="700" fill="#1e40af">Cipher Block Chaining (CBC) Mode:</text>
      <text x="450" y="85" font-size="9.5" fill="#64748b">&bull; Each plaintext block is XORed with previous ciphertext block</text>
      <text x="450" y="103" font-size="9.5" fill="#64748b">&bull; Random IV ensures identical messages produce distinct ciphertexts</text>
      <text x="450" y="121" font-size="9.5" fill="#64748b">&bull; Defeats dictionary and replay pattern attacks</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 8.2 — Cipher Block Chaining (CBC) Encryption with Initialization Vector (IV) (§8.2.1).</div>
</div>

<h3>Public Key Cryptography: RSA Algorithm (§8.2.2)</h3>
<p>Public-key cryptography uses a key pair: public key <span class="math-inline">(n, e)</span> known to all, and private key <span class="math-inline">(n, d)</span> kept strictly confidential by the owner.</p>

<div class="callout callout-formula">
  <div class="callout-header">🧮 RSA Key Generation & Encryption Steps</div>
  <ol>
    <li>Choose two distinct prime numbers <span class="math-inline">p</span> and <span class="math-inline">q</span>.</li>
    <li>Compute modulus <span class="math-inline">n = p \times q</span> and totient <span class="math-inline">z = (p - 1)(q - 1)</span>.</li>
    <li>Choose public exponent <span class="math-inline">e &lt; n</span> such that <span class="math-inline">e</span> and <span class="math-inline">z</span> are coprime: <span class="math-inline">\gcd(e, z) = 1</span>.</li>
    <li>Find private exponent <span class="math-inline">d</span> such that <span class="math-inline">(e \times d) \bmod z = 1</span> (modular inverse of <span class="math-inline">e</span> modulo <span class="math-inline">z</span>).</li>
    <li><strong>Encryption:</strong> For message <span class="math-inline">m &lt; n</span>:
      <div class="math-display">c = m^e \bmod n</div>
    </li>
    <li><strong>Decryption:</strong>
      <div class="math-display">m = c^d \bmod n</div>
    </li>
  </ol>
</div>

<!-- Interactive RSA Key & Cipher Calculator -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🔐 Live RSA Key Generation & Encryption Demonstrator</div>
    <span class="interactive-badge">Interactive Calculator</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:1rem;">
    Test RSA with pedagogical small primes to inspect the step-by-step modular arithmetic:
  </p>
  <div class="calc-grid">
    <div class="calc-field">
      <label class="calc-label">Prime p</label>
      <select id="rsa-p-input" class="calc-input" onchange="calcSec8RSA()">
        <option value="3" selected>p = 3</option>
        <option value="5">p = 5</option>
        <option value="7">p = 7</option>
        <option value="11">p = 11</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">Prime q</label>
      <select id="rsa-q-input" class="calc-input" onchange="calcSec8RSA()">
        <option value="11" selected>q = 11</option>
        <option value="5">q = 5</option>
        <option value="7">q = 7</option>
        <option value="13">q = 13</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">Plaintext Message m (m &lt; n)</label>
      <input type="number" id="rsa-m-input" class="calc-input" value="8" min="1" max="30" oninput="calcSec8RSA()">
    </div>
  </div>
  <div id="rsa-output-box" class="calc-result-box" style="margin-top:1rem;">
    <!-- Computed live -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In the RSA algorithm, if primes p = 3 and q = 5, what is the value of totient z = (p - 1)(q - 1)?",
                    "opts": [
                        "15",
                        "8",
                        "12",
                        "2"
                    ],
                    "ans": 1,
                    "exp": "z = (p - 1) * (q - 1) = (3 - 1) * (5 - 1) = 2 * 4 = 8 (§8.2.2)."
                }
            ]
        },
        {
            "id": "ch8-3",
            "num": "8.3",
            "title": "Message Integrity and Digital Signatures",
            "subtitle": "Cryptographic hash functions, MACs, digital signatures, and CA certificates",
            "content": r"""
<p>Message integrity requires confirming that data has not been modified and that it originated from the claimed sender.</p>

<h3>Cryptographic Hash Functions</h3>
<p>A hash function <span class="math-inline">H(m)</span> produces a fixed-size digest (128-bit MD5, 256-bit SHA-256) from arbitrary-length input <span class="math-inline">m</span>. It must be <strong>collision resistant</strong>: computationally infeasible to find <span class="math-inline">x \ne y</span> such that <span class="math-inline">H(x) = H(y)</span>.</p>

<h3>Message Authentication Code (MAC)</h3>
<p>Alice and Bob share a secret authentication key <span class="math-inline">s</span>. Alice appends <span class="math-inline">s</span> to message <span class="math-inline">m</span>, calculates <span class="math-inline">H(m + s)</span>, and sends <span class="math-inline">(m, H(m + s))</span>. Bob appends his shared key <span class="math-inline">s</span> and verifies the hash matches. Trudy cannot forge the MAC because she does not possess <span class="math-inline">s</span>.</p>

<h3>Digital Signatures</h3>
<p>To sign a message digitally, Alice computes the cryptographic hash of the message <span class="math-inline">H(m)</span> and encrypts the hash using her <strong>private key</strong>: <span class="math-inline">K_A^-(H(m))</span>. Anyone can verify the signature using Alice's <strong>public key</strong>: <span class="math-inline">K_A^+(K_A^-(H(m))) = H(m)</span>.</p>

<div class="callout callout-def">
  <div class="callout-header">📘 Certification Authorities (CAs) & Public-Key Infrastructure (PKI)</div>
  How does Bob know that a public key <span class="math-inline">K_A^+</span> actually belongs to Alice, rather than an imposter? A <strong>Certification Authority (CA)</strong> validates Alice's physical identity and issues an <strong>X.509 Digital Certificate</strong> binding Alice's identity to her public key, signed by the CA's own private key!
</div>
""",
            "quiz": [
                {
                    "q": "How does a sender create a digital signature for a message m?",
                    "opts": [
                        "By encrypting the entire message with the recipient's public key",
                        "By hashing the message and encrypting the hash with the sender's private key",
                        "By computing an unkeyed 16-bit checksum",
                        "By sending the password in plain text"
                    ],
                    "ans": 1,
                    "exp": "A digital signature is created by computing a cryptographic hash H(m) and encrypting that hash using the sender's private key (§8.3.3)."
                }
            ]
        },
        {
            "id": "ch8-4",
            "num": "8.4",
            "title": "End-Point Authentication Protocols",
            "subtitle": "Evolution from ap1.0 to ap4.0 and defeating playback attacks with Nonces",
            "content": r"""
<p>How can Bob verify that the entity communicating with him is truly Alice? Kurose & Ross trace the design of authentication protocols:</p>

<ul>
  <li><strong>ap1.0:</strong> Alice simply sends <em>"I am Alice"</em>. <em>Flaw:</em> Trudy can impersonate Alice by sending the exact same string!</li>
  <li><strong>ap2.0:</strong> Bob checks the IP source address in the IP datagram header. <em>Flaw:</em> Trudy can easily <strong>spoof</strong> the IP source address.</li>
  <li><strong>ap3.0:</strong> Alice sends her secret password. <em>Flaw:</em> Trudy sniffs the password on the wire and reuses it.</li>
  <li><strong>ap3.1:</strong> Alice encrypts her password with a shared symmetric key <span class="math-inline">K_{A-B}</span>.
    <br><span style="color:var(--danger-text); font-weight:700;">Fatal Flaw (Playback / Replay Attack):</span> Trudy records the encrypted password ciphertext and plays it back to Bob later. Bob decrypts it, finds the correct password, and grants Trudy access!
  </li>
  <li><strong>ap4.0 (Challenge-Response with Nonce):</strong>
    A <strong>nonce</strong> is a random number used only once in a lifetime.
    <ol>
      <li>Alice sends: <em>"I am Alice"</em>.</li>
      <li>Bob generates a random nonce <span class="math-inline">R</span> and sends it to Alice (Challenge).</li>
      <li>Alice encrypts the nonce using shared secret key: <span class="math-inline">K_{A-B}(R)</span> and returns it (Response).</li>
      <li>Bob decrypts the response; if it equals <span class="math-inline">R</span>, Alice is authenticated!</li>
    </ol>
    <em>Defeats the playback attack because Bob generates a completely different random nonce for every session!</em>
  </li>
</ul>

<!-- Interactive Authentication Evolution Stepper -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🕵️ Interactive Authentication Protocol Explorer (ap1.0 &rarr; ap4.0)</div>
    <span class="interactive-badge">Security Simulation</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:1rem;">
    Select an authentication protocol to step through the packet exchange and observe how Trudy attempts an attack:
  </p>
  <div class="fig-controls" style="margin-bottom:1rem;">
    <button class="btn-secondary" id="sec8-btn-ap1" onclick="stepSec8Auth('ap1')">Protocol ap1.0</button>
    <button class="btn-secondary" id="sec8-btn-ap2" onclick="stepSec8Auth('ap2')">Protocol ap2.0</button>
    <button class="btn-secondary" id="sec8-btn-ap3" onclick="stepSec8Auth('ap3')">Protocol ap3.0</button>
    <button class="btn-secondary" id="sec8-btn-ap31" onclick="stepSec8Auth('ap31')">Protocol ap3.1 (Replay)</button>
    <button class="btn-primary" id="sec8-btn-ap4" onclick="stepSec8Auth('ap4')">Protocol ap4.0 (Nonce)</button>
  </div>
  <div id="sec8-auth-diagram" style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:1.25rem;">
    <!-- Rendered dynamically -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "Why does protocol ap3.1 (sending an encrypted password) fail against a playback attack?",
                    "opts": [
                        "Because the key length is too short",
                        "Because the adversary can record the encrypted password ciphertext and play it back in a subsequent session without needing to decrypt it",
                        "Because IP spoofing bypasses encryption",
                        "Because UDP does not support acknowledgments"
                    ],
                    "ans": 1,
                    "exp": "In a replay/playback attack, Trudy does not need to know the plaintext password; simply resending the recorded ciphertext satisfies the server's check (§8.4)."
                }
            ]
        },
        {
            "id": "ch8-5",
            "num": "8.5",
            "title": "Securing E-Mail: PGP",
            "subtitle": "Pretty Good Privacy (PGP) hybrid encryption and digital signatures",
            "content": r"""
<p>Email security is provided at the application layer by <strong>PGP (Pretty Good Privacy)</strong>. PGP provides confidentiality, integrity, and sender non-repudiation using a <strong>hybrid cryptosystem</strong>:</p>
<ol>
  <li>Sender generates a random, single-use symmetric <strong>session key <span class="math-inline">K_S</span></strong>.</li>
  <li>Sender encrypts the email message <span class="math-inline">m</span> with <span class="math-inline">K_S</span> using symmetric AES.</li>
  <li>Sender encrypts <span class="math-inline">K_S</span> using recipient's public key: <span class="math-inline">K_B^+(K_S)</span>.</li>
  <li>Sender digitally signs the message hash with sender's private key: <span class="math-inline">K_A^-(H(m))</span>.</li>
  <li>Sender packages and transmits all components together.</li>
</ol>
""",
            "quiz": [
                {
                    "q": "Why does PGP use a symmetric session key to encrypt email messages rather than encrypting the message directly with the recipient's RSA public key?",
                    "opts": [
                        "Public key algorithms (RSA) are computationally slow on large data, so PGP encrypts the payload with fast symmetric cipher (AES) and encrypts only the small session key with RSA",
                        "Symmetric keys cannot be broken by quantum computers",
                        "PGP does not use public key cryptography",
                        "To bypass spam filters"
                    ],
                    "ans": 0,
                    "exp": "Symmetric ciphers are orders of magnitude faster than asymmetric algorithms. Hybrid encryption gets the speed of symmetric ciphers with the key distribution ease of public key (§8.5)."
                }
            ]
        },
        {
            "id": "ch8-6",
            "num": "8.6",
            "title": "Securing TCP Connections: SSL / TLS",
            "subtitle": "SSL handshake, master secret derivation, 4 session keys, and record sequence numbers",
            "content": r"""
<p><strong>SSL (Secure Sockets Layer)</strong> and its standardized successor <strong>TLS (Transport Layer Security)</strong> provide transport-layer security for TCP applications (HTTPS, port 443).</p>

<h3>The SSL/TLS Handshake</h3>
<ol>
  <li><strong>ClientHello:</strong> Client sends supported cipher suites and a random nonce <span class="math-inline">R_C</span>.</li>
  <li><strong>ServerHello:</strong> Server selects cipher suite, sends server nonce <span class="math-inline">R_S</span> and its <strong>CA Certificate</strong>.</li>
  <li><strong>Pre-Master Secret:</strong> Client validates server's certificate, generates a random 48-byte Pre-Master Secret (PMS), encrypts it with the server's public key, and sends it to the server.</li>
  <li><strong>Master Secret Derivation:</strong> Both sides independently compute the <strong>Master Secret (MS)</strong> from the PMS, <span class="math-inline">R_C</span>, and <span class="math-inline">R_S</span>.</li>
  <li><strong>Key Derivation:</strong> From the Master Secret, four separate keys are sliced:
    <br>&bull; <span class="math-inline">K_{EB}</span>: Client-to-server data encryption key.
    <br>&bull; <span class="math-inline">K_{MB}</span>: Client-to-server MAC key.
    <br>&bull; <span class="math-inline">K_{EA}</span>: Server-to-client data encryption key.
    <br>&bull; <span class="math-inline">K_{MA}</span>: Server-to-client MAC key.
  </li>
  <li><strong>Finished Messages:</strong> Both sides exchange encrypted MAC hashes of all prior handshake messages to verify no tampering occurred.</li>
</ol>

<div class="callout callout-def">
  <div class="callout-header">📘 Preventing Truncation and Replay Attacks in SSL Records</div>
  Each SSL record includes a <strong>sequence number</strong> in its MAC computation. Because sequence numbers increment with each record, Trudy cannot replay or reorder records. Furthermore, a special SSL <code>close_notify</code> alert prevents Trudy from prematurely ending a TCP session (truncation attack).
</div>
""",
            "quiz": [
                {
                    "q": "How many separate session keys are derived from the Master Secret in SSL/TLS 1.2?",
                    "opts": [
                        "1 key (shared for everything)",
                        "2 keys (one public, one private)",
                        "4 keys (client encrypt, client MAC, server encrypt, server MAC)",
                        "8 keys"
                    ],
                    "ans": 2,
                    "exp": "SSL derives 4 keys: two encryption keys (one per direction) and two MAC keys (one per direction) to maintain cryptographic separation (§8.6.2)."
                }
            ]
        },
        {
            "id": "ch8-7",
            "num": "8.7",
            "title": "Network-Layer Security: IPsec and VPNs",
            "subtitle": "Tunnel Mode vs Transport Mode, AH vs ESP, and Security Associations (SAs)",
            "content": r"""
<p><strong>IPsec</strong> provides security at the network layer for all IP traffic, transparent to applications. It is the foundation for <strong>Virtual Private Networks (VPNs)</strong>.</p>

<h3>AH vs ESP Protocols</h3>
<ul>
  <li><strong>Authentication Header (AH):</strong> Provides source authentication and message integrity, but <strong>NO encryption (no confidentiality)</strong>.</li>
  <li><strong>Encapsulating Security Payload (ESP):</strong> Provides <strong>data confidentiality (encryption)</strong>, message integrity, and source authentication. Widely used.</li>
</ul>

<h3>Transport Mode vs Tunnel Mode</h3>
<ul>
  <li><strong>Transport Mode:</strong> IPsec header inserted directly after original IP header. Protects upper layers; used for host-to-host security. Original IP addresses remain visible.</li>
  <li><strong>Tunnel Mode:</strong> The <em>entire original IP datagram</em> (including original IP headers) is encrypted and placed inside a brand-new outer IP datagram with new tunnel router IP addresses! Used for router-to-router VPN gateways.</li>
</ul>

<!-- FIGURE 8.5: IPSEC TUNNEL MODE SVG -->
<div class="svg-figure">
  <div class="svg-container">
    <svg viewBox="0 0 740 140" xmlns="http://www.w3.org/2000/svg" style="background:var(--bg-card); border-radius:10px; width:100%;">
      <text x="30" y="25" font-size="11" font-weight="700" fill="#1e40af">IPsec Tunnel Mode Datagram Layout:</text>

      <!-- New Outer IP Header -->
      <rect x="30" y="45" width="130" height="40" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="95" y="65" font-size="10" font-weight="700" fill="#1e40af" text-anchor="middle">New IP Header</text>
      <text x="95" y="78" font-size="8.5" fill="#3b82f6" text-anchor="middle">Tunnel Gateway IPs</text>

      <!-- ESP Header -->
      <rect x="165" y="45" width="85" height="40" rx="4" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
      <text x="207" y="65" font-size="10" font-weight="700" fill="#b91c1c" text-anchor="middle">ESP Header</text>
      <text x="207" y="78" font-size="8.5" fill="#ef4444" text-anchor="middle">SPI, Seq #</text>

      <!-- Encrypted Original Datagram -->
      <rect x="255" y="45" width="280" height="40" rx="4" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="395" y="65" font-size="10.5" font-weight="700" fill="#6d28d9" text-anchor="middle">🔒 Encrypted Original IP Datagram</text>
      <text x="395" y="78" font-size="8.5" fill="#8b5cf6" text-anchor="middle">Orig IP Header + TCP Header + Application Data</text>

      <!-- ESP Trailer -->
      <rect x="540" y="45" width="85" height="40" rx="4" fill="#fed7aa" stroke="#f97316" stroke-width="1.5"/>
      <text x="582" y="65" font-size="10" font-weight="700" fill="#9a3412" text-anchor="middle">ESP Trailer</text>
      <text x="582" y="78" font-size="8.5" fill="#ea580c" text-anchor="middle">Padding, NextHdr</text>

      <!-- ESP Auth Trailer -->
      <rect x="630" y="45" width="80" height="40" rx="4" fill="#d1fae5" stroke="#10b981" stroke-width="1.5"/>
      <text x="670" y="65" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">ESP Auth</text>
      <text x="670" y="78" font-size="8.5" fill="#10b981" text-anchor="middle">HMAC MAC</text>

      <!-- Bracket Annotations -->
      <path d="M 255 95 L 255 105 L 625 105 L 625 95" fill="none" stroke="#8b5cf6" stroke-width="1.5"/>
      <text x="440" y="120" font-size="9" font-weight="700" fill="#6d28d9" text-anchor="middle">Encrypted (Confidentiality)</text>

      <path d="M 165 125 L 165 132 L 710 132 L 710 125" fill="none" stroke="#047857" stroke-width="1.5"/>
      <text x="440" y="140" font-size="8.5" font-weight="700" fill="#047857" text-anchor="middle">Authenticated (Integrity & Anti-Replay)</text>
    </svg>
  </div>
  <div class="figure-caption">Figure 8.5 — Structure of an IPsec Datagram in Tunnel Mode (§8.7.4).</div>
</div>

<div class="callout callout-def">
  <div class="callout-header">📘 Security Associations (SAs)</div>
  An SA is a <strong>unidirectional simplex logical connection</strong>. If two VPN gateways A and B communicate securely, they require <strong>two SAs</strong> (one from A to B, one from B to A). Each SA is uniquely identified by a 32-bit <strong>Security Parameter Index (SPI)</strong>.
</div>
""",
            "quiz": [
                {
                    "q": "In IPsec Tunnel Mode, what happens to the original IP datagram?",
                    "opts": [
                        "It is fragmented into 8-byte chunks",
                        "The entire original IP datagram (header + payload) is encrypted and encapsulated inside a new outer IP datagram",
                        "Only the TCP header is encrypted",
                        "It is converted to an ATM cell"
                    ],
                    "ans": 1,
                    "exp": "In IPsec Tunnel Mode, the complete original datagram is encrypted and encapsulated inside a new outer datagram, hiding internal private network addresses (§8.7.4)."
                }
            ]
        },
        {
            "id": "ch8-8",
            "num": "8.8",
            "title": "Securing Wireless LANs",
            "subtitle": "WEP vulnerabilities and IEEE 802.11i (WPA2)",
            "content": r"""
<h3>Wired Equivalent Privacy (WEP) Vulnerabilities</h3>
<p>WEP was designed for 802.11 but contained fatal architectural flaws:</p>
<ul>
  <li>Used a tiny <strong>24-bit Initialization Vector (IV)</strong> concatenated with a shared secret key. Because 24 bits has only <span class="math-inline">2^{24} \approx 16.7</span> million values, a busy AP reuses IVs within hours, allowing attackers to recover the key!</li>
  <li>Used the linear, unkeyed CRC-32 checksum, allowing attackers to modify ciphertext packets undetected.</li>
</ul>

<h3>IEEE 802.11i (WPA2)</h3>
<p>WPA2 solved WEP's flaws by introducing: <strong>802.1X / EAP authentication</strong> with an Authentication Server (RADIUS), derivation of temporary <strong>Pairwise Master Keys (PMK)</strong> via a 4-way handshake, and strong <strong>AES-CCMP</strong> block cipher encryption.</p>
""",
            "quiz": [
                {
                    "q": "What was the fatal flaw in WEP's use of the Initialization Vector (IV)?",
                    "opts": [
                        "The IV was too long (512 bits)",
                        "The IV was only 24 bits, causing rapid IV reuse and key exposure on busy networks",
                        "It used RSA instead of AES",
                        "It required physical ethernet cables"
                    ],
                    "ans": 1,
                    "exp": "WEP's short 24-bit IV guaranteed frequent IV reuse, allowing eavesdroppers to decrypt traffic and recover the secret key (§8.8.1)."
                }
            ]
        },
        {
            "id": "ch8-9",
            "num": "8.9",
            "title": "Operational Security: Firewalls and IDS",
            "subtitle": "Stateless packet filtering, ACLs, stateful inspection, and Intrusion Detection Systems",
            "content": r"""
<p>A <strong>firewall</strong> isolates an organization's internal network from the Internet, allowing only authorized traffic to enter or leave.</p>

<h3>Types of Firewalls</h3>
<ul>
  <li><strong>Stateless Packet Filters:</strong> Examines each packet in isolation and applies an <strong>Access Control List (ACL)</strong> based on:
    <br>&bull; IP source and destination addresses
    <br>&bull; Protocol type (TCP, UDP, ICMP)
    <br>&bull; TCP/UDP source and destination ports
    <br>&bull; TCP flags (e.g. ACK bit = 1 indicates existing connection, ACK = 0 with SYN = 1 indicates incoming connection request).
  </li>
  <li><strong>Stateful Packet Filters:</strong> Tracks active TCP connections in a <strong>connection state table</strong>. Blocks any incoming packet with ACK bit set unless it matches an existing entry in the state table initiated from inside the LAN!</li>
  <li><strong>Application Gateways:</strong> Acts as an application-specific proxy (e.g. Telnet gateway) inspecting application data payloads.</li>
</ul>

<!-- Interactive Firewall ACL Rule Evaluator -->
<div class="interactive-box" style="margin:1.5rem 0;">
  <div class="interactive-header">
    <div class="interactive-title">🧱 Interactive Firewall ACL Packet Filter Simulator</div>
    <span class="interactive-badge">Operational Security</span>
  </div>
  <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.75rem;">
    Configure an arriving packet's 5-tuple header fields to test how the enterprise Access Control List (ACL) filters it (first-match evaluation):
  </p>
  
  <div style="overflow-x:auto; margin-bottom:1rem;">
    <table style="width:100%; border-collapse:collapse; font-size:0.8rem; background:var(--bg-card); border:1px solid var(--border); border-radius:6px;">
      <thead>
        <tr style="background:var(--bg-secondary); border-bottom:1px solid var(--border); text-align:left;">
          <th style="padding:6px 8px;">Rule #</th>
          <th style="padding:6px 8px;">Action</th>
          <th style="padding:6px 8px;">Protocol</th>
          <th style="padding:6px 8px;">Source IP</th>
          <th style="padding:6px 8px;">Src Port</th>
          <th style="padding:6px 8px;">Dest IP</th>
          <th style="padding:6px 8px;">Dest Port</th>
          <th style="padding:6px 8px;">Flag</th>
        </tr>
      </thead>
      <tbody>
        <tr id="sec8-acl-row-1" style="border-bottom:1px solid var(--border-light);">
          <td style="padding:6px 8px; font-weight:700;">1</td><td style="padding:6px 8px; color:var(--accent-text); font-weight:700;">ALLOW</td><td>TCP</td><td>192.168.1.* (Internal)</td><td>*</td><td>* (External)</td><td>80, 443</td><td>Any</td>
        </tr>
        <tr id="sec8-acl-row-2" style="border-bottom:1px solid var(--border-light);">
          <td style="padding:6px 8px; font-weight:700;">2</td><td style="padding:6px 8px; color:var(--accent-text); font-weight:700;">ALLOW</td><td>TCP</td><td>*</td><td>*</td><td>192.168.1.50 (Server)</td><td>80</td><td>Any</td>
        </tr>
        <tr id="sec8-acl-row-3" style="border-bottom:1px solid var(--border-light);">
          <td style="padding:6px 8px; font-weight:700;">3</td><td style="padding:6px 8px; color:var(--accent-text); font-weight:700;">ALLOW</td><td>TCP</td><td>*</td><td>*</td><td>192.168.1.*</td><td>*</td><td>ACK=1</td>
        </tr>
        <tr id="sec8-acl-row-4" style="border-bottom:1px solid var(--border-light);">
          <td style="padding:6px 8px; font-weight:700;">4</td><td style="padding:6px 8px; color:var(--danger-text); font-weight:700;">DROP</td><td>TCP</td><td>*</td><td>*</td><td>192.168.1.*</td><td>*</td><td>ACK=0 (SYN)</td>
        </tr>
        <tr id="sec8-acl-row-5">
          <td style="padding:6px 8px; font-weight:700;">5</td><td style="padding:6px 8px; color:var(--danger-text); font-weight:700;">DROP</td><td>ALL</td><td>*</td><td>*</td><td>*</td><td>*</td><td>Any (Default)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="calc-grid">
    <div class="calc-field">
      <label class="calc-label">Source IP</label>
      <select id="fw-src-ip" class="calc-input" onchange="testSec8Firewall()">
        <option value="192.168.1.15" selected>192.168.1.15 (Internal Host)</option>
        <option value="203.0.113.88">203.0.113.88 (External Internet)</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">Destination IP</label>
      <select id="fw-dst-ip" class="calc-input" onchange="testSec8Firewall()">
        <option value="198.51.100.1" selected>198.51.100.1 (Web Server)</option>
        <option value="192.168.1.50">192.168.1.50 (Internal Server)</option>
        <option value="192.168.1.20">192.168.1.20 (Internal Workstation)</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">Destination Port</label>
      <select id="fw-dst-port" class="calc-input" onchange="testSec8Firewall()">
        <option value="80" selected>Port 80 (HTTP)</option>
        <option value="443">Port 443 (HTTPS)</option>
        <option value="22">Port 22 (SSH)</option>
        <option value="8080">Port 8080 (Alt Web)</option>
      </select>
    </div>
    <div class="calc-field">
      <label class="calc-label">TCP ACK Flag</label>
      <select id="fw-ack-flag" class="calc-input" onchange="testSec8Firewall()">
        <option value="0" selected>ACK = 0 (Connection SYN request)</option>
        <option value="1">ACK = 1 (Established connection response)</option>
      </select>
    </div>
  </div>

  <div id="fw-result-box" class="calc-result-box" style="margin-top:1rem;">
    <!-- Evaluated live -->
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "How does a stateful packet filter prevent an outside attacker from injecting packets with the TCP ACK bit set into an internal network?",
                    "opts": [
                        "It drops all TCP packets",
                        "It checks its internal connection state table to verify that the arriving packet belongs to an ongoing connection initiated by an internal host",
                        "It asks the DNS root server for permission",
                        "It decrypts the packet using RSA"
                    ],
                    "ans": 1,
                    "exp": "A stateful firewall maintains a dynamic state table of active connections and drops packets with ACK set unless they match a valid established connection (§8.9.1)."
                }
            ]
        },
        {
            "id": "ch8-10",
            "num": "8.10",
            "title": "Chapter 8 Summary & Worked Problems",
            "subtitle": "Review concepts and worked RSA small-number calculation",
            "content": r"""
<div class="interactive-card">
  <div class="interactive-header">
    <div class="interactive-title">📝 Worked Homework Problem 8: RSA Calculation Trace</div>
    <span class="interactive-badge">P11 from Kurose & Ross</span>
  </div>
  <p><strong>Problem:</strong> Suppose <span class="math-inline">p = 3</span> and <span class="math-inline">q = 11</span>.</p>
  <p>(a) Find modulus <span class="math-inline">n</span> and Euler's totient <span class="math-inline">z</span>.<br>
     (b) Choose <span class="math-inline">e = 3</span>. Verify that <span class="math-inline">\gcd(e, z) = 1</span> and find private key <span class="math-inline">d</span> such that <span class="math-inline">(e \times d) \bmod z = 1</span>.<br>
     (c) Encrypt the message <span class="math-inline">m = 8</span>. Then decrypt the resulting ciphertext to recover <span class="math-inline">m</span>.</p>
  <button class="btn-secondary" onclick="toggleSolution('ch8-prob1-sol')">Show / Hide Step-by-Step Solution</button>
  <div id="ch8-prob1-sol" class="calc-result-box" style="display:none; margin-top:0.75rem;">
    <div class="calc-step">Step 1: Compute modulus and totient:
      <div class="math-display">n = p \times q = 3 \times 11 = \mathbf{33}</div>
      <div class="math-display">z = (p - 1)(q - 1) = 2 \times 10 = \mathbf{20}</div>
    </div>
    <div class="calc-step">Step 2: Check <span class="math-inline">e = 3</span>: <span class="math-inline">\gcd(3, 20) = 1</span> (coprime, valid choice!).</div>
    <div class="calc-step">Step 3: Find <span class="math-inline">d</span> such that <span class="math-inline">(3 \times d) \bmod 20 = 1</span>:
      <br>&emsp;Testing values: for <span class="math-inline">d = 7</span>: <span class="math-inline">3 \times 7 = 21 = 1 \times 20 + 1 \equiv 1 \pmod{20}</span>.
      <br>&emsp;Therefore, private key <span class="math-inline">d = \mathbf{7}</span>!
    </div>
    <div class="calc-step">Step 4: Encryption of <span class="math-inline">m = 8</span>:
      <div class="math-display">c = m^e \bmod n = 8^3 \bmod 33 = 512 \bmod 33</div>
      <div class="math-display">512 = 15 \times 33 + 17 \implies c = \mathbf{17}</div>
    </div>
    <div class="calc-step">Step 5: Decryption of <span class="math-inline">c = 17</span>:
      <div class="math-display">m = c^d \bmod n = 17^7 \bmod 33</div>
      <br>&emsp;<span class="math-inline">17^2 = 289 \equiv 25 \equiv -8 \pmod{33}</span>
      <br>&emsp;<span class="math-inline">17^4 \equiv (-8)^2 = 64 \equiv 31 \equiv -2 \pmod{33}</span>
      <br>&emsp;<span class="math-inline">17^6 = 17^4 \times 17^2 \equiv (-2) \times (-8) = 16 \pmod{33}</span>
      <br>&emsp;<span class="math-inline">17^7 = 17^6 \times 17 \equiv 16 \times 17 = 272 = 8 \times 33 + 8 \equiv \mathbf{8} \pmod{33}</span>
    </div>
    <div class="calc-step" style="font-weight:700; color:var(--accent-text);">Final Result: Recovered message is m = 8! Exactly matches the original plaintext!</div>
  </div>
</div>
""",
            "quiz": [
                {
                    "q": "In RSA with p = 3, q = 11, e = 3, and d = 7, what is the ciphertext c when encrypting message m = 8?",
                    "opts": [
                        "8",
                        "17",
                        "24",
                        "31"
                    ],
                    "ans": 1,
                    "exp": "c = m^e mod n = 8^3 mod 33 = 512 mod 33 = 17 (§8.2.2)."
                }
            ]
        }
    ]
}
