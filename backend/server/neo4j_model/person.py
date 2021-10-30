from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, UniqueIdProperty, IntegerProperty
from neomodel.properties import BooleanProperty
from neomodel.relationship_manager import Relationship
from neomodel.cardinality import OneOrMore
class Person(StructuredNode):
    unique_id       = UniqueIdProperty()
    email           = StringProperty()
    password        = StringProperty()
    first_name      = StringProperty(default='')
    last_name       = StringProperty(default='')
    country         = StringProperty(default='')
    city            = StringProperty(default='')
    SEX_TYPES       ={"F":"Female", "M":"Male", "N":"Neutral"}
    sex             = StringProperty(choices=SEX_TYPES, default='N')
    zodiac_sign     = StringProperty(default='')
    personal_bio    = StringProperty(default='')
    age             = IntegerProperty(default=1)
    activated       = BooleanProperty(default = False)

    USER_TYPES      = {"A":"admin", "B":"basic", "P":"premium"}
    user_type       = StringProperty(choices=USER_TYPES, default='B')
    
    matched = Relationship("Person", "Matched")
    likes = RelationshipTo("Person", "Likes")
    