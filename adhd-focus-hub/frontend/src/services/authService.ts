import apiClient, { handleApiResponse, handleApiError } from './api';

interface AuthResponse {
  access_token: string;
  token_type: string;
}

export class AuthService {
  static async login(username: string, password: string): Promise<string> {
    try {
      const response = await apiClient.post<AuthResponse>('/api/v1/auth/login', {
        username,
        password,
      });
      const data = handleApiResponse(response);
      return data.access_token;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  static async register(username: string, password: string): Promise<string> {
    try {
      const response = await apiClient.post<AuthResponse>('/api/v1/auth/register', {
        username,
        password,
      });
      const data = handleApiResponse(response);
      return data.access_token;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default AuthService;
