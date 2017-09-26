py -3.5 "C:\Python35\Scripts\cxfreeze" pyoxy-ui.py --compress --base-name=Win32GUI --target-dir=../app/pyoxy-ui-amd64 --include-modules=cffi
copy pyoxy\*.net ..\app\pyoxy-ui-amd64\
copy pyoxy\*.ntpt ..\app\pyoxy-ui-amd64\
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-ui-amd64\python*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-ui-win32\img\*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-ui-amd64\*.pyd

py -3.5-32 "C:\Program Files (x86)\Python35\Scripts\cxfreeze" pyoxy-ui.py --compress --base-name=Win32GUI --target-dir=../app/pyoxy-ui-win32 --include-modules=cffi
copy pyoxy\*.net ..\app\pyoxy-ui-win32\
copy pyoxy\*.ntpt ..\app\pyoxy-ui-win32\
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-ui-win32\python*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-ui-win32\img\*.dll
C:\Users\Bruno\upx.exe --best ..\app\pyoxy-ui-win32\*.pyd
