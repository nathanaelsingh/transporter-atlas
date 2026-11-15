# Create a new GitHub repository for Transporter Atlas

The repository has **not** yet been created on your account. This package contains everything needed to create it and deploy the website. The proposed name is `transporter-atlas`.

## Mac or Linux: guided automatic setup

1. Download and unzip `Transporter_Atlas_Ready_for_GitHub.zip` into a new folder.
2. Open Terminal in that folder.
3. Install GitHub CLI if needed: on macOS with Homebrew, run `brew install gh`. Git and Python 3 must also be available.
4. Authenticate: `gh auth login`. Select GitHub.com, HTTPS and browser login when prompted.
5. Run: `bash setup_github.sh`.

This creates a **public** repository under your authenticated GitHub account, commits the website and updater, attempts to enable GitHub Pages, and requests the first literature refresh. To create a private repository instead, run `VISIBILITY=private bash setup_github.sh` (private-repo Pages availability depends on your GitHub plan).

Only public literature references and the site's source files are in the package. Personal project notes entered into the Atlas are stored on your own browser device and are not uploaded by the setup script. Do not add unpublished data or embargoed research to a public repository.

## Alternative: use the GitHub website

1. Visit https://github.com/new and make a **public** repository named `transporter-atlas` with no initial README or license.
2. Extract the ZIP locally, then upload all files and folders *inside* it to the repository. Preserve the `.github/workflows/` directory (hidden by default on some computers). Upload the extracted contents, not the ZIP itself.
3. Under repository **Settings > Actions > General > Workflow permissions**, enable **Read and write permissions**, if available.
4. Under **Settings > Pages**, set **Build and deployment source** to **GitHub Actions**.
5. In **Actions**, open **Update literature and deploy atlas** and select **Run workflow**.
6. Check that the workflow has a green checkmark and visit `https://YOUR_USERNAME.github.io/transporter-atlas/`.

The scheduled job updates publication search metadata weekly and redeploys the site. It does **not** independently verify papers or relabel targets as functional transporters. Manual scientific curation remains necessary. Scheduled jobs may be delayed or deactivated due to GitHub policies or prolonged repository inactivity.

## Project files

- `docs/index.html`: deployable website, works as a local standalone file too
- `data/targets.json`: curated target registry
- `data/literature.json`: publication-watch search results, machine generated
- `.github/workflows/update-and-deploy.yml`: Monday literature refresh and Pages deployment
- `scripts/`: literature updater and site builder
- `tests/`: data-integrity tests

See `README.md` for evidence standards and maintenance instructions.
