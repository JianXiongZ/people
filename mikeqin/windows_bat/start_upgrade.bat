for /f %%i in (ip.txt) do (
	start /wait local_cmd.bat %%i
)