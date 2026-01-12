"""
Job Recommendation System - Database Setup Script
==================================================

This script creates and initializes the SQLite database with job data.
Run this script ONCE before running the Flask app.

Command: python setup_database.py
"""

import sqlite3
import os

# =====================================================
# DATABASE SETUP FUNCTION
# =====================================================
def setup_database():
    """
    Creates database and populates with job data
    
    STEPS:
    1. Create or connect to database
    2. Create jobs table
    3. Insert job roles with required skills
    4. Commit and close
    """
    
    # Database file path
    db_file = 'database.db'
    
    # Check if database already exists
    if os.path.exists(db_file):
        print(f"⚠️  Database '{db_file}' already exists!")
        response = input("Do you want to recreate it? (yes/no): ").lower()
        if response != 'yes':
            print("Database setup cancelled.")
            return
        else:
            os.remove(db_file)
            print("Old database deleted.")
    
    # Create connection
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("\n📊 Creating database table...")
    
    # Create jobs table
    cursor.execute("""
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            skills TEXT NOT NULL,
            description TEXT
        )
    """)
    
    print("✓ Table created successfully")
    
    # Job data to insert
    jobs_data = [
        (
            "Software Developer",
            "python,java,sql,problem-solving,version-control",
            "Develops software applications using programming languages"
        ),
        (
            "Web Developer",
            "html,css,javascript,react,node.js",
            "Creates and maintains websites and web applications"
        ),
        (
            "Data Analyst",
            "python,sql,excel,tableau,statistics",
            "Analyzes data and provides business insights"
        ),
        (
            "Frontend Developer",
            "html,css,javascript,react,vue.js",
            "Develops user interface and frontend components"
        ),
        (
            "Backend Developer",
            "python,java,node.js,sql,docker",
            "Develops backend services and APIs"
        ),
        (
            "Data Scientist",
            "python,sql,machine-learning,statistics,pandas",
            "Works on ML models and predictive analytics"
        ),
        (
            "DevOps Engineer",
            "docker,kubernetes,linux,aws,jenkins",
            "Manages infrastructure and deployment pipelines"
        ),
        (
            "QA Engineer",
            "java,python,testing,selenium,automation",
            "Tests software and ensures quality"
        ),
        (
            "Business Analyst",
            "excel,sql,communication,documentation,problem-solving",
            "Analyzes business requirements and processes"
        ),
        (
            "UI/UX Designer",
            "figma,communication,problem-solving,html,css",
            "Designs user interfaces and user experiences"
        )
    ]
    
    print("\n📝 Inserting job data...")
    
    # Insert all jobs
    cursor.executemany("""
        INSERT INTO jobs (role, skills, description) 
        VALUES (?, ?, ?)
    """, jobs_data)
    
    print(f"✓ Inserted {len(jobs_data)} job roles")
    
    # Commit changes
    conn.commit()
    
    # Display inserted data
    print("\n" + "="*60)
    print("📋 DATABASE CONTENT:")
    print("="*60)
    
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    
    for job in jobs:
        print(f"\n🎯 {job[1]}")
        print(f"   Skills: {job[2]}")
    
    # Close connection
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\nDatabase file created: {db_file}")
    print("You can now run: python app.py")
    print("="*60 + "\n")


# =====================================================
# MAIN
# =====================================================
if __name__ == '__main__':
    try:
        print("\n" + "="*60)
        print("🔧 JOB RECOMMENDATION SYSTEM - DATABASE SETUP")
        print("="*60 + "\n")
        
        setup_database()
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check and try again.")
