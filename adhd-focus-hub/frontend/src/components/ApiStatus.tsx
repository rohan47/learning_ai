import React, { useState, useEffect } from 'react';
import { SystemService } from '../services';

const ApiStatus: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkStatus = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Test basic connection
      const [healthResponse, statusResponse] = await Promise.all([
        SystemService.getHealthStatus(),
        SystemService.getAgentStatus()
      ]);
      
      setHealth(healthResponse);
      setStatus(statusResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const clearCache = async () => {
    try {
      await SystemService.clearCache();
      alert('Cache cleared successfully!');
      checkStatus(); // Refresh status
    } catch (err) {
      alert('Failed to clear cache: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  const refreshAgents = async () => {
    try {
      await SystemService.refreshAgents();
      alert('Agents refreshed successfully!');
      checkStatus(); // Refresh status
    } catch (err) {
      alert('Failed to refresh agents: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🔧 API Status</h1>
        <p className="text-gray-600">Check connection to ADHD Focus Hub backend</p>
        
        <div className="flex gap-2">
          <button
            onClick={checkStatus}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Checking...' : 'Refresh Status'}
          </button>
          <button
            onClick={clearCache}
            className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700"
          >
            Clear Cache
          </button>
          <button
            onClick={refreshAgents}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Refresh Agents
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <strong>Connection Error:</strong> {error}
          <p className="text-sm mt-2">
            Make sure the backend is running on {process.env.REACT_APP_API_URL || 'http://localhost:8001'}
          </p>
        </div>
      )}

      {health && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">🏥 Health Status</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                health.status === 'healthy' 
                  ? 'bg-green-100 text-green-800'
                  : health.status === 'degraded'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {health.status === 'healthy' ? '✅' : health.status === 'degraded' ? '⚠️' : '❌'} {health.status}
              </div>
            </div>
            <div className="text-center">
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                health.crew_initialized ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {health.crew_initialized ? '🤖 AI Ready' : '❌ AI Not Ready'}
              </div>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                📦 v{health.version}
              </div>
            </div>
          </div>
        </div>
      )}

      {status && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">🤖 AI Agents Status</h2>
          
          <div className="grid gap-4">
            {Object.entries(status.agents).map(([agentName, agentInfo]: [string, any]) => (
              <div key={agentName} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-semibold capitalize">{agentName} Agent</h3>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${
                    agentInfo.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {agentInfo.available ? '✅ Available' : '❌ Unavailable'}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-1">{agentInfo.role}</p>
                <p className="text-xs text-gray-500">
                  {agentInfo.total_interactions} interactions
                </p>
              </div>
            ))}
          </div>
          
          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Total Agents:</span> {status.total_agents}
              </div>
              <div>
                <span className="font-medium">Total Conversations:</span> {status.total_conversations}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-2">🔗 API Endpoints</h3>
        <div className="text-sm space-y-1">
          <p><strong>Base URL:</strong> {process.env.REACT_APP_API_URL || 'http://localhost:8001'}</p>
          <p><strong>Documentation:</strong> <a href={SystemService.getDocsUrl()} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">View API Docs</a></p>
          <p><strong>Available Services:</strong> Chat, Tasks, Focus, Mood, System</p>
        </div>
      </div>
    </div>
  );
};

export default ApiStatus;
