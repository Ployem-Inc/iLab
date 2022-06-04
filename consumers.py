import os
import json
from email import message
from tkinter import N
from .models.python import Python
from channels.generic.websocket import WebsocketConsumer

class PythonConsumer(WebsocketConsumer):
    """
    AF(id) = a volatile python interpreter with a globally unique id, self destructs after 24 hours 

    Representation Invariant
      - inherits from models.Model
   
    Representation Exposure
      - inherits from models.Model
      - access allowed to all fields but they are all immutable
    """
    ##### Representation #####
    interpreter = Python()
    interpreter_path = interpreter.interpreter_path

    def connect(self): 
        """
        Connects to the interperter and creates a script
        """
        self.accept()

    def disconnect(self, close_code): 
        """
        Disoconnects from the interperter and deletes the script 
        """
        try: os.remove(self.interpreter_path)
        except: pass

    def receive(self, text_data):
        """
        Executes a python script and returns the results, communicating with the frontend via a websocket 

        Inputs    
            :param text_data: <json> containing the id of the interpreter to execute the code with 

        Outputs
            :returns: Status … 
                            … HTTP_202_ACCEPTED if the user is verified
                            … HTTP_403_FORBIDDEN if the user is not verified
                            … HTTP_412_PRECONDITION_FAILED if one one more of the request fields don't meet their precondition(s)
        """
        data = json.loads(text_data)

        n = int(data['n'])
        code = data['code']
        timeout = float(data['timeout'])
        user_inputs = data['userInputs']

        for out, line, need_input in self.interpreter.execute(code, user_inputs, n, timeout):
            self.send(text_data = json.dumps({'out': out, 'n': line, 'input': need_input}))

