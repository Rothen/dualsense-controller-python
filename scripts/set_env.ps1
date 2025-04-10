New-Variable os -Value 'Windows' -Option Constant

New-Variable version -Value ('18') -Option Constant
New-Variable latest -Value ($version -eq 'latest') -Option Constant
New-Variable x64 -Value ('x64' -eq 'x64') -Option Constant

$clang = 'clang'
$clangxx = 'clang++'

function Link-Exe {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Exe,
        [Parameter(Mandatory = $true)]
        [string] $LinkName
    )

    $exe_path = (Get-Command $Exe).Path
    $link_dir = if ($script:windows_host) { Split-Path $exe_path } else { '/usr/local/bin' }
    $link_name = if ($script:windows_host) { "$LinkName.exe" } else { $LinkName }
    $link_path = if ($script:cygwin_host) { "$link_dir/$link_name" } else { Join-Path $link_dir $link_name }
    Write-Output "Creating link $link_path -> $exe_path"
    if ($script:linux_host) {
        sudo ln -f -s $exe_path $link_path
    }
    elseif ($script:cygwin_host) {
        ln.exe -f -s $exe_path $link_path
    }
    elseif ($script:windows_host) {
        New-Item -ItemType HardLink -Path $link_path -Value $exe_path -Force | Out-Null
    }
}

if ($cc) {
    Link-Exe $clang cc
    if ($clang -ne 'clang') {
        Link-Exe $clang 'clang'
    }
    Link-Exe $clangxx c++
    if ($clangxx -ne 'clang++') {
        Link-Exe $clangxx 'clang++'
    }
}

# Load MSVC environment
$vcvarsPath = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
$arch = "x64"  # Change to your desired architecture (e.g., x86, x64, arm, etc.)

cmd.exe /c " `"$vcvarsPath`" $arch && set " | ForEach-Object {
    if ($_ -match "^(.*?)=(.*)$") {
        Set-Item -Path "Env:\$($matches[1])" -Value "$($matches[2])"
    }
}

# Set environment variables
$ErrorActionPreference = "Stop"
$env:CC = "clang-cl.exe"
$env:CXX = "clang-cl.exe"
$env:python_path = "C:\Users\benir\anaconda3\envs\chiaki-ng"