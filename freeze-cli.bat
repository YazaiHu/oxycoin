py -3.5 "C:\Python35\Scripts\cxfreeze" pyoxy-cli.py --compress --target-dir=../app/pyoxy-cli-amd64 --include-modules=cffi
copy pyoxy\*.net ..\app\pyoxy-cli-amd64\
copy pyoxy\*.ntpt ..\app\pyoxy-cli-amd64\
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-cli-amd64\python*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-cli-win32\img\*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-cli-amd64\*.pyd

py -3.5-32 "C:\Program Files (x86)\Python35\Scripts\cxfreeze" pyoxy-cli.py --compress --target-dir=../app/pyoxy-cli-win32 --include-modules=cffi
copy pyoxy\*.net ..\app\pyoxy-cli-win32\
copy pyoxy\*.ntpt ..\app\pyoxy-cli-win32\
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-cli-win32\python*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-cli-win32\img\*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-cli-win32\*.pyd
