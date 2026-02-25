import React, { useState } from "react";
import "./App.css";
import ChatWidget from "./ChatWidget";
import FullChat from "./FullChat";
import Dashboard from "./Dashboard";

function App() {
  const [showFullChat, setShowFullChat] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);

  return (
    <div className="home-container">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-content">
          <div className="logo-section">
            <img src="/logo_a.png" alt="AlphaWave Logo" className="logo-img" />
            <h1>AlphaWave</h1>
          </div>
          <div className="nav-links">
            <button className="nav-link-btn" onClick={() => setShowDashboard(true)}>Dashboard</button>
            <button className="primary-btn" onClick={() => setShowFullChat(true)}>Launch Assistant</button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="hero">
        <div className="hero-content">
          <span className="badge">Next Generation Intelligence</span>
          <h2>Empowering Your Business with AI</h2>
          <p>
            Secure, private, and production-ready RAG solutions tailored for your enterprise needs.
            Experience the power of AlphaWave AI.
          </p>
          <div className="hero-actions">
            <button className="cta-btn">Get Started</button>
            <button className="secondary-btn">Request Demo</button>
          </div>
        </div>
      </main>

      {/* Conditional Full UI */}
      {showFullChat && <FullChat onClose={() => setShowFullChat(false)} />}

      {/* Dashboard Overlay */}
      {showDashboard && <Dashboard onClose={() => setShowDashboard(false)} />}

      {/* Floating Chat Widget (Always available unless full UI is open) */}
      {!showFullChat && <ChatWidget onExpand={() => setShowFullChat(true)} />}
    </div>
  );
}

export default App;