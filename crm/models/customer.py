# -*- encoding:utf-8 -*-

from ..core import db


class Customer(db.Document):
    sales = db.ListField(db.ReferenceField('Sale'))
    business_name = db.StringField(max_length=140)
    rfc = db.StringField(max_length=13, min_length=10, unique=True)


    def get_sales(self):
    	return self.sales

    def set_sales(self, sales):
    	self.sales = sales

    def add_sale(self, sale):
    	self.sales.append(sale)

    def remove_sale(self, sale):
    	self.sales.remove(sale)

    def set_sale(self, index, sale):
    	self.sales.insert(index, sale)

    def get_business_name(self):
    	return self.business_name

    def set_business_name(self, business_name):
    	self.business_name = business_name

    def get_rfc(self):
    	return self.rfc

   	def set_rfc(self, rfc):
   		self.rfc = rfc
