/**
 * Mood and emotional support service
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import {
  MoodCheckRequest,
  MoodCheckResponse,
  MoodTrackingResponse,
  MoodLogOut,
} from './types';

export class MoodService {
  /**
   * Persist a mood entry for the current user
   */
  static async logMood(request: MoodCheckRequest): Promise<MoodLogOut> {
    try {
      const response = await apiClient.post<MoodLogOut>('/api/v1/moods', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get mood analysis and coping suggestions using the emotion agent
   */
  static async checkMood(request: MoodCheckRequest): Promise<MoodCheckResponse> {
    try {
      const response = await apiClient.post<MoodCheckResponse>('/api/v1/mood/log', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  static async listMoods(): Promise<MoodLogOut[]> {
    try {
      const response = await apiClient.get<MoodLogOut[]>('/api/v1/moods');
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Track mood patterns using emotion agent
   */
  static async trackMood(
    currentMood: string,
    energyLevel: number = 5,
    stressLevel: number = 5,
    focusQuality: number = 5,
    sleepQuality: string = 'average'
  ): Promise<MoodTrackingResponse> {
    try {
      const chatRequest = {
        message: `Track my mood: ${currentMood}`,
        context: {
          agent_preference: 'emotion',
          request_type: 'mood_tracking',
          current_mood: currentMood,
          energy_level: energyLevel,
          stress_level: stressLevel,
          focus_quality: focusQuality,
          sleep_quality: sleepQuality
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      const result = handleApiResponse(response);
      
      try {
        return JSON.parse(result.response);
      } catch {
        // Fallback structured response
        return {
          mood_snapshot: {
            mood: currentMood,
            category: 'neutral',
            energy: energyLevel,
            stress: stressLevel,
            focus: focusQuality,
            sleep: sleepQuality,
            wellness_score: (energyLevel + (10 - stressLevel) + focusQuality) / 3
          },
          insights: ["Mood logged successfully"],
          recommendations: ["Practice self-compassion", "Take breaks as needed"],
          tracking_tips: ["Notice patterns between sleep, mood, and productivity"],
          timestamp: new Date().toISOString()
        };
      }
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get coping strategies for current emotional state
   */
  static async getCopingStrategies(
    triggerSituation: string,
    emotionalIntensity: number = 5,
    availableTime: number = 10,
    preferredMethods: string[] = []
  ): Promise<any> {
    try {
      const chatRequest = {
        message: `I need coping strategies for: ${triggerSituation}`,
        context: {
          agent_preference: 'emotion',
          request_type: 'coping_strategies',
          trigger_situation: triggerSituation,
          emotional_intensity: emotionalIntensity,
          available_time: availableTime,
          preferred_methods: preferredMethods
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      const result = handleApiResponse(response);
      
      try {
        return JSON.parse(result.response);
      } catch {
        return {
          situation_analysis: {
            trigger: triggerSituation,
            intensity: emotionalIntensity,
            urgency_level: emotionalIntensity >= 8 ? 'high' : 'moderate'
          },
          immediate_strategies: [
            "🌬️ Take 5 deep breaths",
            "🧘 Use grounding techniques",
            "💭 Acknowledge feelings without judgment"
          ],
          adhd_considerations: [
            "🧩 Break overwhelming situations into smaller pieces",
            "🎭 Remember that ADHD emotions are often more intense"
          ]
        };
      }
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get motivation support for specific tasks
   */
  static async getMotivationSupport(
    taskDescription: string,
    procrastinationReason: string = 'overwhelming',
    personalValues: string[] = [],
    rewardPreferences: string[] = []
  ): Promise<any> {
    try {
      const chatRequest = {
        message: `I need motivation help with: ${taskDescription}`,
        context: {
          agent_preference: 'emotion',
          request_type: 'motivation_support',
          task_description: taskDescription,
          procrastination_reason: procrastinationReason,
          personal_values: personalValues,
          reward_preferences: rewardPreferences
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      const result = handleApiResponse(response);
      
      try {
        return JSON.parse(result.response);
      } catch {
        return {
          task_analysis: {
            task: taskDescription,
            procrastination_reason: procrastinationReason
          },
          targeted_strategies: [
            "🧩 Break task into micro-steps",
            "🎯 Focus on just starting, not finishing"
          ],
          emergency_protocol: [
            "⏰ Commit to just 2 minutes",
            "🔥 Action creates motivation, not the other way around"
          ],
          gentle_reminder: "💝 You don't have to want to do it. You just have to do it."
        };
      }
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get emotional regulation tips
   */
  static async getEmotionalSupport(context?: any): Promise<any> {
    try {
      const chatRequest = {
        message: "I need emotional support and regulation strategies",
        context: {
          ...context,
          agent_preference: 'emotion'
        }
      };
      
      const response = await apiClient.post('/api/v1/chat', chatRequest);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default MoodService;
