import json
import difflib
from flask import Flask, render_template, request



data = json.load(open("data.json"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/definitions', methods =["POST"])
def definitions():
    user_input = request.form['input_text']

    def definitions(word):
        all_definitions = f'<h2> Word: {word} </h2> <br>\n'
        for num,definition in enumerate((data[word])):
            all_definitions += f'{num+1}. {definition} <br> \n'
        return(all_definitions)
        
    def suggest(word):
        suggestions = f'<h2> You also might be interested at: </h2> <br> \n'
        idx = 0
        for key in data.keys():
            if word in key and word != key:
                idx += 1
                suggestions += f'{idx}. {key} <br> \n'
            if idx == 5:  # break not to overwhem
                return(suggestions)
        if idx == 0:  # if no suggestions
            suggestions = ''
        return(suggestions)


    def get_word(word):
        if word in data:
            return(definitions(word))

        elif word.lower() in data:
            return(definitions(word.lower()))

        elif word.capitalize() in data:
            return(definitions(word.capitalize()))

        elif word.upper() in data:
            return(definitions(word.upper()))
        else:
            return(get_close_match(word))
        
    def get_close_match(word):
        
        close_match = difflib.get_close_matches(word, data.keys(), n=1)
        if close_match:
            close_match = close_match[0]
            return f"{word} does not exists in the dictionary. Maybe you ment '{close_match}' ?"
        else:
            return(f"Sorry we couldn't find the word {word} in our dictionary!")

    get_definition = get_word(user_input) 
    get_suggestion = suggest(user_input)


    return render_template("index.html", definitions = get_definition, suggestions = get_suggestion)


if __name__ == "__main__":
    app.run(debug=True)