import speech_recognition as sr
import threading

recognizer = sr.Recognizer()

op_map = {
    "plus": "+", "add": "+", "+": "+",
    "minus": "-", "subtract": "-", "-": "-",
    "x": "*", "into": "*", "multiply": "*", "times": "*", "*": "*",
    "divide": "/", "by": "/", "over": "/", "/": "/",
    "√": "sqrt", "root": "sqrt", "route": "sqrt", "root over": "sqrt",
    "power": "**", "raised to": "**", "^": "**",
    "mod": "%", "modulo": "%", "%": "%"
}

def calculate(expr_list):
    expr = ""
    i = 0
    while i < len(expr_list):
        token = expr_list[i]
        if token == "sqrt":
            i += 1
            if i < len(expr_list):
                expr += f"({expr_list[i]}**0.5)"
        else:
            expr += str(token)
        i += 1
    try:
        result = eval(expr)
        print("Result:", result)
    except Exception as e:
        print("Invalid expression:", e)

def textToCalc(text):
    words = text.lower().split()
    expr_list = []
    for word in words:
        if word in op_map:
            expr_list.append(op_map[word])
        else:
            try:
                expr_list.append(float(word) if '.' in word else int(word))
            except:
                continue
    if expr_list:
        calculate(expr_list)
    else:
        print("Could not understand the calculation")

def listen(stop_flag, collected_texts):
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        while not stop_flag["stop"]:
            try:
                print("""\nStart speaking now (press 'Enter' once you are done)...""")
                audio = recognizer.listen(mic, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                collected_texts.append(text)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print("Error:", e)

def main_loop():
    while True:
        stop_flag = {"stop": False}
        collected_texts = []
        thread = threading.Thread(target=listen, args=(stop_flag, collected_texts))
        thread.start()

        command = input("Press Enter to stop listening and calculate (or type 'exit' to quit): ")
        if command.strip().lower() == "exit":
            stop_flag["stop"] = True
            thread.join()
            print("Exiting program.")
            break

        stop_flag["stop"] = True
        thread.join()

        full_text = " ".join(collected_texts)
        print("\nProcessing...")
        print(f"You said: {full_text}")

        print("\nCalculating...")
        textToCalc(full_text)
        print("\n")

if __name__ == "__main__":
    main_loop()
