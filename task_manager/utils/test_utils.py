def compare_dicts_and_assert(test_object, dict1, dict2):
    for key, value in dict1.items():
        if key in dict2:
            test_object.assertEqual(value, dict2[key])
