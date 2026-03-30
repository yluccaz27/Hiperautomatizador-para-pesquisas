$extensoes = @(
    "enkia.tokyo-night",
    "catppuccin.catppuccin-vsc",
    "github.github-vscode-theme",
    "dracula-theme.theme-dracula",
    "pkief.material-icon-theme",
    "vscode-icons-team.vscode-icons",
    "usernamehw.errorlens",
    "oderwat.indent-rainbow",
    "aaron-bond.better-comments",
    "gruntfuggly.todo-tree",
    "christian-kohler.path-intellisense",
    "johnpapa.vscode-peacock"
)

foreach ($ext in $extensoes) {
    Write-Host "Instalando $ext ..."
    code --install-extension $ext --force
}

Write-Host "Fim. Extensões instaladas."