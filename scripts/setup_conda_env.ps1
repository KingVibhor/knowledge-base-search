# Helper script to create a conda environment and install requirements
# Usage: Open PowerShell, then run: .\scripts\setup_conda_env.ps1

param()

function Abort($msg){ Write-Error $msg; exit 1 }

# Check conda
$conda = Get-Command conda -ErrorAction SilentlyContinue
if (-not $conda) {
    Abort "Conda not found. Install Miniconda/Anaconda and re-run this script: https://docs.conda.io/en/latest/miniconda.html"
}

$envName = "kb-full"
Write-Output "Creating conda env '$envName' with Python 3.10..."
conda create -n $envName python=3.10 -y || Abort "Failed to create conda environment"

Write-Output "Activating environment..."
# Activation in script: use `conda run` to avoid activation issues
Write-Output "Installing numpy and pip from conda-forge..."
conda run -n $envName conda install -c conda-forge numpy pip -y || Abort "Failed to install numpy/pip via conda"

Write-Output "Installing Python requirements via pip... (this may take several minutes)"
conda run -n $envName pip install -r requirements.txt || Abort "pip install failed"

Write-Output "Done. To use the environment, run:`nconda activate $envName`"