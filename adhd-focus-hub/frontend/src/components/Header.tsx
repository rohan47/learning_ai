import React from 'react';
import { Menu, MessageCircle, Sun, Moon } from 'lucide-react';

interface HeaderProps {
  onMenuClick: () => void;
  onChatClick: () => void;
  isDarkMode: boolean;
  onDarkModeToggle: () => void;
}

const Header: React.FC<HeaderProps> = ({ 
  onMenuClick, 
  onChatClick, 
  isDarkMode, 
  onDarkModeToggle 
}) => {
  return (
    <header className="header">
      <div className="header-left">
        <button 
          className="menu-button"
          onClick={onMenuClick}
          aria-label="Toggle menu"
        >
          <Menu size={24} />
        </button>
        
        <div className="logo">
          <span className="logo-icon">🧠</span>
          <h1 className="logo-text">ADHD Focus Hub</h1>
        </div>
      </div>
      
      <div className="header-right">
        <button
          className="icon-button"
          onClick={onDarkModeToggle}
          aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
        
        <button 
          className="chat-button"
          onClick={onChatClick}
          aria-label="Open AI chat"
        >
          <MessageCircle size={20} />
          <span>AI Assistant</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
