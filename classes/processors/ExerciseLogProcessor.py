import datetime
from classes import ProgramLog
from classes.ExerciseLog import ExerciseLog
from classes.StageLog import StageLog
from classes.processors.StageLogProcessor import StageLogProcessor
from enums import DebuggingStage

class ExerciseLogProcessor:

    @staticmethod
    def get_stage_names(exercise_log: ExerciseLog) -> list[str]:
        return [DebuggingStage(stage.stage_name).value for stage in exercise_log.stage_logs]
    
    @staticmethod
    def get_last_stage(exercise_log: ExerciseLog) -> StageLog:
        #Need to sort list by overall stage number and get name of last one. UPDATE: Should be done in StageLog now
        exercises_stages: list[StageLog] = exercise_log.stage_logs
        exercises_stages = [stage for stage in exercises_stages if stage.stage_name.value != "exit"]
        #Remove exit logs as they don't contain a overall_stage_number property
        if len(exercises_stages) > 0:
            exercises_stages.sort(key=lambda x : x.overall_stage_number)
            return(exercises_stages[len(exercises_stages) - 1])
        return None
    
    @staticmethod
    def is_error_reportedly_solved() -> bool:
        pass

    @staticmethod
    def get_last_program_log(exercise_log: ExerciseLog) -> ProgramLog:
        """Declare stages that may contain program logs

        Then iterate backwards through the stages of the exercise log to find first stage with program logs --> return
        Else return none
        """
        stages_with_program_logs: list[DebuggingStage] = [DebuggingStage.run, DebuggingStage.inspect_code, DebuggingStage.fix_error, DebuggingStage.test]
        for i in range(len(exercise_log.stage_logs) - 1, -1, -1):
            stage_log = exercise_log.stage_logs[i]
            if stage_log.stage_name in stages_with_program_logs and stage_log.program_logs is not None:
                return stage_log.program_logs[-1]
        return None

    @staticmethod
    def is_final_program_erroneous(exercise_log: ExerciseLog) -> bool:
        last_program_log = ExerciseLogProcessor.get_last_program_log(exercise_log)
        return last_program_log.compiled if last_program_log is not None else None

    @staticmethod
    def get_time_on_exercise(exercise_log: ExerciseLog) -> float:
        return (exercise_log.end_time - exercise_log.start_time).total_seconds()

    @staticmethod
    def get_written_response_data(exercise_log: ExerciseLog) -> list[list[DebuggingStage, str, any, str]]:
        responses: list[list[DebuggingStage, str, any, str]] = []
        for stage_log in exercise_log.stage_logs:
            if stage_log.stage_name in [DebuggingStage.predict, DebuggingStage.spot_defect, DebuggingStage.inspect_code, DebuggingStage.fix_error]:
                response_data: list[DebuggingStage, str, any, str] = [exercise_log.exercise_name, stage_log.stage_name, stage_log.end_time, stage_log.response]
                responses.append(response_data)
        responses.sort(key=lambda x: (x[0], x[2]))
        return responses
    
    @staticmethod
    def get_time_focused(exercise_log: ExerciseLog) -> float:
        #Returns time spent focused on exercise as a percentage of time spent on exercise
        time_focused: float = 0
        time_on_exercise: float = ExerciseLogProcessor.get_time_on_exercise(exercise_log)
        for stage_log in exercise_log.stage_logs:
            time_focused_on_stage = StageLogProcessor.get_time_focused(stage_log)
            time_focused += time_focused_on_stage
        return (time_focused / time_on_exercise) * 100
    

    @staticmethod
    def were_test_cases_viewed(exercise_log: ExerciseLog) -> bool:
        """Checks whether the test case panes were viewed at any point during the PRIMMDebug exercise
        (i.e., in any of the PRIMMDebug stages that displayed the test case pane)

        Args:
            exercise_log (ExerciseLog): The exercise_log to perform the function on

        Returns:
            bool: A bool value indicating whether a test case pane was viewed at any point during the exercise. Returns None if the exercise doesn't contain test case pane.
        """
        stages_with_test_case_pane: list[DebuggingStage] = [DebuggingStage.inspect_code, DebuggingStage.test]
        relevant_exercise_stages: list[StageLog] = [stage for stage in exercise_log.stage_logs if stage.stage_name in stages_with_test_case_pane]
        for stage in relevant_exercise_stages:
            if stage.test_case_logs is not None:
                return True
        return False