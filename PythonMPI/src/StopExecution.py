"""StopExecution - Stop the execution and raise an exception
"""
class StopExecution(Exception):
    def _render_traceback_(self):
        pass

