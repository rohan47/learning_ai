/**
 * Service for organization-related API calls
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import { OrganizationRequest, ChatResponse } from './types';

export class OrganizationService {
  /**
   * Request an organization plan from the backend
   */
  static async getOrganizationPlan(
    request: OrganizationRequest
  ): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>(
        '/api/v1/organize',
        request
      );
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default OrganizationService;
