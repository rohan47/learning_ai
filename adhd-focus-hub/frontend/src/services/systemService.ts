/**
 * System status and agent management service
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import { SystemStatus, HealthResponse } from './types';

export class SystemService {
  /**
   * Check API health and connection status
   */
  static async getHealthStatus(): Promise<HealthResponse> {
    try {
      const response = await apiClient.get<HealthResponse>('/health');
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get status of all AI agents
   */
  static async getAgentStatus(): Promise<SystemStatus> {
    try {
      const response = await apiClient.get<SystemStatus>('/api/v1/agents/status');
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Test basic API connectivity
   */
  static async testConnection(): Promise<any> {
    try {
      const response = await apiClient.get('/');
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get API documentation URL
   */
  static getDocsUrl(): string {
    const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8001';
    return `${baseUrl}/docs`;
  }

  /**
   * Clear conversation cache
   */
  static async clearCache(): Promise<any> {
    try {
      const response = await apiClient.post('/api/v1/system/clear-cache');
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Refresh all agents
   */
  static async refreshAgents(): Promise<any> {
    try {
      const response = await apiClient.post('/api/v1/system/refresh-agents');
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Check if backend is available
   */
  static async isBackendAvailable(): Promise<boolean> {
    try {
      await this.testConnection();
      return true;
    } catch {
      return false;
    }
  }
}

export default SystemService;
