# This module contains some common functions
# for handling local files.
# The intent is to simplify future coding .

# Imports

import csv
import pandas
import random
import itertools


# Functions

def raise_custom_error(error, message):
    try:
        raise error
    except error as err:
        err.args = (message,)
        raise


# Classes

class CSVReader:

    # Object initialization

    def __init__(self, file_dir = '', header = True, newline = '',
        delimiter = ',', quotechar = '|', as_df = True, sample_size = None,
        seed = None, datetime_cols = None, **kwargs):

        # Optional properties
        self._file_dir = file_dir    # Dataset location; includes file name and extension.
        self._header = header    # Boolean; whether the first row is a header or not.
        self._newline = newline    # The symbol used to indicate a new row in the file.
        self._delimiter = delimiter    # The symbol used to separate dimensions in each row. 
        self._quotechar = quotechar    # The symbol used to enclose quotations.
        self._as_df = as_df    # Arguemnt for methods below.
        self._sample_size = sample_size    # Arguemnt for methods below.
        self._seed = seed    # Random seed

        # Non-optional properties
        self._n = None    # Number of rows in the dataset / sample size
        self._data = None    # Loaded dataset

        # Load the dataset
        random.seed(self._seed)
        self.load(as_df = self._as_df, sample_size = self._sample_size,
            datetime_cols = datetime_cols, **kwargs)

    # Properties

    @property
    def file_dir(self):
        return self._file_dir

    @property
    def header(self):
        return self._header
    
    @property
    def newline(self):
        return self._newline

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def quotechar(self):
        return self._quotechar

    @property
    def as_df(self):
        return self._as_df

    @property
    def sample_size(self):
        return self._sample_size

    @property
    def seed(self):
        return self._seed

    @property
    def n(self):
        return self._n

    @property
    def data(self):
        return self._data
    

    # Setters

    @file_dir.setter
    def file_dir(self, x):
        self._file_dir = x

    @header.setter
    def header(self, x):
        if not isinstance(x, bool):
            raise TypeError
        self._header = x

    @seed.setter
    def seed(self, x):
        self._seed = x
        if x == None:
            random.seed()
        else:
            random.seed(x)


    # Methods

    def count_n(self):

        # Count the number of rows in the dataset.
        # Subtract the total count by 1 if the first row of the dataset is a header.

        if self._header:
            offset = 1
        else:
            offset = 0

        with open(self._file_dir, newline = self._newline) as csv_file:
            self._n = sum(1 for line in csv.reader(csv_file, delimiter = self._delimiter)) - offset

    def load(self, as_df = True, sample_size = None, datetime_cols = None, **kwargs):

        # Load the dataset at the self.__file_dir.
        # 'sample' allows for drawing a random sample
        # of specified size from the dataset.
        # 'as_df' determines whether the output should be a pandas dataframe object.
        # If not, then a list of tuples (each representing a row) is returned.

        # Count the number of rows in the dataset if it has not been done already.

        if not isinstance(self._n, int):
            self.count_n()

        # Determine where the first data row is depending on whether the dataset contains a header.
        
        if self._header:
            lower = 1
        else:
            lower = 0

        # If argument 'sample' is an integer, determine the random rows to be drawn from the dataset.

        if sample_size == None:
            skip = None
        elif isinstance(sample_size, int):
            if sample_size > 0:
                skip = sorted(random.sample(range(lower, self._n + 1), self._n - sample_size))
            else:
                raise_custom_error(ValueError, 'Sample size must be positive.')
        else:
            raise_custom_error(TypeError, 'Argument "sample" should be either a positive integer or None.')

        # Load the dataset.

        if as_df:
            self._data = pandas.read_csv(self._file_dir, skiprows = skip, **kwargs)
        else:
            with open(self.file_dir, newline = self._newline) as csv_file:
                reader = csv.reader(csv_file, delimiter = self._delimiter, quotechar = self._quotechar,
                                    **kwargs)
                if skip == None:
                    self._data = [each for each in reader]
                else:
                    keep = [each for each in range(lower, n) if each not in skip]
                    keep_max = max(keep)
                    output = []
                    for each in enumerate(reader):
                        if each[0] in keep:
                            output.append(each[1])
                        elif each[0] > keep_max:
                            break    # No need to proceed further
                    self._data = output

        # Convert columns to datetime as specified
        if datetime_cols != None:
            for col in datetime_cols:
                self._data[col] = pandas.to_datetime(self._data[col])