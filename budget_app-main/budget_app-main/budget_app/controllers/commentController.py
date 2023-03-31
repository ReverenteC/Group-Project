from budget_app import app

from flask import Flask, render_template, request, redirect, session, flash

from budget_app.models import users, main_bills ,budget, comment

@app.route("/form/submit", methods = ['POST'])
def postComment():
    data = {
        "comment":  request.form['comments'],
        "user_id": session['user_info'], 
        "main_bill_id":request.form['main_bill_id'],
    }
    comment.Comment.save(data)
    if not comment.Comment.validate_post(data):
        return redirect('/dashboard')
    return redirect('/dashboard')

