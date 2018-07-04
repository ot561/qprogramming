from tkinter import *
from tkinter import messagebox
from functools import partial
from shor_alg import shor
from tkinter.messagebox import showinfo
import webbrowser

def run_shor(n):
    return shor(n)
        
def run_projectq():
    s="project q"
    showinfo(title="reply", message = "not implemented %s yet!" % (s) )
    print(s)

def run_qsharp():
    print('no q# for you')
    s="q#"
    showinfo(title="reply", message = "not implemented %s yet!" % (s) )
    print(s)

def run_qiskit():
    s="qiskit"
    showinfo(title="reply", message = "not implemented %s yet!" % (s) )
    print(s)

def run_pyquil():
    s='pyquil'
    showinfo(title="reply", message = "not implemented %s yet!" % (s) )
    print(s)
