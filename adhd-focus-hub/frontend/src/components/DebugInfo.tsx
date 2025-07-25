import React from 'react';

const DebugInfo: React.FC = () => {
  return (
    <div style={{ 
      position: 'fixed', 
      top: '10px', 
      right: '10px', 
      background: '#f0f0f0', 
      padding: '10px', 
      border: '1px solid #ccc',
      fontSize: '12px',
      zIndex: 9999
    }}>
      <div><strong>Debug Info:</strong></div>
      <div>API URL: {process.env.REACT_APP_API_URL || 'undefined'}</div>
      <div>Environment: {process.env.REACT_APP_ENV || 'undefined'}</div>
      <div>Node Env: {process.env.NODE_ENV}</div>
    </div>
  );
};

export default DebugInfo;
