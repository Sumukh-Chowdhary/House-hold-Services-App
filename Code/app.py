from flask import Flask,render_template,request,redirect,flash,url_for,session
from models import db,create_tables,Service,User,Service_Register,Service_Request
from datetime import datetime

app=Flask(__name__)
app.secret_key="mypro-sumukh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

create_tables(app)

@app.route('/')
def welcome():
    return render_template("main.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if  request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=User.query.filter_by(username=username).first()
        if username=='admin' and password=='sumukh_admin':
            session["user_id"]='198090'
            session["username"]='admin_sumukh'
            session["role"]='admin'
            return redirect(url_for('admin'))
        if user and user.blocked==1:
            flash("Your are blocked from using the website")
            return redirect(url_for('welcome'))
        elif user and user.password==password and user.role=='professional':
            session["user_id"]=user.id
            session["username"]=username
            session["role"]=user.role
            return  redirect(url_for('professional'))
        elif user and user.password==password:
            session["user_id"]=user.id
            session["username"]=user.username
            session["role"]=user.role
            flash("Login Successfully")
            return redirect(url_for("customer"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route('/signup',methods=["GET","POST"])
def  signup():
    if  request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        phone=request.form.get("phone")
        role=request.form.get("role")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        existing_username=User.query.filter_by(username=username).first()
        existing_phone=User.query.filter_by(phone=phone).first()
        existing_email=User.query.filter_by(email=email).first()
        if existing_username:
            flash("Username already exists")
            return redirect(url_for('signup'))
        elif existing_phone:
            flash("Phone number already exists")
            return redirect(url_for('signup'))
        elif existing_email:
            flash("Email already exists")
            return redirect(url_for('signup'))
        new_user=User(username=username,password=password,email=email,phone=phone,address=address,pincode=pincode,role=role)
        db.session.add(new_user)
        db.session.commit()     
        flash("Registration successful")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/admin/logout')
def logout():
    session.clear()
    flash("You Been logged out")
    return redirect(url_for('login'))

@app.route('/professional/logout')
def prof_logout():
    session.clear()
    flash("You Been logged out")
    return redirect(url_for('login'))

@app.route('/customer/logout')
def customer_logout():
    session.clear()
    flash("You Been logged out")
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if "user_id" in session and session["role"]=="admin":
        customer=User.query.filter_by(role='customer').count()
        professional=User.query.filter_by(role='professional').count()
        total_requests=Service_Request.query.count()
        return render_template("admin.html",customer=customer,professional=professional,total_requests=total_requests)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/professionals')
def admin_professionals():
    if "user_id" in session and session["role"]=="admin":
        professional=User.query.filter_by(role="professional").all()
        return render_template("admin_professionals.html",professional=professional)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/customers',methods=["GET"])
def admin_customers():
    if "user_id" in session and session["role"]=="admin":
        customer=User.query.filter_by(role="customer").all()
        return render_template("admin_customers.html",customer=customer)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/customers/search',methods=["GET"])
def admin_search_customer():
    if "user_id" in session and session["role"]=="admin":
        search=request.args.get("search",'')
        customer=User.query.filter_by(role="customer").filter(User.username.like('%'+search+'%'))
        return  render_template("admin_customers.html",customer=customer)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/customers/block/<int:customer_id>',methods=["GET","POST"])
def block_customer(customer_id):
    if "user_id" in session and session["role"]=="admin":
        customer=User.query.get(customer_id)
        if customer:
            customer.blocked=not customer.blocked
            db.session.commit()
        return redirect(url_for('admin_customers'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/professional/search',methods=["GET"])
def admin_search_professional():
    if "user_id" in session and session["role"]=="admin":
        search=request.args.get("search",'')
        professional=User.query.filter_by(role="professional").filter(User.username.like('%'+search+'%'))
        return  render_template("admin_professionals.html",professional=professional)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/professional/block/<int:professional_id>',methods=["GET","POST"])
def block_professional(professional_id):
    if "user_id" in session and session["role"]=="admin":
        professional=User.query.get(professional_id)
        if professional:
            professional.blocked=not professional.blocked
            db.session.commit()
        return redirect(url_for('admin_professionals'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/services')
def admin_services():
    if "user_id" in session and session["role"]=="admin":
        services=Service.query.all()
        return render_template("admin_services.html",services=services)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/services/add_service',methods=["POST","GET"])
def add_service():
    if "user_id" in session and session["role"]=="admin":
        if request.method=="POST":
            name=request.form.get("name")
            desc=request.form.get("desc")
            category=request.form.get("category")
            price=request.form.get("price")
            time=request.form.get("time")
            new_service=Service(name=name,desc=desc,price=price,time=time,category=category)
            db.session.add(new_service)
            db.session.commit()
            flash("Service added successfully")
            return redirect(url_for('admin_services'))
        return render_template('add_service.html')
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route('/admin/services/delete/<int:service_id>',methods=["POST"])
def delete_service(service_id):
    if "user_id" in session and session["role"]=="admin":
        Service_Register.query.filter_by(service_id=service_id).delete()
        service=Service.query.get(service_id)
        db.session.delete(service)
        db.session.commit()
        flash("Successfully Deleted")
        return redirect(url_for('admin_services'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional")
def professional():
    if "user_id" in session and session["role"]=="professional":
        professional_id=session.get('user_id')
        professional=User.query.get(professional_id)
        if not professional or professional.role!='professional':
            flash("User not in Session")
            return redirect(url_for('login'))
        registartion_detail=Service_Register.query.filter_by(user_id=professional_id).first()
        total_requests=Service_Request.query.filter_by(professional_id=professional_id).count()
        registartion_detail_name=registartion_detail.service.name if registartion_detail else "No Service"
        return render_template("professional.html",professional=professional,registartion_detail_name=registartion_detail_name,total_requests=total_requests)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional/requests")
def ser_requests():
    if "user_id" in session and session["role"]=="professional":
        professional_id=session.get('user_id')
        requests=Service_Request.query.filter_by(professional_id=professional_id).all()
        return render_template("prof_requests.html",service_requests=requests)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional/requests/accept/<int:request_id>" ,methods=["POST"])
def request_accept(request_id):
    if "user_id" in session and session["role"]=="professional":
        service_register=Service_Request.query.get(request_id)
        service_register.status="Accepted"
        db.session.commit()
        flash("Request accepted")
        return redirect(url_for('ser_requests'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional/requests/reject/<int:request_id>" ,methods=["POST"])
def request_reject(request_id):
    if "user_id" in session and session["role"]=="professional":
        service_register=Service_Request.query.get(request_id)
        service_register.status="Rejected"
        db.session.commit()
        flash("Request Rejected")
        return redirect(url_for('ser_requests'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional/requests/complete/<int:request_id>" ,methods=["POST"])
def request_complete(request_id):
    if "user_id" in session and session["role"]=="professional":
        service_register=Service_Request.query.get(request_id)
        service_register.status="Completed"
        db.session.commit()
        flash("Request Completed")
        return redirect(url_for('ser_requests'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional/register",methods=["GET","POST"])
def prof_register():
    if "user_id" in session and session["role"]=="professional":
        services=Service.query.all()
        registration=Service_Register.query.filter_by(user_id=session.get('user_id')).all()
        register_service_id=[reg.service_id for reg in registration] 
        return render_template("prof_register.html",services=services,registartion_id=register_service_id)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/professional/register/<int:service_id>",methods=["GET","POST"])
def register_service(service_id):
    if "user_id" in session and session["role"]=="professional":
        user_id=session.get('user_id')
        check_first_service=Service_Register.query.filter_by(user_id=user_id).first()
        if check_first_service:
            flash("You have already registered for this service")
            return redirect(url_for('prof_register'))
        else:
            new_register=Service_Register(service_id=service_id,user_id=user_id)
            db.session.add(new_register)
            db.session.commit()
            flash("Service Registered Successfully")
            return redirect(url_for('prof_register'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))
    
@app.route("/professional/unregister/<int:service_id>",methods=["GET","POST"])
def unregister_service(service_id):
    if "user_id" in session and session["role"]=="professional":
        user_id=session.get('user_id')
        check_first=Service_Register.query.filter_by(user_id=user_id,service_id=service_id).first()
        db.session.delete(check_first)
        db.session.commit()
        flash("Service Unregistered Successfully")
        return redirect(url_for('prof_register'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/customer")
def customer():
    if "user_id" in session and session["role"]=="customer":
        customer_id=session.get('user_id')
        customer=User.query.get(customer_id)
        if not customer or customer.role!='customer':
            flash("User not in Session")
            return redirect(url_for('login'))
        total_requests=Service_Request.query.filter_by(customer_id=customer_id).count()
        return render_template("customer.html",customer=customer,total_requests=total_requests)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/customer/services")
def customer_services():
    if "user_id" in session and session["role"]=="customer":
        services_reg=Service_Register.query.all()
        services_details_all=[]
        for reg in services_reg:
            service=Service.query.get(reg.service_id)
            professional=User.query.get(reg.user_id)
            if service and professional:
                services_details_all.append({
                'service_id':service.id,
                'service_name':service.name,
                'service_category':service.category,
                'service_description':service.desc,
                'service_price':service.price,
                'service_time':service.time,
                'professional_id':professional.id,
                'professional_name':professional.username
                })
        return render_template("cust_services.html",services=services_details_all)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/customer/services/book/<int:service_id>",methods=["POST","GET"])
def book_service(service_id):
    if "user_id" in session and session["role"]=="customer":
        service=Service.query.get(service_id)
        professional=User.query.get(service.registrations[0].user_id)
        customer=User.query.get(session['user_id'])

        if request.method=="POST":
            if customer and professional and service:
                service_date_str=request.form['req_date']
                service_date=datetime.strptime(service_date_str,"%Y-%m-%d").date()
                service_request_placed=Service_Request(customer_id=customer.id,
                                                  professional_id=professional.id,
                                                  service_id=service.id,
                                                  service_date=service_date,
                                                  price=service.price,
                                                  status="Pending")
                db.session.add(service_request_placed)
                db.session.commit()
                flash("Service Request Placed Successfully")
                return redirect(url_for('customer_requests'))
        return render_template("book_service.html",service=service,professional=professional,customer=customer)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/customer/requests")
def customer_requests():
    if "user_id" in session and session["role"]=="customer":
        customer_id=session.get('user_id')
        service_requests=Service_Request.query.filter_by(customer_id=customer_id).all()
        return render_template("customer_requests.html",requests=service_requests)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/customer/requests/end/<int:request_id>", methods=['POST'])
def end_request(request_id):
    if "user_id" in session and session["role"]=="customer":    
        customer_id=session.get('user_id')
        service_request=Service_Request.query.get(request_id)
        db.session.delete(service_request)
        db.session.commit()
        return redirect(url_for('customer_requests'))
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

@app.route("/customer/services/search",methods=["GET"])
def services_search():
    if "user_id" in session and session["role"]=="customer":
        search_in_requests=request.args.get("search",'')
        my_search_service_query=Service.query
        my_search_user=User.query
        search_request_list=[]
        search_service_list=[]
        search_user_list=[]
        if search_in_requests:
            search_request_list=my_search_service_query.filter((Service.category.like('%'+search_in_requests+'%'))).all()
            search_service_list=my_search_service_query.filter((Service.name.like('%'+search_in_requests+'%'))).all()
            search_user_list=my_search_user.filter(User.username.like('%'+search_in_requests+'%')).all()
        return render_template("cust_services.html",search_request_list=search_request_list,search_service_list=search_service_list,search_user_list=search_user_list)
    else:
        flash("You dont have permission to access")
        return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)