import React, { useState } from 'react';
import { MoodService } from '../services';
import { Heart, Brain } from 'lucide-react';

const Mood: React.FC = () => {
  const [moodScore, setMoodScore] = useState(5);
  const [energyLevel, setEnergyLevel] = useState(5);
  const [stressLevel, setStressLevel] = useState(5);
  const [notes, setNotes] = useState('');
  const [triggers, setTriggers] = useState<string[]>([]);
  const [triggerInput, setTriggerInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const addTrigger = () => {
    if (triggerInput.trim() && !triggers.includes(triggerInput.trim())) {
      setTriggers(prev => [...prev, triggerInput.trim()]);
      setTriggerInput('');
    }
  };

  const removeTrigger = (trigger: string) => {
    setTriggers(prev => prev.filter(t => t !== trigger));
  };

  const logMood = async () => {
    setIsLoading(true);
    try {
      const moodResponse = await MoodService.logMood({
        mood_score: moodScore,
        energy_level: energyLevel,
        stress_level: stressLevel,
        notes: notes || undefined,
        triggers: triggers.length > 0 ? triggers : undefined
      });

      setResponse(moodResponse);
    } catch (error) {
      console.error('Error logging mood:', error);
      alert('Failed to log mood. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getMoodEmoji = (score: number) => {
    if (score <= 2) return '😢';
    if (score <= 4) return '😕';
    if (score <= 6) return '😐';
    if (score <= 8) return '🙂';
    return '😊';
  };

  const getEnergyEmoji = (score: number) => {
    if (score <= 2) return '😴';
    if (score <= 4) return '😓';
    if (score <= 6) return '😌';
    if (score <= 8) return '⚡';
    return '🔥';
  };

  const getStressEmoji = (score: number) => {
    if (score <= 2) return '😌';
    if (score <= 4) return '😐';
    if (score <= 6) return '😰';
    if (score <= 8) return '😵';
    return '🤯';
  };

  return (
    <div className="page">
      <h1 className="page-title">Mood Tracking</h1>
      <p className="text-gray-600 mb-6">Track your emotional state and get personalized ADHD support</p>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
          <Heart className="text-red-500" size={20} />
          How are you feeling today?
        </h2>

        <div className="space-y-6">
          {/* Mood Score */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Mood {getMoodEmoji(moodScore)} (1-10)
            </label>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500">Low</span>
              <input
                type="range"
                min="1"
                max="10"
                value={moodScore}
                onChange={(e) => setMoodScore(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span className="text-sm text-gray-500">High</span>
              <span className="text-lg font-semibold w-8">{moodScore}</span>
            </div>
          </div>

          {/* Energy Level */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Energy Level {getEnergyEmoji(energyLevel)} (1-10)
            </label>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500">Tired</span>
              <input
                type="range"
                min="1"
                max="10"
                value={energyLevel}
                onChange={(e) => setEnergyLevel(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span className="text-sm text-gray-500">Energetic</span>
              <span className="text-lg font-semibold w-8">{energyLevel}</span>
            </div>
          </div>

          {/* Stress Level */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Stress Level {getStressEmoji(stressLevel)} (1-10)
            </label>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500">Calm</span>
              <input
                type="range"
                min="1"
                max="10"
                value={stressLevel}
                onChange={(e) => setStressLevel(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span className="text-sm text-gray-500">Stressed</span>
              <span className="text-lg font-semibold w-8">{stressLevel}</span>
            </div>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes (optional)
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="How are you feeling? What's on your mind?"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
            />
          </div>

          {/* Triggers */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Triggers or Stressors
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={triggerInput}
                onChange={(e) => setTriggerInput(e.target.value)}
                placeholder="Add a trigger..."
                className="flex-1 p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                onKeyPress={(e) => e.key === 'Enter' && addTrigger()}
              />
              <button
                onClick={addTrigger}
                className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {triggers.map(trigger => (
                <span
                  key={trigger}
                  className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm flex items-center gap-1"
                >
                  {trigger}
                  <button
                    onClick={() => removeTrigger(trigger)}
                    className="text-red-600 hover:text-red-800"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          <button
            onClick={logMood}
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <Brain size={20} />
            {isLoading ? 'Getting Support...' : 'Log Mood & Get Support'}
          </button>
        </div>
      </div>

      {/* Response from emotional support agent */}
      {response && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-green-800">
          Mood logged at {new Date(response.created_at).toLocaleString()}
        </div>
      )}
    </div>
  );
};

export default Mood;
