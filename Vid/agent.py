import sqlite3
import os
import json
import re

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class DatabaseAgent:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_data(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def extract_json(self, text):
        text = text.strip()

        if text.startswith("```"):
            text = re.sub(r"```json|```", "", text).strip()

        match = re.search(r"\[.*\]|\{.*\}", text, re.DOTALL)

        if match:
            return match.group(0)

        raise ValueError("No valid JSON found in the text.")

    def normalize_rows(self, data):
        normalized = []

        for row in data:

            if isinstance(row, dict):
                normalized.append({
                    "id": row["id"],
                    "name": row["name"],
                    "age": int(round(row["age"])),
                    "email": row["email"]
                })

            elif isinstance(row, list):
                normalized.append({
                    "id": row[0],
                    "name": row[1],
                    "age": int(round(row[2])),
                    "email": row[3]
                })

            else:
                raise ValueError("Unknown row format")

        return normalized

    def get_ai_fixes(self):
        data = self.get_data()

        prompt = f"""
You are cleaning a broken user database.

DATA:
{data}

RULES:

- If name is NULL -> infer from email (e.g. "charlie@email.com" -> "Charlie")
- Names must be capitalized
- If email is invalid:
  - Missing '@' -> fix it
  - Missing domain -> use '@email.com'
- If email is NULL -> generate from name (e.g. eve@email.com)
- All email MUST end with '.com'
- Age must be an integer and >= 0
- If age is invalid or NULL -> replace with 0

Return ONLY valid JSON in this format:

[
  {{
    "id": 1,
    "name": "Alice",
    "age": 25,
    "email": "alice@email.com"
  }}
]
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        content = response.text

        print("\nRAW AI RESPONSE:\n")
        print(content)

        clean_json = self.extract_json(content)

        try:
            parsed = json.loads(clean_json)
        except json.JSONDecodeError:
            print("Gemini returned invalid JSON:")
            print(clean_json)
            raise

        return self.normalize_rows(parsed)

    def apply_fixes(self, fixes):
        for row in fixes:
            self.cursor.execute(
                """
                UPDATE users
                SET name = ?, age = ?, email = ?
                WHERE id = ?
                """,
                (row["name"], row["age"], row["email"], row["id"])
            )

        self.conn.commit()

    def close(self):
        self.conn.close()