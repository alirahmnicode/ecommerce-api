def deep_update(base_dict, update_with):
    # Iterate over each item in the new dict
    for key, value in update_with.items():

        # if the value is a dictionary
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            # if the original value is a dictionary then run is through this same function
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            # if the original value is NOT a dictionary then just set the new value
            else:
                base_dict[key] = value

        # if the new value is NOT a dict
        else:
            base_dict[value] = value

    return base_dict
