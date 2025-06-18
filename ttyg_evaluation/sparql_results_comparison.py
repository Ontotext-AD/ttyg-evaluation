def get_var_to_values(
        vars_: list[str],
        bindings: list[dict],
) -> dict[str, list]:
    var_to_values = dict()
    for var in vars_:
        var_to_values[var] = []
        for binding in bindings:
            if var in binding:
                var_to_values[var].append(binding[var]["value"])
            else:
                var_to_values[var].append(None)
    return dict(var_to_values)


def sort_bindings(
        bindings: list[dict],
) -> list[dict]:
    return sorted(
        bindings,
        key=lambda row: tuple(
            row[var]["value"] for var in sorted(row.keys())
        )
    )


def compare_sparql_results(
        expected_sparql_result: dict,
        actual_sparql_result: dict,
        required_vars: list[str],
        results_are_ordered: bool = False,
) -> bool:
    # DESCRIBE results
    if isinstance(actual_sparql_result, str):
        return False

    # ASK
    if "boolean" in expected_sparql_result:
        return "boolean" in actual_sparql_result and \
            expected_sparql_result["boolean"] == actual_sparql_result["boolean"]

    expected_bindings: list[dict] = expected_sparql_result["results"]["bindings"]
    actual_bindings: list[dict] = actual_sparql_result.get("results", dict()).get("bindings", [])
    expected_vars: list[str] = expected_sparql_result["head"]["vars"]
    actual_vars: list[str] = actual_sparql_result["head"].get("vars", [])

    if not actual_bindings:
        if not expected_bindings:
            return len(actual_vars) >= len(required_vars)
        else:
            return False

    if not results_are_ordered:
        expected_bindings = sort_bindings(expected_bindings)
        actual_bindings = sort_bindings(actual_bindings)
    expected_var_to_values: dict[str, list] = get_var_to_values(expected_vars, expected_bindings)
    actual_var_to_values: dict[str, list] = get_var_to_values(actual_vars, actual_bindings)

    mapped_or_skipped_expected_vars, mapped_actual_vars = set(), set()
    for expected_var in expected_vars:
        expected_values = expected_var_to_values[expected_var]
        for actual_var in actual_vars:
            if actual_var not in mapped_actual_vars:
                actual_values = actual_var_to_values[actual_var]
                if expected_values == actual_values:
                    mapped_or_skipped_expected_vars.add(expected_var)
                    mapped_actual_vars.add(actual_var)
                    break
        if expected_var not in mapped_or_skipped_expected_vars and expected_var not in required_vars:
            mapped_or_skipped_expected_vars.add(expected_var)

    return len(mapped_or_skipped_expected_vars) == len(expected_vars)
