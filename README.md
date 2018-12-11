# ETD client

Unofficial client for to the [Exoplanet Transit Database][etd-home].

## Installation

1. Clone this repository: `git clone https://github.com/ArcturusB/etd_client`
2. Install with pip: `pip install .` or `pip install --user .`

## Usage examples

### From the command line

~~~bash
$ etd_client 48.7027 2.1827 --max-mag 12.5 --min-depth 1.5
        object        date  begin center    end begin_pos center_pos   end_pos    D      V depth             RA              DE
4    WASP-69 b  2018-12-11  17:16  18:23  19:29  32.0° SW   24.0° SW  15.0° SW  134   9.87  1.8%  21h  0m  6.2s   -5°  5' 40.1"
15  HAT-P-32 b  2018-12-12  01:06  02:40  04:13  46.0° NW   33.0° NW  21.0° NW  186  11.29  2.2%   2h  4m 10.2s   46° 41' 16.8"
18   WASP-43 b  2018-12-12  04:11  04:46  05:20   33.0° S    34.0° S   33.0° S   70  12.40  2.6%  10h 19m 38.0s   -9° 48' 21.9"
29   WASP-77 b  2018-12-12  20:14  21:19  22:23   34.0° S    34.0° S  31.0° SW  130  10.29  1.7%   2h 28m 37.2s   -7°  3' 38.5"
34   WASP-35 b  2018-12-12  20:33  22:05  23:37  24.0° SE   33.0° SE   36.0° S  184  10.95  1.8%   5h  4m 19.6s   -6° 13' 47.2"
40   WASP-31 b  2018-12-13  05:04  06:24  07:43   22.0° S    22.0° S  18.0° SW  159  11.70  1.5%  11h 17m 45.4s  -19°  3' 17.3"
~~~

### As a Python module

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
