rem Please run this script from the root path. ".\tools\create_executable.bat"
pyinstaller --noconfirm --onefile --console --name "pyJiraCli" --add-data "./pyproject.toml;."  "./src/pyJiraCli/__main__.py"