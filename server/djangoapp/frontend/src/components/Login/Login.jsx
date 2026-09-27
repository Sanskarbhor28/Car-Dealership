import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username || !password) {
      setError('Please enter both username and password.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userName: username, password }),
      });

      const data = await response.json();

      if (response.ok && data.status === 'Authenticated') {
        if (onLoginSuccess) {
          onLoginSuccess(data.userName);
        }
        navigate('/');
      } else {
        setError(data.error || 'Invalid credentials. Please check your username and password.');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-5 col-lg-4">
          <div className="card shadow-lg border-0 rounded-3">
            <div className="card-header bg-dark text-white text-center py-3">
              <h3 className="card-title fw-bold mb-0">Dealer Portal Login</h3>
            </div>
            <div className="card-body p-4">
              {error && (
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="login-username" className="form-label fw-bold">
                    Username
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="login-username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter your username"
                    required
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="login-password" className="form-label fw-bold">
                    Password
                  </label>
                  <input
                    type="password"
                    className="form-control"
                    id="login-password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    required
                  />
                </div>

                <div className="d-grid mb-3">
                  <button
                    type="submit"
                    className="btn btn-dark btn-lg fw-bold"
                    disabled={loading}
                    id="login-submit-btn"
                  >
                    {loading ? 'Authenticating...' : 'Sign In'}
                  </button>
                </div>

                <div className="text-center">
                  <span className="text-muted">Don't have an account? </span>
                  <Link to="/register" className="fw-bold text-decoration-none">
                    Register Now
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
