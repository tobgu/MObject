MObject
=======
A lightweight library to construct objects and object trees for mocking and stubbing. It is not meant
as a replacement for mock frameworks but rather as a complement.

The basics, dynamic object specification
----------------------------------------
Creating a new object is easy.

```python
>>> from mobject import MObject
>>> o = MObject(a=1, b=2)
>>> o.a
1
>>> o.b
2
>>> o
MObject(a=1, b=2)

```

There's also support for easy specification of nested objects through the __ syntax.

```python
>>> from mobject import MObject
>>> o = MObject(a__b=1, a__c=2)
>>> o.a.b
1
>>> o.a.c
2
>>> o
MObject(a__b=1, a__c=2)

```

Classes for object specification
--------------------------------
The examples from above can also be specified as classes which, when instantiated,
produce equivalent objects. Attributes can also be overridden by providing
values at instantiation.

```python
>>> from mobject import MObject
>>> class MyMObject(MObject):
...     a = 1
...     b = 2
...
>>> o = MyMObject()
>>> o.a, o.b
(1, 2)
>>> MyMObject(a=3)
MyMObject(a=3, b=2)

```

Class specification of nested objects is also supported in two different forms.

```python
>>> class MyNestedMObject1(MObject):
...     a = 1
...     b__c = 2
...
>>> class MyNestedMObject2(MObject):
...     a = 1
...     class b(MObject):
...         c = 2
>>> MyNestedMObject1() == MyNestedMObject2()
True
>>> MyNestedMObject1() == MyNestedMObject2(b__c=3)
False

```

Adding behaviour
----------------
You can add behaviour to your objects by assigning callable objects.

```python
>>> o = MObject(fn=lambda x: x + 1)
>>> o.fn(1)
2

```

Nothing particular so far. Here's a special twist though. If your callable takes a first 
argument named 'self' it will get access to the object it is defined for.

```python
>>> o = MObject(a=1, fn=lambda self, x: self.a + x, b__a=3, b__fn=lambda self, x: self.a + x)
>>> o.fn(1)
2
>>> o.b.fn(1)
4

```

Object comparison
-----------------
Objects created with MObject can be compared to any other object. Two objects are equal if all
non callable properties of the objects are equal. Callables are excluded from comparison.
MObjects also define set like comparison operations. This is very convenient when you only want
to compare a subset of an objects properties to that specified by the MObject.

The following examples will hopefully bring clarity to how comparisons work.

```python
>>> class Foo(object):  # Regular class
...     def __init__(self):
...         self.a = 1
...         self.b = 2
...
>>> MObject(a=1, b=2) == Foo()
True
>>> MObject(a=1, b=3) == Foo()
False
>>> MObject(a=1) < Foo()
True
>>> MObject(a=2) < Foo()
False
>>> MObject(a=1, b=2, c=3) > Foo()
True
>>> MObject(a=2, b=2, c=3) > Foo()
False

```