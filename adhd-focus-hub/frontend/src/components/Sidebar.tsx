import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  CheckSquare, 
  Focus, 
  Heart, 
  BookOpen, 
  Folder,
  X 
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/tasks', icon: CheckSquare, label: 'Task Planning' },
    { path: '/focus', icon: Focus, label: 'Focus Sessions' },
    { path: '/mood', icon: Heart, label: 'Mood Tracking' },
    { path: '/learning', icon: BookOpen, label: 'Learning Hub' },
    { path: '/organization', icon: Folder, label: 'Organization' },
  ];

  return (
    <>
      {isOpen && (
        <div 
          className={`sidebar-overlay ${isOpen ? 'visible' : ''}`}
          onClick={onClose}
        />
      )}
      
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <button 
            className="close-btn md:hidden"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <X size={20} />
          </button>
        </div>
        
        <nav>
          <ul className="nav-menu">
            {navItems.map(({ path, icon: Icon, label }) => (
              <li key={path} className="nav-item">
                <Link
                  to={path}
                  className={`nav-link ${location.pathname === path ? 'active' : ''}`}
                  onClick={onClose}
                >
                  <Icon size={20} />
                  <span>{label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        
        <div className="sidebar-footer">
          <div className="card">
            <h4>💡 ADHD Tip</h4>
            <p>Remember: Progress over perfection! Every small step counts.</p>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
