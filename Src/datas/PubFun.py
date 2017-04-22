def list_to_condition(name, lis, flag=False):
    condition = ""
    if flag:
        for val in lis:
            condition += name + " = %s OR " % val
    else:
        for val in lis:
            condition += name + " = '%s' OR " % val
    condition = condition[:-4]
    return condition
