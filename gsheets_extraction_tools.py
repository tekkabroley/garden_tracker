

def map_raw_data_to_columns(sheet, start_row, is_column_name_included, columns, end_row=None):
    """
    :param sheet: google sheets sheet object
    :param start_row: the start row in the sheet
    :param is_column_name_included: Boolean which is True if column name included in dataset
    :param columns: list of sheet column letters
    :param end_row: terminal row on sheet for sourcing data. If end_row is None then all rows below start_row
        will be extracted.
    :return: dict object mapping column names to list of values
    """
    column_values = {}
    for column in columns:
        values = sheet[column]
        start_index = start_row - 1  # convert sheet row to 0 based index

        if is_column_name_included:
            column_name = values[start_index]
            if end_row is not None:
                end_index = end_row - 1  # convert sheet row to 0 based index
                column_values[column_name] = values[start_index + 1: end_index]
            else:
                column_values[column_name] = values[start_index + 1:]

        else:
            if end_row is not None:
                end_index = end_row - 1  # convert sheet row to 0 based index
                column_values[column] = values[start_index: end_index]
            else:
                column_values[column] = values[start_index:]
    return column_values


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
        if len(records) == 0:
            for i in range(num_rows):
                value = column_data[i]
                record = {column_name: value}
                records.append(record)
        else:
            for i in range(num_rows):
                value = column_data[i]
                record = records[i]
                record.update({column_name: value})
    return records
