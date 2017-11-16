from distutils.core import setup
import py2exe

includes = ["sip",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtGui"
            ]

datafiles = [("platforms", ["C:\\Python34\\Lib\\site-packages\\PyQt5\\plugins" +
                            "\\platforms\\qwindows.dll"]),
             ("", [r"c:\windows\syswow64\MSVCP100.dll",
                   r"c:\windows\syswow64\MSVCR100.dll"])]

setup(
    name='HSN_Mifare',
    version='0.1',
    packages=['main'],
    url='',
    license='',
    author='vanmele',
    author_email='benoit.vanmele@hospital-eupen.be',
    description='',
    windows=[{"script": "startupscript.pyw"}],
    scripts=['startupscript.pyw'],
    data_files=datafiles,
    options={
        "py2exe":{
            "includes": includes,
        }
    }
)
