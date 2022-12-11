import sys
import os
import subprocess
from timeit import default_timer as timer
import _thread

import sys
import importlib
import contextlib
import subprocess
from io import StringIO
from wrapt_timeout_decorator import *

PYTHON_PATH = os.path.realpath(sys.executable)
FOLDER = os.path.dirname(os.path.abspath(__file__))
cwd = os.getcwd()

class CodeExecuter():
    def __init__(self,code:str):
        self.output = []
        self.final_output = []
        self.file_path = os.path.join(cwd,"temp_run.py")
        with open(self.file_path,"w") as file:
            file.write(code)
            file.close()

    def execute_code(self):
        process = subprocess.run([PYTHON_PATH,self.file_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.output = ["".join(process.stderr.decode()),process.stdout.decode()]
        self.execution_end = timer()
        os.remove(self.file_path)
        self.final_output = [abs(self.execution_start-self.execution_end),self.output,process.returncode]

    def execute_python(self):
        self.execution_start = timer()
        _thread.start_new_thread(self.execute_code,())
        while abs(self.execution_start-timer()) < 10 and self.final_output == []:
            continue

        if len(self.final_output) == 0:
            return [10,["Timeout!","Code cannot run for more than 10 secs"],1]
        else:
            return self.final_output


class CodeExecutor2:
    @contextlib.contextmanager
    def stdoutIO(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    @timeout(5)
    def execute_python(self, code):
        with self.stdoutIO() as c:
            try:
                exec(code)
            except Exception as e:
                print(e)
        return c.getvalue()