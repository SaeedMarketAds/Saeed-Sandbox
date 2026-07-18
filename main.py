import sys
from inference import InferenceEngine

def main():
    print("========================================")
    print("  Saeed Logic - Local AI System  ")
    print("========================================")
    print("Type 'exit' or 'خروج' to quit.\n")

    try:
        engine = InferenceEngine()
    except Exception as e:
        print(f"Error loading engine: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['خروج', 'exit']:
                print("Closing Saeed Logic...")
                break
                
            if not user_input.strip():
                continue

            bot_response = engine.get_response(user_input)
            print(f"Saeed Logic: {bot_response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            sys.exit(0)

if __name__ == "__main__":
    main()
