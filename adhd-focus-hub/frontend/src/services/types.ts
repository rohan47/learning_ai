/**
 * TypeScript interfaces matching backend Pydantic models
 */

// ===== REQUEST TYPES =====

export interface ChatRequest {
  message: string;
  context?: {
    current_energy?: number;
    current_mood?: string;
    active_tasks?: string[];
    session_context?: any;
    agent_preference?: 'planning' | 'focus' | 'emotion' | 'organize' | 'learning';
    [key: string]: any;
  };
  agent_preference?: 'planning' | 'focus' | 'emotion' | 'organize' | 'learning';
}

export interface TaskBreakdownRequest {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  estimated_duration?: number;
}

export interface FocusSessionRequest {
  task_description: string;
  requested_duration: number;
  distraction_level: number;
  task_id?: string;
}

export interface MoodCheckRequest {
  mood_score: number;
  energy_level: number;
  stress_level: number;
  notes?: string;
  triggers?: string[];
}

export interface OrganizationRequest {
  space_description: string;
  goal: string;
}

export interface LearningRequest {
  topic: string;
  current_struggles?: string;
  learning_style?: string;
  time_available?: number;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskOut {
  id: number;
  title: string;
  description?: string | null;
  completed: boolean;
  created_at: string;
}

export interface MoodLogOut {
  id: number;
  mood_score: number;
  notes?: string | null;
  created_at: string;
}

// ===== RESPONSE TYPES =====

export interface ChatResponse {
  response: string;
  agent_used: string;
  confidence: number;
  suggestions: string[];
  metadata: Record<string, any>;
  timestamp: string;
  // Consultation details for comprehensive responses
  specialists_involved?: string[];
  individual_insights?: Record<string, string>;
  consultation_summary?: string;
  consultation_quality?: string;
}

export interface SubTask {
  id: string;
  title: string;
  description: string;
  estimated_minutes: number;
  difficulty: 'easy' | 'medium' | 'hard';
  energy_required: number;
  order: number;
}

export interface TaskBreakdownResponse {
  subtasks: SubTask[];
  total_estimated_minutes: number;
  difficulty_assessment: string;
  adhd_tips: string[];
  recommended_focus_sessions: number;
}

export interface FocusSessionResponse {
  session_id: string;
  adapted_duration: number;
  break_schedule: BreakSchedule[];
  focus_techniques: string[];
  environment_suggestions: string[];
}

export interface BreakSchedule {
  time_minutes: number;
  duration_minutes: number;
  type: 'short' | 'long' | 'movement';
  suggested_activities: string[];
}

export interface MoodCheckResponse {
  analysis: string;
  coping_strategies: string[];
  recommended_activities: string[];
  escalation_needed: boolean;
}

export interface AgentStatus {
  role: string;
  total_interactions: number;
  available: boolean;
}

export interface SystemStatus {
  total_agents: number;
  agents: Record<string, AgentStatus>;
  total_conversations: number;
  system_uptime: string;
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'down';
  crew_initialized: boolean;
  version: string;
}

// ===== FOCUS TOOLS TYPES =====

export interface FocusSessionPlan {
  task: string;
  duration: number;
  structure: {
    warm_up: string;
    main_work: string;
    wrap_up: string;
  };
  adhd_strategies: string[];
  distraction_plan: Record<string, string>;
  success_metrics: string[];
}

export interface DistractionManagement {
  distraction_assessment: {
    identified_distractions: string[];
    environment: string;
    urgency_level: number;
    complexity_score: number;
  };
  management_strategies: {
    immediate_actions: string[];
    environment_setup: string[];
    mindset_shifts: string[];
    emergency_refocus: string[];
  };
  quick_wins: string[];
}

export interface BreakOptimization {
  break_plan: {
    duration: string;
    type: 'restorative' | 'calming' | 'balanced';
    recommended_activities: string[];
    screen_guidance: string;
    transition_back: string;
  };
  adhd_considerations: string[];
  energy_assessment: {
    current_level: number;
    post_break_target: number;
    next_task_readiness: string;
  };
}

// ===== MOOD TRACKING TYPES =====

export interface MoodSnapshot {
  mood: string;
  category: 'positive' | 'challenging' | 'neutral';
  energy: number;
  stress: number;
  focus: number;
  sleep: string;
  wellness_score: number;
}

export interface MoodTrackingResponse {
  mood_snapshot: MoodSnapshot;
  insights: string[];
  recommendations: string[];
  tracking_tips: string[];
  timestamp: string;
}

// ===== ERROR TYPES =====

export interface ApiError {
  detail: string;
  status_code: number;
  timestamp: string;
}
