from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from wtforms import ValidationError, IntegerField, StringField, FloatField
from wtforms_alchemy import model_form_factory
from database.models import Geolocation
from database.sqlite import Sqlite
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return Sqlite().session

    @classmethod
    def close_session(self):
        return Sqlite().close()

class createForm(ModelForm):
    class Meta:
        model = Geolocation
        include = ["id"]
        field_args = {
            'id': {'id': "new_id"},
            'name_geolocation': {'id': "new_name"},
            'longtitude': {'id': "new_lng"},
            'latitude': {'id': "new_lat"},
            'hashtag1': {'id': "new_hg1"},
            'hashtag2': {'id': "new_hg2"}
        }

class updateForm(FlaskForm):
    id = IntegerField(id="new_id")
    name_geolocation = StringField(id="new_name")
    longtitude = FloatField(id="new_lng")
    latitude = FloatField(id="new_lat")
    hashtag1 = StringField(id="new_hg1")
    hashtag2 = StringField(id="new_hg2")

