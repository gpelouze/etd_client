# ETD client

Unofficial client for to the [Exoplanet Transit Database][etd-home].

## Installation

1. Clone this repository
2. Run `pip install .`

## Example

~~~python
from etd_client import ETDClient
ec = ETDClient(location=(48.7027, 2.1827))
predictions = ec.get_predictions(start_date='2019-01-01', end_date='2019-01-03')
print(predictions)
#     starname planet         ...                            ra                   de
# 0    WASP-76      b         ...            [1.0, 46.0, 31.86]     [2.0, 42.0, 2.0]
# 1   HAT-P-15      b         ...            [4.0, 24.0, 59.55]  [39.0, 27.0, 38.17]
# 2   HAT-P-66      b         ...            [10.0, 2.0, 17.52]    [53.0, 57.0, 3.1]
# 3     KELT-1      b         ...             [0.0, 1.0, 26.92]    [39.0, 23.0, 1.7]
# 4   HAT-P-37      b         ...           [18.0, 57.0, 11.16]    [51.0, 16.0, 8.9]
# ..       ...    ...         ...                           ...                  ...
# 46   WASP-14      b         ...            [14.0, 33.0, 6.35]  [21.0, 53.0, 40.98]
# 47   WASP-43      b         ...           [10.0, 19.0, 38.01]   [-9.0, 48.0, 21.9]
# 48  HAT-P-36      b         ...            [12.0, 33.0, 3.96]   [44.0, 54.0, 55.3]
# 49  HAT-P-67      b         ...            [17.0, 6.0, 26.57]  [44.0, 46.0, 36.79]
# 50  WASP-157      b         ...           [13.0, 26.0, 37.24]    [-8.0, 19.0, 3.2]
# 
# [51 rows x 19 columns]
~~~


## License

This package is released under a MIT open source licence. See `LICENSE.txt`.

[etd-home]: http://var2.astro.cz/ETD
