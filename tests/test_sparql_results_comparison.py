import copy

from ttyg_evaluation import (
    get_var_to_values,
    sort_bindings,
    compare_sparql_results
)


def test_get_var_to_values():
    bindings = []
    result = get_var_to_values(["s"], bindings)
    assert result == {"s": []}

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}},
    ]
    result = get_var_to_values(["x"], bindings)
    assert result == {"x": ["http://example.com/Person/1", "http://example.com/Person/2"]}

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}, "y": {"type": "literal", "value": "A"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
    ]
    result = get_var_to_values(["x", "y"], bindings)
    assert result == {"x": ["http://example.com/Person/1", "http://example.com/Person/2"], "y": ["A", "B"]}

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}, "y": {"type": "literal", "value": "A"}},
    ]
    result = get_var_to_values(["x", "y"], bindings)
    assert result == {"x": ["http://example.com/Person/2", "http://example.com/Person/1"], "y": ["B", "A"]}

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
    ]
    result = get_var_to_values(["x", "y"], bindings)
    assert result == {"x": ["http://example.com/Person/2", "http://example.com/Person/1"], "y": ["B", None]}

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/6"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/5"}, "y": {"type": "literal", "value": "A"}},
    ]
    result = get_var_to_values(["x", "y"], bindings)
    assert result == {
        "x": [
            "http://example.com/Person/2",
            "http://example.com/Person/1",
            "http://example.com/Person/3",
            "http://example.com/Person/6",
            "http://example.com/Person/5",
        ],
        "y": ["B", None, "A", None, "A"]
    }

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}, "y": {"type": "literal", "value": "B"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/6"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/5"}, "y": {"type": "literal", "value": "A"}},
    ]
    result = get_var_to_values(["x", "y"], bindings)
    assert result == {
        "x": [
            "http://example.com/Person/2",
            "http://example.com/Person/1",
            "http://example.com/Person/3",
            "http://example.com/Person/6",
            "http://example.com/Person/5",
        ],
        "y": [None, "B", "A", None, "A"]
    }

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/6"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/5"}},
    ]
    result = get_var_to_values(["x", "y"], bindings)
    assert result == {
        "x": [
            "http://example.com/Person/2",
            "http://example.com/Person/1",
            "http://example.com/Person/3",
            "http://example.com/Person/6",
            "http://example.com/Person/5",
        ],
        "y": [None, None, None, None, None]
    }


def test_sort_bindings():
    bindings = []
    result = sort_bindings(bindings)
    assert result == []

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}},
    ]
    result = sort_bindings(bindings)
    assert result == [
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}},
    ]

    bindings = [
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}, "y": {"type": "literal", "value": "C"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
    ]
    result = sort_bindings(bindings)
    assert result == [
        {"x": {"type": "uri", "value": "http://example.com/Person/1"}, "y": {"type": "literal", "value": "C"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
        {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
    ]

    bindings = [
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "C"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "C"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "1"},
            "z": {"type": "literal", "value": "C"}
        },
    ]
    result = sort_bindings(bindings)
    assert result == [
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "1"},
            "z": {"type": "literal", "value": "C"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "C"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "C"}
        }
    ]

    bindings = [
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "A"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "C"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "1"},
            "z": {"type": "literal", "value": "C"}
        },
    ]
    result = sort_bindings(bindings)
    assert result == [
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "1"},
            "z": {"type": "literal", "value": "C"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "A"}
        },
        {
            "x": {"type": "literal", "value": "1"},
            "y": {"type": "literal", "value": "2"},
            "z": {"type": "literal", "value": "C"}
        }
    ]


def test_compare_empty_sparql_results() -> None:
    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"}
            }
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": []}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == False

    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": []}
    }
    actual_sparql_results = {
        "head": {"vars": ["x", "y"]},
        "results": {"bindings": []}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True

    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": []}
    }
    actual_sparql_results = {
        "head": {"vars": ["x", "y", "z"]},
        "results": {"bindings": []}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True

    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": []}
    }
    actual_sparql_results = {
        "head": {"vars": ["x"]},
        "results": {"bindings": []}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == False

    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": []}
    }
    actual_sparql_results = {
        "head": {"vars": ["x"]},
        "results": {"bindings": []}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, optional_vars=["personName"]) == True


def test_compare_sparql_results_exactly_the_same_results_as_expected() -> None:
    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"}
            }
        ]}
    }
    actual_sparql_results = copy.deepcopy(expected_sparql_results)

    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, results_are_ordered=True) == True

    optional_vars = ["person"]
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, optional_vars=optional_vars) == True
    assert compare_sparql_results(
        expected_sparql_results, actual_sparql_results, optional_vars=optional_vars, results_are_ordered=True
    ) == True

    optional_vars = ["person", "personName"]
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, optional_vars=optional_vars) == True
    assert compare_sparql_results(
        expected_sparql_results, actual_sparql_results, optional_vars=optional_vars, results_are_ordered=True
    ) == True


def test_compare_sparql_results_same_results_as_expected_but_variables_are_renamed() -> None:
    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"}
            }
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["x", "y"]},
        "results": {"bindings": [
            {
                "x": {"type": "uri", "value": "http://example.com/Person/1"},
                "y": {"type": "literal", "value": "Alice"}
            },
            {
                "x": {"type": "uri", "value": "http://example.com/Person/2"},
                "y": {"type": "literal", "value": "Bob"}
            }
        ]}
    }

    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, results_are_ordered=True) == True

    optional_vars = ["person"]
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, optional_vars=optional_vars) == True
    assert compare_sparql_results(
        expected_sparql_results, actual_sparql_results, optional_vars=optional_vars, results_are_ordered=True
    ) == True

    optional_vars = ["person", "personName"]
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, optional_vars=optional_vars) == True
    assert compare_sparql_results(
        expected_sparql_results, actual_sparql_results, optional_vars=optional_vars, results_are_ordered=True
    ) == True


def test_compare_sparql_results_equals_one_binding() -> None:
    expected_sparql_results = {
        "head": {"vars": ["average_person_age"]},
        "results": {"bindings": [
            {
                "average_person_age": {
                    "type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#decimal", "value": "35"
                },
            }
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["avg"]},
        "results": {"bindings": [
            {
                "avg": {
                    "type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#decimal", "value": "35"
                },
            }
        ]}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True


def test_compare_sparql_results_not_equals() -> None:
    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"}
            }
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Alice"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Bob"}
            }
        ]}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == False
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, results_are_ordered=True) == False


def test_compare_sparql_results_different_order() -> None:
    expected_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"}
            }
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["person", "personName"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"}
            }
        ]}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, results_are_ordered=True) == False


def test_compare_sparql_results_different_order_optional_columns() -> None:
    expected_sparql_results = {
        "head": {"vars": ["person", "personName", "personAge"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personName": {"type": "literal", "value": "Alice"},
                "personAge": {"type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#integer", "value": "30"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personName": {"type": "literal", "value": "Bob"},
                "personAge": {"type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#integer", "value": "35"}
            }
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["person", "personAge", "gender"]},
        "results": {"bindings": [
            {
                "person": {"type": "uri", "value": "http://example.com/Person/2"},
                "personAge": {"type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#integer", "value": "35"},
                "gender": {"type": "literal", "value": "male"}
            },
            {
                "person": {"type": "uri", "value": "http://example.com/Person/1"},
                "personAge": {"type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#integer", "value": "30"},
                "gender": {"type": "literal", "value": "female"}
            }
        ]}
    }
    optional_vars = ["personName"]
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results, optional_vars=optional_vars) == True
    assert compare_sparql_results(
        expected_sparql_results, actual_sparql_results,
        optional_vars=optional_vars, results_are_ordered=True
    ) == False


def test_compare_sparql_results_empty_binding_values() -> None:
    expected_sparql_results = {
        "head": {"vars": ["x", "y"]},
        "results": {"bindings": [
            {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/6"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/5"}, "y": {"type": "literal", "value": "A"}},
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["c", "p"]},
        "results": {"bindings": [
            {"c": {"type": "uri", "value": "http://example.com/Person/2"}},
            {"c": {"type": "uri", "value": "http://example.com/Person/1"}, "p": {"type": "literal", "value": "B"}},
            {"c": {"type": "uri", "value": "http://example.com/Person/3"}, "p": {"type": "literal", "value": "A"}},
            {"c": {"type": "uri", "value": "http://example.com/Person/6"}},
            {"c": {"type": "uri", "value": "http://example.com/Person/5"}, "p": {"type": "literal", "value": "A"}},
        ]}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == False

    expected_sparql_results = {
        "head": {"vars": ["x", "y"]},
        "results": {"bindings": [
            {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/6"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/5"}, "y": {"type": "literal", "value": "A"}},
        ]}
    }
    actual_sparql_results = {
        "head": {"vars": ["x", "y"]},
        "results": {"bindings": [
            {"x": {"type": "uri", "value": "http://example.com/Person/2"}, "y": {"type": "literal", "value": "B"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/1"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/3"}, "y": {"type": "literal", "value": "A"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/6"}},
            {"x": {"type": "uri", "value": "http://example.com/Person/5"}, "y": {"type": "literal", "value": "A"}},
        ]}
    }
    assert compare_sparql_results(expected_sparql_results, actual_sparql_results) == True
