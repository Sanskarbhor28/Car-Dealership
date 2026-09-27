import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Dealers from './components/Dealers/Dealers';
import DealerDetails from './components/DealerDetails/DealerDetails';
import PostReview from './components/PostReview/PostReview';
import Login from './components/Login/Login';
import Register from './components/Register/Register';

function App() {
  const [currentUser, setCurrentUser] = useState('');

  useEffect(() => {
    // Check auth status on app load
    const checkAuthStatus = async () => {
      try {
        const res = await fetch('/api/login/', { method: 'GET' });
        if (res.ok) {
          const data = await res.json();
          if (data.status === 'Authenticated') {
            setCurrentUser(data.userName);
          }
        }
      } catch (err) {
        console.log('Auth check error:', err);
      }
    };

    checkAuthStatus();
  }, []);

  const handleLoginSuccess = (username) => {
    setCurrentUser(username);
  };

  const handleLogout = () => {
    setCurrentUser('');
  };

  return (
    <div className="App min-vh-100 d-flex flex-column">
      <Navbar currentUser={currentUser} onLogout={handleLogout} />
      <main className="flex-grow-1">
        <Routes>
          <Route path="/" element={<Dealers currentUser={currentUser} />} />
          <Route path="/dealers" element={<Dealers currentUser={currentUser} />} />
          <Route path="/dealer/:id" element={<DealerDetails currentUser={currentUser} />} />
          <Route path="/postreview/:id" element={<PostReview currentUser={currentUser} />} />
          <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
          <Route path="/register" element={<Register onLoginSuccess={handleLoginSuccess} />} />
        </Routes>
      </main>

      <footer className="bg-dark text-white text-center py-3 mt-5">
        <div className="container">
          <p className="mb-0 text-white-50">
            &copy; 2026 Cars Dealership Capstone Project | Built with Django & React
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
