from db_setup import setup_database 
from agent import DatabaseAgent

def main():

    setup_database()

    agent = DatabaseAgent("database.db")

    print("\nBEFORE:\n")
    print(agent.get_data())

    fixes =agent.get_ai_fixes()

    print("\nApplying Fixes...\n")
    agent.apply_fixes(fixes)

    print("\nAFTER:\n")
    print(agent.get_data())

    agent.close()

if __name__ == "__main__":
    main()