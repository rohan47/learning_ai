/**
 * Main services export - easy imports for components
 */

export { default as ChatService } from './chatService';
export { default as TaskService } from './taskService';
export { default as FocusService } from './focusService';
export { default as MoodService } from './moodService';
export { default as AuthService } from './authService';
export { default as OrganizationService } from './organizationService';
export { default as LearningService } from './learningService';

// Re-export types for convenience
export * from './types';

// Re-export API client for direct use if needed
export { default as apiClient } from './api';
