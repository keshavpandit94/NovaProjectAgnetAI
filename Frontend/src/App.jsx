// src/App.jsx
import React, { useState, useEffect } from 'react'; // ADDED useEffect
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import AuthForm from './components/AuthForm';
import Profile from './components/Profile';
import { LogIn, UserPlus } from 'lucide-react';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userToken, setUserToken] = useState(null);
  const [showAuthForm, setShowAuthForm] = useState(false);
  const [isLoginView, setIsLoginView] = useState(true);
  const [currentView, setCurrentView] = useState('chat');
  const [loadingInitial, setLoadingInitial] = useState(true); // NEW: State to prevent flashing

  // NEW: Check for token on initial load
  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      // NOTE: Ideally, you'd validate this token against your backend /auth/me endpoint.
      // For this setup, we assume a token in localStorage is valid until proven otherwise.
      setUserToken(token);
      setIsAuthenticated(true);
    }
    setLoadingInitial(false);
  }, []); // Runs once on mount

  const handleAuthSuccess = (authData) => {
    // Store token in localStorage upon successful auth
    localStorage.setItem('accessToken', authData.token);
    setUserToken(authData.token);
    setIsAuthenticated(true);
    setShowAuthForm(false);
    setCurrentView('chat');
  };

  const handleLogout = () => {
    // Remove token from localStorage
    localStorage.removeItem('accessToken');
    setUserToken(null);
    setIsAuthenticated(false);
    setCurrentView('chat');
  };

  const openAuthModal = (isLogin) => {
    setIsLoginView(isLogin);
    setShowAuthForm(true);
  };
  
  // Display a simple loading state while checking for token
  if (loadingInitial) {
    return <div className="flex justify-center items-center h-screen dark bg-slate-900 text-slate-100">Loading...</div>;
  }

  // --- Conditional Rendering ---

  if (showAuthForm) {
    return <AuthForm 
        isLoginView={isLoginView} 
        onAuthSuccess={handleAuthSuccess}
        onClose={() => setShowAuthForm(false)} 
        onToggleView={() => setIsLoginView(!isLoginView)}
    />;
  }

  if (isAuthenticated) {
    // Logged-In User: Full Layout
    return (
      <div className="dark h-screen flex overflow-hidden bg-slate-900 text-slate-100">
        <Sidebar 
          onLogout={handleLogout} 
          setCurrentView={setCurrentView} 
          currentView={currentView} // Pass current view to highlight active link
        />
        {currentView === 'chat' ? (
          <ChatInterface userToken={userToken} />
        ) : (
          <Profile userToken={userToken} onLogout={handleLogout} />
        )}
      </div>
    );
  }

  // Logged-Out/Anonymous User: Chat Interface with Auth buttons
  return (
    <div className="dark h-screen flex flex-col bg-slate-800 text-slate-100">
      <header className="flex justify-end p-4 bg-custom-card border-b border-slate-700 shadow-md">
        <div className="flex space-x-3">
          <button 
            onClick={() => openAuthModal(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-transparent text-slate-300 border border-slate-600 rounded-lg hover:bg-slate-700 transition duration-150"
          >
            <LogIn size={20} />
            <span>Login</span>
          </button>
          <button 
            onClick={() => openAuthModal(false)}
            className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-150"
          >
            <UserPlus size={20} />
            <span>Sign Up</span>
          </button>
        </div>
      </header>
      
      <ChatInterface userToken={null} />
    </div>
  );
}

export default App;