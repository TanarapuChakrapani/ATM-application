from flask import Flask,request,redirect,url_for,render_template,make_response,flash
from datetime import datetime
app=Flask(__name__)
app.secret_key=b'\xb6\xec\x8f\xaf\xe1'
Registration_users_details={}
Statements={}
@app.route('/')
def main():
    return render_template('index.html')
@app.route('/Registration',methods=['GET','POST'])
def Registration():
    if request.method=='POST':
        username=request.form['UserName']
        userphonenumber=request.form['PhoneNumber']
        userEmail=request.form['Email']
        userpassword=request.form['Password']
        userCpassword=request.form['CPassword']
        
        if userpassword==userCpassword:
            finalpassword=userCpassword
        else:
            flash('Password Missmatched Please Enter Carefully')
        # STORING REGISTRATION DATA
        if username not in Registration_users_details:
            Registration_users_details[username]={
            'userphonenumber':userphonenumber,
            'userEmail':userEmail,
            'finalpassword':finalpassword,
            'Amount':0
            }

            # STATEMENTS
            if username not in Statements:
                Statements[username]={'Deposite_statement':[],
                                    'Withdraw_statement':[]}
            flash('Registration Successfull')
            return redirect(url_for('Login')) 
        else:
            flash('user already existed!')
    return render_template('Registration.html')
@app.route('/Login',methods=['GET','POST'])
def Login():
    if request.method=='POST':
        login_username=request.form['username']
        login_password=request.form['password']
        if login_username in Registration_users_details:
            stored_password=Registration_users_details[login_username]['finalpassword']
            if stored_password==login_password:
                resp=make_response(redirect(url_for('Dashbord')))
                resp.set_cookie('user',login_username)
                return resp
            else:
                flash('Incorrect Password')
        else:
            flash('Invalid Username')
    return render_template('Login.html')
@app.route('/Dashbord')
def Dashbord():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        return render_template('Dashbord.html',username=username)
    return redirect(url_for('Login'))
@app.route('/Deposite',methods=["GET","POST"])
def Deposite():
    if request.cookies.get('user'):
        if request.method=='POST':
            deposite_amount=int(request.form['amount'])
            if deposite_amount>0:
                if deposite_amount<=50000:
                    if deposite_amount%100==0: 
                        username=request.cookies.get('user') # user data in cookie
                        Registration_users_details[username]['Amount']=Registration_users_details[username]['Amount']+deposite_amount
                        Deposite_time=datetime.now() #Generates current time
                        Deposite_data=(deposite_amount,Deposite_time)
                        Statements[username]['Deposite_statement'].append(Deposite_data)
                        flash('Amount Deposited In Your Account')
                        return render_template('Deposite.html')
                        # return redirect(url_for('Balance'))
                    else:
                        flash('Amount should be in Multiplies of 100₹')
                        return render_template('Deposite.html')
                else:
                    flash('Deposite limit is 50000')
                    return render_template('Deposite.html')
            else:
                flash('amount should be Posite Value')
                return render_template('Deposite.html')
        else:
            return render_template('Deposite.html')
    return redirect(url_for('Login'))
@app.route('/Withdraw',methods=['GET','POST'])
def Withdraw():
    if request.cookies.get('user'):
        if request.method== 'POST':
            Withdraw_amount=int(request.form['amount']) #300
            username=request.cookies.get('user') #fetch user name from cookie data who have
            balance_amount=Registration_users_details[username]['Amount']
            if Withdraw_amount>0:
                if Withdraw_amount%100==0:
                    if balance_amount>=Withdraw_amount:
                        Registration_users_details[username]['Amount']=balance_amount-Withdraw_amount
                        Withdraw_time=datetime.now() #Generates current time
                        Withdraw_data=(Withdraw_amount,Withdraw_time)
                        Statements[username]['Withdraw_statement'].append(Withdraw_data)
                        flash('Withdraw Successfull')
                        return render_template('Withdraw.html')
                    else:
                        flash('Insufficient balance')
                        return render_template('Withdraw.html')
                else:
                    flash('Amount should be in Multiplies of 100₹')
                    return render_template('Withdraw.html')
            else:
                flash('amount should be Posite Value')
                return render_template('Withdraw.html')
        else:
            return render_template('Withdraw.html')
    else:
        return redirect(url_for('Login'))
@app.route('/Balance')
def Balance():
    if request.cookies.get('user'):
        balance_amount=Registration_users_details[request.cookies.get('user')]['Amount']
        return render_template('Balance.html',balance_amount=balance_amount)
    else:
        flash('Please Login to check balance')
        return redirect(url_for('Login'))

@app.route('/userstatements')
def userstatements():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        Deposite_statement_info=Statements[username]['Deposite_statement']
        Withdraw_statement_info=Statements[username]['Withdraw_statement']
        return render_template('ministatement.html',Deposite_statement_info=Deposite_statement_info, Withdraw_statement_info= Withdraw_statement_info)
    else:
        flash('Please Login to check statement')
        return redirect(url_for('Login'))
@app.route('/userlogout')
def userlogout():
    if request.cookies.get('user'):
        resp=make_response(redirect(url_for('Login')))
        resp.delete_cookie('user')
        return resp
    else:
        flash('Please Login to Logout')
        return redirect(url_for('Login'))
@app.route('/userAcDel')
def userAcDel():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        Registration_users_details.pop(username)
        resp=make_response(redirect(url_for('index')))
        resp.delete_cookie('user')
        return resp
    else:
        flash('Please Login to Logout')
        return redirect(url_for('Login'))
app.run(debug=True,use_reloader=True)