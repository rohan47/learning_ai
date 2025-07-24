/**
 * Task management service for planning and breakdown
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import { TaskBreakdownRequest, TaskBreakdownResponse } from './types';

export class TaskService {
  /**
   * Break down a complex task into ADHD-friendly steps
   */
  static async breakdownTask(request: TaskBreakdownRequest): Promise<TaskBreakdownResponse> {
    try {
      const response = await apiClient.post<TaskBreakdownResponse>('/api/v1/tasks/breakdown', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get task planning recommendations using planning agent
   */
  static async getPlanningHelp(taskDescription: string, context?: any): Promise<any> {
    try {
      const chatRequest = {
        message: `Help me plan this task: ${taskDescription}`,
        context: {
          ...context,
          agent_preference: 'planning'
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get time estimation for tasks
   */
  static async estimateTime(taskDescription: string, complexity: 'low' | 'medium' | 'high' | 'urgent' = 'medium'): Promise<any> {
    try {
      const chatRequest = {
        message: `Estimate realistic time for this ${complexity} complexity task: ${taskDescription}`,
        context: {
          agent_preference: 'planning',
          request_type: 'time_estimation'
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get task prioritization help
   */
  static async prioritizeTasks(tasks: string[], context?: any): Promise<any> {
    try {
      const chatRequest = {
        message: `Help me prioritize these tasks: ${tasks.join(', ')}`,
        context: {
          ...context,
          agent_preference: 'planning',
          request_type: 'prioritization'
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default TaskService;
