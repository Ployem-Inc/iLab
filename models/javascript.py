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
syntax_error = "SyntaxError"
new_line = "!$$^^new_line$$@#@"
indent_error = "IndentationError"
run_over = "#$$##@*run_over$$##@*"
input_indicator = "#$^@*@input&&@*"
_check_timeout = lambda start, timeout: time.time() - start > timeout 
infinite_loop = "\033[91mRuntimeError: Code took long, check for infinite loops\033[0m"


##### Classes #####
class Javascript(models.Model):
    """
    AF(id) = a volatile javascript interpreter with a globally unique id, self destructs after 24 hours 

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
    interpreter_path = models.CharField(max_length = alphabet_size**2, default = f"{Path(__file__).parent.absolute()}{os.sep}interpreters/{id_value}.js")
    
    def execute(self, code: str, user_inputs: list = [], n: int = 0, timeout: int = 20) -> bool:
        """
        Executes the code while communicating with the backend via a websocket
        Websocket (docker) <- socket -> Backend (django) <- socket -> Frontend (reactjs)
    
        Inputs
            :code: <str> of script to be executed
            :user_inputs: <list> of user inputs, [] by default
            :n: <int> last printed line, initially 0
            :timeout: <int> how long to run the code for before force stopping in seconds, initially 20s

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
            out = str(process.stdout.readline(), 'utf8').strip().replace(f"{self.interpreter_path}", "")

            if out == run_over: return
            elif out == "": continue
            elif out.startswith(error): 
                run_error = True
                out = "Error Occurred:\n%s" % out.replace(error, "") \
                                                 .replace(new_line, "\n")
            elif out.startswith(syntax_error) or out.startswith(indent_error): run_error = True

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
        command = shlex.split(f"node {self.interpreter_path} spawn")
        return subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    def _prepare_code(self, code) -> str:
        """
        Prepares the code to be executed by changing all input('...') -> input('$...\n') 

        Inputs 
            :code: <str> of script to be executed
        
        Outputs
            :returns: <str> code prepared for execution
        """ 
        code = '\n\t'.join(map(self._modify_codeline, enumerate(code.split("\n"))))
        return f"try {{\n\tconsole.log('#^*&starting#(*&^')\n\t{code}\n\n\tconsole.log('{run_over}')\n}} catch (error) {{console.log(`{error} ${{error}}`)}}"
    
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
            :line: (<int>, <str>) line number and line of code to be modified

        Outputs
            <str> modified line
        """
        n, line = line
        #TODO: any modifications
        return line