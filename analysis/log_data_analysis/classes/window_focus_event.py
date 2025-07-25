import datetime

from analysis.log_data_analysis.classes.timestamp_parser import TimestampParser
from analysis.log_data_analysis.enums import FocusType

class WindowFocusEvent:
    def __init__(self, focus: FocusType, time: str):
        self._focus: FocusType = focus
        self._time: datetime = TimestampParser.parse_timestamp_str(time)

    @property
    def focus(self) -> FocusType:
        return self._focus
    
    @property
    def time(self) -> datetime:
        return self._time
    
    @staticmethod
    def parse_window_focus_event(raw_logs: dict) -> 'WindowFocusEvent':
        return WindowFocusEvent(
            focus = FocusType[raw_logs["focus"]],
            time = raw_logs["time"]
        )
    
    def __repr__(self):
        return f'WindowFocusEvent({self._focus}, {self._time})'