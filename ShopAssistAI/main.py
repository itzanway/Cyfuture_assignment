from src.agent import execution_node

def main():
    print("--- ShopAssist AI Initialized ---")
    print("(Type 'quit' to exit)")
    
    chat_history = []
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        # Update state
        chat_history.append({"role": "user", "content": user_input})
        state = {"messages": [type('obj', (object,), {'content': user_input})], "intent": ""}
        
        # Run Agent
        result = execution_node(state)
        response = result["messages"][0]
        
        print(f"Agent: {response}")
        print("-" * 20)

if __name__ == "__main__":
    main()