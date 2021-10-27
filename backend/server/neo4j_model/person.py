from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, UniqueIdProperty, IntegerProperty
from neomodel.properties import BooleanProperty
from neomodel.relationship_manager import Relationship
from neomodel.cardinality import OneOrMore
class Person(StructuredNode):
    unique_id       = UniqueIdProperty()
    email           = StringProperty()
    first_name      = StringProperty()
    last_name       = StringProperty()
    zodiac_sign     = StringProperty()
    personal_bio    = StringProperty()
    age             = IntegerProperty()
    activated       = BooleanProperty(default = False)

    USER_TYPES      = {"A":"admin", "B":"basic", "P":"premium"}
    user_type       = StringProperty(choices=USER_TYPES)
    
    matched = Relationship("Person", "Matched")
    likes = RelationshipTo("Person", "Likes")
    