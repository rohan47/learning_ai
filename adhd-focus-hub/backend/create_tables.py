#!/usr/bin/env python3
"""
Simple script to create database tables
"""
import sys
import os
import asyncio
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from database import engine, Base
from database.models import User, Task, MoodLog

async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        # Drop all tables first (for clean start)
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
