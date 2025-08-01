import datetime

from analysis.log_data_analysis.classes.stage_log import StageLog
from analysis.log_data_analysis.classes.timestamp_parser import TimestampParser
from analysis.log_data_analysis.enums import DebuggingStage
from analysis.log_data_analysis.testing_service.test_report import TestReport

class ExerciseLog:
    def __init__(self, id: str, student_id: str, exercise_name: str, stage_logs: list[StageLog], start_time: str, end_time: str, session: int):
        self._id: str = id
        self._student_id: str = student_id
        self._exercise_name: str = exercise_name
        self._stage_logs: list[StageLog] = ExerciseLog.sort_stage_logs(stage_logs)
        self._start_time: datetime = TimestampParser.parse_timestamp_str(start_time)
        self._end_time: datetime = TimestampParser.parse_timestamp_str(end_time)
        self._session: int = session
    
    @property
    def id(self) -> str:
        return self._id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def exercise_name(self) -> str:
        return self._exercise_name

    @property
    def stage_logs(self) -> list[StageLog]:
        return self._stage_logs

    @property
    def start_time(self) -> datetime:
        return self._start_time
    
    @property
    def end_time(self) -> datetime:
        return self._end_time
    
    @property
    def session(self) -> int:
        return self._session
    
    @property
    def test_report(self) -> TestReport | None:
        return self._test_report if hasattr(self, '_test_report') else None
    
    @test_report.setter
    def test_report(self, value: TestReport):
        self._test_report = value

    @staticmethod
    def parse_exercise_log(raw_exercise_logs: dict, stage_logs: list[StageLog]) -> 'ExerciseLog':
        return ExerciseLog(
            id = raw_exercise_logs["id"],
            student_id = raw_exercise_logs["studentId"],
            exercise_name = raw_exercise_logs["exerciseId"],
            stage_logs = stage_logs,
            start_time = raw_exercise_logs["startTime"],
            end_time = raw_exercise_logs["endTime"],
            session = raw_exercise_logs.get("session")
        )
    
    @staticmethod
    def sort_stage_logs(stage_logs: list[StageLog]) -> list[StageLog]:
        exit_logs: list[StageLog] = []
        non_exit_logs: list[StageLog] = []
        for log in stage_logs:
            if log.stage_name == DebuggingStage.exit:
                if exit_logs == []:
                    exit_logs.append(log)
            else:
                non_exit_logs.append(log)
        non_exit_logs.sort(key=lambda log: log.overall_stage_number)
        return non_exit_logs + exit_logs
    
    def __repr__(self):
        return f'ExerciseLog(\'{self._student_id}\', \'{self._exercise_name}\', {self._start_time}, {self._stage_logs})'
