@echo off

rem The following variables shall be adapted:
set PROFILE="my_profile"
set FILTER="project=MYPROJ"
set MAX=5
echo Please set the variables inside this file.
echo:

rem Define and execute the command
set command=pyJiraCli --verbose --profile %PROFILE% search %FILTER% --max %MAX%

echo Executing....
echo %command%
echo:
%command%
pause