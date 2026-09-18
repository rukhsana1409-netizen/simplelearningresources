param(
    [Parameter(Mandatory = $true)]
    [string]$Config,

    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $repositoryRoot ".venv\Scripts\python.exe"
$publisher = Join-Path $repositoryRoot "worksheet-generator\publish_assets.py"
$configPath = if ([System.IO.Path]::IsPathRooted($Config)) {
    $Config
} else {
    Join-Path $repositoryRoot $Config
}

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Publishing environment not found. Create .venv and install requirements-publish.txt first."
}

$arguments = @($publisher, "resource", $configPath, "--generate")
if ($Apply) {
    $arguments += "--apply"
}

& $python @arguments
exit $LASTEXITCODE
