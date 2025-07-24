import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Focus from './pages/Focus';
import Mood from './pages/Mood';
import Learning from './pages/Learning';
import Organization from './pages/Organization';
import AIChat from './components/AIChat';
import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Load user preferences
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('adhd-hub-dark-mode');
    if (savedDarkMode) {
      setIsDarkMode(JSON.parse(savedDarkMode));
    }
  }, []);

  // Apply dark mode
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('adhd-hub-dark-mode', JSON.stringify(isDarkMode));
  }, [isDarkMode]);

  return (
    <Router>
      <div className={`app ${isDarkMode ? 'dark' : ''}`}>
        <Header 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          onChatClick={() => setChatOpen(!chatOpen)}
          isDarkMode={isDarkMode}
          onDarkModeToggle={() => setIsDarkMode(!isDarkMode)}
        />
        
        <div className="app-body">
          <Sidebar 
            isOpen={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
          />
          
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/tasks" element={<Tasks />} />
              <Route path="/focus" element={<Focus />} />
              <Route path="/mood" element={<Mood />} />
              <Route path="/learning" element={<Learning />} />
              <Route path="/organization" element={<Organization />} />
            </Routes>
          </main>
        </div>
        
        <AIChat 
          isOpen={chatOpen}
          onClose={() => setChatOpen(false)}
        />
      </div>
    </Router>
  );
}

export default App;
