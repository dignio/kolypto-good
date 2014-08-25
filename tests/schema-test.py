import unittest
import six
from good import Schema, Invalid, MultipleInvalid
from good.schema.util import get_type_name

class s:
    """ Shortcuts """
    # Type names
    t_none = get_type_name(None)
    t_bool = get_type_name(bool)
    t_int = get_type_name(int)
    t_float = get_type_name(float)
    t_str = get_type_name(six.string_types[0])  # Binary string
    t_unicode = get_type_name(six.text_type)  # Unicode string

    es_type = u'Invalid value type'
    es_value = u'Invalid value'


class SchemaTest(unittest.TestCase):
    """ Test Schema """

    def assertValid(self, schema, value, validated_value=None):
        """ Try the given Schema against a value and expect that it's valid

        :type schema: Schema
        :param value: The value to validate
        :type validated_value: The expected validated value
        """
        self.assertEqual(
            schema(value),
            value if validated_value is None else validated_value
        )

    def assertInvalid(self, schema, value, e_path, e_validator, e_message, e_expected, e_provided, **e_info):
        """ Try the given Schema against a value and expect that it's invalid

        :type schema: Schema
        :type value: The value to validate
        :type e_path: Expected Invalid.path value
        :param e_validator: Expected Invalid.validator value
        :param e_message: Expected Invalid.message value
        :param e_expected: Expected Invalid.expected value
        :param e_provided: Expected Invalid.provided value
        :param e_info: Expected Invalid.info value
        """
        with self.assertRaises(Invalid) as ecm:
            schema(value)
        e = ecm.exception

        # Check error
        self.assertIs(type(e), Invalid)  # Strict type
        self.assertEqual(e.path, e_path)
        self.assertEqual(e.validator, e_validator)
        self.assertEqual(e.message, e_message)
        self.assertEqual(e.expected, e_expected)
        self.assertEqual(e.provided, e_provided)
        self.assertEqual(e.info, e_info)

    #region Schema(<literal>)

    def test_literal(self):
        """ Test Schema(<literal>) """
        # None
        schema = Schema(None)
        self.assertValid(schema, None)
        self.assertInvalid(schema, True, [], None, s.es_type, s.t_none, s.t_bool)

        # Bool
        schema = Schema(True)
        self.assertValid(schema, True)
        self.assertInvalid(schema, 1,     [], True, s.es_type,  s.t_bool, s.t_int)
        self.assertInvalid(schema, False, [], True, s.es_value, u'True', u"False")

        # Integer
        schema = Schema(1)
        self.assertValid(schema, 1)
        self.assertInvalid(schema, 1.0, [], 1, s.es_type,  s.t_int, s.t_float)
        self.assertInvalid(schema, '1', [], 1, s.es_value, u'1', u"'1'")

        # Float
        schema = Schema(1.0)
        self.assertValid(schema, 1.0)
        self.assertInvalid(schema,  1,    [], 1.0, s.es_type,  s.t_float, s.t_int)
        self.assertInvalid(schema, '1.0', [], 1.0, s.es_value, u'1', u"'1.0'")

        # String
        schema = Schema(six.b('1'))
        self.assertValid(schema, six.b('1'))
        self.assertValid(schema, u'1')
        self.assertInvalid(schema,   1,  [], six.b('1'), s.es_type,  s.t_unicode, s.t_int)
        self.assertInvalid(schema, u'2', [], six.b('1'), s.es_value, u'abc', u"'1'")

        # Unicode
        schema = Schema(u'1')
        self.assertValid(schema, u'1')
        self.assertValid(schema, six.b('1'))
        self.assertInvalid(schema,   1,  [], u'1', s.es_type,  s.t_unicode, s.t_int)
        self.assertInvalid(schema, u'2', [], u'1', s.es_value, u'abc', u"'1'")

    def test_type(self):
        """ Test Schema(<type>) """
        # None
        schema = Schema(None)
        self.assertValid(schema, None)
        self.assertInvalid(schema, 1, [], None, u'Invalid type', s.t_none, s.t_int)

        # Bool
        schema = Schema(bool)
        self.assertValid(schema, True)
        self.assertInvalid(schema, 1, [], None, u'Invalid type', s.t_bool, s.t_int)

        # Integer
        schema = Schema(int)
        self.assertValid(schema, 1)
        self.assertInvalid(schema, None, [], None, u'Invalid type', s.t_int, s.t_none)

        # Float
        schema = Schema(float)
        self.assertValid(schema, 1.0)
        self.assertInvalid(schema, 1, [], None, u'Invalid type', s.t_float, s.t_int)

        # String
        schema = Schema(six.string_types[0])
        self.assertValid(schema, six.b('a'))
        self.assertValid(schema, u'a')
        self.assertInvalid(schema, 1, [], None, u'Invalid type', s.t_int, s.t_str)

        # Unicode
        schema = Schema(six.text_type)
        self.assertValid(schema, six.b('a'))
        self.assertValid(schema, u'a')
        self.assertInvalid(schema, 1, [], None, u'Invalid type', s.t_int, s.t_unicode)
