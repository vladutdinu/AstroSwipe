from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, UniqueIdProperty, IntegerProperty
from neomodel.relationship_manager import Relationship
class Person(StructuredNode):
    unique_id       = UniqueIdProperty()
    email           = StringProperty()
    first_name      = StringProperty()
    last_name       = StringProperty()
    zodiac_sign     = StringProperty()
    personal_bio    = StringProperty()
    age             = IntegerProperty()

    matched = Relationship("Person", "Matched")
    