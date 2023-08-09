#IMporting required Libraries
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.models.products import Products
from app.models.address import Address
from app.models.users import Users
from app.models.orders import Orders
from app import db

from flask_cors import cross_origin

# Creating Views Blueprint
views = Blueprint('views', __name__, url_prefix="/")

#setting views' origin
@views.route('/')
#Calling Cross Origin method
@cross_origin()

#Opening login.html to login
def login():
    try:
        return render_template("/login/login.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

#setting new origin to dashboard
@views.route('/dashboard')
#Calling Cross Origin method
@cross_origin()
#Get data from sql and display in dashboard.html
def dashboard():
    try:
        query = "select * from products;"
        products = db.engine.execute(query).all()
        return render_template("/dashboard/dashboard.html", products=products, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

#setting new origin to profile
@views.route('/profile')
#Calling Cross Origin method
@cross_origin()
# function profile to get data via sql injection and display via profile.html
def profile():
    try:
        user_id = request.args.get("id")
        user_query = f"select * from users where id='{user_id}';"
        user = db.engine.execute(user_query).first()
        order_query = f"select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id;"
        orders = db.engine.execute(order_query).all()
        ticket_query = f"select * from tickets where user_id='{user['id']}';"
        tickets = db.engine.execute(ticket_query).all()
        address_query = f"select * from address where user_id='{user['id']}'"
        addresses = db.engine.execute(address_query).all()
        return render_template("/profile/profile.html", user=user, orders=orders, addresses=addresses, tickets=tickets, user_id=session.get("user_id"))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

#setting new origin to order
@views.route('/order')
#Calling Cross Origin method
@cross_origin()
# function order to get data via sql injection and display via order.html
def order():
    try:
        product_id = request.args.get("id")
        if not product_id:
            return jsonify({
                "message": "No product for purchase!",
                "status": "error"
            }), 400
        query = f"select * from products where id={product_id};"
        product = db.engine.execute(query).first()
        address_query = f"select * from address where user_id='{session.get('user_id')}'"
        addresses = db.engine.execute(address_query).all() or []
        return render_template("/order/order.html", product=product, addresses=addresses, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

#setting new origin to help
@views.route("/help")
#Calling Cross Origin method
@cross_origin()
# function help-page display order.html
def help_page():
    try:
        return render_template("/help/help.html", user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

#special route for editor where we can edit code and see output
@views.route("/editor")
#Calling Cross Origin method
@cross_origin()
#Displaing editor.html
def editor():
    try:
        return render_template("/editor/editor.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400