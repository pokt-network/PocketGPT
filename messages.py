def get_messages(code: str, description: str):
    return [
        {"role": "system", "content": "You are a senior software engineer."},
        {
            "role": "user",
            "content": "I will provide you all of the source code and documentation for our project. Files will be delineated by --- FILENAME: {{filename}} --- and whitespace. You will then help me implement a solution in Go to task at hand.",
        },
        {
            "role": "assistant",
            "content": "Where is the code?",
        },
        {"role": "user", "content": code},
        {
            "role": "assistant",
            "content": "Where is the task?",
        },
        {"role": "user", "content": description},
    ]


def get_messages_test():
    return [
        {"role": "system", "content": "You are a senior software engineer."},
        {
            "role": "user",
            "content": "I will provide you all of the source code and documentation for our project. Files will be delineated by --- FILENAME: {{filename}} --- and whitespace. You will then help me implement a solution in Go to task at hand.",
        },
        {
            "role": "assistant",
            "content": "Where is the code?",
        },
        {"role": "user", "content": "print(hello)"},
        {
            "role": "assistant",
            "content": "Where is the task?",
        },
        {"role": "user", "content": "print hello all"},
    ]
