from flask import jsonify
from flask_restful import abort, Resource
from . import db_session
from .products import Product
from .pars2 import parser


def abort_if_product_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")


class ProductsResource(Resource):
    def get(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        products = session.query(Product).get(product_id)
        return jsonify({'product': products.to_dict()})

    def delete(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        products = session.query(Product).get(product_id)
        session.delete(products)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        product = session.query(Product).all()
        return jsonify({'product': [item.to_dict() for item in product]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        product = Product(
            name=args['name'],
            price=args['price'],
            text=args['text'],
        )
        if args['image']:
            product.image = args['image']
        else:
            product.image = 'static/img/defoult_product.jpeg'
        session.add(product)
        session.commit()
        return jsonify({'success': 'OK'})