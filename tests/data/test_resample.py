# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from numpy import nan
from pandas import (
    date_range,
    DataFrame,
    Timestamp
)

from zipline.data.resample import MinuteResampleSessionBarReader

from zipline.testing.fixtures import (
    WithTradingCalendars,
    WithBcolzFutureMinuteBarReader,
    ZiplineTestCase
)


class TestResampleSessionBars(WithBcolzFutureMinuteBarReader,
                              WithTradingCalendars,
                              ZiplineTestCase):

    TRADING_CALENDAR_STRS = ('CME',)

    minutes = date_range('2016-03-15 3:31',
                         '2016-03-15 3:36',
                         freq='min',
                         tz='US/Eastern').tz_convert('UTC')
    START_DATE = END_DATE = Timestamp('2016-03-15')

    @classmethod
    def make_future_minute_bar_data(cls):
        yield 1, DataFrame({
            'open': [nan, 103.50, 102.50, 104.50, 101.50, nan],
            'high': [nan, 103.90, 102.90, 104.90, 101.90, nan],
            'low': [nan, 103.10, 102.10, 104.10, 101.10, nan],
            'close': [nan, 103.30, 102.30, 104.30, 101.30, nan],
            'volume': [0, 1003, 1002, 1004, 1001, 0]
        },
            index=cls.minutes,
        )

    def test_resample(self):
        calendar = self.trading_calendars['CME']

        session = calendar.minute_to_session_label(self.minutes[0])
        session_bar_reader = MinuteResampleSessionBarReader(
            self.bcolz_future_minute_bar_reader
        )
        result = session_bar_reader.load_raw_arrays(
            ['open'], session, session, [1])

        import nose; nose.tools.set_trace()
        assert True
