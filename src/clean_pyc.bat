for /f "delims=" %%d in ('dir /s /b /ad ^| findstr /I "__pycache__"') do (
	@echo deleting "%%d" ......
	@del /s /f /q "%%d"
	@rmdir "%%d"
)

for /f "delims=" %%f in ('dir /s /b /a *.bak') do (
	@echo deleting "%%f" ......
	@del /s /f /q "%%f"
)
@echo Complate!!!
@pause