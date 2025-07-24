import React, { useState } from 'react';
import { FocusService } from '../services';

const Focus: React.FC = () => {
  const [task, setTask] = useState('');
  const [duration, setDuration] = useState(25);
  const [difficulty, setDifficulty] = useState<'low' | 'medium' | 'high'>('medium');
  const [sessionPlan, setSessionPlan] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createFocusSession = async () => {
    if (!task.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const plan = await FocusService.getFocusSessionPlan(
        task, 
        duration, 
        difficulty, 
        ['phone', 'social media'] // example distractions
      );
      setSessionPlan(plan);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create focus session');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="page-title">🎯 Focus Sessions</h1>
      <p className="text-gray-600 mb-6">Create ADHD-friendly focus sessions with AI guidance</p>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-xl font-semibold mb-4">Create Focus Session</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Task Description
            </label>
            <input
              type="text"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="What do you want to focus on?"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duration (minutes)
              </label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value) || 25)}
                min="5"
                max="90"
                className="w-full p-3 border border-gray-300 rounded-lg"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty Level
              </label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value as 'low' | 'medium' | 'high')}
                className="w-full p-3 border border-gray-300 rounded-lg"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          
          <button
            onClick={createFocusSession}
            disabled={loading || !task.trim()}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating Session...' : 'Create Focus Session'}
          </button>
        </div>
      </div>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {sessionPlan && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">📋 Your Focus Session Plan</h2>
          
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-green-600">Task: {sessionPlan.task}</h3>
              <p className="text-gray-600">Duration: {sessionPlan.duration} minutes</p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">Session Structure:</h4>
              <ul className="space-y-1 text-sm">
                <li>• {sessionPlan.structure.warm_up}</li>
                <li>• {sessionPlan.structure.main_work}</li>
                <li>• {sessionPlan.structure.wrap_up}</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">ADHD Strategies:</h4>
              <ul className="space-y-1 text-sm">
                {sessionPlan.adhd_strategies.map((strategy: string, idx: number) => (
                  <li key={idx}>• {strategy}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">Success Metrics:</h4>
              <ul className="space-y-1 text-sm">
                {sessionPlan.success_metrics.map((metric: string, idx: number) => (
                  <li key={idx}>• {metric}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Focus;
