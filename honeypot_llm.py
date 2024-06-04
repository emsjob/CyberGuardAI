from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import dotenv_values
import argparse
from datetime import datetime
import yaml
from time import sleep
import random
import os

config = dotenv_values(".env")
today = datetime.now()

history = open("history.txt", "a+", encoding="utf-8")

if os.stat('history.txt').st_size == 0:
    with open('personalitySSH.yml', 'r', encoding="utf-8") as file:
        identity = yaml.safe_load(file)

    identity = identity['personality']

    prompt = identity['prompt']

else:
    history.write("\nHere the session stopped. Now you will start it again from the beginning with the same user. You must respond just with starting message and nothing more. " +
                              "Make sure you use same file and folder names. Ignore date-time in <>. This is not your concern.\n")
    history.seek(0)
    prompt = history.read()

def main():
    parser = argparse.ArgumentParser(description="Simple command line with Hugging Face model")
    parser.add_argument("--personality", type=str, help="A brief summary of chatbot's personality",
                        default=prompt +
                        f"\nBased on these examples make something of your own (different username and hostname) to be a starting message. Always start the communication in this way and make sure your output ends with '$'. For the last login date use {today}\n" +
                        "Ignore date-time in <> after user input. This is not your concern.\n")

    args = parser.parse_args()

    initial_prompt = f"You are Linux OS terminal. Your personality is: {args.personality}"
    messages = [{"role": "system", "content": initial_prompt}]
    if os.stat('history.txt').st_size == 0:
        for msg in messages:
            history.write(msg["content"])
    else:
        history.write("The session continues in following lines.\n\n")

    history.close()

    model_name = "google/gemma-2b"
    token = "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"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, token=token)

    def generate_response(messages):
        prompt_text = " ".join([msg["content"] for msg in messages])
        inputs = tokenizer.encode(prompt_text, return_tensors="pt")
        outputs = model.generate(inputs, max_new_tokens=800, temperature=0.0)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    while True:
        logs = open("history.txt", "a+", encoding="utf-8")
        try:
            msg = generate_response(messages)
            message = {"content": msg, "role": 'assistant'}

            if "$cd" in message["content"] or "$ cd" in message["content"]:
                message["content"] = message["content"].split("\n")[1]

            lines = []

            messages.append(message)

            logs.write(messages[len(messages) - 1]["content"])
            logs.close()

            logs = open("history.txt", "a+", encoding="utf-8")

            if "will be reported" in messages[len(messages) - 1]["content"]:
                print(messages[len(messages) - 1]["content"])
                raise KeyboardInterrupt

            if "PING" in message["content"]:
                lines = message["content"].split("\n")
                print(lines[0])

                for i in range(1, len(lines) - 5):
                    print(lines[i])
                    sleep(random.uniform(0.1, 0.5))

                for i in range(len(lines) - 4, len(lines) - 1):
                    print(lines[i])

                user_input = input(f'{lines[len(lines) - 1]}'.strip() + " ")
                messages.append({"role": "user", "content": user_input + f"\t<{datetime.now()}>\n"})
                logs.write(" " + user_input + f"\t<{datetime.now()}>\n")

            else:
                user_input = input(f'\n{messages[len(messages) - 1]["content"]}'.strip() + " ")
                messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
                logs.write(" " + user_input + f"\t<{datetime.now()}>\n")

        except KeyboardInterrupt:
            messages.append({"role": "user", "content": "\n"})
            print("")
            break

        logs.close()

if __name__ == "__main__":
    main()
