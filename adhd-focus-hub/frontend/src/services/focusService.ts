/**
 * Focus management service for sessions and attention
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import { 
  FocusSessionRequest, 
  FocusSessionResponse, 
  FocusSessionPlan,
  DistractionManagement,
  BreakOptimization 
} from './types';

export class FocusService {
  /**
   * Start an adaptive focus session
   */
  static async startFocusSession(request: FocusSessionRequest): Promise<FocusSessionResponse> {
    try {
      const response = await apiClient.post<FocusSessionResponse>('/api/v1/focus/start', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get focus session plan using focus agent
   */
  static async getFocusSessionPlan(
    taskName: string, 
    duration: number = 25, 
    difficulty: 'low' | 'medium' | 'high' = 'medium',
    distractions: string[] = []
  ): Promise<FocusSessionPlan> {
    try {
      const chatRequest = {
        message: `Create a focus session plan for: ${taskName}`,
        context: {
          agent_preference: 'focus',
          request_type: 'focus_session',
          task_name: taskName,
          target_duration: duration,
          difficulty_level: difficulty,
          known_distractions: distractions
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      const result = handleApiResponse(response);
      
      // Parse the JSON response from the focus tool
      try {
        return JSON.parse(result.response);
      } catch {
        // If response isn't JSON, create a structured response
        return {
          task: taskName,
          duration: duration,
          structure: {
            warm_up: "2 minutes - Clear workspace and set intention",
            main_work: `${duration - 2} minutes - Deep work on ${taskName}`,
            wrap_up: "Last minute - Note progress and next steps"
          },
          adhd_strategies: [
            "🎯 Single-task focus only",
            "📱 Phone in another room or drawer",
            "⏰ Visible timer with gentle alert"
          ],
          distraction_plan: {},
          success_metrics: [
            "Stayed on task for at least 80% of session",
            "Made measurable progress"
          ]
        };
      }
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get distraction management strategies
   */
  static async getDistractionManagement(
    distractions: string[],
    environment: string = 'home',
    urgencyLevel: number = 5
  ): Promise<DistractionManagement> {
    try {
      const chatRequest = {
        message: `Help me manage these distractions: ${distractions.join(', ')}`,
        context: {
          agent_preference: 'focus',
          request_type: 'distraction_management',
          current_distractions: distractions,
          environment: environment,
          urgency_level: urgencyLevel
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      const result = handleApiResponse(response);
      
      try {
        return JSON.parse(result.response);
      } catch {
        return {
          distraction_assessment: {
            identified_distractions: distractions,
            environment: environment,
            urgency_level: urgencyLevel,
            complexity_score: distractions.length * (urgencyLevel / 10)
          },
          management_strategies: {
            immediate_actions: ["🧘 Take 3 deep breaths", "🎯 Refocus on current task"],
            environment_setup: ["🚪 Close door if possible", "🎧 Use headphones"],
            mindset_shifts: ["🌊 Distractions are normal with ADHD"],
            emergency_refocus: ["⏰ Use 10-minute micro-sessions"]
          },
          quick_wins: ["Start with just 5 minutes of focused work"]
        };
      }
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get break optimization suggestions
   */
  static async getBreakOptimization(
    workDuration: number = 25,
    energyLevel: number = 5,
    nextTaskType: string = 'cognitive'
  ): Promise<BreakOptimization> {
    try {
      const chatRequest = {
        message: `Suggest optimal break activities after ${workDuration} minutes of work`,
        context: {
          agent_preference: 'focus',
          request_type: 'break_optimization',
          work_duration: workDuration,
          energy_level: energyLevel,
          next_task_type: nextTaskType
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      const result = handleApiResponse(response);
      
      try {
        return JSON.parse(result.response);
      } catch {
        const breakDuration = workDuration <= 25 ? 5 : workDuration <= 45 ? 10 : 15;
        return {
          break_plan: {
            duration: `${breakDuration} minutes`,
            type: energyLevel <= 3 ? 'restorative' : energyLevel >= 8 ? 'calming' : 'balanced',
            recommended_activities: ["🚶 Light walk", "🥤 Hydrate", "🧘 Deep breathing"],
            screen_guidance: nextTaskType === 'cognitive' ? "⚠️ Avoid screens" : "Screens OK in moderation",
            transition_back: "Spend 30 seconds reviewing what you accomplished"
          },
          adhd_considerations: [
            "⏰ Set a timer for your break",
            "🔄 Move your body - ADHD brains need movement"
          ],
          energy_assessment: {
            current_level: energyLevel,
            post_break_target: Math.min(energyLevel + 1, 10),
            next_task_readiness: "optimal"
          }
        };
      }
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get general focus tips and strategies
   */
  static async getFocusTips(context?: any): Promise<any> {
    try {
      const chatRequest = {
        message: "Give me ADHD-friendly focus tips and strategies",
        context: {
          ...context,
          agent_preference: 'focus'
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default FocusService;
