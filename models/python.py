"""
ilab models
"""
import io
import re
import os
import time
from turtle import st
import uuid
import traceback
import shlex, subprocess
from pathlib import Path
from django.db import models

##### Global Constants #####
alphabet_size = 26
error = "*$$##Error$$##!"
new_line = "!$$^^new_line$$@#@"
run_over = "#$$##@*run_over$$##@*"
input_indicator = "#$^@*@input&&@*"
exception_handle = '\n\t\t'.join(["errors = io.StringIO()", 
                             "traceback.print_exc(file=errors)", 
                             "content = str(errors.getvalue())", 
                             f"content = content.replace('\\n','{new_line}')", 
                             "print('{}\\t%s' % (content))".format(error), 
                             "errors.close()"])
_check_timeout = lambda start, timeout: time.time() - start > timeout 
infinite_loop = "\033[91mRuntimeError: Code took long, check for infinite loops\033[0m"


##### Classes #####
class Python(models.Model):
    """
    AF(id) = a volatile python interpreter with a globally unique id, self destructs after 24 hours 

    Representation Invariant
      - inherits from models.Model
   
    Representation Exposure
      - inherits from models.Model
      - access allowed to all fields but they are all immutable
    """
    ##### Representation #####
    id_value         = uuid.uuid4()
    docker_image     = models.CharField(max_length = alphabet_size)
    id               = models.UUIDField(primary_key = True,  editable = False, unique = True, default = id_value)
    interpreter_path = models.CharField(max_length = alphabet_size**2, default = f"{Path(__file__).parent.absolute()}{os.sep}interpreters/{id_value}.py")
    
    def execute(self, code: str, user_inputs: list = [], n: int = 0, timeout: int = 60) -> bool:
        """
        Executes the code while communicating with the backend via a websocket
        Websocket (docker) <- socket -> Backend (django) <- socket -> Frontend (reactjs)
    
        Inputs
            :code: <str> of script to be executed
            :user_inputs: <list> of user inputs, [] by default
            :n: <int> last printed line, initially 0
            :timeout: <int> how long to run the code for before force stopping in seconds

        Throws
            <RunTimeError> if execution takes longer than timeout seconds
        """
        code = self._prepare_code(code)
        self._overwrite(code)

        process = self._spawn()
        process.stdout.flush()
        process.stdin.flush()
        
        # i ::= last line executed, j ::= number of requested user inputs
        i, j = 0, 0 
        stop = False            
        start = time.time()
        while True:
            i += 1
            run_error = False
            need_input = False
            out = str(process.stdout.readline(), 'utf8').strip()
            
            if out == run_over: return
            elif out == "": continue
            elif out.startswith(error): 
                run_error = True
                out = "Error Occurred:\n%s" % out.replace(error, "") \
                                                 .replace(new_line, "\n") \
                                                 .replace(self.interpreter_path, "")
            # Handling user input prompts
            if out.startswith(input_indicator): 
                out = out.replace(input_indicator, "")
                if len(user_inputs) > j: 
                    process.stdin.write(f"{user_inputs[j]}\n".encode())
                    process.stdin.flush()
                    j += 1
                else: need_input = True
            
            if _check_timeout(start, timeout): 
                stop = True
                out = infinite_loop 

            if i > n: yield out, i, need_input
            if run_error or need_input or stop: return
            
    def __str__(self) -> str:
        """ Override models.Model.__str__() """
        raise NotImplementedError

    ##### Helper Methods #####
    def _spawn(self) -> subprocess:
        """
        Creates a sub-process to run this interpreter
        
        Outputs
            :returns: <subprocess> a sub-process that runs the interpreter
        """
        command = shlex.split(f"python3 {self.interpreter_path} spwan")
        return subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    def _prepare_code(self, code) -> str:
        """
        Prepares the code to be executed by changing all input('...') -> input('$...\n') 

        Inputs 
            :code: <str> of script to be executed
        
        Outputs
            :returns: <str> code prepared for execution
        """ 
        code = '\n\t\t'.join(map(self._modify_codeline, code.split("\n")))
        return f"if __name__ == '__main__':\n\tprint('#^*&starting#(*&^')\n\timport io\n\timport traceback\n\ttry:\n\t\t{code}\n\t\tprint('{run_over}')\n\texcept Exception as e:\n\t\t{exception_handle}"
    
    def _overwrite(self, code):
        """
        Overwrite the interpreter's script with code

        Inputs
            :code: <str> containing the code
        """
        with open(self.interpreter_path, 'w') as script:
            script.seek(0)
            script.truncate(0)
            script.write(code)
            script.close()

    def _modify_codeline(self, line):
        """
        Modifies a line of code so the interpreter can use

        Modifications
            - inputs('...') -> inputs('$...\n')

        Inputs
            :line: <str> line of code to be modified

        Outputs
            <str> modified line
        """
        input_calls = re.findall(r"input\([\'\"].*[\'\"]\)", line)
        for input_call in input_calls:
            modified_call = "input('{}' + {} + {})".format(input_indicator, input_call[6:-1], repr('\\n'))
            line = re.sub(r"{}".format(input_call.replace('(', '\(').replace(')', '\)')), modified_call, line)
        return line