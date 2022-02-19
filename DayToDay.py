from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, ListAttribute, NumberAttribute, MapAttribute
)


class Event(MapAttribute):
    order = NumberAttribute()
    event = UnicodeAttribute()


class DaytoDay(Model):

    class Meta:
        table_name = "DayToDay"
        region = 'us-east-1'

    trip = UnicodeAttribute()
    dayOne = ListAttribute(null=True, of=Event)
    dayTwo = ListAttribute(null=True, of=Event)
    dayThree = ListAttribute(null=True, of=Event)
    dayFour = ListAttribute(null=True, of=Event)
    dayFive = ListAttribute(null=True, of=Event)
