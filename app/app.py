from typing import List, Dict
from flask import Flask
from sqlalchemy import func
import json
import sys
from init import create_app
from models import db, Assignment, Realty

app = create_app()


# method which loads all records into server memory; faster but heavy
def getMatchedRealtyCount():
    matchedRealtyCount = 0

    # sorting assignments by 'most difficult' first, since they get harder to satisfy as more realties get matched
    assignments = Assignment.query.order_by(
        Assignment.min_area_living.desc(), 
        func.char_length(Assignment.post_numbers), 
        Assignment.min_floor_number.desc(), 
        Assignment.max_floor_number
    ).all()

    # sorting realties by 'most undesirable' first, since they get harder to satisfy as more realties get matched
    realties = Realty.query.order_by(
        Realty.area_living
    ).all()

    for assignment in assignments:
        realtyMatchIndex = next(iter([index for (index, realty) in enumerate(realties)
            if 
            assignment.min_floor_number <= realty.floor_number <= assignment.max_floor_number and
            realty.location_postcode in assignment.post_numbers.split(';') and
            realty.area_living >= assignment.min_area_living
        ]or []), None)

        if realtyMatchIndex:
            del realties[realtyMatchIndex]
            matchedRealtyCount += 1

    return matchedRealtyCount


# method using many queries; slow but light on server memory
def getMatchedRealtyCountOld():
    matchedRealtyIdSet = set()
    matchedRealtyCount = 0

    assignments = Assignment.query.order_by(
        Assignment.min_area_living.desc(), 
        func.char_length(Assignment.post_numbers), 
        Assignment.min_floor_number.desc(), 
        Assignment.max_floor_number).all()

    for assignment in assignments:
        realtyMatch = Realty.query.order_by(
            Realty.area_living
        ).filter(
            Realty.floor_number >= assignment.min_floor_number,
            Realty.floor_number <= assignment.max_floor_number,
            Realty.location_postcode.in_(assignment.post_numbers.split(';')),
            Realty.area_living >= assignment.min_area_living,
            Realty.id.notin_(matchedRealtyIdSet)
        ).first()

        if realtyMatch:
            matchedRealtyIdSet.add(realtyMatch.id)
            matchedRealtyCount += 1

    return matchedRealtyCount


@app.route('/')
def index() -> str:
    return json.dumps({'matched assignments': getMatchedRealtyCount()}, indent = 2)

@app.route('/old')
def oldMethod() -> str:
    return json.dumps({'(old method) matched assignments': getMatchedRealtyCountOld()}, indent = 2)    

if __name__ == '__main__':
    app.run(host='0.0.0.0')