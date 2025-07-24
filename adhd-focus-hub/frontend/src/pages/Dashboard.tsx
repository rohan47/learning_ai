import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Welcome to Your ADHD Focus Hub 🧠</h1>
        <p className="page-description">
          Your personalized AI-powered assistant for managing ADHD symptoms, 
          improving focus, and achieving your goals with compassion and understanding.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="card">
          <h3>🎯 Quick Focus Session</h3>
          <p>Start a 25-minute Pomodoro session with AI guidance</p>
          <button className="btn-primary mt-4">Start Focusing</button>
        </div>

        <div className="card">
          <h3>📋 Break Down a Task</h3>
          <p>Turn overwhelming tasks into manageable steps</p>
          <button className="btn-primary mt-4">Plan Task</button>
        </div>

        <div className="card">
          <h3>💙 Mood Check-in</h3>
          <p>Track your emotional state and get personalized support</p>
          <button className="btn-primary mt-4">Check Mood</button>
        </div>

        {/* Recent Activity */}
        <div className="card col-span-full">
          <h3>📊 Today's Progress</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span>Focus Sessions Completed</span>
              <span className="status-success">2/3</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Tasks Completed</span>
              <span className="status-success">4/7</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Mood Rating</span>
              <span className="status-warning">6/10</span>
            </div>
          </div>
        </div>

        {/* AI Suggestions */}
        <div className="card col-span-full">
          <h3>🤖 AI Recommendations</h3>
          <div className="space-y-3">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="font-medium">Focus Suggestion</p>
              <p className="text-sm text-gray-600 mt-1">
                Your energy seems high today! This might be a good time to tackle 
                that complex project you've been avoiding.
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="font-medium">Mood Boost</p>
              <p className="text-sm text-gray-600 mt-1">
                You've completed 4 tasks today! Remember to celebrate these wins 
                and take a well-deserved break.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
