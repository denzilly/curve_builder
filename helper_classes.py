from marshmallow import Schema, fields, ValidationError, validate
from datetime import datetime
import json
from openpyxl import load_workbook


file = 'input_data.xlsx'


def validate_date(date):
    today = datetime.today().date()
    if date < today:
        raise ValidationError(
            f"Date {date} must be equal or greater than today")


class InstrumentSchema(Schema):

    curve = fields.String(required=True, validate=validate.Length(min=2))
    type = fields.String(
        required=True,
        validate=validate.OneOf(["IRS", "FUT", "FRA"],
                                error="Curve type must be one of: IRS, FUT, or FRA")
    )
    effective_date = fields.Date(required=True, validate=validate_date)
    termination = fields.Date(required=True, validate=validate_date)
    rate = fields.Float(required=True)
    switch = fields.Int(required=True, validate=validate.OneOf([1, 0]))
    params = fields.Raw()
    subtype = fields.Raw()
    tenor = fields.Raw()


class NodeSchema(Schema):
    date = fields.Date(required=True, validate=validate_date)
    curve = fields.String(required=True, validate=validate.Length(min=2))
    df = fields.Float(required=True, validate=validate.Range(min=0.0, max=2.0))


def validate_object(object, schema):
    try:
        validated_object = schema.load(data=json.loads(object))
        return True, validated_object
    except ValidationError as err:
        return False, err.messages


class ExcelReader:
    def __init__(self, file):
        self.wb = load_workbook(file, data_only=True)
        self.instrument_ws = self.wb['Instruments_json']
        self.node_ws = self.wb['Nodes_json']

        self.instrument_schema = InstrumentSchema()
        self.node_schema = NodeSchema()

        self.instruments = []
        self.nodes = []

    def import_data(self, ws, schema, output_obj):

        for row in ws.rows:
            if row[0].value != None:
                success, result = validate_object(row[0].value, schema)
                if success:
                    output_obj.append(result)
                else:
                    print(row[0].value)
                    print(result)


reader = ExcelReader(file)
# reader.import_data(reader.node_ws, reader.node_schema, reader.nodes)
reader.import_data(reader.instrument_ws,
                   reader.instrument_schema, reader.instruments)
