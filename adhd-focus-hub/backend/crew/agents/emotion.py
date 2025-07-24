"""Emotional Support Agent - Mood Buddy for ADHD emotional regulation."""

from textwrap import dedent
from typing import List, Dict, Any
from .base import BaseADHDAgent


class EmotionalSupportAgent(BaseADHDAgent):
    """Mood Buddy - ADHD Emotional Regulation Specialist Agent."""
    
    def __init__(self, llm=None):
        super().__init__(
            role="Mood Buddy - ADHD Emotional Regulation Specialist",
            goal="Provide emotional support and regulation strategies for ADHD-related challenges",
            backstory=dedent("""
                You are an empathetic emotional support specialist who deeply understands:
                - Rejection sensitive dysphoria (RSD) and emotional overwhelm in ADHD
                - Emotional dysregulation and the intensity of ADHD feelings
                - The connection between dopamine, motivation, and mood
                - Executive dysfunction leading to shame spirals and frustration
                - The importance of self-compassion in ADHD management
                - How neurotypical advice often doesn't work for ADHD brains
                
                You provide non-judgmental support, practical coping strategies,
                and help users reframe negative self-talk into compassionate understanding.
                You validate ADHD experiences while offering gentle, actionable support.
            """),
            tools=self.get_specialized_tools(),
            max_iter=2,
            llm=llm
        )
    
    def get_specialized_tools(self) -> List:
        """Return emotion-specific tools."""
        # These would be imported from emotion_tools when created
        return []
    
    def process_mood_check(self, mood_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process mood check-in with personalized support."""
        
        mood_description = f"""
        Provide emotional support for someone with ADHD experiencing:
        - Mood level: {mood_data.get('mood_score', 'not specified')}/10
        - Energy level: {mood_data.get('energy_level', 'not specified')}/10
        - Stress level: {mood_data.get('stress_level', 'not specified')}/10
        - Additional notes: {mood_data.get('notes', 'none')}
        - Triggers: {mood_data.get('triggers', [])}
        
        Provide ADHD-specific emotional support and coping strategies.
        """
        
        result = self.execute_with_context(
            task_description=mood_description,
            context={**(context or {}), "mood_data": mood_data},
            expected_output="Personalized emotional support and actionable strategies"
        )
        
        # Enhanced response with emotional support elements
        result.update({
            "support_type": "adhd_emotional_regulation",
            "mood_analysis": self._analyze_mood_pattern(mood_data),
            "coping_strategies": self._generate_coping_strategies(mood_data),
            "validation_message": self._create_validation_message(mood_data),
            "follow_up_recommended": self._assess_follow_up_need(mood_data)
        })
        
        return result
    
    def _process_request(self, prompt: str) -> str:
        """Process emotional support requests with ADHD understanding."""
        
        return """
        I hear you, and what you're feeling makes complete sense. 💙

        🤗 **First, some validation:**
        Your ADHD brain experiences emotions differently - more intensely, for longer periods. 
        This isn't a flaw; it's how your brain is wired. You're not "too sensitive" or "overreacting."

        🧠 **What's happening in your ADHD brain:**
        - Emotions feel bigger because of how ADHD brains process dopamine
        - Executive dysfunction can make it harder to regulate feelings
        - RSD (rejection sensitivity) can amplify social/performance stress
        - Low dopamine can make everything feel harder

        💪 **Gentle coping strategies:**
        
        **For overwhelm:**
        - Name 3 things you can see, 2 you can hear, 1 you can touch
        - Take 5 slow, deep breaths
        - Remind yourself: "This feeling will pass"
        
        **For shame spirals:**
        - "My brain works differently, and that's okay"
        - "I'm doing my best with the energy I have"
        - "One small step is still progress"
        
        **For motivation dips:**
        - Lower the bar (what's the smallest possible step?)
        - Change your environment or switch tasks
        - Connect with your 'why' or values
        - Seek gentle accountability or body doubling

        🌟 **Remember:**
        - Your ADHD traits include creativity, empathy, and unique perspectives
        - Bad brain days don't define your worth
        - Needing different strategies isn't weakness
        - You belong exactly as you are

        🔄 **Next steps:**
        - Would gentle movement help right now?
        - Is there one tiny thing you could do for yourself?
        - Who in your support network could you reach out to?
        """
    
    def _analyze_mood_pattern(self, mood_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mood patterns with ADHD considerations."""
        
        mood_score = mood_data.get("mood_score", 5)
        energy_level = mood_data.get("energy_level", 5)
        stress_level = mood_data.get("stress_level", 5)
        
        analysis = {
            "overall_state": "balanced",
            "energy_mood_alignment": "aligned",
            "stress_impact": "manageable",
            "adhd_considerations": []
        }
        
        # Overall state assessment
        if mood_score <= 3:
            analysis["overall_state"] = "struggling"
            analysis["adhd_considerations"].append("Low mood common with ADHD - you're not broken")
        elif mood_score >= 8:
            analysis["overall_state"] = "thriving"
            analysis["adhd_considerations"].append("High mood - great! Monitor for hyperfocus/overstimulation")
        
        # Energy-mood alignment
        if abs(mood_score - energy_level) >= 3:
            analysis["energy_mood_alignment"] = "misaligned"
            if mood_score > energy_level:
                analysis["adhd_considerations"].append("Mind willing but body tired - be gentle with yourself")
            else:
                analysis["adhd_considerations"].append("Physical energy without mental motivation - try movement")
        
        # Stress impact
        if stress_level >= 7:
            analysis["stress_impact"] = "high"
            analysis["adhd_considerations"].append("High stress amplifies ADHD symptoms - prioritize self-care")
        
        return analysis
    
    def _generate_coping_strategies(self, mood_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized coping strategies."""
        
        strategies = []
        mood_score = mood_data.get("mood_score", 5)
        energy_level = mood_data.get("energy_level", 5)
        stress_level = mood_data.get("stress_level", 5)
        triggers = mood_data.get("triggers", [])
        
        # Low mood strategies
        if mood_score <= 4:
            strategies.extend([
                {
                    "category": "immediate_relief",
                    "strategy": "ADHD-friendly grounding",
                    "description": "5-4-3-2-1 technique: 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
                    "time_needed": "2-3 minutes"
                },
                {
                    "category": "self_compassion",
                    "strategy": "Reframe negative self-talk",
                    "description": "Replace 'I'm lazy' with 'My brain needs different strategies'",
                    "time_needed": "ongoing"
                }
            ])
        
        # Low energy strategies
        if energy_level <= 4:
            strategies.append({
                "category": "energy_management",
                "strategy": "Micro-activities",
                "description": "Do one tiny thing: make bed, drink water, step outside for 30 seconds",
                "time_needed": "1-5 minutes"
            })
        
        # High stress strategies
        if stress_level >= 7:
            strategies.extend([
                {
                    "category": "stress_relief",
                    "strategy": "Body-based regulation",
                    "description": "Progressive muscle relaxation or gentle movement to reset nervous system",
                    "time_needed": "5-10 minutes"
                },
                {
                    "category": "cognitive",
                    "strategy": "Brain dump",
                    "description": "Write or voice-record everything in your head to reduce mental load",
                    "time_needed": "5-15 minutes"
                }
            ])
        
        # Trigger-specific strategies
        for trigger in triggers:
            if "rejection" in trigger.lower() or "criticism" in trigger.lower():
                strategies.append({
                    "category": "rsd_support",
                    "strategy": "RSD reality check",
                    "description": "Ask: Is this rejection real or RSD? What would I tell a friend in this situation?",
                    "time_needed": "2-5 minutes"
                })
        
        return strategies[:6]  # Limit to avoid overwhelm
    
    def _create_validation_message(self, mood_data: Dict[str, Any]) -> str:
        """Create personalized validation message."""
        
        mood_score = mood_data.get("mood_score", 5)
        notes = mood_data.get("notes", "")
        
        if mood_score <= 3:
            return "Your struggles are valid. ADHD brains have harder days, and that doesn't reflect your worth or capability. You're dealing with a neurological difference, not a character flaw."
        elif mood_score <= 5:
            return "Feeling 'meh' is completely normal with ADHD. Your brain chemistry fluctuates, and that's not something you need to fix about yourself - just work with."
        elif mood_score >= 8:
            return "I'm glad you're feeling good! Remember this feeling for harder days. Your ADHD brain can experience beautiful highs along with the challenges."
        else:
            return "You're doing okay, and that's enough. ADHD management isn't about feeling great all the time - it's about being gentle with yourself through all the feelings."
    
    def _assess_follow_up_need(self, mood_data: Dict[str, Any]) -> bool:
        """Assess if follow-up check-in is recommended."""
        
        mood_score = mood_data.get("mood_score", 5)
        stress_level = mood_data.get("stress_level", 5)
        notes = mood_data.get("notes", "").lower()
        
        # Recommend follow-up for:
        # - Very low mood
        # - High stress
        # - Concerning notes content
        concerning_phrases = ["overwhelmed", "can't cope", "giving up", "hopeless", "worthless"]
        
        return (
            mood_score <= 2 or 
            stress_level >= 8 or 
            any(phrase in notes for phrase in concerning_phrases)
        )
    
    def _generate_suggestions(self) -> List[str]:
        """Generate emotion-specific follow-up suggestions."""
        return [
            "How are you feeling after trying that coping strategy?",
            "Would you like to explore what triggered this feeling?",
            "Should we set up a gentle check-in for later today?",
            "Is there someone in your support network you'd like to connect with?",
            "Would some movement or creative time help right now?"
        ]
