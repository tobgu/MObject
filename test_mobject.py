import pytest
from mobject import MObject


def test_simple_object_creation():
    o = MObject(a=1, b=2)

    assert o.a == 1
    assert o.b == 2


def test_nested_object_creation():
    o = MObject(a__b=1, a__c=2, a__d__e=3)

    assert o.a.b == 1
    assert o.a.c == 2
    assert o.a.d.e == 3


def test_invalid_nesting_exception():
    with pytest.raises(ValueError):
        MObject(a__b=2, a__b__c=3)


def test_object_with_static_method():
    o = MObject(a__b=lambda x: x+1)

    assert o.a.b(3) == 4


def test_object_with_instance_method():
    TERM_A = 1
    TERM_B = 2
    o = MObject(a__b=lambda self, x: self.c + x, a__c=TERM_B)

    assert o.a.b(TERM_A) == TERM_B + TERM_A


def test_mutate_mobject_from_instance_method():
    def set_a(self, new_value):
        self.a = new_value

    o = MObject(a=1, set_a=set_a)
    o.set_a(2)

    assert o.a == 2


class TestMObject(MObject):
    def set_c(self, x):
        self.c = x

    def append_d(self, x):
        self.d.append(x)

    a = 1
    b__c = 2
    b__d = []
    b__f = lambda self, x: self.c + x
    b__set_c = set_c
    b__append_d = append_d


class InheritedTestMObject(TestMObject):
    foo = 3
    a = 4


def test_class_based_definition_base_case():
    o = TestMObject()
    assert o.a == 1
    assert o.b.c == 2


def test_class_based_definition_with_mutation():
    o = TestMObject()

    o.b.set_c(3)
    assert o.b.c == 3

    o.b.append_d(4)
    assert o.b.d == [4]

    # Overwriting the values in one object does not destroy the original
    o2 = TestMObject()
    assert o2.b.c == 2
    assert o2.b.d == []


def test_class_based_definition_with_inheritance():
    o = InheritedTestMObject()
    assert o.foo == 3
    assert o.a == 4
    assert o.b.c == 2


def test_class_based_definition_overridden_data():
    o = InheritedTestMObject(a=5, b__c=6)
    assert o.foo == 3
    assert o.a == 5
    assert o.b.c == 6
    assert o.b.d == []


def test_private_properties():
    o = MObject(_a=1, b___c=2)
    assert o._a == 1
    assert o.b._c == 2


def test_dunder_properties():
    o = MObject(__a=1, b____c=2, b_______d=3)
    assert o.__a == 1
    assert o.b.__c == 2
    assert o.b._____d == 3


#    assert o.a == 1


# - Equality: The subset defined by the object graph is also available on in the the object compared to
# - Multiple inheritance
# - Python 2/3 compatibility
# - Nice repr()
# - Nested attributes through nested classes
