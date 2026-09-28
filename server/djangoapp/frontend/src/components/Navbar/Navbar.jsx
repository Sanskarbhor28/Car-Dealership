import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = ({ currentUser, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await fetch('/djangoapp/logout', { method: 'GET' });
    } catch (e) {
      console.error('Logout request failed', e);
    }
    onLogout();
    navigate('/');
  };

  return (
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow-sm mb-4">
      <div class="container">
        <Link class="navbar-brand brand-title text-primary fs-3" to="/">
          🚗 Cars Dealership
        </Link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContent"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <Link class="nav-link fs-5" to="/">Home</Link>
            </li>
            <li class="nav-item">
              <a class="nav-link fs-5" href="/About.html">About Us</a>
            </li>
            <li class="nav-item">
              <a class="nav-link fs-5" href="/Contact.html">Contact Us</a>
            </li>
          </ul>

          <div class="d-flex align-items-center gap-3">
            {currentUser ? (
              <>
                <span class="navbar-text text-white fw-bold fs-6">
                  👤 Welcome, <span class="text-warning">{currentUser}</span>
                </span>
                <button
                  class="btn btn-outline-light btn-sm px-3"
                  onClick={handleLogout}
                  id="logout-btn"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" class="btn btn-outline-primary btn-sm px-3 text-white">
                  Login
                </Link>
                <Link to="/register" class="btn btn-primary btn-sm px-3">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
