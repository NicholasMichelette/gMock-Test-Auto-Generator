from cpp_gen import CppClass, CppFile
from cpp_parser import CPPParser


def create_mock_class_from_file(file_obj):
    # format file

    # parse file
    parser = CPPParser(file_obj)
    parser.detect_methods()

    # create mock class
    mock_class = create_mock_class(parser)

    # write mock class to file
    mock_file = CppFile()
    mock_file.add_component(mock_class.get_class())
    mock_file.write_to_file(mock_class.name)


def create_mock_class(parser):
    # create mock class
    mock_class = MockClass(parser.detected_class_name)
    for m in parser.methods:
        params = [] if not m.params else m.params
        mock_class.add_mock_method(m.return_type, m.name, params,
                                   m.is_virtual, m.is_constant)
    return mock_class


class MockClass:
    def __init__(self, name):
        self.name = "MOCK_" + name
        self.mock_class = CppClass(self.name)
        self.mock_class.add_public_specifier()

    # return_type and name are strings, params is a list of strings, virtual and const are booleans
    def add_mock_method(self, return_type, name, params, virtual, const):
        statement = "MOCK_METHOD(" + return_type + ", " + name + ", ("
        params_as_list_of_str = [' '.join(i) for i in params]
        statement += ', '.join(params_as_list_of_str)
        statement = statement + ")"

        if virtual:
            statement = statement + ", (override"
            if const:
                statement = statement + ", const))"
            else:
                statement = statement + "))"
        else:
            if const:
                statement = statement + ", (const))"
            else:
                statement = statement + ")"

        self.mock_class.add_statement(statement, indent=True,
                                      has_semicolon=True)

    def get_class(self):
        return self.mock_class
