from flask import Flask, render_template, request, jsonify, session
import mysql.connector
import uuid
import os 

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ========== DATABASE CONNECTION ==========
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="learning_path_db"
    )
    return conn



# ========== RULE BASED LEARNING PATH ==========
def generate_learning_path(subject, skill_level):

    if subject.lower() == "geography":

        if skill_level.lower() == "beginner":
            path = [
                "Introduction to Geography",
                "Map Reading Basics",
                "Physical Geography",
                "Human Geography",
                "Basic GIS Tools",
                "Practice Projects"
            ]

        elif skill_level.lower() == "intermediate":
            path = [
                "Advanced Map Analysis",
                "Human & Economic Geography",
                "Remote Sensing",
                "GIS Tools",
                "Spatial Data Analysis",
                "Field Projects"
            ]

        else:
            path = [
                "Advanced GIS Systems",
                "Geospatial Data Science",
                "Remote Sensing Analysis",
                "Geographical Modeling",
                "Research Projects",
                "Professional GIS Certification"
            ]

    elif subject.lower() == "music":

        path = [
            "Music Theory Basics",
            "Instrument Practice",
            "Rhythm and Timing",
            "Composition Basics",
            "Music Production Tools",
            "Performance Practice"
        ]

    else:

        path = [
            "Fundamental Concepts",
            "Core Skills Development",
            "Intermediate Practice",
            "Advanced Tools",
            "Real World Projects",
            "Career Specialization"
        ]

    return " → ".join(path)


# ========== HOME PAGE ==========
@app.route('/')
def home():
    return render_template('index.html')


# ========== SAVE LEARNER ==========
@app.route('/save_learner', methods=['POST'])
def save_learner():

    data = request.get_json()

    # session create
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

    name = data.get('name')
    academic = data.get('academic')
    skills = data.get('skills')
    socio = data.get('socio')
    pace = data.get('pace')
    language = data.get('language')
    subject = data.get('subject')
    skill_level = data.get('skillLevel')
    goal = data.get('goal')

    conn = get_db_connection()
    cur = conn.cursor()

    # Save learner
    cur.execute("""
    INSERT INTO learners
    (name, academic, skills, socio_context, learning_pace, language, subject, skill_level, career_goal)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (name, academic, skills, socio, pace, language, subject, skill_level, goal))

    conn.commit()

    learner_id = cur.lastrowid

    # Generate path
    generated_path = generate_learning_path(subject, skill_level)

    # Save path with session
    cur.execute("""
    INSERT INTO learning_paths (learner_id, path, session_id)
    VALUES (%s,%s,%s)
    """, (learner_id, generated_path, session["user_id"]))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "learning_path": generated_path
    })


# ========== HISTORY PAGE ==========
@app.route('/history')
def history():

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
    SELECT path, created_at
    FROM learning_paths
    WHERE session_id = %s
    ORDER BY created_at DESC
    """, (session.get("user_id"),))

    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("history.html", data=data)


# ========== RUN SERVER ==========
if __name__ == "__main__":
    app.run(debug=True)