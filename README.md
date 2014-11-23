MObject
=======
Lightweight library to construct objects and object trees for mocking and stubbing. It is not meant
as a replacement for mock frameworks but rather as a complement.

The basics, dynamic object specification
----------------------------------------
Creating a new object is easy:

.. code:: python
    >>> from mobject import MObject
    >>> o = MObject(a=1, b=2)
    >>> o.a
    1
    >>> o.b
    2
    >>> o
    MObject(a=1, b=2)
    
There's also support for easy specification of nested objects through the __ syntax:

.. code:: python
    >>> from mobject import MObject
    >>> o = MObject(a__b=1, a__c=2)
    >>> o.a.b
    1
    >>> o.a.c
    2
    >>> o
    MObject(a__b=1, a__c=2)

Static object specification
---------------------------
The examples from above can also be specified as classes which, when instantiated,
produce equivalent objects. Chosen attributes can also be overridden with

.. code:: python
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
    
Class specification of nested objects is also supported in two different forms:
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

    

