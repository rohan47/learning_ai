# Copilot Instructions for ADHD Focus Hub

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is an ADHD Focus Hub project with a React TypeScript frontend and Python CrewAI backend. The system uses specialized AI agents to help users with ADHD manage their tasks, focus, emotions, organization, and learning.

## Key Technologies
- **Frontend**: React 18+ with TypeScript, modern CSS/SCSS
- **Backend**: Python with CrewAI, FastAPI, SQLAlchemy
- **AI Agents**: CrewAI multi-agent system with OpenAI integration
- **Database**: PostgreSQL with Redis for caching
- **Containerization**: Docker and Docker Compose

## Code Style Guidelines
- Use TypeScript for all frontend code with strict type checking
- Follow React functional components with hooks
- Use Pydantic models for API validation
- Follow FastAPI best practices for route organization
- Use async/await patterns for API calls
- Implement proper error handling and user feedback
- Focus on ADHD-friendly UX patterns (clear feedback, gentle reminders, positive reinforcement)

## ADHD-Specific Considerations
- Design for executive dysfunction and working memory challenges
- Provide clear, actionable steps and immediate feedback
- Use time-aware interfaces with buffer time estimates
- Implement gentle accountability without overwhelming pressure
- Consider emotional regulation and rejection sensitivity
- Support variable attention spans and energy levels

## Agent Specializations
- **Planning Agent**: Task breakdown, time estimation, priority management
- **Focus Coach**: Adaptive Pomodoro, distraction management, attention support
- **Emotional Support**: Mood tracking, coping strategies, motivation
- **Organization**: Information management, decluttering, structure
- **Learning**: Content processing, study strategies, knowledge building
