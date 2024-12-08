import json
import datetime

# Load the JSON file for chatbot categories
with open('customer_support_chatbot_restructured.json', 'r') as f:
    categories = json.load(f)

# Define keywords for each category
category_keywords = {
    "Product Information": ["spec", "price", "features", "model", "product"],
    "Order Status": ["order", "status", "shipping", "delivery", "track"],
    "Returns and Refunds": ["return", "refund", "exchange", "refunds", "return policy"],
    "Technical Support": ["error", "problem", "issue", "support", "technical"],
    "General FAQs": ["faq", "help", "questions", "contact", "general"]
}

# Define positive and negative sentiment keywords
positive_keywords = ["good", "great", "happy", "excellent", "love", "satisfied", "awesome", "thank"]
negative_keywords = ["bad", "poor", "angry", "disappointed", "sad", "hate", "upset", "worst"]

# Admin password (for simplicity, we use a hardcoded password)
ADMIN_PASSWORD = "admin123"

# Log interactions to a JSON file
def log_interaction(query, category, response, sentiment, language):
    """Logs user interactions to a JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "query": query,
        "category": category,
        "response": response,
        "sentiment": sentiment,
        "language": language
    }
    try:
        # Append to an existing log file or create a new one
        with open('chatbot_interactions.json', 'r') as log_file:
            logs = json.load(log_file)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    with open('chatbot_interactions.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)

# Admin login
def admin_login():
    print("Admin Login")
    password = input("Enter admin password: ")
    if password == ADMIN_PASSWORD:
        return True
    else:
        print("Incorrect password.")
        return False

# Display categories
def display_categories():
    print("Available categories:")
    for i, category in enumerate(categories.keys(), start=1):
        print(f"{i}. {category}")

# Function to categorize a query using keyword matching
def categorize_query(user_query):
    user_query = user_query.lower()
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in user_query:
                return category
    return "General FAQs"  # Default category if no match is found

# Function to detect sentiment of the user query
def detect_sentiment(user_query):
    user_query = user_query.lower()
    positive_count = sum(1 for word in positive_keywords if word in user_query)
    negative_count = sum(1 for word in negative_keywords if word in user_query)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

# Function to get a response based on the selected category and language
def get_response(user_query, selected_category, selected_language):
    data = categories[selected_category]
    for i, sample_query in enumerate(data["Queries"]):
        if sample_query.lower() in user_query.lower():
            return data["Responses"][selected_language][i]
    return "Sorry, I couldn't understand that. Please try again."

# Admin function to update or add responses
def update_responses():
    category_name = input("Enter the category name to update or add responses to: ")
    
    # Check if the category exists
    if category_name not in categories:
        print(f"Category {category_name} not found.")
        return
    
    print(f"Selected Category: {category_name}")
    
    action = input("Do you want to add a new response or update an existing one? (add/update): ").lower()
    
    if action == "add":
        new_query = input("Enter the new query: ")
        new_response_en = input("Enter the response for this query in English: ")
        new_response_es = input("Enter the response for this query in Spanish: ")
        new_response_bn = input("Enter the response for this query in Bengali: ")
        categories[category_name]["Queries"].append(new_query)
        categories[category_name]["Responses"]["en"].append(new_response_en)
        categories[category_name]["Responses"]["es"].append(new_response_es)
        categories[category_name]["Responses"]["bn"].append(new_response_bn)
        print("New query and responses added successfully.")

    elif action == "update":
        existing_query = input("Enter the query to update: ")
        if existing_query in categories[category_name]["Queries"]:
            index = categories[category_name]["Queries"].index(existing_query)
            new_response_en = input(f"Enter the new response for '{existing_query}' in English: ")
            new_response_es = input(f"Enter the new response for '{existing_query}' in Spanish: ")
            new_response_bn = input(f"Enter the new response for '{existing_query}' in Bengali: ")
            categories[category_name]["Responses"]["en"][index] = new_response_en
            categories[category_name]["Responses"]["es"][index] = new_response_es
            categories[category_name]["Responses"]["bn"][index] = new_response_bn
            print("Response updated successfully.")
        else:
            print("Query not found in the selected category.")
    else:
        print("Invalid action. Please enter 'add' or 'update'.")
    
    # Save the updated categories back to the JSON file
    with open('customer_support_chatbot_restructured_multilingual.json', 'w') as f:
        json.dump(categories, f, indent=4)
    print("Changes saved successfully.")

# Function to view logs and filter them by category or date
def view_logs():
    try:
        with open('chatbot_interactions.json', 'r') as log_file:
            logs = json.load(log_file)
        
        if not logs:
            print("No logs found.")
            return
        
        filter_option = input("Would you like to filter logs by category or date? (category/date/none): ").lower()
        
        if filter_option == "category":
            category_filter = input("Enter category to filter by: ").lower()
            filtered_logs = [log for log in logs if category_filter in log["category"].lower()]
            print_logs(filtered_logs)
        
        elif filter_option == "date":
            date_filter = input("Enter date (YYYY-MM-DD): ")
            filtered_logs = [log for log in logs if log["timestamp"].startswith(date_filter)]
            print_logs(filtered_logs)
        
        else:
            print_logs(logs)

    except FileNotFoundError:
        print("Log file not found.")

def print_logs(logs):
    if logs:
        for log in logs:
            print(f"\nTimestamp: {log['timestamp']}")
            print(f"Query: {log['query']}")
            print(f"Category: {log['category']}")
            print(f"Response: {log['response']}")
            print(f"Sentiment: {log['sentiment']}")
            print(f"Language: {log['language']}")
            print("-" * 50)
    else:
        print("No matching logs found.")

# Main chatbot function
def chat():
    print("Welcome to the Customer Support Chatbot!")
    
    # Language selection
    language = input("Select your language (en for English, es for Spanish, bn for Bengali): ").lower()
    while language not in ['en', 'es', 'bn']:
        print("Invalid language selection. Please choose 'en', 'es', or 'bn'.")
        language = input("Select your language (en for English, es for Spanish, bn for Bengali): ").lower()
    
    print(f"You selected {language.upper()} language.")
    
    while True:
        print("\nMenu:")
        print("1. Start a chat session")
        print("2. View or filter logs")
        print("3. Admin options")
        print("0. Exit")
        menu_choice = input("Please select an option: ")

        if menu_choice == "0":
            print("Chatbot: Goodbye!")
            break
        elif menu_choice == "1":
            display_categories()
            category_choice = input("Choose a category (by number): ")
            try:
                selected_category = list(categories.keys())[int(category_choice) - 1]
                print(f"You selected: {selected_category}")
                while True:
                    user_query = input(f"\nAsk a question related to {selected_category}: ")
                    if user_query.lower() in ["exit", "quit", "back"]:
                        print("Returning to main menu...\n")
                        break
                    
                    # Categorize query and get response
                    response = get_response(user_query, selected_category, language)
                    sentiment = detect_sentiment(user_query)
                    log_interaction(user_query, selected_category, response, sentiment, language)
                    print(f"Chatbot: {response} (Sentiment: {sentiment})")
            except (ValueError, IndexError):
                print("Invalid category choice. Returning to main menu...\n")
        elif menu_choice == "2":
            view_logs()
        elif menu_choice == "3":
            if admin_login():
                print("Welcome, Admin!")
                admin_action = input("Would you like to update responses or add new ones? (yes/no): ").lower()
                if admin_action == "yes":
                    update_responses()
                else:
                    print("Returning to main menu.")
            else:
                print("Access denied. Returning to main menu.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    chat()
