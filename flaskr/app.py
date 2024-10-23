from flask import Flask, render_template, g, current_app
import sqlite3

from flask import Flask  # flask est la classe qui provient du module flask
app = Flask(__name__)   # app est l'instance de la classe flask, donc elle représente l'application

app.config['DATABASE'] = 'data.db'  #chemin vers la BDD


# Fonction pour obtenir la connexion à la BDD
def get_db():
                                    #sqlite3.row  indique à la connexion de renvoyer des lignes qui se comportent comme des dictionnaires, cela permet d'accéder aux colonnes par leyr nom

    return sqlite3.connect("data.db")                                                      # retourne les résultats sous forme de dictionnaire


# Route vers la table "product"
@app.route("/products")
def get_products():
    
    db = get_db()
    cursor = db.cursor()                                                           # la fonction get_db() permet de se connecter à la BDD
    products = cursor.execute ('SELECT * FROM product LIMIT 50').fetchall()       # récupère les données de la table product
    print(products)
    return render_template('products.html' , products = products)

# Route vers la table "customer"
@app.route("/customers")
def get_customers():
    
    db = get_db()
    cursor = db.cursor()                                                           
    customers = cursor.execute ('SELECT * FROM customer LIMIT 50').fetchall()      
    print(customers)
    return render_template('customers.html' , customers = customers)

# Route vers la table "customer_order"
@app.route("/customer_orders")
def get_customer_orders():
    
    db = get_db()
    cursor = db.cursor()                                                           
    customer_orders = cursor.execute ('SELECT * FROM customer_order LIMIT 50').fetchall()      
    print(customer_orders)
    return render_template('customer_orders.html' , customer_orders = customer_orders)

# Route vers la table "order_detail"
@app.route("/order_details")
def get_order_details():
    
    db = get_db()
    cursor = db.cursor()                                                           
    order_details = cursor.execute ('SELECT * FROM order_detail LIMIT 50').fetchall()      
    print(order_details)
    return render_template('order_details.html' , order_details = order_details)

# Route vers la table complète
@app.route("/tables")
def get_table():
    
    db = get_db()
    cursor = db.cursor()   
    requete =  '''SELECT customer.id, customer.country, customer_order.id, customer_order.invoice_nb, customer_order.invoice_date, order_detail.id, order_detail.quantity, order_detail.product_id, product.description, product.price
                  FROM customer  
                  JOIN customer_order ON customer.id  == customer_order.customer_id
                  JOIN order_detail ON customer_order.id == order_detail.order_id
                  JOIN product ON order_detail.product_id == product.id
                    LIMIT 50'''                                                        
    tables = cursor.execute(requete).fetchall()      
   
    return render_template('tables.html' , tables = tables)






def close_db(e=None):                 # close_db   vérifie si une connexion a été créé en vérifiant si g.db a été définie. Si la connexion existe, elle est fermée.            
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)  # indique à Flask d'appeler la fonction close_bd à chaque fois que le contexte de l'appli est terminé
    

  








