"""
@app.route("/question", methods=["GET", "POST"])
@login_required
def question():

    # Get question
    if request.method == "GET":
        return render_template("studentform.html")
    if request.method == "POST":
        if not request.form.get("title"):
            return error ("Please provide a question title.")

        # Post form question to database
        db.execute("INSERT INTO project (title, description, code, id) VALUES(:title, :description, :code, :id)",
                    title = request.form.get("title"), description = request.form.get("description"), code = request.form.get("code"), id=session["user_id"])
        # Return to main forum
    return redirect(url_for("index"))
 """