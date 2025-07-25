import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import DebugInfo from './components/DebugInfo';
import ApiTest from './components/ApiTest';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Focus from './pages/Focus';
import Mood from './pages/Mood';
import Learning from './pages/Learning';
import Organization from './pages/Organization';
import Login from './pages/Login';
import Register from './pages/Register';
import ChatPage from './pages/Chat';
import AIChat from './components/AIChat';
import { AuthProvider, useAuth } from './context/AuthContext';
import './App.css';

const RequireAuth: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

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
      <AuthProvider>
        <div className={`app ${isDarkMode ? 'dark' : ''}`}>
          <Header
            onMenuClick={() => setSidebarOpen(!sidebarOpen)}
            onChatClick={() => setChatOpen(!chatOpen)}
            isDarkMode={isDarkMode}
            onDarkModeToggle={() => setIsDarkMode(!isDarkMode)}
          />

          <div className="app-body">
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            <main className="main-content">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route
                  path="/"
                  element={
                    <RequireAuth>
                      <Dashboard />
                    </RequireAuth>
                  }
                />
                <Route
                  path="/tasks"
                  element={
                    <RequireAuth>
                      <Tasks />
                    </RequireAuth>
                  }
                />
                <Route
                  path="/focus"
                  element={
                    <RequireAuth>
                      <Focus />
                    </RequireAuth>
                  }
                />
                <Route
                  path="/mood"
                  element={
                    <RequireAuth>
                      <Mood />
                    </RequireAuth>
                  }
                />
                <Route
                  path="/learning"
                  element={
                    <RequireAuth>
                      <Learning />
                    </RequireAuth>
                  }
                />
                <Route
                  path="/organization"
                  element={
                    <RequireAuth>
                      <Organization />
                    </RequireAuth>
                  }
                />
                <Route
                  path="/chat"
                  element={
                    <RequireAuth>
                      <ChatPage />
                    </RequireAuth>
                  }
                />
              </Routes>
            </main>
          </div>

          <AIChat isOpen={chatOpen} onClose={() => setChatOpen(false)} />
          <DebugInfo />
          <ApiTest />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
