from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, UniqueIdProperty, IntegerProperty
from server.neo4j_model.person import Person
class Zodiac(StructuredNode):
    zodiac_sign = StringProperty()

    person = RelationshipFrom(Person, 'Born under')