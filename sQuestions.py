@app.route("/sqlist")
def index():
    """Show list of questions"""
    questions = db.execute("SELECT * FROM Question WHERE User_ID = :userid", userid=session["user_id"])

    return render_template("sQuestions.html", questions=questions)


