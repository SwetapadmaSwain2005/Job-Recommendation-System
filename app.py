"""
Job Recommendation System for Freshers
========================================
Backend Application using Flask and SQLite

Project Purpose:
- Helps freshers find suitable job roles based on their skills
- Matches user skills with job requirements
- Shows skill match percentage and missing skills
- Simple and clean architecture for easy understanding
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# ============================================================
# FUNCTION 1: Get Database Connection
# ============================================================
def get_db_connection():
    """
    PURPOSE:
    - Safely connects to SQLite database
    - Sets up row factory for easy data access
    
    HOW IT WORKS:
    - Opens connection to database.db
    - Uses Row factory so we can access columns by name
    - Returns connection object
    
    INTERVIEW ANSWER:
    "This function ensures safe database connection and allows
    us to fetch job data efficiently using named columns."
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# FUNCTION 2: Clean and Validate User Skills
# ============================================================
def clean_user_skills(skills_input):
    """
    PURPOSE:
    - Takes raw user input and converts to clean skill list
    - Removes duplicates, extra spaces, converts to lowercase
    
    HOW IT WORKS:
    - Splits input by comma
    - Removes whitespace from each skill
    - Converts to lowercase for matching
    - Removes empty strings
    
    INTERVIEW ANSWER:
    "This function validates and cleans user input to ensure
    accurate skill matching and prevent errors."
    """
    if not skills_input or skills_input.strip() == "":
        return []
    
    skills = [skill.strip().lower() for skill in skills_input.split(',')]
    skills = [skill for skill in skills if skill]  # Remove empty strings
    return list(set(skills))  # Remove duplicates


# ============================================================
# FUNCTION 3: Get All Jobs from Database
# ============================================================
def get_job_data():
    """
    PURPOSE:
    - Fetches all job roles and their required skills from database
    - Prepares data for matching algorithm
    
    HOW IT WORKS:
    - Connects to database
    - Executes SELECT query to get all jobs
    - Returns list of all job records
    
    INTERVIEW ANSWER:
    "This function loads all job requirements from the database,
    which we then use for skill matching and recommendation."
    """
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs ORDER BY role").fetchall()
    conn.close()
    return jobs


# ============================================================
# FUNCTION 4: Calculate Skill Match Percentage
# ============================================================
def calculate_match(user_skills, job_skills_string):
    """
    PURPOSE:
    - Compares user skills with job requirements
    - Calculates match percentage
    
    HOW IT WORKS:
    - Takes user skills list and job skills string
    - Converts job skills to list
    - Finds common skills using set intersection
    - Calculates: (matched skills / total job skills) × 100
    
    FORMULA:
    Match % = (Common Skills / Total Job Required Skills) × 100
    
    INTERVIEW ANSWER:
    "I use set operations to find common skills, then calculate
    percentage match. This shows how many job requirements the
    user already meets."
    
    EXAMPLE:
    User: [python, sql]
    Job: [python, sql, java]
    Common: [python, sql] = 2
    Match: (2/3) × 100 = 66%
    """
    job_skills = [skill.strip().lower() for skill in job_skills_string.split(',')]
    
    # Find common skills using set intersection
    user_skills_set = set(user_skills)
    job_skills_set = set(job_skills)
    matched_skills = user_skills_set & job_skills_set
    
    # Calculate percentage
    if len(job_skills_set) == 0:
        return 0
    
    match_percentage = int((len(matched_skills) / len(job_skills_set)) * 100)
    return match_percentage


# ============================================================
# FUNCTION 5: Find Missing Skills
# ============================================================
def find_missing_skills(user_skills, job_skills_string):
    """
    PURPOSE:
    - Identifies skills user needs to learn for specific job
    - Helps freshers understand learning gaps
    
    HOW IT WORKS:
    - Converts job skills to list
    - Uses set difference to find missing skills
    - Returns list of skills to learn
    
    INTERVIEW ANSWER:
    "This function shows freshers exactly which skills they need
    to develop to become suitable for a specific job role."
    
    EXAMPLE:
    User: [python, sql]
    Job: [python, sql, java]
    Missing: [java]  ← User must learn this
    """
    job_skills = [skill.strip().lower() for skill in job_skills_string.split(',')]
    
    user_skills_set = set(user_skills)
    job_skills_set = set(job_skills)
    
    # Missing skills = job skills - user skills
    missing_skills = job_skills_set - user_skills_set
    return sorted(list(missing_skills))


# ============================================================
# FUNCTION 6: Recommend Jobs (Main Logic)
# ============================================================
def recommend_jobs(user_skills):
    """
    PURPOSE:
    - Main recommendation engine
    - Ranks all jobs based on skill match
    - Creates final recommendation list
    
    HOW IT WORKS:
    1. Get all jobs from database
    2. For each job:
       - Calculate match percentage
       - Find missing skills
       - Store in recommendation dict
    3. Sort by match percentage (highest first)
    4. Return ranked list
    
    INTERVIEW ANSWER:
    "This is the core function that processes all jobs, calculates
    match scores, and ranks them. It's the main decision-making
    engine of the recommendation system."
    
    STEP-BY-STEP:
    1. Fetch all jobs
    2. Loop through each job
    3. Calculate match for each job
    4. Find missing skills for each job
    5. Sort by match score
    6. Return sorted list
    """
    jobs = get_job_data()
    recommendations = []
    
    for job in jobs:
        match_percentage = calculate_match(user_skills, job['skills'])
        missing_skills = find_missing_skills(user_skills, job['skills'])
        
        recommendation = {
            'job_role': job['role'],
            'match_percentage': match_percentage,
            'missing_skills': missing_skills,
            'all_required_skills': [s.strip() for s in job['skills'].split(',')],
            'user_has_skills': [s for s in user_skills if s in 
                               [x.strip().lower() for x in job['skills'].split(',')]]
        }
        
        recommendations.append(recommendation)
    
    # Sort by match percentage (highest first)
    recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    return recommendations


# ============================================================
# ROUTE 1: Home Page
# ============================================================
@app.route('/')
def index():
    """
    PURPOSE:
    - Displays home page with skill input form
    
    HOW IT WORKS:
    - Renders index.html template
    - User enters skills here
    
    INTERVIEW ANSWER:
    "This is the entry point. User lands here, enters their skills,
    and submits to the recommendation engine."
    """
    return render_template('index.html')


# ============================================================
# ROUTE 2: Process Recommendation
# ============================================================
@app.route('/recommend', methods=['POST'])
def recommend():
    """
    PURPOSE:
    - Receives user skills from form
    - Processes recommendation logic
    - Returns results page
    
    HOW IT WORKS:
    1. Get skills from form input
    2. Validate and clean skills
    3. Call recommend_jobs() function
    4. Pass results to result.html template
    5. Display recommendations to user
    
    INTERVIEW ANSWER:
    "This route handles the core recommendation logic. It receives
    user input, validates it, processes the matching algorithm,
    and returns ranked job suggestions."
    """
    # Get user input from form
    skills_input = request.form.get('skills', '')
    
    # Validate input
    if not skills_input or skills_input.strip() == "":
        return render_template('index.html', 
                             error="Please enter at least one skill")
    
    # Clean user skills
    user_skills = clean_user_skills(skills_input)
    
    if len(user_skills) == 0:
        return render_template('index.html', 
                             error="Please enter valid skills")
    
    # Get recommendations
    recommendations = recommend_jobs(user_skills)
    
    # Render results page
    return render_template('result.html', 
                         user_skills=user_skills,
                         recommendations=recommendations,
                         total_recommendations=len(recommendations))


# ============================================================
# ROUTE 3: API Endpoint for AJAX (Optional)
# ============================================================
@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """
    PURPOSE:
    - API endpoint for potential frontend AJAX calls
    - Returns JSON instead of HTML
    
    HOW IT WORKS:
    - Same logic as /recommend route
    - Returns JSON response
    - Useful for modern frontend frameworks
    
    INTERVIEW ANSWER:
    "This is an optional API endpoint that returns JSON data,
    making it easy to integrate with modern frontend frameworks."
    """
    skills_input = request.json.get('skills', '')
    user_skills = clean_user_skills(skills_input)
    
    if len(user_skills) == 0:
        return jsonify({'error': 'No valid skills provided'}), 400
    
    recommendations = recommend_jobs(user_skills)
    return jsonify({'recommendations': recommendations})


# ============================================================
# ERROR HANDLING
# ============================================================
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', 
                         error="Page not found. Please try again."), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('index.html', 
                         error="Server error. Please try again."), 500


# ============================================================
# MAIN APPLICATION ENTRY
# ============================================================
if __name__ == '__main__':
    # Check if database exists, if not show message
    if not os.path.exists('database.db'):
        print("\n" + "="*60)
        print("⚠️  DATABASE NOT FOUND!")
        print("="*60)
        print("Please run: python setup_database.py")
        print("This will create and populate the database.")
        print("="*60 + "\n")
    
    # Run Flask application
    app.run(debug=True, host='127.0.0.1', port=5000)
