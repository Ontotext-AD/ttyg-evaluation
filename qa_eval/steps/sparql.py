from collections import Counter


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


def get_permutation_indices(list1: list, list2: list) -> list:
    if len(list1) != len(list2) or Counter(list1) != Counter(list2):
        return []

    indices = []
    used = [False] * len(list1)

    for item2 in list2:
        for i in range(len(list1)):
            if not used[i] and list1[i] == item2:
                indices.append(i)
                used[i] = True
                break

    return indices


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

    if (not actual_bindings) and (not expected_bindings):
        return len(actual_vars) >= len(required_vars)
    elif (not actual_bindings) or (not expected_bindings):
        return False

    # re-order the vars, so that required come first
    expected_vars = required_vars + [var for var in expected_vars if var not in required_vars]

    expected_var_to_values: dict[str, list] = get_var_to_values(expected_vars, expected_bindings)
    actual_var_to_values: dict[str, list] = get_var_to_values(actual_vars, actual_bindings)

    permutation = []
    mapped_or_skipped_expected_vars, mapped_actual_vars = set(), set()
    for expected_var in expected_vars:
        expected_values = expected_var_to_values[expected_var]
        for actual_var in actual_vars:
            if actual_var not in mapped_actual_vars:
                actual_values = actual_var_to_values[actual_var]
                if not results_are_ordered:
                    permutation_indices = get_permutation_indices(expected_values, actual_values)
                    if permutation_indices:
                        if permutation:
                            if permutation_indices == permutation:
                                mapped_or_skipped_expected_vars.add(expected_var)
                                mapped_actual_vars.add(actual_var)
                                break
                        else:
                            permutation = permutation_indices
                            mapped_or_skipped_expected_vars.add(expected_var)
                            mapped_actual_vars.add(actual_var)
                            break
                elif expected_values == actual_values:
                    mapped_or_skipped_expected_vars.add(expected_var)
                    mapped_actual_vars.add(actual_var)
                    break
        if expected_var not in mapped_or_skipped_expected_vars:
            if expected_var in required_vars:
                return False
            # optional, we can skip it
            mapped_or_skipped_expected_vars.add(expected_var)

    return len(mapped_or_skipped_expected_vars) == len(expected_vars)
