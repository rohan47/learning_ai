import React, { useState } from 'react';
import { AuthService } from '../services';

const ApiTest: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testApiConnection = async () => {
    setLoading(true);
    setResult('Testing...');
    try {
      // Test if we can reach the backend
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/health`);
      if (response.ok) {
        const data = await response.json();
        setResult(`✅ Backend connection successful: ${JSON.stringify(data)}`);
      } else {
        setResult(`❌ Backend responded with status: ${response.status}`);
      }
    } catch (error) {
      setResult(`❌ Connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const testRegistration = async () => {
    setLoading(true);
    setResult('Testing registration...');
    try {
      const token = await AuthService.register(`testuser_${Date.now()}`, 'testpass123');
      setResult(`✅ Registration successful! Token: ${token.substring(0, 50)}...`);
    } catch (error) {
      setResult(`❌ Registration failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      position: 'fixed', 
      bottom: '10px', 
      left: '10px', 
      background: '#f0f0f0', 
      padding: '15px', 
      border: '1px solid #ccc',
      maxWidth: '400px',
      fontSize: '12px',
      zIndex: 9999
    }}>
      <div><strong>API Test:</strong></div>
      <div>
        <button onClick={testApiConnection} disabled={loading} style={{ margin: '5px' }}>
          Test Backend Connection
        </button>
        <button onClick={testRegistration} disabled={loading} style={{ margin: '5px' }}>
          Test Registration
        </button>
      </div>
      <div style={{ marginTop: '10px', whiteSpace: 'pre-wrap' }}>
        {result}
      </div>
    </div>
  );
};

export default ApiTest;
