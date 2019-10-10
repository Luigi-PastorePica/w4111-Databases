"""
Programmer: Luigi A. Pastore Pica
UNI: lap2204
Template code provided by Donald F. Ferguson, Ph.D.

This file contains the class CSVDataTable, which loads a CSV file into memory as a table and performs RDB-like
operations on such table's data. The code also allows for saving of the changes back into the original CSV file, making
this a simple but competent (yet not very efficient) implementation of a database.
"""


from HW_Assignments.HW1_Template.src.BaseDataTable import BaseDataTable
import copy
import csv
import logging
import json
import os
import pandas as pd
from operator import itemgetter

pd.set_option("display.width", 256)
pd.set_option('display.max_columns', 20)


class CSVDataTable(BaseDataTable):
    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """

    _rows_to_print = 10
    _no_of_separators = 2

    def __init__(self, table_name, connect_info, key_columns, debug=True, load=True, rows=None):
        """

        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        self._data = {
            "table_name": table_name,
            "connect_info": connect_info,
            "key_columns": key_columns,
            "debug": debug
        }

        self._logger = logging.getLogger()

        self._logger.debug("CSVDataTable.__init__: data = " + json.dumps(self._data, indent=2))

        if rows is not None:
            self._rows = copy.copy(rows)
        else:
            self._rows = []
            self._load()

    def __str__(self):

        result = "CSVDataTable: config data = \n" + json.dumps(self._data, indent=2)

        no_rows = len(self._rows)
        if no_rows <= CSVDataTable._rows_to_print:
            rows_to_print = self._rows[0:no_rows]
        else:
            temp_r = int(CSVDataTable._rows_to_print / 2)
            rows_to_print = self._rows[0:temp_r]
            keys = self._rows[0].keys()

            for i in range(0, CSVDataTable._no_of_separators):
                tmp_row = {}
                for k in keys:
                    tmp_row[k] = "***"
                rows_to_print.append(tmp_row)

            rows_to_print.extend(self._rows[int(-1*temp_r)-1:-1])

        df = pd.DataFrame(rows_to_print)
        result += "\nSome Rows: = \n" + str(df)

        return result

    def _add_row(self, r):
        if self._rows is None:
            self._rows = []
        self._rows.append(r)

    def _load(self):

        dir_info = self._data["connect_info"].get("directory")
        file_n = self._data["connect_info"].get("file_name")
        full_name = os.path.join(dir_info, file_n)

        with open(full_name, "r") as txt_file:
            csv_d_rdr = csv.DictReader(txt_file)
            for r in csv_d_rdr:
                self._add_row(r)

        self._logger.debug("CSVDataTable._load: Loaded " + str(len(self._rows)) + " rows")

    def save(self):
        """
        Write the information back to a file.
        :return: None
        """
        dir_info = self._data["connect_info"].get("directory")
        file_n = self._data["connect_info"].get("file_name")
        full_name = os.path.join(dir_info, file_n)

        with open(full_name, "w") as csv_file:
            field_list = list(self._rows[0].keys())
            csv_d_writer = csv.DictWriter(csv_file, fieldnames=field_list)
            rows_written = 0
            for row in self._rows:
                csv_d_writer.writerow(row)
                rows_written += 1

        self._logger.debug("CSVDataTable.save: Wrote " + str(rows_written) + " rows to " + full_name)

    @staticmethod
    def matches_template(row, template):

        result = True
        if template is not None:
            for k, v in template.items():
                if v != row.get(k, None):
                    result = False
                    break

        return result

    def _validate_template_and_fields(self, template, field_list=None):
        """

        This method makes sure that the keys in the template and the fields provided are actually column names of the
        CSVDataTable instance.

        Code provided by Donald Ferguson, Ph.D.

        :param template: A template whose keys we want to validate
        :param field_list: A list of fields which we want to validate
        :return: True, Always.
        """

        c_set = set(list(self._rows[0].keys()))

        if template is not None:
            t_set = set(template.keys())
        else:
            t_set = None

        if field_list is not None:
            f_set = set(field_list)
        else:
            f_set = None

        if f_set is not None and not f_set.issubset(c_set):
            raise ValueError("One or more fields from {} are invalid.".format(f_set))

        if t_set is not None and not t_set.issubset(c_set):
            raise ValueError("One or more fields from {} are invalid.".format(t_set))

        return True

    def find_by_primary_key(self, key_fields, field_list=None):
        """
        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        :param field_list: A subset of the fields of the record to return.
        :return: None, or a dictionary containing the requested fields for the record identified
            by the key.
        """

        # Idea: if field list is None, return the whole row. For now, this is not the behavior of this method

        # If len(key_fields) != len(self.key_columns), don't bother trying to match by primary key.
        # This will raise an exception if lengths do not match. It will do nothing otherwise
        self._check_key_fields_length(key_fields)

        template = self._generate_template(key_fields)

        results = self.find_by_template(template, field_list)

        if len(results) == 0:
            return None
        elif len(results) == 1:
            return results.pop()  # results is a list of dictionaries
        else:
            # raise LookupError('Found more than one record with key {} : \n {}'.format(key_fields,
            #                                                                           json.dumps(results, indent=2)))
            raise LookupError('Found more than one record with key {} : \n {}'.format(key_fields,
                                                                                      pd.DataFrame(results)))

    def _generate_template(self, key_fields):
        """
        Generates a template from key_columns and key_fields

        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        """
        template = {}
        key_columns = self._data.get("key_columns")
        for field_pos in range(len(key_fields)):
            column = key_columns[field_pos]
            field = key_fields[field_pos]
            template[column] = field

        return template

    def _check_key_fields_length(self, key_fields):
        key_columns = self._data.get("key_columns")
        # Number of key fields should match number of key columns
        if len(key_fields) != len(key_columns):
            key_length_mismatch_exception = 'len(key_fields) should match len(key_columns). {} != {}'
            raise ValueError(key_length_mismatch_exception.format(len(key_fields), len(key_columns)))

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None):
        """
        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
        :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A list containing dictionaries. A dictionary is in the list representing each record
            that matches the template. The dictionary only contains the requested fields.
        """

        self._validate_template_and_fields(template, field_list)
        results = []
        all_fields = list(self._rows[0].keys())

        # Too many nested flow control blocks.
        # Consider extracting into helper methods in order to adhere to single responsibility principle
        for row in self._rows:
            if self.matches_template(row, template):
                short_row = {}
                full_row = {}
                if field_list is not None and len(field_list) > 0:
                    for field in field_list:
                        short_row[field] = row.get(field)
                    results.append(short_row)

                else:
                    for field in all_fields:
                        full_row[field] = row.get(field)
                    results.append(full_row)

        # This version of this function does not work, but I do not know the reason.
        # I will leave it here because if it is made to produce the appropriate results, the code will much more
        # understandable, clean and maintainable.
        # if field_list is not None and len(field_list) > 0:
        #     short_row = {}
        #     for row in self._rows:
        #         if self.matches_template(row, template):
        #             for field in field_list:
        #                 short_row[field] = row.get(field)
        #             results.append(short_row)
        #
        # else:
        #     full_row = {}
        #     for row in self._rows:
        #         if self.matches_template(row, template):
        #             for field in all_fields:
        #                 full_row[field] = row.get(field)
        #             results.append(full_row)

        return results

    def delete_by_key(self, key_fields):
        """

        Deletes the record that matches the key.

        :param key_fields: Keys used to find row to be deleted.
        :return: A count of the rows deleted.
        """

        # If len(key_fields) != len(self.key_columns), don't bother trying to match by primary key.
        # This will raise an exception if lengths do not match. It will do nothing otherwise
        self._check_key_fields_length(key_fields)

        template = self._generate_template(key_fields)

        rows_deleted = self.delete_by_template(template)

        return rows_deleted

    def delete_by_template(self, template):
        """
        :param template: Template to determine rows to delete.
        :return: Number of rows deleted.
        """

        self._validate_template_and_fields(template)
        rows_deleted = 0
        row_index = 0

        while row_index < len(self._rows):
            if self.matches_template(self._rows[row_index], template):
                self._rows.remove(self._rows[row_index])
                rows_deleted += 1
                row_index -= 1  # List shortens with each call to remove and contents shift

            row_index += 1
                
        return rows_deleted

    def update_by_key(self, key_fields, new_values):
        """
        :param key_fields: List of value for the key fields.
        :param new_values: A dict of field:value to set for updated row.
        :return: Number of rows updated.
        """

        # If len(key_fields) != len(self.key_columns), don't bother trying to match by primary key.
        # This will raise an exception if lengths do not match. It will do nothing otherwise
        self._check_key_fields_length(key_fields)

        template = self._generate_template(key_fields)

        rows_updated = self.update_by_template(template, new_values)

        return rows_updated  # something not working. either the test or the method.

    def update_by_template(self, template, new_values):
        """
        :param template: Template for rows to match.
        :param new_values: New values to set for matching fields.
        :return: Number of rows updated.
        """

        self._validate_template_and_fields(template)
        rows_updated = 0

        for row in self._rows:
            if self.matches_template(row, template):
                for field in new_values:
                    row[field] = new_values[field]
                rows_updated += 1

        return rows_updated

    def insert(self, new_record):
        """
        :param new_record: A dictionary representing a row to add to the set of records.
        :return: None
        """

        duplicate = False
        try:
            self._check_for_duplicates(new_record)
        except ValueError as ve:
            duplicate = True
            print(ve, "The duplicate record will not be inserted")

        if duplicate is False:
            self._add_row(new_record)
            first_field = list(self._rows[0].keys())  # First key in a row (row is an ordered dictionary). See README.md
            self._rows = sorted(self._rows, key=itemgetter(first_field[0]))  # Sorts list by first field. See README.md

        return None

    def _check_for_duplicates(self, new_record):
        """
        :param new_record: A dictionary containing the new record that must be checked against the exiting table
        :return: None
        """
        key_values = []
        for key in self._data['key_columns']:
            key_values.append(new_record[key])

        res = self.find_by_primary_key(key_fields=key_values)
        if res is not None:
            template = self._generate_template(key_values)
            raise ValueError("A record with the same key already exists.\n"
                             "Duplicate Key: {}\n".format(template))
        return None

    def get_rows(self):
        return self._rows
