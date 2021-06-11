
# DEPRECATE
def validate_num_rows_is_equal(columnar_dataset):
    """
    Check if all columns in columnar_dataset have the same number of rows
    :param columnar_dataset: dict objecct mapping column name to list of values
    :return: True if all columns have the same number of rows and False otherwise.
    """
    column_lengths = list(map(lambda col: len(columnar_dataset[col]), columnar_dataset))
    init_row_cnt = column_lengths[0]
    column_length_equality = map(lambda col_len: col_len == init_row_cnt, column_lengths[1:])
    return all(column_length_equality)
