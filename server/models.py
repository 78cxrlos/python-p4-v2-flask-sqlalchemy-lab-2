from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
    #added relationship
    reviews = db.relationship('Review', back_populates='customer')

    # Add association proxy for items
    items = association_proxy('reviews', 'item')


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
    #added relationship
    reviews = db.relationship('Review', back_populates='item')

    # Add relationship to Review
    reviews = db.relationship('Review', back_populates='item')

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True
        exclude = ('reviews.customer',)

    reviews = Nested('ReviewSchema', many=True, exclude=('customer',))


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_relationships = True
        load_instance = True
        exclude = ('reviews.item',)

    reviews = Nested('ReviewSchema', many=True, exclude=('item',))


class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_relationships = True
        load_instance = True
        exclude = ('customer.reviews', 'item.reviews')

    customer = Nested(CustomerSchema, exclude=('reviews',))
    item = Nested(ItemSchema, exclude=('reviews',))