"""Organization Agent - Tidy Tech for ADHD-friendly organization and structure."""

from textwrap import dedent
from typing import List, Dict, Any
from .base import BaseADHDAgent


class OrganizationAgent(BaseADHDAgent):
    """Tidy Tech - ADHD-Friendly Organization Specialist Agent."""
    
    def __init__(self, llm=None):
        super().__init__(
            role="Tidy Tech - ADHD Organization and Structure Specialist",
            goal="Help users create sustainable, ADHD-friendly organization systems for information, spaces, and routines",
            backstory=dedent("""
                You are an organization specialist who understands that traditional 
                organization advice often fails for ADHD brains. You know:
                - ADHD brains need visible, external structure
                - "Out of sight, out of mind" is very real for ADHD
                - Complex systems are abandoned; simple systems are used
                - Perfectionism is the enemy of functional organization
                - Dopamine-driven organization works better than obligation-driven
                - Executive dysfunction affects maintenance of systems
                
                You help create "good enough" systems that work with ADHD traits,
                not against them. Your focus is on functional over beautiful,
                simple over comprehensive, and sustainable over perfect.
            """),
            tools=self.get_specialized_tools(),
            max_iter=2,
            llm=llm
        )
    
    def get_specialized_tools(self) -> List:
        """Return organization-specific tools."""
        # These would be imported from organization_tools when created
        return []
    
    def create_organization_system(self, area: str, challenges: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create ADHD-friendly organization system."""
        
        system_description = f"""
        Design an ADHD-friendly organization system for: {area}
        
        Current challenges: {', '.join(challenges)}
        
        ADHD considerations:
        - Visual accessibility (can't organize what you can't see)
        - Low maintenance requirements
        - Dopamine-friendly and rewarding to use
        - Resilient to "mess-ups" and restarts
        - Accommodates hyperfocus and executive dysfunction cycles
        """
        
        result = self.execute_with_context(
            task_description=system_description,
            context=context or {},
            expected_output="ADHD-friendly organization system with specific steps"
        )
        
        # Enhanced response with organization-specific elements
        result.update({
            "system_type": "adhd_friendly_organization",
            "difficulty_level": self._assess_system_difficulty(area, challenges),
            "maintenance_frequency": self._determine_maintenance_schedule(area),
            "visual_elements": self._suggest_visual_aids(area),
            "backup_plans": self._create_backup_strategies(challenges)
        })
        
        return result
    
    def _process_request(self, prompt: str) -> str:
        """Process organization requests with ADHD-friendly approaches using LLM."""
        if self.llm is not None:
            return self.llm(prompt)
        # Fallback if no LLM is provided
        return (
            "I'm here to help you organize. (No LLM available, please configure an LLM for dynamic responses.)"
        )
    
    def _assess_system_difficulty(self, area: str, challenges: List[str]) -> str:
        """Assess the difficulty level of organizing this area."""
        
        complex_areas = ["office", "paperwork", "digital files", "closet", "garage"]
        simple_areas = ["desk", "bag", "counter", "nightstand"]
        
        area_lower = area.lower()
        challenge_complexity = len(challenges)
        
        if any(complex_area in area_lower for complex_area in complex_areas) or challenge_complexity >= 4:
            return "challenging"
        elif any(simple_area in area_lower for simple_area in simple_areas) and challenge_complexity <= 2:
            return "beginner_friendly"
        else:
            return "moderate"
    
    def _determine_maintenance_schedule(self, area: str) -> Dict[str, str]:
        """Determine realistic maintenance schedule."""
        
        schedules = {
            "high_traffic": {
                "daily": "2-minute pickup",
                "weekly": "10-minute reset", 
                "monthly": "system review"
            },
            "medium_traffic": {
                "daily": "quick visual scan",
                "weekly": "5-minute tidy",
                "monthly": "organization check"
            },
            "low_traffic": {
                "weekly": "quick check",
                "monthly": "light maintenance",
                "quarterly": "full review"
            }
        }
        
        # Determine traffic level based on area
        area_lower = area.lower()
        if any(high_area in area_lower for high_area in ["desk", "kitchen", "bathroom", "entryway"]):
            return schedules["high_traffic"]
        elif any(med_area in area_lower for med_area in ["bedroom", "office", "living"]):
            return schedules["medium_traffic"]
        else:
            return schedules["low_traffic"]
    
    def _suggest_visual_aids(self, area: str) -> List[str]:
        """Suggest visual organization aids for ADHD brains."""
        
        base_visual_aids = [
            "📋 Clear labels with pictures or icons",
            "🌈 Color-coding system (3 colors max)",
            "📦 Transparent storage containers",
            "🎯 Visual progress tracking"
        ]
        
        area_lower = area.lower()
        
        # Area-specific visual aids
        if "desk" in area_lower or "office" in area_lower:
            base_visual_aids.extend([
                "📌 Visible to-do list or kanban board",
                "📅 Large calendar or planner",
                "🗂️ Desktop file sorter with labels"
            ])
        
        if "closet" in area_lower or "bedroom" in area_lower:
            base_visual_aids.extend([
                "👔 Outfit planning area",
                "🏷️ Clothing category labels",
                "📊 Seasonal rotation system"
            ])
        
        if "kitchen" in area_lower:
            base_visual_aids.extend([
                "🥫 Pantry inventory list",
                "📋 Meal planning board",
                "⏰ Timer station for cooking"
            ])
        
        return base_visual_aids[:6]  # Limit to avoid overwhelm
    
    def _create_backup_strategies(self, challenges: List[str]) -> List[Dict[str, str]]:
        """Create backup strategies for common ADHD organization challenges."""
        
        strategies = []
        
        for challenge in challenges:
            challenge_lower = challenge.lower()
            
            if "overwhelm" in challenge_lower or "too much" in challenge_lower:
                strategies.append({
                    "challenge": "Feeling overwhelmed",
                    "backup_strategy": "15-minute rule: Set timer, work for 15 minutes only",
                    "reset_method": "Focus on ONE category or surface"
                })
            
            if "maintain" in challenge_lower or "keep up" in challenge_lower:
                strategies.append({
                    "challenge": "Hard to maintain system",
                    "backup_strategy": "Lower the bar: aim for 70% organized",
                    "reset_method": "Weekly 10-minute 'good enough' reset"
                })
            
            if "find" in challenge_lower or "lose" in challenge_lower:
                strategies.append({
                    "challenge": "Can't find things",
                    "backup_strategy": "One designated 'landing zone' for important items",
                    "reset_method": "Daily 2-minute item return routine"
                })
            
            if "perfectionism" in challenge_lower or "all or nothing" in challenge_lower:
                strategies.append({
                    "challenge": "Perfectionism paralysis",
                    "backup_strategy": "Good enough is good enough",
                    "reset_method": "Progress over perfection mantra"
                })
        
        # Add default backup if no specific matches
        if not strategies:
            strategies.append({
                "challenge": "System breakdown",
                "backup_strategy": "Restart small: choose one tiny area",
                "reset_method": "No shame, just begin again"
            })
        
        return strategies[:4]  # Limit to key strategies
    
    def _generate_suggestions(self) -> List[str]:
        """Generate organization-specific follow-up suggestions."""
        return [
            "Which part of this system feels most doable to start with?",
            "Would you like help setting up a maintenance routine?",
            "Should we simplify this further or add any visual elements?",
            "How does your space typically get disorganized?",
            "Would accountability or body doubling help with implementation?"
        ]
