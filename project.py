from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

polls = [
    {
        "id": 0,
        "question": "What's your favorite cuisine",
        "options": ["Indian", "Mexican", "Italian", "Carribean"],
        "votes": [8, 6, 5, 4]
    }
]

@app.route("/")
def Welcome():
    return render_template("poll_list.html", polls=polls)

@app.route("/vote")
def vote_default():
    if polls:
        return redirect(url_for("vote", poll_id = 0))
    return "No polls available", 404

@app.route("/results")
def results_default():
    if polls:
        return redirect(url_for("results", poll_id=0))
    return "No results available", 404

@app.route("/vote/<int:poll_id>", methods = ["GET, POST"])
def vote(poll_id):
    if poll_id < 0 or poll_id >= len(polls):
        return render_template("404.html", message="Results not found"), 404
    
    poll = polls[poll_id]
    if request.method == "POST":
        selected = int(request.form["option"])
        poll["votes"][selected] += 1
        return redirect(url_for("results", poll_id=poll_id))
    
    return render_template("vote.html",poll=poll,poll_id=poll_id)

@app.route("/results/<int:poll_id>")
def results(poll_id):
    if poll_id < 0 or poll_id >= len(polls):
        return render_template("404.html", message="Results not found"), 404
    
    poll = polls[poll_id]
    total_votes = sum(poll["votes"])
    percentages = [
    (opt, count, round((count / total_votes) * 100) if total_votes > 0 else 0)
    for opt, count in zip(poll["options"], poll["votes"])
    ]
    winner_index = poll["votes"].index(max(poll["votes"])) if poll["votes"] else -1
    return render_template("results.html", poll=poll, percentages=percentages, winner_index=winner_index)    

@app.route("/delete/<int:poll_id>", methods=["POST"])
def delete_poll(poll_id):
    if request.form.get("_method") == "DELETE":
        if poll_id < len(polls):
            polls.pop(poll_id)
        return redirect(url_for("Welcome"))
    return "Invalid delete request", 400

@app.route("/edit/<int:poll_id>", methods=["GET", "POST"])
def edit_poll(poll_id):
    if poll_id < 0 or poll_id >= len(polls):
        return render_template("404.html", message="Poll not found"), 404
    poll = polls[poll_id]

    if request.method == "POST" and request.form.get("_method") == "PUT":
        poll["question"] = request.form.get("question", "")
        poll["options"] = [opt for opt in request.form.getlist("option") if opt.strip()]
        poll["votes"] = [0] * len(poll['options'])
        return redirect(url_for("vote", poll_id=poll_id))
    
    return render_template("edit.html", poll=poll,poll_id=poll_id)


if __name__ == "__main__":
    app.run(debug = True)