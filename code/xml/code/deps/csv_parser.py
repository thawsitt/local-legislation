import csv

# csv_parser.py (v1) Apr 09, 2018
# -------------------------------
# Parses metadata from the csv file generated by RWD's database.
# This module uses Python 3.
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class CSVParser():

    def __init__(self, csv_file_name, utils):
        self.csv_file_name = csv_file_name
        self.utils = utils
        self.column_names = self.utils.getColumnNames()

    def getMetadata(self):
        # Return a dictionary
        # Key: 4-digit recordID (string)
        # Value: a dictionary (metadata (key, value) pairs)
        metadata = dict()
        with open(self.csv_file_name, newline='') as csvfile:
            database = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in database:
                dictionary = self.readIntoDict(row)
                record_id = str(dictionary[self.column_names[0]]).zfill(4)  # e.g: "0001"
                metadata[record_id] = dictionary
        return metadata

    # Helper Functions

    def readIntoDict(self, row):
        dictionary = dict()
        for i in range(len(row)):
            key = self.column_names[i]
            value = row[i] if row[i] else None  # Convert '' to None
            key, value = self.processData(key, value)
            dictionary[key] = value
        return dictionary

    def processData(self, key, value):
        # deal with tab character in csv files exported by database
        # This tab character is known to appear in the following fields
        # BaseText, GeneralNotes, SourceNotes, PlaceNotes, DateNotes, Transcription Notes
        if value and ('' in value):
            value_list = value.split('')
            value = list(filter(None, value_list))  # filter empty strings
            if len(value) == 1:
                value = value[0]  # ["lonely string"] => "lonely string"
        return (key, value)
