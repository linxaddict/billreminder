from flask import request, jsonify
from flask_restful import Resource

from billreminder.extensions import db
from billreminder.http_status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_204_NO_CONTENT
from billreminder.model.models import Bill
from billreminder.model.schemas import BillSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BillsView(Resource):
    schema = BillSchema(strict=True)

    def get(self):
        bills = Bill.query.all()
        return self.schema.dump(bills, many=True)

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'error': 'No input data provided'}, HTTP_400_BAD_REQUEST

        bill, errors = self.schema.load(request.get_json())

        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        db.session.add(bill)
        db.session.commit()

        inserted_bill, errors = self.schema.dump(bill)

        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        return inserted_bill, HTTP_201_CREATED


class BillView(Resource):
    schema = BillSchema(strict=True)

    def get(self, bill_id):
        bill = Bill.query.filter(Bill.id == bill_id).first()

        if not bill:
            return {'error': 'Bill not found'}, HTTP_404_NOT_FOUND

        return self.schema.dump(bill).data, HTTP_200_OK

    def delete(self, bill_id):
        bill = Bill.query.filter(Bill.id == bill_id).first()

        if not bill:
            return {'error': 'Bill not found'}, HTTP_404_NOT_FOUND

        db.session.delete(bill)
        db.session.commit()

        return HTTP_204_NO_CONTENT

    def put(self, bill_id):
        bill = Bill.query.filter(Bill.id == bill_id).first()

        if not bill:
            return {'error': 'Bill not found'}, HTTP_404_NOT_FOUND

        json_data = request.get_json()
        if not json_data:
            return {'error': 'No input data provided'}, HTTP_400_BAD_REQUEST

        errors = self.schema.validate(json_data, db.session)
        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        bill.update(**json_data)
        update_bill, errors = self.schema.dump(bill)

        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        return update_bill, HTTP_200_OK
