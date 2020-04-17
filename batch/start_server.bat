cd C:\Users\neil_\Documents\PythonScripts\Server\Website\batch
start /min db_updater.bat
timeout 3 /nobreak
start /min app.bat
start localhost.bat