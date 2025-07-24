/**
 * Chat service for AI agent communication
 */

import apiClient, { handleApiResponse, handleApiError } from './api';
import { ChatRequest, ChatResponse } from './types';

export class ChatService {
  /**
   * Send a message to AI agents and get intelligent routing response
   */
  static async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>('/api/v1/chat', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get conversation summary
   */
  static async getConversationSummary(limit: number = 10): Promise<any> {
    try {
      const response = await apiClient.get(`/api/v1/conversations/summary?limit=${limit}`);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Send a fresh chat message (bypasses cache)
   */
  static async sendFreshMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>('/api/v1/chat/fresh', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Send a comprehensive consultation request (uses orchestrator with all agents)
   */
  static async sendComprehensiveMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>('/api/v1/chat/comprehensive', request);
      return handleApiResponse(response);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default ChatService;
