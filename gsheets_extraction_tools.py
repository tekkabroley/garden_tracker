

def build_gsheets_ranges(sheet_name, start_row, columns):
    """
    Build gsheets ranges from start_row and columns.
    :param sheet_name:
    :param start_row:
    :param columns:
    :return: list of ranges
    """
    output = []
    for column in columns:
        range_ = f"{sheet_name}!{column}{start_row}:{column}"
        output.append(range_)
    return output


def map_raw_data_to_columns(value_ranges, is_column_header_included=None):
    """
    Transform raw to columnar data
    :param value_ranges:
    :param is_column_header_included:
    :return: dict mapping column_name -> list of values
    """
    output = {}  # {column name: values (list of primitives)}
    for vr in value_ranges:
        columns = vr["values"]
        cnt = 0
        for column in columns:
            cnt += 1
            if is_column_header_included is True:
                column_header = column[0].strip()
                column_values = column[1:]
            else:
                column_header = f"column {cnt}"  # replace this with the appropriate column letter from the range
                column_values = column
            output[column_header] = column_values
    return output


def map_columnar_data_to_records(columnar_dataset):
    """
    Convert columnar dataset to list of records
    :param columnar_dataset: dict of column_name -> list of values
    :return: list of dict objects mapping column name to value for given row
    """
    records = []
    for column_name in columnar_dataset:
        column_data = columnar_dataset[column_name]
        num_rows = len(column_data)
        column_name_ = column_name.strip()
        if len(records) == 0:
            for i in range(num_rows):
                value = column_data[i]
                record = {column_name_: value}
                records.append(record)
        else:
            for i in range(num_rows):
                value = column_data[i]
                record = records[i]
                record.update({column_name_: value})
    return records
