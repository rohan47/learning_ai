import React, { useState, useEffect } from 'react';
import { TaskService, ChatService } from '../services';
import { Plus, Clock, CheckCircle, AlertCircle } from 'lucide-react';

interface Task {
  id: string;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  estimatedDuration?: number;
  subtasks?: string[];
}

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium' as const });
  const [isLoading, setIsLoading] = useState(false);
  const [planningResponse, setPlanningResponse] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTasks = async () => {
      setIsLoading(true);
      try {
        const data = await TaskService.listTasks();
        setTasks(data.map(t => ({
          id: t.id.toString(),
          title: t.title,
          description: t.description || undefined,
          priority: 'medium'
        })));
      } catch (err) {
        console.error('Error loading tasks:', err);
        setError(err instanceof Error ? err.message : 'Failed to load tasks');
      } finally {
        setIsLoading(false);
      }
    };
    loadTasks();
  }, []);

  const addTask = async () => {
    if (!newTask.title.trim()) return;

    setIsLoading(true);
    try {
      const created = await TaskService.createTask({
        title: newTask.title,
        description: newTask.description || undefined,
      });

      const planningHelp = await TaskService.getPlanningHelp(
        `${newTask.title}: ${newTask.description}`,
        { priority: newTask.priority }
      );

      setTasks(prev => [
        ...prev,
        {
          id: created.id.toString(),
          title: created.title,
          description: created.description || undefined,
          priority: newTask.priority,
        },
      ]);
      setPlanningResponse(planningHelp.response);
      setNewTask({ title: '', description: '', priority: 'medium' });
    } catch (error) {
      console.error('Error adding task:', error);
      setError(error instanceof Error ? error.message : 'Failed to add task');
    } finally {
      setIsLoading(false);
    }
  };

  const breakdownTask = async (taskId: string) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    setIsLoading(true);
    try {
      const breakdown = await TaskService.breakdownTask({
        title: task.title,
        description: task.description,
        priority: task.priority,
        estimated_duration: task.estimatedDuration
      });

      setTasks(prev => prev.map(t => 
        t.id === taskId 
          ? { ...t, subtasks: breakdown.subtasks.map(sub => sub.description) }
          : t
      ));
    } catch (error) {
      console.error('Error breaking down task:', error);
      alert('Failed to break down task. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const estimateTime = async (taskId: string) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    setIsLoading(true);
    try {
      const timeEstimate = await TaskService.estimateTime(task.title, task.priority);
      
      setTasks(prev => prev.map(t => 
        t.id === taskId 
          ? { ...t, estimatedDuration: 25 } // Default estimate, would parse from response
          : t
      ));
      
      setPlanningResponse(timeEstimate.response);
    } catch (error) {
      console.error('Error estimating time:', error);
      alert('Failed to estimate time. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="page">
      <h1 className="page-title">Task Planning</h1>
      <p className="text-gray-600 mb-6">AI-powered task breakdown and planning with ADHD-aware strategies</p>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <span className="font-semibold">Error:</span> {error}
        </div>
      )}

      {/* Add New Task */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Add New Task</h2>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Task title..."
            value={newTask.title}
            onChange={(e) => setNewTask(prev => ({ ...prev, title: e.target.value }))}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <textarea
            placeholder="Task description (optional)..."
            value={newTask.description}
            onChange={(e) => setNewTask(prev => ({ ...prev, description: e.target.value }))}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
          />
          <div className="flex gap-4">
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask(prev => ({ ...prev, priority: e.target.value as any }))}
              className="p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
              <option value="urgent">Urgent</option>
            </select>
            <button
              onClick={addTask}
              disabled={isLoading || !newTask.title.trim()}
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Plus size={20} />
              {isLoading ? 'Adding...' : 'Add Task'}
            </button>
          </div>
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-4">
        {tasks.map(task => (
          <div key={task.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold">{task.title}</h3>
                {task.description && (
                  <p className="text-gray-600 mt-1">{task.description}</p>
                )}
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(task.priority)}`}>
                {task.priority}
              </span>
            </div>

            {task.estimatedDuration && (
              <div className="flex items-center gap-2 text-gray-600 mb-4">
                <Clock size={16} />
                <span>Estimated: {task.estimatedDuration} minutes</span>
              </div>
            )}

            {task.subtasks && (
              <div className="mb-4">
                <h4 className="font-medium mb-2">Subtasks:</h4>
                <ul className="space-y-1">
                  {task.subtasks.map((subtask, index) => (
                    <li key={index} className="flex items-center gap-2 text-gray-700">
                      <CheckCircle size={16} className="text-green-500" />
                      {subtask}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex gap-2">
              <button
                onClick={() => breakdownTask(task.id)}
                disabled={isLoading}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
              >
                Break Down
              </button>
              <button
                onClick={() => estimateTime(task.id)}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                Estimate Time
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Planning Response */}
      {planningResponse && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-800 mb-2">Planning Assistant Response:</h3>
          <p className="text-blue-700 whitespace-pre-wrap">{planningResponse}</p>
        </div>
      )}
    </div>
  );
};

export default Tasks;
