from distutils.core import setup
import py2exe

setup(console=['main.py'], options={"py2exe": {"includes": ["sys", "PyQt5.QtWidgets", "PyQt5.QtCore", "requests"]}})
