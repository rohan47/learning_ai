"""Emotional regulation and support tools for ADHD."""

from typing import Dict, Any, List, Type
import json
from datetime import datetime

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class MoodTrackingInput(BaseModel):
    current_mood: str = Field(description="Current emotional state")
    energy_level: int = Field(description="Energy level 1-10", default=5)
    stress_level: int = Field(description="Stress level 1-10", default=5)
    focus_quality: int = Field(description="Focus quality 1-10", default=5)
    sleep_quality: str = Field(description="Last night's sleep quality", default="average")


class CopingStrategiesInput(BaseModel):
    trigger_situation: str = Field(description="Situation causing distress")
    emotional_intensity: int = Field(description="Emotional intensity 1-10", default=5)
    available_time: int = Field(description="Available time in minutes", default=10)
    preferred_methods: List[str] = Field(description="Preferred coping methods", default=[])


class MotivationSupportInput(BaseModel):
    task_description: str = Field(description="Task needing motivation")
    procrastination_reason: str = Field(description="Why avoiding the task", default="overwhelming")
    personal_values: List[str] = Field(description="Personal values and goals", default=[])
    reward_preferences: List[str] = Field(description="Preferred rewards", default=[])


class MoodTrackingTool(BaseTool):
    """Tool for tracking and analyzing ADHD-related mood patterns."""
    
    name: str = "mood_tracking"
    description: str = "Track mood patterns and provide insights for ADHD emotional regulation"
    args_schema: Type[BaseModel] = MoodTrackingInput
    
    def _run(self, current_mood: str, energy_level: int = 5, stress_level: int = 5, focus_quality: int = 5, sleep_quality: str = "average") -> str:
        """Track mood and provide insights."""
        
        # Analyze mood patterns
        mood_category = self._categorize_mood(current_mood)
        
        # Calculate overall wellness score
        wellness_score = (energy_level + (10 - stress_level) + focus_quality) / 3
        
        # Sleep impact assessment
        sleep_impact = {
            "poor": -2,
            "below_average": -1,
            "average": 0,
            "good": 1,
            "excellent": 2
        }.get(sleep_quality, 0)
        
        adjusted_wellness = max(1, min(10, wellness_score + sleep_impact))
        
        # Generate insights
        insights = []
        if stress_level >= 7:
            insights.append("🚨 High stress detected - prioritize stress reduction activities")
        if energy_level <= 3:
            insights.append("⚡ Low energy - consider gentle movement or nutrition check")
        if focus_quality <= 4:
            insights.append("🎯 Focus challenges - may need environment changes or shorter work periods")
        if sleep_quality in ["poor", "below_average"]:
            insights.append("😴 Sleep affecting daily function - consider sleep hygiene strategies")
        
        # Recommendations based on mood category
        recommendations = self._get_mood_recommendations(mood_category, wellness_score)
        
        result = {
            "mood_snapshot": {
                "mood": current_mood,
                "category": mood_category,
                "energy": energy_level,
                "stress": stress_level,
                "focus": focus_quality,
                "sleep": sleep_quality,
                "wellness_score": round(adjusted_wellness, 1)
            },
            "insights": insights,
            "recommendations": recommendations,
            "tracking_tips": [
                "📊 Notice patterns between sleep, mood, and productivity",
                "🌙 Evening mood often differs from morning - track both",
                "🎭 ADHD emotions can be intense but temporary",
                "📝 Writing about feelings can help process them"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    def _categorize_mood(self, mood: str) -> str:
        """Categorize mood into broader categories."""
        mood_lower = mood.lower()
        
        positive_moods = ["happy", "excited", "energetic", "confident", "calm", "content", "motivated"]
        negative_moods = ["sad", "anxious", "frustrated", "overwhelmed", "angry", "stressed", "depressed"]
        neutral_moods = ["okay", "neutral", "tired", "bored", "restless"]
        
        if any(word in mood_lower for word in positive_moods):
            return "positive"
        elif any(word in mood_lower for word in negative_moods):
            return "challenging"
        else:
            return "neutral"
    
    def _get_mood_recommendations(self, category: str, wellness_score: float) -> List[str]:
        """Get mood-specific recommendations."""
        if category == "positive" and wellness_score >= 7:
            return [
                "🚀 Great energy for tackling challenging tasks",
                "📅 Consider planning ahead while feeling good",
                "💪 Use this momentum for difficult conversations or decisions",
                "🌟 Practice gratitude to anchor this positive state"
            ]
        elif category == "challenging":
            return [
                "🤗 Be extra gentle with yourself today",
                "🔄 Focus on routine, low-stakes tasks",
                "👥 Reach out to supportive people if needed",
                "🌱 Remember: difficult emotions are temporary",
                "💝 Practice self-compassion over self-criticism"
            ]
        else:
            return [
                "⚖️ Balanced day - good for steady progress",
                "🎯 Focus on one meaningful task",
                "🌿 Add small pleasures throughout the day",
                "📈 Gentle push toward slightly challenging goals"
            ]


class CopingStrategiesTool(BaseTool):
    """Tool for providing ADHD-specific coping strategies."""
    
    name: str = "coping_strategies"
    description: str = "Provide immediate and long-term coping strategies for ADHD emotional challenges"
    args_schema: Type[BaseModel] = CopingStrategiesInput
    
    def _run(self, trigger_situation: str, emotional_intensity: int = 5, available_time: int = 10, preferred_methods: List[str] = []) -> str:
        """Provide coping strategies for current situation."""
        
        # Immediate strategies based on time available
        immediate_strategies = []
        if available_time >= 20:
            immediate_strategies.extend([
                "🚶 Take a walk outside",
                "🧘 Guided meditation or breathing exercise",
                "📝 Journal about the situation and feelings"
            ])
        elif available_time >= 10:
            immediate_strategies.extend([
                "🌬️ 4-7-8 breathing technique",
                "🤸 Light stretching or movement",
                "🎵 Listen to calming or energizing music"
            ])
        else:
            immediate_strategies.extend([
                "💨 5 deep belly breaths",
                "🧊 Hold ice cubes or splash cold water on face",
                "🗣️ Say kind words to yourself out loud"
            ])
        
        # Intensity-specific strategies
        if emotional_intensity >= 8:
            crisis_strategies = [
                "🆘 Use grounding techniques (5-4-3-2-1 method)",
                "🏃 Physical movement to release intense energy",
                "📞 Call a trusted friend or family member",
                "🩹 Focus on safety and basic needs first"
            ]
        else:
            crisis_strategies = []
        
        # ADHD-specific considerations
        adhd_strategies = [
            "🧩 Break down overwhelming situations into smaller pieces",
            "⏰ Set timers for coping activities to manage time blindness",
            "🎭 Remember that ADHD emotions are often more intense but pass more quickly",
            "🔄 Use body doubling - cope alongside someone else virtually",
            "📊 Track what works for you in different situations"
        ]
        
        # Long-term building strategies
        long_term_strategies = [
            "🌱 Build a personalized coping toolkit",
            "📚 Learn about ADHD emotional regulation",
            "👥 Connect with ADHD community for support",
            "💊 Ensure medication is optimized if using",
            "🏥 Consider therapy specializing in ADHD"
        ]
        
        # Customize based on preferences
        if "movement" in preferred_methods:
            immediate_strategies.insert(0, "🏃 Choose any movement that feels good right now")
        if "creative" in preferred_methods:
            immediate_strategies.insert(0, "🎨 Quick creative expression (draw, write, sing)")
        if "social" in preferred_methods:
            immediate_strategies.insert(0, "👥 Text or call someone who understands")
        
        result = {
            "situation_analysis": {
                "trigger": trigger_situation,
                "intensity": emotional_intensity,
                "urgency_level": "high" if emotional_intensity >= 8 else "moderate" if emotional_intensity >= 6 else "manageable",
                "available_time": available_time
            },
            "immediate_strategies": immediate_strategies,
            "crisis_strategies": crisis_strategies if crisis_strategies else ["No crisis-level intervention needed"],
            "adhd_considerations": adhd_strategies,
            "long_term_building": long_term_strategies,
            "reminder": "🌈 You've gotten through difficult moments before, and you can get through this one too. ADHD brains are resilient and creative."
        }
        
        return json.dumps(result, indent=2)


class MotivationSupportTool(BaseTool):
    """Tool for providing ADHD-specific motivation and anti-procrastination support."""
    
    name: str = "motivation_support"
    description: str = "Provide motivation strategies tailored to ADHD brain patterns"
    args_schema: Type[BaseModel] = MotivationSupportInput
    
    def _run(self, task_description: str, procrastination_reason: str = "overwhelming", personal_values: List[str] = [], reward_preferences: List[str] = []) -> str:
        """Provide motivation support for specific task."""
        
        # Analyze procrastination reason
        reason_strategies = {
            "overwhelming": [
                "🧩 Break task into micro-steps (2-minute actions)",
                "🎯 Focus on just starting, not finishing",
                "📝 Write down what specifically feels overwhelming"
            ],
            "boring": [
                "🎮 Gamify the task with points or challenges",
                "🎵 Add music or background noise",
                "⏰ Race against the clock in short bursts",
                "👥 Do it alongside someone else (body doubling)"
            ],
            "perfectionism": [
                "✅ Set 'good enough' standards",
                "⏰ Time-box the task to prevent over-polishing",
                "🎭 Give yourself permission to make mistakes",
                "📊 Focus on progress over perfection"
            ],
            "unclear": [
                "❓ Spend 5 minutes clarifying what success looks like",
                "📋 Make a simple plan or outline",
                "🎯 Identify the very first concrete action",
                "📞 Ask for clarification if needed"
            ]
        }
        
        specific_strategies = reason_strategies.get(procrastination_reason, reason_strategies["overwhelming"])
        
        # Connect to personal values
        value_connections = []
        if personal_values:
            for value in personal_values:
                value_connections.append(f"🌟 This task supports your value of '{value}' by moving you toward your goals")
        else:
            value_connections = ["🎯 Consider how this task connects to what matters most to you"]
        
        # ADHD motivation boosters
        adhd_boosters = [
            "⚡ Use your natural hyperfocus when it appears",
            "🔄 Work with your energy rhythms, not against them",
            "🎁 Promise yourself a specific reward after completion",
            "📱 Use apps or tools that provide instant feedback",
            "🌊 Ride the wave of any sudden motivation that appears"
        ]
        
        # Reward system
        reward_system = []
        if "social" in reward_preferences:
            reward_system.append("👥 Share your accomplishment with someone who celebrates you")
        if "movement" in reward_preferences:
            reward_system.append("🚶 Take a victory walk or dance party")
        if "creative" in reward_preferences:
            reward_system.append("🎨 Spend time on a creative project you love")
        if "food" in reward_preferences:
            reward_system.append("🍰 Enjoy a special treat or favorite meal")
        
        if not reward_system:
            reward_system = [
                "✅ Add it to your 'done' list and celebrate",
                "🎉 Do a little happy dance",
                "📱 Text someone about your win"
            ]
        
        # Emergency motivation protocol
        emergency_protocol = [
            "⏰ Commit to just 2 minutes",
            "📍 Change your physical location",
            "🎭 Pretend you're helping a friend with this task",
            "💡 Ask: 'What would I do if this were fun?'",
            "🔥 Remember: Action creates motivation, not the other way around"
        ]
        
        result = {
            "task_analysis": {
                "task": task_description,
                "procrastination_reason": procrastination_reason,
                "complexity_assessment": "high" if len(task_description.split()) > 20 else "moderate"
            },
            "targeted_strategies": specific_strategies,
            "value_connections": value_connections,
            "adhd_motivation_boosters": adhd_boosters,
            "reward_system": reward_system,
            "emergency_protocol": emergency_protocol,
            "mindset_shift": "🧠 ADHD brains are wired for interest, not importance. Find or create the interest hook.",
            "gentle_reminder": "💝 You don't have to want to do it. You just have to do it. Self-compassion over self-criticism."
        }
        
        return json.dumps(result, indent=2)
