
from budget_app import app

from flask import Flask, render_template, request, redirect, session, flash

from budget_app.models import users, main_bills ,budget, sub_bills

@app.route('/expenses/<int:id>/new_sub_bill') 
def new_sub_bill(id):
    if 'user_info' not in session:
        return redirect ('/')
    use = users.User.get_one_by_id({'id': session['user_info']})
    main = main_bills.Main_bill.get_bill_by_id({'id':id})
    return render_template('create_sub_bill.html', use = use, main = main)
    
@app.route('/expenses/new_sub_bill/create', methods = ['POST'])
def create_sub_bill():
    if 'user_info' not in session:
        return redirect ('/')
    print('reached data inpuit')

    data = {
        'sub_bill_name' : request.form['sub_bill_name'],
        'amount' : request.form['amount'],
        'main_bill_id' : request.form['main_bill_id']
    }
    new_b = sub_bills.Sub_bills.save(data)
    print(f'this is the new bill{new_b}')
    return redirect('/dashboard')

@app.route('/expenses/<int:id>/sub_bill_delete')
def delete_subbill(id):
    if 'user_info' not in session:
        return redirect ('/')
    sub_bills.Sub_bills.delete_sub_bill({'id':id})
    return redirect('/dashboard')


@app.route("/expenses/<int:id>/sub/edit")
def updateSubBill(id):
    sub_bill = sub_bills.Sub_bills.getById({"id":id})

    return render_template("edit_sub_bill.html", sub_bill = sub_bill)



@app.route("/expenses/edit/<int:id>/sub" ,methods = ['POST'])
def updatesubBill(id):
#firgure out validation on all things that need it lol
    data = {
        'id' : id,
        'sub_bill_name' : request.form['sub_bill_name'],
        'amount' : request.form['amount'],
        'main_bill_id' : request.form['main_bill_id']
    }
    sub_bills.Sub_bills.update_sub_bill(data)

    return redirect('/dashboard')