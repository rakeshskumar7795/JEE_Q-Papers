' Starts the JEE dashboard in the background (no console window).
' Open http://localhost:8501 if the browser does not open by itself.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Run "cmd /c py -m streamlit run app.py", 0, False
