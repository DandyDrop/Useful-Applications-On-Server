import random
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=["GET"])
def handler():
    option = request.form.get("FUNCTION")
    if option:
        if option == "SOME_FUNCTION":
            from_index = request.form.get("from_index")
            to_index = request.form.get("to_index")
            try:
                return some_func(int(from_index), int(to_index))
            except Exception as e:
                return "Got an error:\n\n" + str(e) + \
                       '\n\nCommon mistakes:\nInvalid declaration of arguments'
              
        else:
            return "Didnt understand you"
              
    return "No command - no action"


def some_func(from_index: int, to_index: int) -> str:
    return "something"[from_index:to_index]


if __name__ == '__main__':
    app.run(host="0.0.0.0")




