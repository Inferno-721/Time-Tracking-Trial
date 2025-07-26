import React from "react";
import "./Download.css";

const Download = () => (
  <div className="download-container">
    <div className="download-card">
      <div className="success-icon">✅</div>
      <h1>Account Created Successfully!</h1>
      <p>Your account has been activated. Download the time tracking app to get started.</p>
      
      <div className="download-section">
        <h2>Download Time Tracker</h2>
        <div className="download-buttons">
          <a href="/downloads/local-app.exe" download className="download-btn windows">
            <span className="os-icon">��</span>
            <div>
              <span className="os-name">Windows</span>
              <span className="file-size">15.2 MB</span>
            </div>
          </a>
          
          <a href="/downloads/local-app.dmg" download className="download-btn mac">
            <span className="os-icon">��</span>
            <div>
              <span className="os-name">macOS</span>
              <span className="file-size">18.7 MB</span>
            </div>
          </a>
          
          <a href="/downloads/local-app.AppImage" download className="download-btn linux">
            <span className="os-icon">��</span>
            <div>
              <span className="os-name">Linux</span>
              <span className="file-size">12.8 MB</span>
            </div>
          </a>
        </div>
      </div>
      
      <div className="instructions">
        <h3>Getting Started</h3>
        <ol>
          <li>Download the app for your operating system</li>
          <li>Install and run the application</li>
          <li>Log in with your email and password</li>
          <li>Start tracking your time!</li>
        </ol>
      </div>
    </div>
  </div>
);

export default Download;