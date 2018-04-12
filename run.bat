

@echo OFF


REM Script name: run

REM Arguments:   3 file names for config_file clients_file transactions_file

REM Synopsis:    Script sets environment variables and invokes the system's
REM              main application menu, passing the three argument through


set config=%1 
set clients=%2
set trans=%3
set companies=%4


if not defined config goto con
if not defined clients goto clnt
if not defined trans goto tran
if not defined companies goto company
goto run


:con
echo No config file
goto EOF

:clnt
echo No clients file
goto EOF

:tran
echo No transactions file
goto EOF


:company
echo No companies file
goto EOF 

echo Hello




:run


SET PROJECT_BASE_DIR=%CD%

SET PYTHONPATH=%PROJECT_BASE_DIR%/packages;%PROJECT_BASE_DIR%/tests


echo  
echo  
echo
  


python3 packages/ui/mainapp.py %*



:EOF