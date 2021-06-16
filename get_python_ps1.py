import sys

PS1_SOURCE = """
New-Item -Path . -Name python-install -ItemType "directory"
$InstallPath = (Resolve-Path -Path .\python-install).Path

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/{pyver}/python-{pyver}{suffix}.exe" -OutFile .\python.exe
.\python.exe /passive /uninstall | Wait-Job
.\python.exe /passive InstallAllUsers=0 Include_doc=0 Include_test=0 PrependPath=0 TargetDir=$InstallPath | Wait-Job

Copy-Item -Path C:\Windows\py.exe -Destination $InstallPath\py.exe
Copy-Item -Path C:\Windows\pyw.exe -Destination $InstallPath\pyw.exe
{dllinst}
Compress-Archive -Path $InstallPath\* -DestinationPath .\python-{pyver}{arch}.zip
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python " + __file__ + " <version> <bits>")
        exit(1)
    pyver = sys.argv[1]
    bits = "64"
    if len(sys.argv) > 2:
        bits = sys.argv[2]
    suffix = "-amd64" if bits == "64" else ""
    arch = ".win64" if bits == "64" else ".win32"

    dllinst = f"Copy-Item -Path C:\Windows\pyshellext.amd64.dll -Destination $InstallPath\pyshellext.amd64.dll" if bits == "64" else ""

    with open(f"get_python_{pyver}_{bits}.ps1", "w") as f:
        f.write(PS1_SOURCE.format(pyver=pyver, suffix=suffix, arch=arch, dllinst=dllinst))
