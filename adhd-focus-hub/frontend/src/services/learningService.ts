/**
 * Service for learning-related API calls
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import { LearningRequest, ChatResponse } from './types';

export class LearningService {
  /**
   * Request a personalized learning plan
   */
  static async getLearningPlan(
    request: LearningRequest
  ): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>(
        '/api/v1/learn',
        request
      );
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default LearningService;
