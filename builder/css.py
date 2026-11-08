"""CSS Styles for the Interactive Networking Textbook (100% self-contained, no CDN)"""

CSS_STYLES = """
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-card: #ffffff;
  --bg-elevated: #f1f5f9;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --border: #e2e8f0;
  --border-light: #f1f5f9;
  
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-light: #eff6ff;
  --primary-text: #1d4ed8;
  
  --accent: #10b981;
  --accent-light: #ecfdf5;
  --accent-text: #047857;
  
  --warning: #f59e0b;
  --warning-light: #fffbeb;
  --warning-text: #b45309;
  
  --danger: #ef4444;
  --danger-light: #fef2f2;
  --danger-text: #b91c1c;
  
  --purple: #8b5cf6;
  --purple-light: #f5f3ff;
  --purple-text: #6d28d9;

  /* Layer colors */
  --layer-app: #8b5cf6;
  --layer-trans: #2563eb;
  --layer-net: #10b981;
  --layer-link: #f59e0b;
  --layer-phy: #ef4444;

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --radius: 10px;
}

.dark {
  --bg-primary: #0b1120;
  --bg-secondary: #0f172a;
  --bg-card: #1e293b;
  --bg-elevated: #334155;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border: #334155;
  --border-light: #1e293b;
  
  --primary: #3b82f6;
  --primary-hover: #60a5fa;
  --primary-light: #1e3a8a33;
  --primary-text: #93c5fd;
  
  --accent: #10b981;
  --accent-light: #064e3b33;
  --accent-text: #6ee7b7;
  
  --warning: #f59e0b;
  --warning-light: #78350f33;
  --warning-text: #fcd34d;
  
  --danger: #ef4444;
  --danger-light: #7f1d1d33;
  --danger-text: #fca5a5;
  
  --purple: #a855f7;
  --purple-light: #581c8733;
  --purple-text: #d8b4fe;

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  -webkit-font-smoothing: antialiased;
}

/* Math Typography & Formulas (Clean HTML & Offline) */
.math-display {
  display: block;
  text-align: center;
  font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", "Times New Roman", Georgia, serif;
  font-size: 1.25rem;
  letter-spacing: 0.02em;
  padding: 0.85rem 1.25rem;
  margin: 1rem 0;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow-x: auto;
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
}

.math-inline {
  font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", "Times New Roman", Georgia, serif;
  font-size: 1.05rem;
  padding: 0.1rem 0.25rem;
  background: var(--bg-elevated);
  border-radius: 4px;
  display: inline-block;
  vertical-align: baseline;
  line-height: 1.2;
}

.math-var {
  font-style: italic;
  padding: 0 1px;
}

.math-frac {
  display: inline-flex;
  flex-direction: column;
  vertical-align: middle;
  text-align: center;
  padding: 0 0.35rem;
  line-height: 1.1;
  font-size: 0.95em;
}

.math-num {
  border-bottom: 1.5px solid currentColor;
  padding-bottom: 2px;
}

.math-denom {
  padding-top: 2px;
}

.math-sub {
  font-size: 0.75em;
  vertical-align: sub;
  font-style: normal;
}

.math-sup {
  font-size: 0.75em;
  vertical-align: super;
  font-style: normal;
}

/* App Header */
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background-color: var(--bg-primary);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(8px);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
}

.logo-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.logo-badge {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: white;
  font-weight: 800;
  font-size: 0.85rem;
  padding: 0.4rem 0.65rem;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.logo-text h1 {
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.2;
}

.logo-text p {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.header-center {
  flex: 1;
  max-width: 480px;
  margin: 0 1.5rem;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 2.25rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.875rem;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: var(--primary);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.search-icon {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  fill: var(--text-muted);
  pointer-events: none;
}

/* Search Results Dropdown & Lesson Highlights */
.search-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25);
  max-height: 440px;
  overflow-y: auto;
  z-index: 1000;
  display: none;
}

.search-dropdown-header {
  padding: 0.65rem 1rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: background 0.15s ease;
}

.search-item:hover, .search-item.selected {
  background: var(--bg-elevated);
}

.search-item-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.search-item-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  background: rgba(37, 99, 235, 0.15);
  color: var(--primary);
}

.search-item-snippet {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.45;
}

.search-item-snippet mark {
  background: rgba(234, 179, 8, 0.35);
  color: inherit;
  font-weight: 800;
  padding: 0.05rem 0.25rem;
  border-radius: 3px;
}

.search-highlight {
  font-weight: 800 !important;
  color: #000000 !important;
  background: #fde047 !important;
  padding: 0.08em 0.3em;
  border-radius: 3px;
  box-shadow: 0 0 5px rgba(250, 204, 21, 0.7);
  display: inline;
}

.search-empty {
  padding: 1.25rem 1rem;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.6;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.nav-btn {
  padding: 0.45rem 0.8rem;
  font-size: 0.825rem;
  font-weight: 500;
  border-radius: 6px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.nav-btn:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.nav-btn.active {
  background: var(--primary-light);
  color: var(--primary-text);
  border-color: var(--primary);
  font-weight: 600;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  color: var(--text-primary);
  border-color: var(--primary);
}

/* Main Container Layout */
.app-container {
  display: flex;
  flex: 1;
  position: relative;
}

/* Sidebar */
.sidebar {
  width: 320px;
  background-color: var(--bg-primary);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  position: sticky;
  top: 64px;
  height: calc(100vh - 64px);
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  transition: transform 0.25s ease;
}

.sidebar-title {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  padding: 0.5rem 0.75rem 0.25rem;
}

.ch-accordion {
  border: 1px solid var(--border-light);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 0.35rem;
  background: var(--bg-primary);
}

.ch-header {
  padding: 0.65rem 0.75rem;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  font-size: 0.85rem;
  font-weight: 600;
  transition: background 0.15s ease;
}

.ch-header:hover {
  background: var(--bg-elevated);
}

.ch-header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.ch-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  color: white;
}

.sec-list {
  display: none;
  padding: 0.25rem 0;
  background: var(--bg-primary);
}

.ch-accordion.open .sec-list {
  display: block;
}

.ch-accordion.open .arrow-icon {
  transform: rotate(90deg);
}

.sec-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.45rem 0.85rem 0.45rem 1.85rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-decoration: none;
  cursor: pointer;
  border-left: 2px solid transparent;
  transition: all 0.15s ease;
}

.sec-item:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.sec-item.active {
  background: var(--primary-light);
  color: var(--primary-text);
  border-left-color: var(--primary);
  font-weight: 600;
}

.check-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1px solid var(--text-muted);
}

.sec-item.completed .check-dot {
  background-color: var(--accent);
  border-color: var(--accent);
}

/* Main Content Pane */
.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  max-width: 1060px;
  margin: 0 auto;
}

.content-section {
  display: none;
}

.content-section.active {
  display: block;
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.sec-heading {
  font-size: 1.85rem;
  font-weight: 800;
  line-height: 1.25;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.sec-subheading {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  font-weight: 400;
}

/* Callout Boxes */
.callout {
  padding: 1.1rem 1.35rem;
  border-radius: 10px;
  margin: 1.35rem 0;
  border-left: 5px solid;
  font-size: 0.94rem;
  line-height: 1.65;
  box-shadow: var(--shadow-sm);
}

.callout-header {
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 0.45rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.callout-def {
  background: var(--primary-light);
  border-color: var(--primary);
  color: var(--text-primary);
}
.callout-def .callout-header { color: var(--primary-text); }

.callout-insight {
  background: var(--warning-light);
  border-color: var(--warning);
  color: var(--text-primary);
}
.callout-insight .callout-header { color: var(--warning-text); }

.callout-mistake {
  background: var(--danger-light);
  border-color: var(--danger);
  color: var(--text-primary);
}
.callout-mistake .callout-header { color: var(--danger-text); }

.callout-formula {
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--text-primary);
}
.callout-formula .callout-header { color: var(--accent-text); }

.callout-lecture {
  background: var(--purple-light);
  border-color: var(--purple);
  color: var(--text-primary);
}
.callout-lecture .callout-header { color: var(--purple-text); }

.callout-exam {
  background: #fff1f2;
  border-color: #e11d48;
  color: #881337;
}
.dark .callout-exam {
  background: #4c051933;
  color: #fecdd3;
  border-color: #fb7185;
}
.callout-exam .callout-header { color: #e11d48; }

/* SVG Figures & Interactive Canvases */
.svg-figure {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.5rem;
  margin: 1.85rem 0;
  box-shadow: var(--shadow-md);
  text-align: center;
  position: relative;
}

.svg-container {
  width: 100%;
  max-width: 860px;
  margin: 0 auto;
  overflow-x: auto;
}

.svg-container svg {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  height: auto;
}

.figure-caption {
  margin-top: 1rem;
  font-size: 0.88rem;
  color: var(--text-muted);
  font-weight: 600;
}

.figure-notice {
  font-size: 0.825rem;
  color: var(--primary-text);
  margin-top: 0.35rem;
  font-weight: 500;
}

.fig-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.fig-step-badge {
  font-size: 0.8rem;
  padding: 0.25rem 0.65rem;
  border-radius: 20px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  font-weight: 600;
}

/* Interactive Components */
.interactive-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.65rem;
  margin: 1.85rem 0;
  box-shadow: var(--shadow-md);
}

.interactive-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.95rem;
  margin-bottom: 1.25rem;
}

.interactive-title {
  font-size: 1.15rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.interactive-badge {
  font-size: 0.72rem;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  background: var(--accent-light);
  color: var(--accent-text);
  font-weight: 700;
}

/* Grid System */
.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
}

.form-group {
  margin-bottom: 0.85rem;
}

.form-label {
  display: block;
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.35rem;
}

.form-input, .form-select {
  width: 100%;
  padding: 0.55rem 0.85rem;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.9rem;
  outline: none;
  transition: all 0.15s ease;
}

.form-input:focus, .form-select:focus {
  border-color: var(--primary);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.6rem 1.35rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s ease, transform 0.1s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--bg-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border);
  padding: 0.6rem 1.35rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
}

.btn-secondary:hover {
  background: var(--border);
}

/* Calculation Result Box */
.calc-result-box {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.15rem;
  margin-top: 1.15rem;
}

.calc-step {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.88rem;
  padding: 0.45rem 0;
  border-bottom: 1px dashed var(--border);
  line-height: 1.5;
}

.calc-step:last-child {
  border-bottom: none;
  font-weight: 700;
  color: var(--primary-text);
  font-size: 0.98rem;
  padding-top: 0.6rem;
}

/* Simulator Viewport */
.sim-viewport {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.35rem;
  min-height: 190px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.sim-controls {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-top: 1.15rem;
  flex-wrap: wrap;
}

/* Flashcards */
.flip-card {
  perspective: 1000px;
  width: 100%;
  max-width: 560px;
  height: 290px;
  margin: 1.5rem auto;
  cursor: pointer;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}

.flip-card.flipped .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.85rem;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-md);
  background: var(--bg-card);
}

.flip-card-back {
  transform: rotateY(180deg);
  background: var(--primary-light);
  color: var(--text-primary);
  border-color: var(--primary);
}

/* Quizzes */
.quiz-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: var(--shadow-sm);
}

.quiz-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.quiz-question {
  font-weight: 600;
  font-size: 1.02rem;
  margin-bottom: 1.15rem;
  line-height: 1.55;
}

.quiz-options {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.quiz-opt {
  padding: 0.85rem 1.15rem;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.quiz-opt:hover {
  background: var(--bg-elevated);
  border-color: var(--primary);
}

.quiz-opt.selected {
  border-color: var(--primary);
  background: var(--primary-light);
  color: var(--primary-text);
  font-weight: 600;
}

.quiz-opt.correct {
  border-color: var(--accent);
  background: var(--accent-light);
  color: var(--accent-text);
  font-weight: 600;
}

.quiz-opt.wrong {
  border-color: var(--danger);
  background: var(--danger-light);
  color: var(--danger-text);
}

.quiz-feedback {
  margin-top: 1.15rem;
  padding: 0.85rem 1.15rem;
  border-radius: 8px;
  font-size: 0.9rem;
  display: none;
  line-height: 1.55;
}

.quiz-feedback.show {
  display: block;
}

/* HTTP Dissector */
.dissector-line {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: block;
}

.dissector-line:hover {
  background: rgba(37, 99, 235, 0.2);
}

.dissector-line.active {
  background: var(--primary);
  color: white;
  font-weight: 600;
}

/* Nav Footer */
.section-nav-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 3.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

/* Responsive */
@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    left: -320px;
    z-index: 40;
    box-shadow: var(--shadow-lg);
  }
  .sidebar.open {
    transform: translateX(320px);
  }
  .main-content {
    padding: 1.25rem;
  }
  .header-center {
    display: none;
  }
}

/* Print Styles */
@media print {
  .app-header, .sidebar, .section-nav-footer, .nav-btn, .icon-btn, .quiz-controls, .sim-controls {
    display: none !important;
  }
  .main-content {
    max-width: 100% !important;
    padding: 0 !important;
  }
  .content-section {
    display: block !important;
    page-break-after: always;
  }
  .callout, .interactive-card, .svg-figure {
    box-shadow: none !important;
    border: 1px solid #ccc !important;
  }
}
"""
