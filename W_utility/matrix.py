# combine two dicts into one (former) and add value together
def Combine_dicts_number(main_dict, secondary_dict):
    for key, value in secondary_dict.iteritems():
        if key in main_dict:
            main_dict[key] += value
        else:
            main_dict[key] = value
    return main_dict


# combine two dicts into one (former) and add value together
def Combine_dicts_string(main_dict, secondary_dict, separator):
    for key, value in secondary_dict.iteritems():
        if key in main_dict:
            main_dict[key] = str(main_dict[key]) + separator + value
        else:
            main_dict[key] = value
    return main_dict     