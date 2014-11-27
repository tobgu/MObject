import pytest
from mobject import *


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


def set_c(self, x):
    self.c = x


def append_d(self, x):
    self.d.append(x)


class TestMObject(MObject):
    a = 1
    b__c = 2
    b__d = []
    b__f = lambda self, x: self.c + x
    b__set_c = set_c
    b__append_d = append_d


class InheritedTestMObject(TestMObject):
    foo = 3
    a = 4


def test_repr():
    o = TestMObject()
    assert str(o) == "TestMObject(a=1, b__append_d(self, x), b__c=2, b__d=[], b__f(self, x), b__set_c(self, x))"


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


class NestedTestMObject(MObject):
    aa = 11

    class bb(MObject):
        cc = 22


def test_class_based_definition_nested_classes():
    o = NestedTestMObject()
    assert o.aa == 11
    assert o.bb.cc == 22

    o2 = NestedTestMObject(bb__cc=33)
    assert o2.bb.cc == 33


class MultiInheritedTestMObject(TestMObject, NestedTestMObject):
    aaa = 111


def test_class_based_definition_multiple_inheritance():
    o = MultiInheritedTestMObject()
    assert o.a == 1
    assert o.aa == 11
    assert o.aaa == 111


class NestedRealObject(object):
    def __init__(self):
        self.aa = 3


class RealObject(object):
    def __init__(self):
        self.a = 1
        self.b = NestedRealObject()

    def foo_fn(self):
        return self


def test_equality():
    assert MObject(a=1, b__aa=3) == RealObject()
    assert MObject(a=1, b__aa=4) != RealObject()
    assert MObject(a=1, b__aa=3, c=2) != RealObject()
    assert MObject(a=1) != RealObject()

    # Callables are not considered for equality
    assert MObject(a=1, b__aa=3, baz_fn=lambda self: self) == RealObject()


def test_proper_subset():
    assert MObject(a=1) < RealObject()
    assert MObject(b__aa=3) < RealObject()
    assert not MObject(a=1, b__aa=3) < RealObject()
    assert not MObject(a=2) < RealObject()


def test_subset():
    assert MObject(a=1, b__aa=3) <= RealObject()
    assert not MObject(a=1, b__aa=3, c=4) <= RealObject()


def test_proper_superset():
    assert MObject(a=1, b__aa=3, c=4) > RealObject()
    assert not MObject(a=2, b__aa=3, c=4) > RealObject()
    assert not MObject(a=1, b__aa=3) > RealObject()


def test_superset():
    assert MObject(a=1, b__aa=3) >= RealObject()
    assert not MObject(a=1) >= RealObject()


def test_short_mob():
    assert mob(a=1, b=2) == MObject(a=1, b=2)