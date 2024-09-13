function ShowStdOutStdErr {
    Write-Output "exit code: $LASTEXITCODE"

    if ((Get-Item tmp\stdout.txt).Length -ne 0) {
        Write-Output "`nstdout:"
        Get-Content tmp\stdout.txt
    }

    if ((Get-Item tmp\stderr.txt).Length -ne 0) {
        Write-Error "`nstderr:"
        Get-Content tmp\stderr.txt
    }

    Write-Output "`nLaunch Failed"
    Pause
}

$PYTHON = if ($env:PYTHON) { $env:PYTHON } else { 'python' }
$VENV_DIR = Join-Path $PSScriptRoot 'venv'

New-Item -Path 'tmp' -ItemType Directory -ErrorAction SilentlyContinue

try {
    & $PYTHON -c '' 2>tmp\stderr.txt | Out-File tmp\stdout.txt
} catch {
    Write-Output 'Cannot launch python'
    . ShowStdOutStdErr

    exit
}

try {
    & $PYTHON -m pip --help 2>tmp\stderr.txt | Out-File tmp\stdout.txt
} catch {
    if (!$env:PIP_INSTALLER_LOCATION) {
        . ShowStdOutStdErr

        exit
    }

    & $PYTHON $env:PIP_INSTALLER_LOCATION 2>tmp\stderr.txt | Out-File tmp\stdout.txt

    if ($LASTEXITCODE -ne 0) {
        Write-Output 'Cannot install pip'
        . ShowStdOutStdErr
        exit
    }
}

if ($VENV_DIR -ne '-') {
    if (Test-Path (Join-Path $VENV_DIR 'Scripts\Python.exe')) {
        $PYTHON = Join-Path $VENV_DIR 'Scripts\Python.exe'
    } else {
        $PYTHON_FULLNAME = & $PYTHON -c 'import sys; print(sys.executable)'

        Write-Output "Using python: $PYTHON_FULLNAME"
        Write-Output "Creating VENV: $VENV_DIR"

        & $PYTHON_FULLNAME -m venv $VENV_DIR 2>tmp\stderr.txt | Out-File tmp\stdout.txt

        if ($LASTEXITCODE -eq 0) {
            $PYTHON = Join-Path $VENV_DIR 'Scripts\Python.exe'
        } else {
            Write-Output "Failed creating VENV: '$VENV_DIR'"
            . ShowStdOutStdErr

            exit
        }
    }

    Write-Output "Using VENV: $VENV_DIR"
}

& pip install -r requirements.txt
& streamlit run interactive_page.py