# ADHD Focus Hub

> AI-powered ADHD management system with specialized CrewAI agents for focus, planning, emotional support, organization, and learning.

## 🧠 Overview

ADHD Focus Hub is a comprehensive platform designed specifically for individuals with ADHD. It features a multi-agent AI system powered by CrewAI, with each agent specializing in different aspects of ADHD management:

- **Plan-It Pro** 📋 - Task planning and breakdown specialist
- **Focus Friend** 🎯 - Attention management and focus sessions
- **Mood Buddy** 💙 - Emotional regulation and support
- **Tidy Tech** 🗂️ - Organization and structure systems
- **Study Smart** 📚 - Learning optimization and strategies

## ✨ Features

### 🤖 Multi-Agent AI System
- Intelligent routing to appropriate specialists
- Context-aware responses based on user state
- Conversation history and learning (trimmed to a configurable limit)
- ADHD-specific understanding and support

### 🎯 Focus Management
- Adaptive Pomodoro sessions (15-45 minutes)
- Distraction management techniques
- Environment optimization suggestions
- Hyperfocus awareness and breaks

### 📋 Task Planning
- Task breakdown into 15-minute chunks
- Time estimates with "ADHD tax" buffer
- Priority assessment based on energy levels
- Dopamine-driven task ordering

### 💙 Emotional Support
- Mood tracking and analysis
- Rejection sensitivity dysphoria (RSD) support
- Coping strategy recommendations
- Gentle, non-judgmental guidance

### 🗂️ Organization Systems
- ADHD-friendly organization methods
- Visual and accessible storage solutions
- Maintenance schedules and backup plans
- "Good enough" philosophy over perfectionism

### 📚 Learning Optimization
- Multi-sensory learning approaches
- Interest-driven study plans
- Memory retention techniques
- Accommodations for executive dysfunction

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional)
- OpenAI API key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd adhd-focus-hub
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
# or with uv: uv sync

# Run the backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 5. Using Docker (Recommended)
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start all services
../scripts/dev_compose.sh
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

The default `docker-compose.yml` is optimized for local development. It mounts
the source code into the containers and enables automatic reloads when files
change. For a production deployment, use
`docker-compose.production.yml` which builds the images once and runs them
without any source-code volumes. You can start it with
`../scripts/prod_compose.sh`. All configuration values should be supplied via
environment variables.

## 🏗️ Project Structure

```
adhd-focus-hub/
├── backend/                    # Python FastAPI backend
│   ├── crew/                   # CrewAI agents and orchestration
│   │   ├── agents/             # Specialized ADHD agents
│   │   │   ├── planning.py     # Plan-It Pro agent
│   │   │   ├── focus.py        # Focus Friend agent
│   │   │   ├── emotion.py      # Mood Buddy agent
│   │   │   ├── organize.py     # Tidy Tech agent
│   │   │   └── learning.py     # Study Smart agent
│   │   ├── tools/              # Agent-specific tools
│   │   └── crew.py             # Main orchestrator
│   ├── api/                    # FastAPI application
│   │   ├── main.py             # Main app and routes
│   │   └── models.py           # Pydantic models
│   └── requirements.txt
├── frontend/                   # React TypeScript frontend
│   ├── src/
│   │   ├── components/         # Reusable components
│   │   ├── pages/              # Page components
│   │   └── services/           # API integration
│   └── package.json
├── docker-compose.yml          # Full stack orchestration
├── .env.example               # Environment template
└── README.md
```

## 🔧 Configuration

### Required Environment Variables

```env
# OpenAI API (required for AI agents)
OPENAI_API_KEY=your_openai_api_key_here

# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:password@localhost:5432/adhd_focus_hub

# Redis (for caching and sessions)
REDIS_URL=redis://localhost:6379

# Application security
SECRET_KEY=your_secret_key_here

# Environment
ENVIRONMENT=development

# Frontend
REACT_APP_API_URL=http://localhost:8000
# Max conversation history to keep
CREW_MAX_HISTORY=50
```

## 🤖 AI Agents

### Plan-It Pro (Planning Agent)
- Breaks down overwhelming tasks into manageable steps
- Provides ADHD-aware time estimates with buffer time
- Considers energy levels and dopamine motivation
- Offers gentle accountability without pressure

### Focus Friend (Focus Coach)
- Adaptive Pomodoro sessions (15-45 minutes)
- Distraction management and environment optimization
- Hyperfocus awareness and transition support
- Movement breaks and sensory regulation

### Mood Buddy (Emotional Support)
- Rejection sensitive dysphoria (RSD) support
- Emotional regulation strategies
- Mood tracking and pattern recognition
- Self-compassion and reframing techniques

### Tidy Tech (Organization)
- ADHD-friendly organization systems
- Visual accessibility and external structure
- Low-maintenance, sustainable approaches
- "Good enough" over perfectionism

### Study Smart (Learning)
- Multi-sensory and interest-driven learning
- Executive function accommodations
- Memory and retention optimization
- Adaptive study session planning

## 🌟 ADHD-Specific Features

### Time Management
- **ADHD Tax**: Built-in buffer time for transitions and distractions
- **Variable Sessions**: 15-45 minute focus blocks based on capacity
- **Energy Matching**: Task recommendations based on current energy

### Emotional Regulation
- **RSD Support**: Specialized guidance for rejection sensitivity
- **Gentle Redirection**: Non-judgmental approach to focus drift
- **Validation**: Acknowledgment of neurological differences

### Executive Function Support
- **External Structure**: Visual organization and reminders
- **Task Chunking**: Breaking overwhelming projects into steps
- **Flexible Systems**: Accommodating chaos phases and restarts

### Motivation & Dopamine
- **Interest-Driven**: Starting with engaging aspects first
- **Immediate Rewards**: Quick wins and progress celebration
- **Variety**: Multiple approaches to prevent boredom

## 🔌 API Endpoints

### Chat with AI Agents
```
POST /api/v1/chat
{
  "message": "I'm feeling overwhelmed with my project",
  "context": {
    "mood_score": 4,
    "energy_level": 6
  }
}
```

### Task Planning
```
POST /api/v1/tasks/breakdown
{
  "title": "Write research paper",
  "description": "10-page paper on climate change",
  "estimated_duration": 180
}
```

### Focus Sessions
```
POST /api/v1/focus/start
{
  "task_description": "Work on presentation slides",
  "requested_duration": 25,
  "distraction_level": 7
}
```

### Mood Tracking
Store a mood entry and optionally request emotional support.

```
POST /api/v1/moods
{
  "mood_score": 6,
  "energy_level": 4,
  "stress_level": 8,
  "notes": "Feeling scattered today"
}
```

For a mood analysis without saving to your log:

```
POST /api/v1/mood/log
{
  "mood_score": 6,
  "energy_level": 4,
  "stress_level": 8,
  "notes": "Feeling scattered today"
}
```

## 🧪 Development

### Running Tests
```bash
# Run the entire test suite
python test_tools.py

# Backend tests only
cd backend
pytest

# Frontend tests
cd ../frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
black .
isort .
flake8

# Frontend linting
cd frontend
npm run lint
```

## 🚀 Deployment

### Docker Production
```bash
# Build and run production containers
../scripts/prod_compose.sh
```
This compose file uses the Docker images defined in the repository and does not
mount the application source code. Provide all secrets and URLs through
environment variables before running the stack.

### Manual Deployment
1. **Backend**: Deploy to Railway, Render, or similar Python hosting
2. **Frontend**: Deploy to Vercel, Netlify, or similar static hosting
3. **Database**: Use managed PostgreSQL (AWS RDS, Digital Ocean, etc.)
4. **Redis**: Use managed Redis service


## 🙏 Acknowledgments

- Built with love for the ADHD community
- Powered by CrewAI for multi-agent intelligence
- Designed with ADHD-specific needs in mind
- Focused on compassion and understanding

## 💡 ADHD-Friendly Usage Tips

- **Start Small**: Try one feature at a time
- **Be Patient**: The AI learns your patterns over time
- **Customize**: Adjust settings to match your needs
- **Self-Compassion**: Remember that progress isn't linear
- **Community**: Connect with others in similar journeys

---

*Remember: You're not broken, you're differently wired. This tool is here to help you work WITH your ADHD brain, not against it.* 💙
