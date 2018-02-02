from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify("Hello, world!")


# configure database settings
POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'postgres',
    'host': 'db',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# create the database interface
db = SQLAlchemy(app)

#### MODELS ####
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.String(50))
    quantity = db.Column(db.Integer)


db.create_all()

# hello world route
@app.route('/hello/<name>', methods=['GET'])
def create_user(name):
    return jsonify({'message': name})

# route to get a list of all products
@app.route('/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    output = []
    # text, complete user_id
    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['name'] = product.name
        product_data['price'] = product.price
        product_data['quantity'] = product.quantity
        output.append(product_data)

    return jsonify({"products" : output })

# route to cretae a product in the database
@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()

    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'New product created!'})

# run the flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    print('App running on port 5001.')
