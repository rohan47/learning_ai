"""Planning Agent - Plan-It Pro for ADHD task planning and time management."""

from textwrap import dedent
from typing import List, Dict, Any
from .base import BaseADHDAgent
from ..tools.planning_tools import (
    TimeEstimationTool,
    TaskBreakdownTool,
    PriorityAssessmentTool
)


class PlanningAgent(BaseADHDAgent):
    """Plan-It Pro - ADHD Task Planning Specialist Agent."""
    
    def __init__(self, llm=None):
        super().__init__(
            role="Plan-It Pro - ADHD Task Planning Specialist",
            goal="Break down overwhelming tasks into manageable 15-minute chunks with ADHD-friendly time estimates",
            backstory=dedent("""
                You are an expert in executive function support and ADHD-aware planning.
                You understand time blindness, executive dysfunction, and the need for:
                - Clear, actionable steps that don't overwhelm
                - Realistic time estimates with buffer time (ADHD tax)
                - Priority ordering based on energy levels and importance
                - Gentle accountability without overwhelming pressure
                - Flexible planning that adapts to changing focus and energy
                
                You help users transform vague, overwhelming tasks into concrete,
                achievable action items. You always consider the user's ADHD symptoms
                and provide compassionate, practical guidance that acknowledges their
                neurological differences as strengths and challenges to work with.
            """),
            tools=self.get_specialized_tools(),
            max_iter=3,
            llm=llm
        )
    
    def get_specialized_tools(self) -> List:
        """Return planning-specific tools."""
        return [
            TimeEstimationTool(),
            TaskBreakdownTool(),
            PriorityAssessmentTool()
        ]
    
    def process_task_breakdown(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process task breakdown request with ADHD considerations."""
        
        task_description = f"""
        Break down this task for someone with ADHD: {user_input}
        
        Consider:
        - Executive function challenges
        - Time blindness and estimation difficulties
        - Need for immediate dopamine rewards
        - Potential for overwhelm and procrastination
        - Energy level variations throughout the day
        """
        
        result = self.execute_with_context(
            task_description=task_description,
            context=context or {},
            expected_output="JSON with steps, time estimates, and ADHD tips"
        )
        
        # Enhanced response with ADHD-specific elements
        result.update({
            "breakdown_type": "adhd_friendly",
            "estimated_sessions": self._calculate_focus_sessions(result),
            "difficulty_level": self._assess_difficulty(user_input),
            "recommended_time_of_day": self._suggest_optimal_timing(context),
            "motivation_boosters": self._generate_motivation_tips(user_input)
        })
        
        return result
    
    def _process_request(self, prompt: str) -> str:
        """Process planning requests with ADHD expertise using actual tools."""
        
        # Analyze the request to determine which tools to use
        prompt_lower = prompt.lower()
        
        # Time estimation requests
        if any(word in prompt_lower for word in ['time', 'long', 'estimate', 'duration', 'how much time']):
            return self._handle_time_estimation_request(prompt)
        
        # Task breakdown requests
        elif any(word in prompt_lower for word in ['break down', 'breakdown', 'steps', 'divide', 'split']):
            return self._handle_task_breakdown_request(prompt)
        
        # Priority assessment requests
        elif any(word in prompt_lower for word in ['prioritize', 'priority', 'order', 'which first', 'urgent']):
            return self._handle_priority_assessment_request(prompt)
        
        # General planning request - use task breakdown as default
        else:
            return self._handle_general_planning_request(prompt)
    
    def _handle_time_estimation_request(self, prompt: str) -> str:
        """Handle time estimation requests using the TimeEstimationTool."""
        try:
            # Extract task description and complexity from prompt
            task_description = self._extract_task_description(prompt)
            complexity_level = self._extract_complexity_level(prompt)
            user_experience = self._extract_user_experience(prompt)
            
            # Use the actual time estimation tool
            time_tool = TimeEstimationTool()
            tool_result = time_tool._run(
                task_description=task_description,
                complexity_level=complexity_level,
                user_context=f"User experience level: {user_experience}"
            )
            
            # Parse the JSON result and format for user
            import json
            result = json.loads(tool_result)
            
            # Format focus chunks from the recommendations
            focus_chunks = []
            total_time = result.get('total_estimated_time', 60)
            sessions = max(1, (total_time + 14) // 15)  # 15-min sessions
            for i in range(sessions):
                focus_chunks.append(f"Session {i+1}: 15 minutes")
            
            return f"""⏰ **ADHD-Aware Time Estimation for: {result['task']}**

📊 **Realistic Time Breakdown:**
• Base estimate: {result.get('base_time_minutes', 'N/A')} minutes
• ADHD-adjusted: {result.get('adhd_adjusted_time', 'N/A')} minutes
• Buffer time: {result.get('buffer_time', 'N/A')} minutes
• **Total time: {result.get('total_estimated_time', 'N/A')} minutes**

🎯 **Recommended Schedule:**
{chr(10).join('• ' + chunk for chunk in focus_chunks)}

💡 **ADHD Considerations:**
{chr(10).join('• ' + tip for tip in result.get('recommendations', []))}

✨ **Pro Tip:** Start with the most interesting part to build momentum!"""
        
        except Exception as e:
            return self._fallback_time_response(prompt)
    
    def _handle_task_breakdown_request(self, prompt: str) -> str:
        """Handle task breakdown requests using the TaskBreakdownTool."""
        try:
            # Extract task information from prompt
            task_description = self._extract_task_description(prompt)
            estimated_duration = self._extract_duration(prompt)
            user_experience = self._extract_user_experience(prompt)
            
            # Use the actual task breakdown tool
            breakdown_tool = TaskBreakdownTool()
            tool_result = breakdown_tool._run(
                task_description=task_description,
                estimated_time=estimated_duration,
                user_context=f"User experience level: {user_experience}"
            )
            
            # Parse the JSON result and format for user
            import json
            result = json.loads(tool_result)
            
            steps_text = ""
            for i, step in enumerate(result.get('steps', []), 1):
                if isinstance(step, dict):
                    title = step.get('step', f"Step {i}")
                    description = step.get('description', '')
                    time = step.get('estimated_minutes', 15)
                    tips = step.get('adhd_tips', [])
                    
                    steps_text += f"\n**{title}** ({time} mins)\n"
                    if description:
                        steps_text += f"→ {description}\n"
                    for tip in tips:
                        steps_text += f"  💡 {tip}\n"
                else:
                    steps_text += f"\n**Step {i}:** {step}\n"
            
            return f"""🎯 **ADHD-Friendly Breakdown: {result.get('original_task', task_description)}**

📋 **Step-by-Step Plan:**{steps_text}

⏱️ **Total Time:** {result.get('total_estimated_time', estimated_duration)} minutes
📈 **Difficulty:** {result.get('difficulty_level', 'medium').title()}

🌟 **Success Tips:**
{chr(10).join('• ' + tip for tip in result.get('success_tips', []))}"""
        
        except Exception as e:
            return self._fallback_breakdown_response(prompt)
    
    def _handle_priority_assessment_request(self, prompt: str) -> str:
        """Handle priority assessment requests using the PriorityAssessmentTool."""
        try:
            # Extract tasks and context from prompt
            tasks = self._extract_tasks_list(prompt)
            energy_level = self._extract_energy_level(prompt)
            
            if not tasks:
                return "I'd love to help prioritize your tasks! Could you tell me what tasks you're trying to organize?"
            
            # Use the actual priority assessment tool
            priority_tool = PriorityAssessmentTool()
            tool_result = priority_tool._run(
                tasks=tasks,
                deadline_info="",
                user_context=f"Energy level: {energy_level}/10"
            )
            
            # Parse the JSON result and format for user
            import json
            result = json.loads(tool_result)
            
            priority_text = ""
            prioritized_tasks = result.get('prioritized_tasks', [])
            for i, task in enumerate(prioritized_tasks, 1):
                if isinstance(task, dict):
                    task_name = task.get('task', f'Task {i}')
                    priority = task.get('priority_score', 'N/A')
                    reasoning = task.get('reasoning', '')
                    
                    priority_text += f"\n{i}. **{task_name}**\n"
                    priority_text += f"   Priority Score: {priority}\n"
                    if reasoning:
                        priority_text += f"   � {reasoning}\n"
                else:
                    priority_text += f"\n{i}. **{task}**\n"
            
            return f"""🎯 **ADHD-Smart Task Prioritization** (Energy Level: {energy_level}/10)

📋 **Recommended Order:**{priority_text}

🧠 **ADHD Strategy Tips:**
{chr(10).join('• ' + tip for tip in result.get('recommendations', []))}"""
        
        except Exception as e:
            return self._fallback_priority_response(prompt)
    
    def _handle_general_planning_request(self, prompt: str) -> str:
        """Handle general planning requests using LLM."""
        if self.llm is not None:
            return self.llm(prompt)
        # Fallback if no LLM is provided
        return (
            "I'm here to help you plan. (No LLM available, please configure an LLM for dynamic responses.)"
        )
    
    def _calculate_focus_sessions(self, result: Dict) -> int:
        """Calculate recommended number of focus sessions."""
        # Simple heuristic based on estimated time
        estimated_minutes = result.get("estimated_minutes", 30)
        return max(1, (estimated_minutes + 14) // 15)  # Round up to 15-min sessions
    
    def _assess_difficulty(self, task: str) -> str:
        """Assess task difficulty for ADHD brain."""
        # Simple keyword-based assessment
        complex_keywords = ["research", "analyze", "plan", "organize", "write"]
        routine_keywords = ["call", "email", "schedule", "pay", "order"]
        
        task_lower = task.lower()
        
        if any(keyword in task_lower for keyword in complex_keywords):
            return "complex"
        elif any(keyword in task_lower for keyword in routine_keywords):
            return "routine"
        else:
            return "moderate"
    
    def _suggest_optimal_timing(self, context: Dict[str, Any]) -> str:
        """Suggest optimal time of day based on user context."""
        if not context:
            return "morning"
        
        energy_level = context.get("energy_level", 5)
        mood_score = context.get("mood_score", 5)
        
        if energy_level >= 7 and mood_score >= 6:
            return "morning"
        elif energy_level >= 5:
            return "afternoon"
        else:
            return "evening"
    
    def _generate_motivation_tips(self, task: str) -> List[str]:
        """Generate task-specific motivation tips."""
        return [
            "🏆 Reward yourself after each mini-session",
            "🎵 Try body doubling with focus music or study-with-me videos",
            "⚡ Start with the part that sparks your curiosity most",
            "🎯 Set a 'minimum viable progress' goal to reduce pressure",
            "🤝 Tell someone your goal for gentle accountability"
        ]
    
    def _generate_suggestions(self) -> List[str]:
        """Generate planning-specific follow-up suggestions."""
        return [
            "Would you like me to create a detailed schedule for this?",
            "Should we set up reminders and accountability check-ins?",
            "Would breaking this down further help reduce overwhelm?",
            "How does your energy typically fluctuate throughout the day?",
            "What usually motivates you to start tasks like this?"
        ]

    # Helper methods for extracting information from prompts
    def _extract_task_description(self, prompt: str) -> str:
        """Extract task description from user prompt."""
        # Simple extraction - in production, this would be more sophisticated
        prompt_lower = prompt.lower()
        
        # Look for common task indicators
        for phrase in ['write', 'create', 'complete', 'finish', 'work on', 'do']:
            if phrase in prompt_lower:
                # Extract the part after the action word
                idx = prompt_lower.find(phrase)
                task_part = prompt[idx:].split('.')[0].split('?')[0]
                return task_part.strip()
        
        # Fallback: use the first sentence
        return prompt.split('.')[0].split('?')[0].strip()

    def _extract_complexity_level(self, prompt: str) -> str:
        """Extract complexity level from prompt."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['complex', 'difficult', 'hard', 'challenging']):
            return 'high'
        elif any(word in prompt_lower for word in ['simple', 'easy', 'quick', 'basic']):
            return 'low'
        else:
            return 'medium'

    def _extract_user_experience(self, prompt: str) -> str:
        """Extract user experience level from prompt."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['beginner', 'new', 'first time', 'never done']):
            return 'beginner'
        elif any(word in prompt_lower for word in ['expert', 'experienced', 'good at', 'familiar']):
            return 'expert'
        else:
            return 'intermediate'

    def _extract_task_title(self, prompt: str) -> str:
        """Extract a concise task title from prompt."""
        # Simple title extraction
        task_desc = self._extract_task_description(prompt)
        words = task_desc.split()[:5]  # First 5 words
        return ' '.join(words).title()

    def _extract_duration(self, prompt: str) -> int:
        """Extract estimated duration from prompt."""
        import re
        
        # Look for time patterns like "2 hours", "30 minutes", etc.
        time_patterns = re.findall(r'(\d+)\s*(hour|hr|minute|min)', prompt.lower())
        
        total_minutes = 60  # Default
        for number, unit in time_patterns:
            if 'hour' in unit or 'hr' in unit:
                total_minutes = int(number) * 60
            else:
                total_minutes = int(number)
            break
        
        return total_minutes

    def _extract_tasks_list(self, prompt: str) -> List[str]:
        """Extract list of tasks from prompt."""
        import re
        
        # Look for numbered lists or bullet points
        tasks = []
        
        # Pattern for numbered lists (1. task, 2. task, etc.)
        numbered_tasks = re.findall(r'\d+[.)]\s*([^0-9\n]+)', prompt)
        if numbered_tasks:
            return [task.strip() for task in numbered_tasks]
        
        # Pattern for bullet points or dashes
        bullet_tasks = re.findall(r'[•\-*]\s*([^\n•\-*]+)', prompt)
        if bullet_tasks:
            return [task.strip() for task in bullet_tasks]
        
        # Fallback: split by common separators
        if ',' in prompt:
            tasks = [task.strip() for task in prompt.split(',')]
        elif 'and' in prompt:
            tasks = [task.strip() for task in prompt.split(' and ')]
        
        return tasks[:10]  # Limit to 10 tasks

    def _extract_energy_level(self, prompt: str) -> int:
        """Extract energy level from prompt."""
        import re
        
        # Look for explicit energy mentions
        energy_patterns = re.findall(r'energy\s*(?:level\s*)?(?:is\s*)?(\d+)', prompt.lower())
        if energy_patterns:
            return min(10, max(1, int(energy_patterns[0])))
        
        # Infer from mood words
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ['tired', 'exhausted', 'low']):
            return 3
        elif any(word in prompt_lower for word in ['energetic', 'focused', 'high']):
            return 8
        else:
            return 6  # Default medium energy

    def _format_focus_chunks(self, chunks: List) -> str:
        """Format focus chunks into readable text."""
        result = ""
        for i, chunk in enumerate(chunks):
            if isinstance(chunk, int):
                result += f"• Session {(i//2)+1}: {chunk} minutes\n"
            else:
                result += f"• {chunk}\n"
        return result

    def _fallback_time_response(self, prompt: str) -> str:
        """Fallback response for time estimation."""
        return """
⏰ **Time Estimation Help**

I'd be happy to help estimate time for your task! For the most accurate ADHD-aware estimate, please tell me:

• What specific task you're working on
• How complex it seems (simple/medium/complex)
• Your experience level with this type of task

I'll provide realistic time estimates with ADHD tax and break it into focus-friendly chunks!
"""

    def _fallback_breakdown_response(self, prompt: str) -> str:
        """Fallback response for task breakdown."""
        return """
📋 **Task Breakdown Help**

I can break down any overwhelming task into ADHD-friendly steps! Please share:

• The main task you need to complete
• Roughly how long you think it might take
• Any specific challenges you're worried about

I'll create a step-by-step plan with timing and ADHD-specific tips!
"""

    def _fallback_priority_response(self, prompt: str) -> str:
        """Fallback response for priority assessment."""
        return """
🎯 **Priority Assessment Help**

I can help you prioritize tasks using ADHD-friendly criteria! Please list your tasks like:

1. Task one
2. Task two  
3. Task three

I'll consider your energy levels, urgency, and dopamine potential to suggest the best order!
"""
