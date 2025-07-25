import React from 'react';
import AIChat from '../components/AIChat';

const ChatPage: React.FC = () => {
  return (
    <div className="page">
      <AIChat mode="page" />
    </div>
  );
};

export default ChatPage;
