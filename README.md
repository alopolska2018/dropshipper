In order to run:
1.Download and install mongodb community: https://www.mongodb.com/try/download/community?tck=docs_server
2.After configuring conda env, edit scrapyrt/resources.py (ex C:\ProgramData\Anaconda3\envs\dropshipper\Lib\site-packages\scrapyrt\resources.py)
 as per: https://github.com/gdelfresno/scrapyrt/commit/ee3be051ea647358a6bb297632d1ea277a6c02f8
3.If you didn't check "Add Anaconda to my PATH environment variable" in anaconda installer you have to add conda to sys path
as per https://stackoverflow.com/a/58211115
4.Add shortcut of run_scrapyrt.bat to run automatically at startup as per https://support.microsoft.com/en-us/windows/add-an-app-to-run-automatically-at-startup-in-windows-10-150da165-dcd9-7230-517b-cf3c295d89dd
