from serial_variables import serial_variable
from lines import line
from plots import plot

def dict_to_list_iterable_converter(unscanned_iterable: list | tuple):
    if isinstance(unscanned_iterable, list):
        scanned_iterable = []
    elif isinstance(unscanned_iterable, tuple):
        scanned_iterable = ()
    for var in unscanned_iterable:
        if isinstance(var, serial_variable):
            converted_var = var.serial_to_dict()
            scanned_iterable.append(converted_var)
        elif isinstance(var, line):
            converted_var = var.line_to_dict()
            scanned_iterable.append(converted_var)
        elif isinstance(var, plot):
            converted_var = var.plot_to_dict()
            scanned_iterable.append(converted_var)
        elif isinstance(var, (list, tuple)):
            converted_var = dict_to_list_iterable_converter(var)
            scanned_iterable.append(converted_var)
        else:
            scanned_iterable.append(var)
    return scanned_iterable

def dict_to_list(dict_obj: dict):
    dict_as_list = []
    if not dict_obj:
        return dict_as_list
    for item in dict_obj.items():
        key = item[0]
        if isinstance(key, serial_variable):
            converted_key = key.serial_to_dict()
        elif isinstance(key, line):
            converted_key = key.line_to_dict()
        elif isinstance(key, plot):
            converted_key = key.plot_to_dict()
        elif isinstance(key, (list, tuple)):
            converted_key = dict_to_list_iterable_converter(key)
        else:
            converted_key = key
        value = item[1]
        if isinstance(value, serial_variable):
            converted_value = value.serial_to_dict()
        elif isinstance(value, line):
            converted_value = value.line_to_dict()
        elif isinstance(value, plot):
            converted_value = value.plot_to_dict()
        elif isinstance(value, (list, tuple)):
            converted_value = dict_to_list_iterable_converter(value)
        else:
            converted_value = value
        converted_item = (converted_key, converted_value)
        dict_as_list.append(converted_item)
    return dict_as_list

def list_to_dict_iterable_converter(unscanned_iterable: list | tuple, iterable_is_key: bool):
    if isinstance(unscanned_iterable, tuple):
        scanned_iterable = ()
    elif isinstance(unscanned_iterable, list):
        scanned_iterable = []
    for var in unscanned_iterable:
        if isinstance(var, dict):
            converted_var = object_dict_converter(var)
            scanned_iterable.append(converted_var)
        elif isinstance(var, (list, tuple)):
            converted_var = list_to_dict_iterable_converter(var)
            scanned_iterable.append(converted_var)
        else:
            converted_var = var
            scanned_iterable.append(converted_var)
        if isinstance(converted_var, dict) and iterable_is_key:
            return TypeError
        elif isinstance(converted_var, TypeError):
            return TypeError
    return scanned_iterable

def object_dict_converter(obj_dict: dict):
    serial_variable_dict = {
        'serial_number': int,
        'serial_name': str,
        'serial_units': str,
        'data_array': list
    }
    line_dict = {
        'x_serial': serial_variable,
        'y_serial': serial_variable,
        'color': str,
        'linewidth': float | int,
        'linestyle': str,
        'marker': str,
        'markersize': float | int,
        'markeredgewidth': float | int,
        'markeredgecolor': str,
        'markerfacecolor': str,
        'markerfacecoloralt': str,
        'label': str,
        'gapcolor': str | None,
        'fillstyle': str,
        'antialiased': bool,
        'dash_capstyle': str,
        'solid_capstyle': str,
        'dash_joinstyle': str,
        'solid_joinstyle': str,
        'pickradius': float | int,
        'drawstyle': str,
        'markevery': int | float | None
    }
    plot_dict = {
        'lines': list[line],
        'title': str,
        'x_label': str,
        'y_label': str,
        'legend pos': str,
        'plot pos': str
    }
    obj_dict_keys = list(obj_dict)
    if obj_dict_keys == list(serial_variable_dict):
        dict_as_obj = serial_variable.serial_from_dict(obj_dict)
    elif obj_dict_keys == list(line_dict):
        dict_as_obj = line.line_from_dict(obj_dict)
    elif obj_dict_keys == list(plot_dict):
        dict_as_obj = plot.plot_from_dict(obj_dict)
    else:
        return obj_dict
    return dict_as_obj

def list_to_dict(dict_as_list: list):
    dict_obj = {}
    if not dict_as_list:
        return dict_obj
    for item_tuple in dict_as_list:
        if not isinstance(item_tuple, (tuple, list)):
            return TypeError
        elif len(item_tuple) != 2:
            return TypeError
        else:
            tuple_key = item_tuple[0]
            tuple_value = item_tuple[1]
        if isinstance(tuple_key, dict):
            converted_key = object_dict_converter(tuple_key)
        elif isinstance(tuple_key, (list, tuple)):
            converted_key = list_to_dict_iterable_converter(tuple_key, True)
        else:
            converted_key = tuple_key
        if isinstance(tuple_value, dict):
            converted_value = object_dict_converter(tuple_value)
        elif isinstance(tuple_value, (list, tuple)):
            converted_value = list_to_dict_iterable_converter(tuple_value, False)
        else:
            converted_value = tuple_value
        if isinstance(converted_key, dict) or isinstance(converted_key, TypeError):
            return TypeError
        else:
            dict_obj[converted_key] = converted_value
    return dict_obj