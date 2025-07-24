"""Learning Agent - Study Smart for ADHD-friendly learning and knowledge processing."""

from textwrap import dedent
from typing import List, Dict, Any
from .base import BaseADHDAgent


class LearningAgent(BaseADHDAgent):
    """Study Smart - ADHD Learning and Knowledge Processing Specialist Agent."""
    
    def __init__(self, llm=None):
        super().__init__(
            role="Study Smart - ADHD Learning and Knowledge Specialist",
            goal="Optimize learning strategies for ADHD brains through multi-sensory, interest-driven, and adaptive approaches",
            backstory=dedent("""
                You are a learning specialist who understands how ADHD brains 
                process, retain, and retrieve information differently. You know:
                - Interest and novelty drive ADHD learning better than obligation
                - Multi-sensory approaches work better than single-mode learning
                - Information needs to be chunked and connected to existing knowledge
                - Active processing beats passive consumption
                - Movement and fidgeting can enhance learning for ADHD brains
                - Executive function challenges affect planning and follow-through
                
                You help transform boring or overwhelming learning into engaging,
                memorable experiences that work with ADHD neurology. You focus on
                strategies that leverage ADHD strengths like creativity, pattern
                recognition, and hyperfocus while accommodating challenges.
            """),
            tools=self.get_specialized_tools(),
            max_iter=2,
            llm=llm
        )
    
    def get_specialized_tools(self) -> List:
        """Return learning-specific tools."""
        # These would be imported from learning_tools when created
        return []
    
    def create_learning_plan(self, subject: str, learning_goals: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create ADHD-optimized learning plan."""
        
        learning_description = f"""
        Design an ADHD-friendly learning plan for: {subject}
        
        Learning goals: {', '.join(learning_goals)}
        
        ADHD learning considerations:
        - Interest-driven motivation over external pressure
        - Multi-sensory and active learning methods
        - Chunked information with clear connections
        - Accommodates variable attention and energy
        - Leverages hyperfocus periods productively
        - Includes movement and fidget-friendly options
        """
        
        result = self.execute_with_context(
            task_description=learning_description,
            context=context or {},
            expected_output="ADHD-optimized learning plan with specific strategies"
        )
        
        # Enhanced response with learning-specific elements
        result.update({
            "learning_type": "adhd_optimized",
            "engagement_level": self._assess_subject_engagement(subject),
            "optimal_study_sessions": self._design_study_sessions(context),
            "retention_strategies": self._suggest_retention_methods(subject),
            "motivation_hooks": self._identify_interest_hooks(subject, learning_goals)
        })
        
        return result
    
    def _process_request(self, prompt: str) -> str:
        """Process learning requests with ADHD-optimized strategies."""
        
        return """
        Let's create a learning approach that works WITH your ADHD brain! 🧠📚

        🎯 **ADHD Learning Superpowers:**
        Your brain is actually designed for certain types of learning:
        - Pattern recognition and big-picture thinking
        - Creative connections between ideas
        - Hyperfocus deep-dives when interested
        - Learning through movement and hands-on experience

        ⚡ **Your Optimized Learning Plan:**
        
        **1. Find Your Hook** 🎣
        - What's personally interesting about this topic?
        - How does it connect to your goals/interests?
        - What's the most intriguing part to start with?
        
        **2. Multi-Sensory Learning Menu** 🌈
        Choose 2-3 that appeal to you:
        - 🎵 Listen: podcasts, audiobooks, music
        - 👀 Visual: diagrams, mind maps, videos
        - ✋ Hands-on: experiments, building, writing
        - 🚶 Movement: walking while learning, fidget tools
        - 💬 Social: explaining to others, study groups
        
        **3. ADHD-Friendly Study Sessions** ⏰
        - **Micro-learning**: 15-minute focused bursts
        - **Hyperfocus windows**: longer when energy is high
        - **Active breaks**: movement between sessions
        - **Variety**: switch methods to maintain interest
        
        **4. Information Processing** 🧩
        - Start with big picture, then zoom into details
        - Create connections to existing knowledge
        - Use analogies and storytelling
        - Teach back what you learned (even to a pet!)
        
        **5. Retention Boosters** 🚀
        - Spaced repetition with apps or flashcards
        - Create silly mnemonics or memory palaces
        - Practice retrieval, not just re-reading
        - Connect learning to emotions or personal stories
        
        💡 **ADHD Study Pro Tips:**
        - Study when genuinely curious, not just when "supposed to"
        - Change locations to reset attention
        - Use timers to prevent hyperfocus burnout
        - Celebrate small learning wins
        - Have backup subjects for when main topic feels impossible
        
        🎵 **Environment Optimization:**
        - Background music or white noise (if it helps)
        - Comfortable seating that allows movement
        - Good lighting and minimal visual distractions
        - Fidget tools or stress balls
        - Water and healthy snacks nearby
        
        🧠 **Working WITH Your ADHD Brain:**
        - Low energy? Do review or passive learning
        - High energy? Tackle new, complex concepts
        - Restless? Try walking meetings or standing desk
        - Distracted? Switch subjects or take a movement break
        """
    
    def _assess_subject_engagement(self, subject: str) -> str:
        """Assess potential engagement level for the subject."""
        
        high_interest_subjects = [
            "creative", "art", "music", "storytelling", "psychology", "technology",
            "entrepreneurship", "gaming", "social justice", "innovation"
        ]
        
        medium_interest_subjects = [
            "history", "science", "languages", "cooking", "fitness", "travel",
            "personal development", "communication"
        ]
        
        subject_lower = subject.lower()
        
        if any(interest in subject_lower for interest in high_interest_subjects):
            return "naturally_engaging"
        elif any(interest in subject_lower for interest in medium_interest_subjects):
            return "moderately_interesting"
        else:
            return "requires_motivation_strategy"
    
    def _design_study_sessions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design optimal study sessions based on ADHD patterns."""
        
        base_session = {
            "micro_session": {
                "duration": "15 minutes",
                "best_for": "New concepts, review, low energy days",
                "structure": "5min warm-up + 8min focus + 2min note/reflect"
            },
            "standard_session": {
                "duration": "25-30 minutes", 
                "best_for": "Regular study, moderate energy",
                "structure": "Pomodoro with active breaks"
            },
            "hyperfocus_session": {
                "duration": "45-90 minutes",
                "best_for": "High interest topics, high energy",
                "structure": "Deep dive with gentle check-ins"
            }
        }
        
        if context and context.get("energy_level"):
            energy = context["energy_level"]
            if energy <= 4:
                base_session["recommended"] = "micro_session"
            elif energy >= 8:
                base_session["recommended"] = "hyperfocus_session"
            else:
                base_session["recommended"] = "standard_session"
        
        return base_session
    
    def _suggest_retention_methods(self, subject: str) -> List[Dict[str, str]]:
        """Suggest retention methods based on subject and ADHD brain."""
        
        methods = [
            {
                "method": "Active Recall",
                "description": "Test yourself instead of re-reading",
                "adhd_twist": "Use flashcards with rewards or gamify with apps"
            },
            {
                "method": "Spaced Repetition",
                "description": "Review at increasing intervals",
                "adhd_twist": "Use apps like Anki with interesting images/mnemonic"
            },
            {
                "method": "Teaching Back",
                "description": "Explain concepts to someone else",
                "adhd_twist": "Record yourself teaching or explain to pets/plants"
            },
            {
                "method": "Story Connections",
                "description": "Connect facts to narrative or personal experience",
                "adhd_twist": "Create wild, memorable stories with the information"
            }
        ]
        
        # Subject-specific additions
        subject_lower = subject.lower()
        
        if "math" in subject_lower or "science" in subject_lower:
            methods.append({
                "method": "Visual Problem Solving",
                "description": "Draw diagrams and visual representations",
                "adhd_twist": "Use colors and movement in diagrams"
            })
        
        if "language" in subject_lower or "writing" in subject_lower:
            methods.append({
                "method": "Immersive Practice",
                "description": "Use the language in real contexts",
                "adhd_twist": "Games, music, and social interaction in target language"
            })
        
        return methods[:5]  # Limit to prevent overwhelm
    
    def _identify_interest_hooks(self, subject: str, learning_goals: List[str]) -> List[str]:
        """Identify potential interest hooks to motivate learning."""
        
        hooks = []
        
        # Goal-based hooks
        for goal in learning_goals:
            goal_lower = goal.lower()
            if "career" in goal_lower or "job" in goal_lower:
                hooks.append("🚀 Career advancement and new opportunities")
            if "personal" in goal_lower or "hobby" in goal_lower:
                hooks.append("🎨 Personal fulfillment and creative expression")
            if "skill" in goal_lower:
                hooks.append("💪 Mastery and competence building")
        
        # Subject-based hooks
        subject_lower = subject.lower()
        
        if "technology" in subject_lower:
            hooks.append("🔧 Building cool things and solving problems")
        if "psychology" in subject_lower or "human" in subject_lower:
            hooks.append("🧠 Understanding yourself and others better")
        if "history" in subject_lower:
            hooks.append("🕰️ Wild stories from the past that shaped today")
        if "science" in subject_lower:
            hooks.append("🔬 Discovering how the world actually works")
        
        # Universal ADHD hooks
        hooks.extend([
            "🎮 Gamify learning with challenges and rewards",
            "🤝 Connect with others who share this interest",
            "🌟 Use this knowledge to help or teach others"
        ])
        
        return hooks[:5]  # Focus on most relevant hooks
    
    def _generate_suggestions(self) -> List[str]:
        """Generate learning-specific follow-up suggestions."""
        return [
            "Which learning method sounds most interesting to try first?",
            "Would you like help setting up a study schedule that works with your energy patterns?",
            "Should we explore ways to make this subject more personally relevant?",
            "Would study buddies or accountability help with motivation?",
            "How do you typically learn best when you're really interested in something?"
        ]
