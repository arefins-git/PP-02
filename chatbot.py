import logging
from datetime import datetime

categories = {
    "queryCategories": [
        {
            "category": "Product Information",
            "sampleQueries": [
                "What is the warranty period for Product X?",
                "Does Product Y support wireless charging?",
                "What are the dimensions of Product Z?",
                "Is there a user manual available for Product X?"
            ],
            "sampleResponses": [
                "Product X comes with a one-year warranty covering manufacturing defects.",
                "Yes, Product Y supports wireless charging.",
                "The dimensions of Product Z are 5.5 x 2.7 x 0.3 inches.",
                "You can find the user manual for Product X [here]."
            ]
        },
        {
            "category": "Order Status",
            "sampleQueries": [
                "Can I change the shipping address for my order?",
                "What should I do if my order is delayed?",
                "How can I cancel my order?",
                "Will I receive a tracking number for my order?"
            ],
            "sampleResponses": [
                "Unfortunately, once an order is placed, the shipping address cannot be changed.",
                "If your order is delayed, please check the tracking link for updates or contact customer service.",
                "To cancel your order, please visit our order management page [link].",
                "Yes, you will receive a tracking number via email once your order has shipped."
            ]
        },
        # ... (rest of the categories)
    ]
}


def get_response(user_query):
    for category_data in categories["queryCategories"]:
        for i, sample_query in enumerate(category_data["sampleQueries"]):
            if sample_query.lower() in user_query.lower():
                return category_data["sampleResponses"][i]
    return "Sorry, I couldn't understand that. Please try again."


logging.basicConfig(filename='chatbot.log', level=logging.INFO)


def log_query(user_query, response):
    logging.info(f"{datetime.now()} - User: {user_query} - Bot: {response}")


def chat():
    print("Welcome to the Customer Support Chatbot!")
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        response = get_response(user_query)
        log_query(user_query, response)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    chat()
