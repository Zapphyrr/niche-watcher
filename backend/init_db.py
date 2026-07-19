#!/usr/bin/env python3
"""Initialize database tables"""
import sys
from database import Base, engine
from models import User, UserCredential, Post, Besthackernews

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
