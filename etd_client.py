#!/usr/bin/env python3

import datetime
import re
import warnings

import bs4
import requests
import pandas as pd

class ETDClient():
    def __init__(self, location=None):
        ''' Get transit prediction

        Parameters
        ==========
        location : 2-tuple of float or None (default: None)
            A tuple containing the latitude and longitude of the observation
            location.
        '''
        self.base_url = 'http://var2.astro.cz/ETD'
        self.predictions_url = self.base_url + '/predictions.php'
        self.predict_details_url = self.base_url + 'predict_details.php'
        if location is None:
            self.location = None, None
        else:
            self.location = location

    @property
    def location(self):
        return self.lat, self.lon

    @location.setter
    def location(self, location):
        lat, lon = location
        self.lat = lat
        self.lon = (lon + 360) % 360

    def _parse_position(self, position):
        alt, az = position.split(',')
        alt = float(alt.strip('°'))
        return alt, az

    def _parse_ra_de(self, coord):
        r = re.compile('(?:RA|DE): ([+-]? ?\d+) +(\d+) +([\d. ]+)')
        m = r.match(coord)
        if m:
            coord = [float(c.replace(' ', '')) for c in m.groups()]
        else:
            raise ValueError('Could not match {}'.format(coord))
        return coord

    def _parse_predictions_table(self, html, start_date, end_date):
        b = bs4.BeautifulSoup(html, features='lxml')
        table = next(b.find('div', attrs={'class': 'center'}).children)
        parsed_table = []
        for row in table.find_all('tr')[2:]:
            # dirty removal of <sup> tags (that usually mark non-linear
            # ephemeris)
            for child in row.recursiveChildGenerator():
                if child.name == 'sup':
                    child.extract()
                    break
            cells = row.get_text(separator='\xa0')
            if cells:
                parsed_table.append(cells.split('\xa0'))

        data = []
        for transit in parsed_table:

            starname = transit[0]
            planet = transit[1]
            constellation = transit[2]

            begin_time = transit[3]
            begin_position= transit[4]
            center_datetime = transit[5]
            center_position = transit[6]
            end_time = transit[7]
            end_position = transit[8]

            duration = transit[9]
            mag = transit[10]
            depth = transit[11]
            orbit_elements = transit[12]
            ra = transit[13]
            de = transit[14]

            # Guess year, because it is not displayed in the results table...
            # Start using the start date of the search range
            center_datetime = '{} {}'.format(start_date.year, center_datetime)
            center_datetime = datetime.datetime.strptime(
                center_datetime, '%Y %d.%m. %H:%M')
            # If the search range spans over two different years, and the
            # guessed date is before the start of the search range, add one
            # year. Will break if the search range is longer than 1 yr.
            if ((start_date.year != end_date.year) and
                (center_datetime.date() < start_date - datetime.timedelta(days=1))):
                center_datetime = datetime.datetime(
                    year=center_datetime.year + 1,
                    month=center_datetime.month,
                    day=center_datetime.day,
                    hour=center_datetime.hour,
                    minute=center_datetime.minute,
                    )
            # Compute begin and end times using duration and center time.
            # This is much easier than reading the time from the search results
            # and guessing the date.
            d = datetime.timedelta(minutes=float(duration))
            begin_datetime = center_datetime - d / 2
            end_datetime = center_datetime + d / 2

            # Parse position of star in the sky at the beginning, center, and
            # end of the transit
            begin_alt, begin_az = self._parse_position(begin_position)
            center_alt, center_az = self._parse_position(center_position)
            end_alt, end_az = self._parse_position(end_position)

            # Parse orbit elements
            elements = orbit_elements.split('+')
            primary_transit = elements[0]
            period = elements[1].strip(' ').strip('*E')
            if len(elements) > 2:
                msg = '{} parsed to {}+{}.'
                msg = msg.format(orbit_elements, primary_transit, period)
                warnings.warn(msg)
            primary_transit = 2400000 + float(primary_transit)
            period = float(period)

            # Parse star coordinates
            ra = self._parse_ra_de(ra)
            de = self._parse_ra_de(de)

            transit_data = [
                starname,
                planet,
                constellation,
                begin_datetime,
                center_datetime,
                end_datetime,
                begin_alt,
                begin_az,
                center_alt,
                center_az,
                end_alt,
                end_az,
                float(duration),
                float(mag),
                float(depth),
                primary_transit,
                period,
                ra,
                de
                ]

            data.append(transit_data)

        columns = [
            'starname',
            'planet',
            'constellation',
            'begin_time',
            'center_time',
            'end_time',
            'begin_alt',
            'begin_az',
            'center_alt',
            'center_az',
            'end_alt',
            'end_az',
            'duration',
            'mag',
            'depth',
            'primary_transit',
            'period',
            'ra',
            'de',
            ]
        return pd.DataFrame(data, columns=columns)

    def get_predictions(self, start_date=None, end_date=None, location=None):
        ''' Get transit prediction

        Parameters
        ==========
        start_date : str, datetime.date or None (default: None)
            Start day of the search window. Strings should be 'YYYY-MM-DD'.
            If None, the current day is used.
        end_date : str, datetime.date or None (default: None)
            End day of the search window. Strings should be 'YYYY-MM-DD'.
            If None, start_date + 1 day is used.
        location : 2-tuple of float or None (default: None)
            A tuple containing the latitude and longitude of the observation
            location.
            If None, use the previously set location.

        Returns
        =======
        predictions : pd.DataFrame
            A DataFrame containing the following columns:

            name              Description               Unit        Example
            ----------------- ------------------------- ----------- ------------------------------
            starname          Name of the host star                 WASP-33
            planet            Name of the planet                    b
            constellation     Constellation abbrev.                 And
            begin_time        Times of the beginning,   UT          2018-12-10 16:44:30
            center_time         center, and end                     2018-12-10 18:06:00
            end_time            of the transit.                     2018-12-10 19:27:30
            begin_alt         Altitude and azimuth      ° (alt)     45
            begin_az            of the star at the                  E
            center_alt          beginning, center,                  58
            center_az           and end of the                      E
            end_alt             transit.                            71
            end_az                                                  SE
            duration          Duration of the transit   minutes     163
            mag               Magnitude of the star     mag         8.3
            depth             Depth of the transit      mag         0.0151
            primary_transit   Primary transit           BJD         2.45416e+06
            period            Orbital period            days        1.21987
            ra                Right asc. of the star    [h, m, s]   [2.0, 26.0, 51.08]
            de                Declination of the star   [°, ', "]   [37.0, 33.0, 2.5]
        '''

        if location is None:
            lat, lon = self.location
        if start_date is None:
            start_date = datetime.date.today()
        if end_date is None:
            end_date = start_date + datetime.timedelta(days=1)
        fmt = '%Y-%m-%d'
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, fmt).date()
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, fmt).date()

        query = {
            'sirka': lat,
            'delka': lon,
            'init': str(start_date),
            'till': str(end_date),
            'f': 'userdefined',
            }
        with requests.get(self.predictions_url, params=query, timeout=10) as r:
            r.raise_for_status()

        predictions = self._parse_predictions_table(
            r.content, start_date, end_date)
        return predictions

    def get_planet_predictions(self, starname, planet, location=None):
        raise NotImplementedError
