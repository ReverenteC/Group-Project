from budget_app.config.mysqlconnection import connectToMySQL

from budget_app.models import main_bills


class Budget:
    db = 'budget_app'
    def __init__(self, data):
        self.id =data['id']
        self.user_id = data['user_id']
        self.main_bills = []

    @classmethod
    def get_main_bills_by_budget_id(cls,budget_id):
        query = "SELECT budget.*, main_bills.* FROM budget LEFT JOIN main_bills ON budget.id = main_bills.budget_main_bills_id WHERE budget.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, budget_id)
        main_bill_list = []
        this_budget = cls(result[0])
        for i in result:
            print(i)
            data ={
                "id" : i ['main_bills.id'],
                "bill_type" : i["bill_type"],
                "created_at" : i['main_bills.created_at'],
                "updated_at" : i['main_bills.updated_at'],
                "budget_main_bills_id" :['budget_main_bills_id']
            }
            sub_bills = main_bills.Main_bill.get_Sub_bills({"id" : i["main_bills.id"]})
            main_bill = main_bills.Main_bill(data)
            if sub_bills:
                main_bill.sub_bills = sub_bills
            # main_bill_list.append(main_bill)
            this_budget.main_bills.append(main_bill)
        # this_budget.main_bills.append(main_bill_list)
        print(this_budget)
        return this_budget
    
    @classmethod
    def get_budgets_by_user_id(cls ,data):
        query = "SELECT * FROM budget WHERE user_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        for i in results:
            print(i)
            id_to_return = i['id']
            print(id_to_return)
        return id_to_return
    