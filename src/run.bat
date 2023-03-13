@echo off
set d=%date:~0,10%
set d=%d:/=_%

set t=%time:~0,8%
set t=%t::=_%
echo 
:: ..\python-3.10.8-embed-amd64\python.exe TestStart.py 2>.\report\%d%_%t%_Test_Log.txt
..\python-3.10.8-embed-amd64\python.exe TestStart.py
@pause