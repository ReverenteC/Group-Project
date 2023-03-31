
from budget_app import app

from flask import Flask, render_template, request, redirect, session, flash


from budget_app.models import users, main_bills ,budget, comment,sub_bills


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def register_form():

    return render_template('index.html')

@app.route('/create', methods = ['POST'])
def register():

    if request.form['action'] == 'register':

        if not users.User.validate(request.form):
            return redirect('/')

        pw_hash = bcrypt.generate_password_hash(request.form["password"])

        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password': pw_hash
        
        }

        user_info = users.User.save(data)

        # budget.Budget.save({"id" : user_info})

        session['user_info'] = user_info
        


    else:


        user_info = users.User.get_onewith_email ({'email': request.form['email'].lower()})
        print(user_info)
        if user_info:
            if len(request.form['password']) < 8:
                flash("Incorrect password")
                return redirect("/")
            if bcrypt.check_password_hash(user_info.password, request.form['password']):
                session["user_info"] = user_info.id
                return redirect("/dashboard")
            else:
                flash("Incorrect Password")
                return redirect("/")
        else:
            flash("No user with this email")
            return redirect("/")
        
    return redirect ("/dashboard")


@app.route("/dashboard")
def dash():
    if 'user_info' in session:
        current_user = session['user_info']
        # expense = main_bills.Main_bill.get_all_from_id({'id' : session['user_info']})
        id =budget.Budget.get_budgets_by_user_id({'id' : session['user_info']})
        expense = budget.Budget.get_main_bills_by_budget_id({"id" :id})
        all_comments = comment.Comment.get_all()
        return render_template("home.html", user = current_user, expense = expense, use = users.User.get_one_by_id({'id': session['user_info']}), comments = all_comments)

@app.route('/user/<int:id>/update')
def update_user_page(id):

    if 'user_info' not in session:
        return redirect('/')
    print('asiduahidhiodhwodwodwodnoq')

    return render_template('edit.html', user = users.User.get_one_by_id({'id': session['user_info']}))


@app.route('/user/<int:id>/info/update', methods = ['POST']) 
def update_user(id):

    print('this is wokring')
    if 'user_info' not in session:
        return redirect('/')

#firgue out validation

    data={
            "id":id,
            "email":request.form["email"],
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],

    }

    users.User.update(data)
    print(f'ththth {data}')
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
