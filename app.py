from flask import Flask, render_template, request, redirect, session, url_for
from random import randint

app = Flask(__name__)
app.secret_key = 'maedeh-secret-key'

@app.route("/", methods=["GET", "POST"])
def index():
    if "round" not in session:
        session["round"] = 1
        session["score"] = 0

    message = ""
    random_num = randint(0, 10)

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
        except ValueError:
            message = "🚫 Please enter a valid number!"
            return render_template("index.html", round=session["round"], score=session["score"], message=message)

        correct_num = int(request.form["random_num"])

        if guess < 0 or guess > 10:
            message = "⚠️ Please enter a number between 0 and 10!"
        elif guess == correct_num:
            session["score"] += 1
            message = f"✅ Great! You guessed {guess} and the number was {correct_num}."
        else:
            message = f"❌ Nope! You guessed {guess}, but the number was {correct_num}."

        session["round"] += 1

        if session["round"] > 10:
            return redirect(url_for("result"))

    return render_template("index.html", round=session["round"], score=session["score"], message=message, random_num=random_num)

@app.route("/result")
def result():
    score = session.get("score", 0)
    if score == 10:
        message = "🎉 Perfect! You guessed all right!"
    elif score >= 7:
        message = "🔥 Great job!"
    elif score >= 4:
        message = "🙂 Not bad!"
    elif score >= 1:
        message = "😬 You tried!"
    else:
        message = "😢 You lose!"

    session.clear()
    return render_template("result.html", score=score, message=message)

if __name__ == "__main__":
    app.run(debug=True)
