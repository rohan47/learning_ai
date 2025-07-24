import React, { useState } from 'react';
import { ChatService } from '../services';
import { Folder, CheckSquare, FileText, Lightbulb } from 'lucide-react';

interface OrganizationTip {
  category: string;
  tip: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

const Organization: React.FC = () => {
  const [spaceDescription, setSpaceDescription] = useState('');
  const [organizationGoal, setOrganizationGoal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const getOrganizationHelp = async () => {
    if (!spaceDescription.trim() || !organizationGoal.trim()) return;

    setIsLoading(true);
    try {
      const organizationResponse = await ChatService.sendMessage({
        message: `Help me organize my space: ${spaceDescription}. My goal is: ${organizationGoal}`,
        context: {
          agent_preference: 'organize',
          request_type: 'organization_help'
        }
      });

      setResponse(organizationResponse);
    } catch (error) {
      console.error('Error getting organization help:', error);
      alert('Failed to get organization help. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const quickTips: OrganizationTip[] = [
    {
      category: 'Start Small',
      tip: 'Pick one small area (like your desk surface) to organize first',
      difficulty: 'easy'
    },
    {
      category: 'ADHD-Friendly',
      tip: 'Use clear containers so you can see what\'s inside',
      difficulty: 'easy'
    },
    {
      category: 'Daily Habits',
      tip: 'Spend 10 minutes each evening doing a "reset" of your main workspace',
      difficulty: 'medium'
    },
    {
      category: 'Systems',
      tip: 'Create designated "homes" for frequently used items',
      difficulty: 'medium'
    }
  ];

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="page">
      <h1 className="page-title">Organization Hub</h1>
      <p className="text-gray-600 mb-6">ADHD-friendly organization systems and personalized decluttering guidance</p>

      {/* Quick Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Lightbulb className="text-blue-600" size={20} />
          Quick ADHD Organization Tips
        </h2>
        <div className="grid md:grid-cols-2 gap-4">
          {quickTips.map((tip, index) => (
            <div key={index} className="bg-white p-4 rounded-lg shadow-sm">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-medium text-blue-800">{tip.category}</h3>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(tip.difficulty)}`}>
                  {tip.difficulty}
                </span>
              </div>
              <p className="text-gray-700 text-sm">{tip.tip}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Get Personalized Help */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Folder className="text-green-600" size={20} />
          Get Personalized Organization Help
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe the space you want to organize
            </label>
            <textarea
              value={spaceDescription}
              onChange={(e) => setSpaceDescription(e.target.value)}
              placeholder="e.g., My bedroom desk is cluttered with papers, books, and random items. I can't find anything and it's affecting my productivity..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What's your organization goal?
            </label>
            <input
              type="text"
              value={organizationGoal}
              onChange={(e) => setOrganizationGoal(e.target.value)}
              placeholder="e.g., Create a productive workspace, reduce stress, find things easily..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <button
            onClick={getOrganizationHelp}
            disabled={isLoading || !spaceDescription.trim() || !organizationGoal.trim()}
            className="w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <CheckSquare size={20} />
            {isLoading ? 'Getting Organization Plan...' : 'Get ADHD-Friendly Organization Plan'}
          </button>
        </div>
      </div>

      {/* Organization Response */}
      {response && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="font-semibold text-green-800 mb-4 flex items-center gap-2">
            <FileText className="text-green-600" size={20} />
            Your Personalized Organization Plan
          </h3>
          
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg">
              <h4 className="font-medium text-green-800 mb-2">AI Guidance:</h4>
              <p className="text-green-700 whitespace-pre-wrap">{response.response}</p>
            </div>

            {response.suggestions && response.suggestions.length > 0 && (
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Next Steps:</h4>
                <ul className="list-disc list-inside space-y-1 text-green-700">
                  {response.suggestions.map((suggestion: string, index: number) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="bg-white p-4 rounded-lg">
              <p className="text-sm text-gray-600">
                <strong>Agent:</strong> {response.agent_used} | 
                <strong> Confidence:</strong> {Math.round(response.confidence * 100)}%
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Organization;
