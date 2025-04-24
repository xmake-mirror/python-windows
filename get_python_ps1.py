import sys

PS1_SOURCE = """
New-Item -Path . -Name python-install -ItemType "directory"
$InstallPath = (Resolve-Path -Path .\python-install).Path

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/{pyver}/python-{pyver}{suffix}.exe" -OutFile .\python.exe
.\python.exe /passive /uninstall | Wait-Job
.\python.exe /passive InstallAllUsers=0 Include_doc=0 Include_test=0 PrependPath=0 TargetDir=$InstallPath | Wait-Job
Compress-Archive -Path $InstallPath\* -DestinationPath .\python-{pyver}{arch}.zip

New-Item -Path .\python-install -Name launcher -ItemType "directory"
Copy-Item -Path C:\Windows\py.exe -Destination $InstallPath\launcher\py.exe
Copy-Item -Path C:\Windows\pyw.exe -Destination $InstallPath\launcher\pyw.exe
{dllinst}
Compress-Archive -Path $InstallPath\launcher\* -DestinationPath .\python-launcher-{pyver}{arch}.zip
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python " + __file__ + " <version> <bits>")
        exit(1)
    pyver = sys.argv[1]
    arch_input = "64"
    if len(sys.argv) > 2:
        arch_input = sys.argv[2]
    if arch_input == "64":
        suffix = "-amd64"
        arch = ".win64"
        dllinst = "Copy-Item -Path C:\Windows\pyshellext.amd64.dll -Destination $InstallPath\launcher\pyshellext.amd64.dll"
    elif arch_input == "arm64":
        suffix = "-arm64"
        arch = ".winarm64"
        dllinst = ""
    elif arch_input == "32":
        suffix = ""
        arch = ".win32"
        dllinst = ""
    else:
        print(f"Error: Unsupported architecture '{arch_input}'. Use '32', '64', or 'arm64'.")
        exit(1)

    with open(f"get_python_{pyver}_{arch_input}.ps1", "w") as f:
        f.write(PS1_SOURCE.format(pyver=pyver, suffix=suffix, arch=arch, dllinst=dllinst))
