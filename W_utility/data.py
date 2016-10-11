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


#===========================data random selection
# randomly select a certain number of items from a data set
from random import sample
def random_select_data (items, num):
    all = len(items)
    if (num > all):
        print ext_print ('error number for data random selection  ---use all data instead')
        return items
    elif (num == all):
        return items
    else:
        selected_items = []
        ran_list = map(int,(sample(xrange(all), num)))
        for i in ran_list:
            selected_items.append(items[i])
        return selected_items
    

# get needed input data size for processing
def generate_random_datasets(all_texts, use_num):
    total = len(all_texts)
    datasets = []
    if (use_num == "all"):
        datasets.append(all_texts)
    elif ('/' in use_num):
        use_pers = use_num.split('/')
        if len(use_pers) == 3:
            current_num = int(use_pers[0])
            while current_num <= int(use_pers[1]):
                if current_num >= total:
                    datasets.append(all_texts)
                    break
                else:
                    datasets.append(random_select_data(all_texts, current_num))
                    current_num = current_num + int(use_pers[2])
        else:
            return False
    else:
        datasets.append(random_select_data(all_texts, int(use_num)))
    return datasets