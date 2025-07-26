import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createEmployee } from "../api";
import "./Onboard.css";

const Onboard = () => {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await createEmployee({ email, name, password });
      setMessage("Account created successfully! Check your email for activation.");
      setTimeout(() => navigate("/download"), 2000);
    } catch (err) {
      setMessage("Error creating account. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="onboard-container">
      <div className="onboard-card">
        <div className="logo-section">
          <div className="logo">⏰</div>
          <h1>Time Tracker</h1>
          <p>Employee Onboarding</p>
        </div>

        <form onSubmit={handleSubmit} className="onboard-form">
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              type="text"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
            />
          </div>

          <button 
            type="submit" 
            className={`submit-btn ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? "Creating Account..." : "Create Account"}
          </button>
        </form>

        {message && (
          <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}

        <div className="features">
          <div className="feature">
            <span className="feature-icon">��</span>
            <span>Track your time</span>
          </div>
          <div className="feature">
            <span className="feature-icon">��</span>
            <span>Secure & private</span>
          </div>
          <div className="feature">
            <span className="feature-icon">��</span>
            <span>Easy to use</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Onboard;