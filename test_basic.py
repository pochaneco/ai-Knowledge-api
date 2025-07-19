#!/usr/bin/env python3
# Simple test to check if app can be imported and run
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from app import create_app
    print("Successfully imported create_app")
    
    app = create_app('testing')
    print("Successfully created app")
    
    with app.app_context():
        from app.models import db
        db.create_all()
        print("Successfully created database tables")
        
    print("Basic functionality test passed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
