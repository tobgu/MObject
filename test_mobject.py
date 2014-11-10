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


# - Equality: The subset defined by the object graph is also available on inte the object compared to
# - "Static" definition of mocks
# - Python 2/3 compatibility