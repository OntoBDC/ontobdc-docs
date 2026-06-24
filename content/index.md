---
hide:
  - toc
---

<style>
.main-wrapper {
  display: flex;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  align-items: stretch;
}

@media (max-width: 768px) {
  .main-wrapper {
    flex-direction: column;
  }
  .side-card {
    display: none !important;
  }
}

.hero-container {
  flex: 2;
  padding: 3rem 1.5rem;
  background: var(--md-default-bg-color);
  border-radius: 1.25rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid rgba(0, 188, 212, 0.2);
  text-align: center;
}

.side-card {
  flex: 1;
  padding: 2rem;
  background: var(--md-default-bg-color);
  border-radius: 1.25rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid rgba(0, 188, 212, 0.2);
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: left;
}

.feature-icon {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  color: #00bcd4;
}

.feature-icon svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
}

.feature-content h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--md-default-fg-color);
  letter-spacing: 0.5px;
}

.feature-content p {
  margin: 0;
  font-size: 1rem;
  color: var(--md-default-fg-color--light);
  line-height: 1.4;
}

.full-width-card {
  width: 100%;
  padding: 3rem 1.5rem;
  background: var(--md-default-bg-color);
  border-radius: 1.25rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid rgba(0, 188, 212, 0.2);
  text-align: center;
  margin-top: 0.5rem; /* Reduced from 1.5rem to pull it up */
}

html[data-md-color-scheme="slate"] .hero-container,
html[data-md-color-scheme="slate"] .side-card,
html[data-md-color-scheme="slate"] .full-width-card {
  background: var(--md-default-bg-color);
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  border: 1px solid rgba(0, 188, 212, 0.4);
}

.hero-container h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--md-default-fg-color);
}

.hero-container h1 span.bd-accent {
  color: #00bcd4;
}

.hero-container p.subtitle {
  font-size: 1.2rem;
  color: var(--md-default-fg-color--light);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.side-card h3 {
  margin-top: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--md-default-fg-color);
}

.side-card p {
  color: var(--md-default-fg-color--light);
  font-size: 1rem;
  line-height: 1.5;
}

.btn-primary {
  display: inline-block;
  background-color: #00bcd4;
  color: #fff !important;
  text-decoration: none;
  padding: 0.8rem 1.5rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 1rem;
  transition: filter 0.2s, transform 0.2s;
  margin-top: 1rem;
  white-space: nowrap; /* Prevent text wrapping inside buttons */
}

.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
}

.full-width-card h2 {
  margin-top: 0;
  font-size: 2rem;
  font-weight: 800;
  color: var(--md-default-fg-color);
  margin-bottom: 1rem;
}

.full-width-card p {
  color: var(--md-default-fg-color--light);
  font-size: 1.2rem;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
}

.mini-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-top: 3rem;
  text-align: left;
}

.mini-card {
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: var(--md-default-bg-color);
  border: 1px solid rgba(0, 188, 212, 0.15);
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  transition: border-color 0.3s ease, transform 0.3s ease;
  display: flex;
  flex-direction: column;
  container-type: inline-size;
}

.mini-card:hover {
  border-color: #00bcd4;
  transform: translateY(-3px);
}

.mini-card h3 {
  margin-top: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--md-default-fg-color);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mini-card p {
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--md-default-fg-color--light);
  margin: 0;
}

.mini-card .btn-primary {
  align-self: center;
  width: auto;
  min-width: 140px;
  margin: 2rem auto 0 auto;
}
</style>

<div class="main-wrapper" style="flex-wrap: wrap;">
  <div class="hero-container">
    <a href="https://youtu.be/98zhTFi2I14" target="_blank" rel="noopener noreferrer" style="display: block; width: 100%; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: transform 0.2s;">
      <img src="https://img.youtube.com/vi/98zhTFi2I14/maxresdefault.jpg" alt="OntoBDC Video" style="width: 100%; height: auto; display: block;">
    </a>
  </div>

  <div class="side-card">
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 1.5rem; padding-bottom: 1.5rem;">
      <img src="assets/images/ontobdc-logo.png" data-i18n="site.logo_alt" data-i18n-attr="alt" alt="OntoBDC Logo" style="max-height: 64px; margin-bottom: 0.75rem;">
      <h2 style="margin: 0; font-size: 1.5rem;">Onto<span class="bd-accent" data-i18n="hero.title_accent">BDC</span></h2>
      <p style="font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.4;">
        <strong style="color: var(--md-default-fg-color);" data-i18n="hero.strong_subtitle">Ontology-Based Datasets & Containers</strong><br /><br />
        <span style="display: block; margin-top: 0.25rem; color: var(--md-default-fg-color--light);" data-i18n="hero.soft_subtitle">A unified standard to define, distribute, and orchestrate open data datasets through code.</span>
      </p>
    </div>
  </div>

  <div class="full-width-card">
    <h2 data-i18n="capabilities.title">Do everything with capabilities</h2>
    <p data-i18n="capabilities.description">These are small executable scripts embedded directly within the "digital briefcase" (the .obdc pointer) that teach any computer or system on the network how to read, transform, or validate that specific dataset.</p>

    <div class="mini-cards-grid">
      <div class="mini-card">
        <h3 data-i18n="capabilities.card1_title">🛡️ Data Sovereignty</h3>
        <p data-i18n="capabilities.card1_desc">Validate engineering projects locally (Edge Execution). Eliminate costly proprietary licenses and orchestrate sensitive data without transferring it to third-party infrastructures.</p>
      </div>
      <div class="mini-card">
        <h3 data-i18n="capabilities.card2_title">⏳ Future-Proof</h3>
        <p data-i18n="capabilities.card2_desc">Project data must last decades. OntoBDC ensures your data and inspection tools can be reproduced identically 20 years from now, immunizing your organization against software obsolescence.</p>
      </div>
      <div class="mini-card">
        <h3 data-i18n="capabilities.card3_title">🤖 AI-Ready</h3>
        <p data-i18n="capabilities.card3_desc">Using the container manifest as a structured guide, LLMs can autonomously trigger capabilities with less hallucinations, enabling advanced auditing without sending IP to Big Tech clouds.</p>
      </div>
    </div>
  </div>

  <div class="full-width-card" style="margin-top: 1.5rem; background: var(--md-code-bg-color); border: none;">
    <h2 data-i18n="ownership.title">Your data is your data</h2>
    <p data-i18n="ownership.description">OntoBDC embraces true open data principles. You retain full ownership, control, and accessibility of your engineering data without being tied to proprietary formats or vendor lock-in.</p>

    <div class="mini-cards-grid">
      <div class="mini-card">
        <h3 data-i18n="ownership.card1_title">🎯 Single Source of Truth</h3>
        <p data-i18n="ownership.card1_desc">You define the ultimate reference. Consolidate your engineering data into a single, reliable semantic model that governs all project rules and information.</p>
      </div>
      <div class="mini-card">
        <h3 data-i18n="ownership.card2_title">🔄 Seamless Synchronization</h3>
        <p data-i18n="ownership.card2_desc">Keep data flowing perfectly. Automatically synchronize information across multiple .obdc containers and integrate effortlessly with third-party systems.</p>
      </div>
      <div class="mini-card">
        <h3 data-i18n="ownership.card3_title">🔌 Offline Local Execution</h3>
        <p data-i18n="ownership.card3_desc">Work without limits. Process, validate, and query your complex data entirely offline, right on your machine, with zero dependency on internet connections.</p>
      </div>
    </div>
  </div>

  <div class="full-width-card" style="margin-top: 1.5rem;">
    <h2 id="get_started" data-i18n="get_started.title">Get Started!</h2>
    <p data-i18n="get_started.description">Choose the best way to experience and implement OntoBDC for your workflow.</p>

    <div class="mini-cards-grid">
      <div class="mini-card">
        <h3 data-i18n="get_started.card1_title">🌐 Online Demo</h3>
        <p data-i18n="get_started.card1_desc">Try OntoBDC directly in your browser without installing anything. Explore capabilities and see it in action.</p>
        <a href="#" class="btn-primary" style="margin-top: 1.2rem; padding: 0.6rem 1.2rem; font-size: 0.9rem; text-align: center; align-self: center;" data-i18n="get_started.card1_btn">Try Online</a>
      </div>
      <div class="mini-card">
        <h3 data-i18n="get_started.card2_title">💻 Local CLI</h3>
        <p data-i18n="get_started.card2_desc">Install via pip and initialize your first digital briefcase in seconds directly from your terminal.</p>
        <div style="background: #1a1b26; padding: 0.75rem; border-radius: 0.5rem; font-family: monospace; font-size: clamp(8px, 4.5cqi, 14px); color: #a9b1d6; margin-top: 1.0rem; border: 1px solid rgba(255,255,255,0.1); text-align: left; line-height: 1.4; white-space: nowrap; overflow: hidden;">
          <span style="color: #bb9af7;">&gt;_ pip install</span> ontobdc<br>
          <span style="color: #7dcfff;">&gt;_ ontobdc</span> --version<br>
          <span style="color: #7dcfff;">&gt;_ ontobdc</span> init
        </div>
        <a href="#" class="btn-primary" style="margin-top: 1.2rem; padding: 0.6rem 1.2rem; font-size: 0.9rem; text-align: center; align-self: center;" data-i18n="get_started.card2_btn">Documentation</a>
      </div>
      <div class="mini-card">
        <h3 data-i18n="get_started.card3_title">☁️ Google Colab</h3>
        <p data-i18n="get_started.card3_desc">Run OntoBDC in the cloud using Google Colab. Mount your Google Drive to seamlessly process and orchestrate your remote engineering data.</p>
        <a href="#" class="btn-primary" style="margin-top: 1.2rem; padding: 0.6rem 1.2rem; font-size: 0.9rem; text-align: center; align-self: center;" data-i18n="get_started.card3_btn">Google Colab</a>
      </div>
    </div>
  </div>
</div>