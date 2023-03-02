from flask import Flask, render_template, request,session,make_response,redirect,url_for
from database import Connection
from flask import request

app = Flask(__name__)
app.secret_key="abcdef"

@app.route('/')
def index():
    return render_template('index.html')
 

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/applyloan')
def applyloan():
    return render_template('loanapply.html')


@app.route('/agent')
def agent():
    return render_template('agentindex.html')


@app.route('/manager')
def manager():
    return render_template('managerindex.html')

# @app.route('/status')
# def status():
#     return render_template('get_status.html')


@app.route('/loandetails',methods=['GET','POST'])
def loandetails():
    email = session['email']
    # print(email)
    if request.method == 'POST':
        amt = int(request.form['uamt'])
        coll = int(request.form['ucoll'])
        typem = int(request.form['utype'])
        agentdetails = request.form['uagent']
        cnn = Connection()
        if typem == 2:
            if cnn.StoreDetails(amt,coll,7,'Home',email,agentdetails) == True:
                return render_template('success.html')
        if typem == 3:
            if cnn.StoreDetails(amt,coll,5,'Car',email,agentdetails) == True:
                return render_template('success.html')
        if typem == 4:
            if cnn.StoreDetails(amt,coll,3,'Education',email,agentdetails) == True:
                return render_template('success.html')
                    

@app.route('/signupuser',methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        pass1 = request.form.get('upass1')
        pass2 = request.form.get('upass2')
        name  = request.form.get('uname')        
        score = int(request.form.get('uscore'))
        email = request.form.get('uemail')

        # store data into database
        cnn = Connection()
        if cnn.checkuser(email) == True:
            msg = "Already existing user"
            print("Already existing user")
            return render_template ('index.html',message = msg)
        else:
            if cnn.storeUser(name,score,email,pass1) == True:
                if(pass1==pass2):
                    msg="Signup Successful !!!"
                    return render_template('index.html')
                    msg="* Password and confirm password must be same ! *"
                    return render_template('index.html',message=msg)
                else:
                    msg="Signup Failed !!!"
                    return render_template('index.html',message=msg)

@app.route('/loginUser',methods=['GET','POST'])
def loginUser():
    if request.method=='POST':
        email = request.form['uemail']
        pass1 = request.form['upass']

        # check the email and pass in the database
        cnn = Connection()
        if cnn.checkUser(email,pass1) == True:
            session['email'] = email
            return redirect (url_for("user")) 
            # print("$$$$$$$$$$$$$$$$$BHGABSDK$$$$$$$$$$$$$$$$$$$")
            # return render_template('home.html',email=email)
        else:
            msg="Invalid Credentials !!!"
            return render_template('index.html',message=msg)
    else:
        if "email" in session:
            return redirect(url_for('user'))
        return render_template('index.html')
    

@app.route('/loginAgent',methods=['GET','POST'])
def loginAgent():
    if request.method=='POST':
        agent_user = request.form['uagent']
        pass1 = request.form['upass']
        session['agent_user'] = agent_user
        cnn = Connection()
        if cnn.checkAgent(agent_user,pass1) == True:
            return redirect (url_for("agentuser")) 
            # return render_template('home.html',email=email)
        else:
            msg="Invalid Credentials !!!"
            return render_template('agentindex',message=msg)
    else:
        if "agent_user" in session:
            return redirect(url_for('agentuser'))
        return render_template('agentindex.html')


@app.route('/loginManager',methods=['GET','POST'])
def loginManager():
    if request.method =='POST':
        print("1111111111111111111111111111111111111")
        manager_user = request.form['umanager']
        pass1 = request.form['upass']
        session['manager_user'] = manager_user
        cnn = Connection()
        if cnn.checkManager(manager_user,pass1) == True:
            return redirect (url_for("manageruser")) 
            # return render_template('home.html',email=email)
        else:
            msg="Invalid Credentials !!!"
            return render_template('managerindex',message=msg)
    else:
        if "manager_user" in session:
            return redirect(url_for('manageruser'))
        return render_template('managerindex.html')

@app.route('/verifydata_agent',methods=['GET','POST'])
def verifydata_agent():
    if request.method == 'POST':
        email = request.form['uemail']
        session['email'] = email
        id = int(request.form['uid'])
        session['id'] = id
        agent_user = session['agent_user']
        cnn  = Connection()
        if cnn.verifyagent_customer(email,agent_user) == True:
            data = [()]
            emp = ()
            emp = cnn.getallloaninfo(email,id)
            data.insert(0,emp)
            print(data)
            headings = ("LOAN ID","LOAN AMOUNT",  "LOAN TYPE","INTEREST RATE", "COLLATERAL VALUE","EMAIL","AGENT ID")
            return render_template('demo.html',headings =  headings, data = data)
        else:
            return render_template('wrong.html')
        
        # if verifyuser_agent(email) == True:
        #     return render_template('success.html')

@app.route('/verifydata_manager',methods=['GET','POST'])
def verifydata_manager():
    if request.method == 'POST':
        email = request.form['uemail']
        session['email'] = email
        id = int(request.form['uid'])
        session['id'] = id
        cnn  = Connection()
        data = [()]
        emp = ()
        emp = cnn.getallloaninfo1(email,id)
        data.insert(0,emp)
        print(data)
        headings = ("LOAN ID","LOAN AMOUNT", "LOAN TYPE","INTEREST RATE","EMAIL", "COLLATERAL VALUE","Agent ID")
        print(headings)
        return render_template('demo1.html',headings =  headings, data = data)

@app.route('/user')
def user():
    if 'email' in session:
        print("22222222222222222222222")
        email = session['email']
        return render_template("home.html")
    else:
        return redirect(url_for('loginUser'))

@app.route('/agentuser')
def agentuser():
    if 'agent_user' in session:
        agent_user = session['agent_user']
        return render_template("verifydata_agent.html")
    else:
        return redirect(url_for('loginAgent'))

@app.route('/manageruser')
def manageruser():
    print("2222222222222222222222222222222222222")
    if 'manager_user' in session:
        agent_user = session['manager_user']
        return render_template("verifydata_manager.html")
    else:
        return redirect(url_for('loginManager'))

@app.route('/logout')   
def logout():
    print("%%%%%%%%%%%%%%%%%%%%%%%bhaggandy%%%%%%%%%%%%%%%%%%%%%%%")
    session.pop("email",None)
    return redirect(url_for('loginUser'))

@app.route('/logoutagent')   
def logoutagent():
    print("%%%%%%%%%%%%%%%%%%%%%%%bhaggandy%%%%%%%%%%%%%%%%%%%%%%%")
    session.pop("agent_user",None)
    return render_template('agentindex.html')

@app.route('/logoutmanager')   
def logoutmanager():
    print("%%%%%%%%%%%%%%%%%%%%%%%bhaggandy%%%%%%%%%%%%%%%%%%%%%%%")
    session.pop("manager_user",None)
    return render_template('managerindex.html')

@app.route('/addloandata')
def addloandata():
    if 'agent_user' in session:
        agent_user = session['agent_user']
        id = session['id']
        email = session['email']
        print(agent_user)
        print(type(agent_user))
        print(id)
        print(type(id))
        print(email)
        print(type(email))
        cnn =  Connection()
        if cnn.acceptedloans(email,agent_user,id) == True:
            return render_template('verifydata_agent.html')


@app.route('/addfinalloandata')
def addfinalloandata():
    if 'manager_user' in session:
        manager_user = session['manager_user']
        id = session['id']
        email = session['email']
        print(id)
        print(type(id))
        print(email)
        print(type(email))
        cnn =  Connection()
        if cnn.manageracceptedloans(email,id) == True:
            return render_template('verifydata_manager.html')


@app.route('/status')
def status():
    email = session['email']
    cnn  = Connection()
    data = []
    data = cnn.getallstatusinfo(email,3)
    # data.insert(0,emp)
    print(data)
    headings = ("LOAN ID","LOAN AMOUNT",  "LOAN TYPE","INTEREST RATE", "COLLATERAL VALUE","EMAIL","AGENT ID","STATUS")
    return render_template('get_status.html',headings =  headings, data = data)


@app.route('/deduct_emi')
def deduct_emi():
    if 'email' in session:
        email = session['email']
       ## loanid = session['id']
        cnn = Connection()
        if cnn.deduct_emi(1) == True:
            return render_template('emi_deducted.html')


@app.route('/add_rejected_loandata')
def add_rejected_loandata():
    if 'agent_user' in session:
        agent_user = session['agent_user']
        id = session['id']
        email = session['email']
        print(agent_user)
        print(type(agent_user))
        print(id)
        print(type(id))
        print(email)
        print(type(email))
        cnn =  Connection()
        if cnn.rejectedloans(email,agent_user,id) == True:
            return render_template('verifydata_agent.html')
        else:
            return render_template('wrong.html')

    elif 'manager_user' in session: 
        manager_user = session['manager_user']
        id = session['id']
        email = session['email']
        print(id)
        print(type(id))
        print(email)
        print(type(email))
        cnn =  Connection()
        if cnn.rejectedloans1(email,manager_user,id) == True:
            return render_template('verifydata_manager.html')
        else:
            return render_template('wrong.html')  


if __name__ == "__main__":
    app.run(debug = True)
