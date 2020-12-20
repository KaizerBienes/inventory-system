from wtforms import Form, StringField, IntegerField, DecimalField, validators

class SearchInventoryValidator(Form):
    search = StringField(label='Search Key', validators=[validators.Optional()])

class GetInventoryValidator(Form):
    inventory_id = IntegerField(label='Inventory ID', validators=[validators.InputRequired()])

class CreateInventoryValidator(Form):
    category_name = StringField(
        label='Category Name',
        validators=[validators.Length(min=3, max=50), validators.InputRequired()])
    item_number = StringField(
        label='Item Number',
        validators=[validators.Length(min=1, max=50), validators.InputRequired()])
    item_name = StringField(
        label='Item Number',
        validators=[validators.Length(min=1, max=50), validators.InputRequired()])
    description = StringField(
        label='Description',
        validators=[validators.Length(min=1, max=255), validators.Optional()])
    cost_price = DecimalField(
        label='Item Price',
        validators=[validators.InputRequired(), validators.NumberRange(0, 1000000)],
        places=2,
        rounding=None)
    quantity = DecimalField(
        label='Quantity',
        validators=[validators.InputRequired(), validators.NumberRange(0, 10000000)])
    unit_abbreviation = StringField(
        label='Unit',
        validators=[validators.Length(min=1, max=10), validators.InputRequired()])

class UpdateInventoryValidator(Form):
    inventory_id = IntegerField(
        label="Inventory ID",
        validators=[validators.InputRequired()])
    category_name = StringField(
        label='Category Name',
        validators=[validators.Length(min=3, max=50), validators.InputRequired()])
    item_number = StringField(
        label='Item Number',
        validators=[validators.Length(min=1, max=50), validators.InputRequired()])
    item_name = StringField(
        label='Item Number',
        validators=[validators.Length(min=1, max=50), validators.InputRequired()])
    description = StringField(
        label='Description',
        validators=[validators.Length(min=1, max=255), validators.InputRequired()])
    cost_price = DecimalField(
        label='Item Price',
        validators=[validators.InputRequired(), validators.NumberRange(0, 1000000)],
        places=2,
        rounding=None)
    quantity = IntegerField(
        label='Quantity',
        validators=[validators.InputRequired(), validators.NumberRange(0, 10000000)])
    unit_abbreviation = StringField(
        label='Unit',
        validators=[validators.Length(min=1, max=10), validators.InputRequired()])

class DeleteInventoryValidator(Form):
    inventory_id = IntegerField(
        label='Inventory ID',
        validators=[validators.InputRequired()])
