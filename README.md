AI DATABASE MANAGEMENT AGENT

A Python agent that connects to a SQLite database, detects broken or missing data, and uses Google's Gemini API to generate and apply fixes automatically.

WHAT IT DOES

The project seeds a users table with intentionally messy data — missing names, invalid emails, negative ages, null fields — then:
- Reads the current (broken) data from the database
- Sends it to Gemini with a set of cleanup rules
- Parses the AI's JSON response
- Applies the corrected values back to the database with a single UPDATE per row

EXAMPLE

Before:

(1, 'Alice', 25, 'alice@email.com')
(2, 'Bob', None, 'bobemail.com')
(3, None, 30, 'charlie@email.com')
(4, 'David', -5, 'david@email.com')
(5, 'Eve', 22, None)

After:

(1, 'Alice', 25, 'alice@email.com')
(2, 'Bob', 0, 'bob@email.com')
(3, 'Charlie', 30, 'charlie@email.com')
(4, 'David', 0, 'david@email.com')
(5, 'Eve', 22, 'eve@email.com')

CLEANUP RULES

1. Missing name → inferred from email
2 Names are capitalized
3. Invalid or missing email → repaired or generated from the name
4. All emails normalized to end in .com
5. Negative or missing age → replaced with 0

PROJECT STRUCTURE

├── main.py        # Entry point — sets up the DB, runs the agent, prints before/after

├── agent.py        # DatabaseAgent class: reads data, calls Gemini, parses & applies fixes

├── db_setup.py     # Creates the SQLite table and seeds it with broken sample data

└── .env            # Holds your GEMINI_API_KEY (not committed)


SETUP

1. Clone the repo
 git clone https://github.com/abhirami-anand/AI-Database-Management-Agent.git
cd AI-Database-Management-Agent
2. Install dependencies
 pip install google-genai python-dotenv
3. Create a .env file in the project root with your Gemini API key:
 GEMINI_API_KEY=your_key_here
4. Run it
 python main.py


REQUIREMENTS

1. Python 3.10+
2. A Gemini API key
   

NOTES

- The database (database.db) is recreated from scratch every run via db_setup.py, so it's safe to re-run repeatedly while testing.
- .env and database.db are excluded from version control via .gitignore — never commit your API key.


Author: Abhirami Anand

