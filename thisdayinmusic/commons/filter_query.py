from flask_restful import reqparse
from sqlalchemy import extract


def query_by_day_and_month(class_reference):
    parser = reqparse.RequestParser()
    parser.add_argument('month', type=int, help='Month cannot be converted')
    parser.add_argument('day', type=int, help='Day cannot be converted')
    args = parser.parse_args()

    day = args['day']
    month = args['month']

    query = class_reference.query

    if args['day'] and args['month']:
        query = query.filter(extract('month', class_reference.date) == month,
                             extract('day', class_reference.date) == day)

    return query
