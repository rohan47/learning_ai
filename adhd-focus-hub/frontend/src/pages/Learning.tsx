import React, { useState } from 'react';
import { ChatService } from '../services';
import { BookOpen, Brain, Target, Zap } from 'lucide-react';

const Learning: React.FC = () => {
  const [learningTopic, setLearningTopic] = useState('');
  const [currentStruggles, setCurrentStruggles] = useState('');
  const [learningStyle, setLearningStyle] = useState('mixed');
  const [timeAvailable, setTimeAvailable] = useState(30);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const getLearningStrategy = async () => {
    if (!learningTopic.trim()) return;

    setIsLoading(true);
    try {
      const learningResponse = await ChatService.sendMessage({
        message: `Help me learn: ${learningTopic}. Current struggles: ${currentStruggles || 'None specified'}. I have ${timeAvailable} minutes available.`,
        context: {
          agent_preference: 'learning',
          request_type: 'learning_strategy',
          learning_style: learningStyle,
          time_available: timeAvailable,
          struggles: currentStruggles
        }
      });

      setResponse(learningResponse);
    } catch (error) {
      console.error('Error getting learning strategy:', error);
      alert('Failed to get learning strategy. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const adhdLearningTips = [
    {
      icon: Brain,
      title: 'Break It Down',
      description: 'Divide complex topics into smaller, manageable chunks',
      color: 'bg-blue-100 text-blue-600'
    },
    {
      icon: Zap,
      title: 'Use Multiple Senses',
      description: 'Combine visual, auditory, and kinesthetic learning methods',
      color: 'bg-yellow-100 text-yellow-600'
    },
    {
      icon: Target,
      title: 'Active Recall',
      description: 'Test yourself frequently instead of just re-reading',
      color: 'bg-green-100 text-green-600'
    },
    {
      icon: BookOpen,
      title: 'Spaced Repetition',
      description: 'Review material at increasing intervals for better retention',
      color: 'bg-purple-100 text-purple-600'
    }
  ];

  return (
    <div className="page">
      <h1 className="page-title">Learning Hub</h1>
      <p className="text-gray-600 mb-6">ADHD-optimized learning strategies and personalized study plans</p>

      {/* ADHD Learning Tips */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {adhdLearningTips.map((tip, index) => {
          const IconComponent = tip.icon;
          return (
            <div key={index} className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-blue-500">
              <div className={`inline-flex p-2 rounded-lg ${tip.color} mb-3`}>
                <IconComponent size={20} />
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">{tip.title}</h3>
              <p className="text-gray-600 text-sm">{tip.description}</p>
            </div>
          );
        })}
      </div>

      {/* Get Personalized Learning Strategy */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Brain className="text-blue-600" size={20} />
          Get Personalized Learning Strategy
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What do you want to learn?
            </label>
            <input
              type="text"
              value={learningTopic}
              onChange={(e) => setLearningTopic(e.target.value)}
              placeholder="e.g., JavaScript programming, Spanish vocabulary, calculus derivatives..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Current struggles or challenges (optional)
            </label>
            <textarea
              value={currentStruggles}
              onChange={(e) => setCurrentStruggles(e.target.value)}
              placeholder="e.g., Hard to focus for long periods, forget what I read, get overwhelmed by complex concepts..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={2}
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Learning Style Preference
              </label>
              <select
                value={learningStyle}
                onChange={(e) => setLearningStyle(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="visual">Visual (diagrams, charts, colors)</option>
                <option value="auditory">Auditory (listening, discussion)</option>
                <option value="kinesthetic">Kinesthetic (hands-on, movement)</option>
                <option value="mixed">Mixed (combination of styles)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Time Available (minutes)
              </label>
              <input
                type="number"
                value={timeAvailable}
                onChange={(e) => setTimeAvailable(parseInt(e.target.value) || 30)}
                min="10"
                max="240"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <button
            onClick={getLearningStrategy}
            disabled={isLoading || !learningTopic.trim()}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <Target size={20} />
            {isLoading ? 'Creating Learning Plan...' : 'Get ADHD-Friendly Learning Strategy'}
          </button>
        </div>
      </div>

      {/* Learning Strategy Response */}
      {response && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-800 mb-4 flex items-center gap-2">
            <BookOpen className="text-blue-600" size={20} />
            Your Personalized Learning Strategy
          </h3>
          
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-2">Learning Strategy:</h4>
              <p className="text-blue-700 whitespace-pre-wrap">{response.response}</p>
            </div>

            {response.suggestions && response.suggestions.length > 0 && (
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">Study Tips:</h4>
                <ul className="list-disc list-inside space-y-1 text-blue-700">
                  {response.suggestions.map((suggestion: string, index: number) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="bg-white p-4 rounded-lg">
              <p className="text-sm text-gray-600">
                <strong>Agent:</strong> {response.agent_used} | 
                <strong> Confidence:</strong> {Math.round(response.confidence * 100)}% |
                <strong> Focus Time:</strong> {timeAvailable} minutes
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Learning;
