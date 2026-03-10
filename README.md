# Learning Path Generator

A Flask-based web application that generates personalized learning paths based on learner profiles and preferences.

## Features

### 1. **Learner Profile Management**
- Captures comprehensive learner information including:
  - Name and academic background
  - Skills assessment
  - Socio-economic context
  - Learning pace preference
  - Language preference
  - Subject selection
  - Current skill level (Beginner/Intermediate/Advanced)
  - Career goals

### 2. **Dynamic Learning Path Generation**
- Rule-based path generation engine
- Subject-specific pathways (e.g., Geography, Music)
- Skill-level appropriate content sequencing
- Structured progression from fundamentals to advanced topics

### 3. **Session Management**
- Unique user session tracking using UUID
- Persistent session storage via Flask sessions
- Cross-request user identification

### 4. **Learning History Tracking**
- Stores all generated learning paths per user session
- Timestamp-based history organization
- Descending chronological order display

### 5. **MySQL Database Integration**
- Uses `mysql-connector-python` for database connectivity
- Compatible with macOS without requiring MySQL development libraries
- Two main tables:
  - `learners`: Stores learner profile data
  - `learning_paths`: Stores generated paths with session tracking

## Tech Stack

- **Backend Framework**: Flask 3.1.2
- **Database Driver**: mysql-connector-python (no compilation required)
- **Database**: MySQL
- **Template Engine**: Jinja2
- **Session Management**: Flask sessions with UUID-based user tracking

## Project Structure

```
Learning Path Project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Home page with learner form
│   └── history.html      # Learning path history display
└── README.md             # Project documentation
```

## Installation & Setup

### Prerequisites
- Python 3.x installed
- MySQL server running locally
- Database `learning_path_db` created in MySQL

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- flask==3.1.2
- mysql-connector-python
- jinja2==3.1.6
- werkzeug==3.1.3
- itsdangerous==2.2.0
- blinker==1.9.0
- click==8.3.0
- colorama==0.4.6

### Step 2: Database Configuration

Ensure your MySQL server is running and the database exists:

```sql
CREATE DATABASE learning_path_db;
```

Update database credentials in `app.py` (lines 11-15):

```python
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",              # Your MySQL username
        password="DB Passwords",   # Your MySQL password
        database="learning_path_db"
    )
    return conn
```

### Step 3: Create Database Tables

Run the following SQL commands to create required tables:

```sql
CREATE TABLE learners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    academic TEXT,
    skills TEXT,
    socio_context TEXT,
    learning_pace VARCHAR(50),
    language VARCHAR(50),
    subject VARCHAR(100),
    skill_level VARCHAR(50),
    career_goal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE learning_paths (
    id INT AUTO_INCREMENT PRIMARY KEY,
    learner_id INT,
    path TEXT,
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## How It Works

### 1. **Home Page (`/`)**
- User fills out a comprehensive learner profile form
- Data is submitted via POST to `/save_learner`

### 2. **Learner Data Processing (`/save_learner`)**
- Receives JSON data from the frontend
- Creates/retrieves user session using UUID
- Inserts learner profile into `learners` table
- Calls `generate_learning_path()` function
- Stores generated path in `learning_paths` table
- Returns the generated learning path as JSON

### 3. **Path Generation Logic**
The `generate_learning_path(subject, skill_level)` function:
- Takes subject and skill level as inputs
- Applies rule-based logic for different subjects
- Generates 6-step sequential learning paths
- Returns path as arrow-separated string (e.g., "Topic 1 → Topic 2 → ...")

**Example Paths:**

**Geography - Beginner:**
```
Introduction to Geography → Map Reading Basics → Physical Geography → 
Human Geography → Basic GIS Tools → Practice Projects
```

**Music - All Levels:**
```
Music Theory Basics → Instrument Practice → Rhythm and Timing → 
Composition Basics → Music Production Tools → Performance Practice
```

### 4. **History Page (`/history`)**
- Retrieves all learning paths for current session
- Displays paths in descending order of creation time
- Shows timestamp for each generated path

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with learner form |
| `/save_learner` | POST | Save learner data and generate path |
| `/history` | GET | View learning path history |

## Session Management

- Each user gets a unique UUID stored in Flask session
- Session persists across requests during browser session
- Learning paths are linked to session ID for history tracking
- Secret key configured in `app.secret_key`

## Key Features in Code

### Database Connection Helper
```python
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hardik@9981",
        database="learning_path_db"
    )
    return conn
```

### Rule-Based Path Generator
- Supports multiple subjects with differentiated paths
- Three difficulty levels (beginner/intermediate/advanced)
- Fallback generic path for unsupported subjects

### Session-Aware Data Storage
```python
if "user_id" not in session:
    session["user_id"] = str(uuid.uuid4())
```

## Advantages

✅ **No Compilation Required**: Uses pure Python MySQL driver  
✅ **macOS Compatible**: No need for MySQL development libraries  
✅ **Session Tracking**: Persistent user identification across requests  
✅ **History Feature**: Users can view past learning paths  
✅ **Extensible**: Easy to add new subjects and difficulty levels  
✅ **Structured Data**: Normalized database schema with foreign keys  

## Future Enhancements

- [ ] Add more subjects and specialized learning paths
- [ ] Implement AI-based path personalization
- [ ] User authentication and persistent profiles
- [ ] Progress tracking for completed steps
- [ ] Resource recommendations for each step
- [ ] Export learning paths as PDF
- [ ] Admin dashboard for managing paths
- [ ] RESTful API for mobile app integration

## Troubleshooting

### MySQL Connection Error
If you see connection errors:
1. Verify MySQL server is running
2. Check username/password in `get_db_connection()`
3. Ensure database `learning_path_db` exists
4. Confirm MySQL is listening on localhost

### Session Not Working
Make sure `app.secret_key` is set in the Flask app configuration.

### Import Errors
Install all dependencies:
```bash
pip install -r requirements.txt
```

## License

This project is open-source and available for educational purposes.

## Contact

For questions or contributions, please reach out to the project maintainer.
