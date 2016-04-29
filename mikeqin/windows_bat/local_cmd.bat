@echo start upgrade %1
@echo root@%1
@plink.exe -ssh root@%1 -pw "" -m cmd.txt
@echo upgrade %1 finish
@pause
@exit

REM telnet or ssh demo for plink
REM @plink.exe -ssh root@%1 -pw "" -m cmd.txt
REM @plink.exe -telnet root@%1 < cmd.txt
