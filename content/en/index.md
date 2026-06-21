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
    <img src="assets/images/ontobdc-logo.png" alt="OntoBDC Logo" style="max-height: 120px; margin-bottom: 1rem;">
    <h1>Onto<span class="bd-accent">BDC</span></h1>
    <p class="subtitle">
      <strong style="color: var(--md-default-fg-color);">Ontology-Based Datasets & Containers</strong><br />
      <span style="display: block; margin-top: 0.5rem;">A unified standard to define, distribute, and orchestrate open data datasets through code.</span>
    </p>
  </div>
  
  <div class="side-card">
    <div class="feature-item">
      <div class="feature-icon">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
      </div>
      <div class="feature-content">
        <h3>OPEN SOURCE</h3>
        <p>Built for the community</p>
      </div>
    </div>
    
    <div class="feature-item">
      <div class="feature-icon">
        <svg viewBox="0 0 24 24"><path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/></svg>
      </div>
      <div class="feature-content">
        <h3>IT'S FREE</h3>
        <p>No proprietary licenses</p>
      </div>
    </div>

    <div class="feature-item">
      <div class="feature-icon">
        <svg viewBox="0 0 24 24"><path d="M9 21c0 .5.4 1 1 1h4c.6 0 1-.5 1-1v-1H9v1zm3-19C8.1 2 5 5.1 5 9c0 2.4 1.2 4.5 3 5.7V17c0 .5.4 1 1 1h6c.6 0 1-.5 1-1v-2.3c1.8-1.2 3-3.3 3-5.7 0-3.9-3.1-7-7-7z"/></svg>
      </div>
      <div class="feature-content">
        <h3>EMPOWER</h3>
        <p>Your engineering teams</p>
      </div>
    </div>
  </div>

  <div class="full-width-card">
    <h2>Do everything with capabilities</h2>
    <p>These are small executable scripts embedded directly within the "digital briefcase" (the .obdc pointer) that teach any computer or system on the network how to read, transform, or validate that specific dataset.</p>

    <div class="mini-cards-grid">
      <div class="mini-card">
        <h3>🛡️ Data Sovereignty</h3>
        <p>Validate engineering projects locally (Edge Execution). Eliminate costly proprietary licenses and orchestrate sensitive data without transferring it to third-party infrastructures.</p>
      </div>
      <div class="mini-card">
        <h3>⏳ Future-Proof</h3>
        <p>Project data must last decades. OntoBDC ensures your data and inspection tools can be reproduced identically 20 years from now, immunizing your organization against software obsolescence.</p>
      </div>
      <div class="mini-card">
        <h3>🤖 AI-Ready</h3>
        <p>Using the container manifest as a structured guide, LLMs can autonomously trigger capabilities with less hallucinations, enabling advanced auditing without sending IP to Big Tech clouds.</p>
      </div>
      <!--
      <div class="mini-card">
        <h3>🔗 Complex Workflows</h3>
        <p>Chain capabilities via built-in DAGs and Finite State Machines. Manage decentralized workflows directly within the data itself, bypassing centralized cloud orchestrators.</p>
      </div>
      -->
    </div>
  </div>

  <div class="full-width-card" style="margin-top: 1.5rem; background: var(--md-code-bg-color); border: none;">
    <h2>Your data is your data</h2>
    <p>OntoBDC embraces true open data principles. You retain full ownership, control, and accessibility of your engineering data without being tied to proprietary formats or vendor lock-in.</p>

    <div class="mini-cards-grid">
      <div class="mini-card">
        <h3>🎯 Single Source of Truth</h3>
        <p>You define the ultimate reference. Consolidate your engineering data into a single, reliable semantic model that governs all project rules and information.</p>
      </div>
      <div class="mini-card">
        <h3>🔄 Seamless Synchronization</h3>
        <p>Keep data flowing perfectly. Automatically synchronize information across multiple .obdc containers and integrate effortlessly with third-party systems.</p>
      </div>
      <div class="mini-card">
        <h3>🔌 Offline Local Execution</h3>
        <p>Work without limits. Process, validate, and query your complex data entirely offline, right on your machine, with zero dependency on internet connections.</p>
      </div>
    </div>
  </div>

  <div class="full-width-card" style="margin-top: 1.5rem;">
    <h2 id="get_started">Get Started!</h2>
    <p>Choose the best way to experience and implement OntoBDC for your workflow.</p>

    <div class="mini-cards-grid">
      <div class="mini-card">
        <h3>🌐 Online Demo</h3>
        <p>Try OntoBDC directly in your browser without installing anything. Explore capabilities and see it in action.</p>
        <a href="#" class="btn-primary" style="margin-top: 1.2rem; padding: 0.6rem 1.2rem; font-size: 0.9rem; text-align: center; align-self: center;">Try Online</a>
      </div>
      <div class="mini-card">
        <h3>💻 Local CLI</h3>
        <p>Install via pip and initialize your first digital briefcase in seconds directly from your terminal.</p>
        <div style="background: #1a1b26; padding: 0.75rem; border-radius: 0.5rem; font-family: monospace; font-size: clamp(8px, 4.5cqi, 14px); color: #a9b1d6; margin-top: 1.0rem; border: 1px solid rgba(255,255,255,0.1); text-align: left; line-height: 1.4; white-space: nowrap; overflow: hidden;">
          <span style="color: #bb9af7;">>_ pip install</span> ontobdc<br>
          <span style="color: #7dcfff;">>_ ontobdc</span> --version<br>
          <span style="color: #7dcfff;">>_ ontobdc</span> init
        </div>
        <a href="#" class="btn-primary" style="margin-top: 1.2rem; padding: 0.6rem 1.2rem; font-size: 0.9rem; text-align: center; align-self: center;">Documentation</a>
      </div>
      <div class="mini-card">
        <h3>☁️ Google Colab</h3>
        <p>Run OntoBDC in the cloud using Google Colab. Mount your Google Drive to seamlessly process and orchestrate your remote engineering data.</p>
        <a href="#" class="btn-primary" style="margin-top: 1.2rem; padding: 0.6rem 1.2rem; font-size: 0.9rem; text-align: center; align-self: center;">Google Colab</a>
      </div>
    </div>
  </div>
</div>