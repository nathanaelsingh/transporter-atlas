# Transporter Atlas — living deorphanization research hub

A reproducible and editable research workspace for investigating orphan transporters, ion channels and membrane proteins in mitochondria, lysosomes, endosomes, Golgi, ER, plasma membrane and other compartments.

## Open immediately

- Open `docs/index.html` locally in your browser. No web server or login is needed.
- The curated registry currently contains 31 candidate entries carried forward from Transporter Atlas v1; the evidence labels are provisional.
- Export your research notes (JSON) regularly: they are stored in your browser, not in the repository.
- Use **Evidence watch** to run a live Europe PMC query. When offline or if browser cross-origin rules block it, use the PubMed / Europe PMC links.

## Quick creation of a new GitHub repository

For a new deployment, see [`SETUP_GITHUB.md`](SETUP_GITHUB.md), or run `bash setup_github.sh` on a Mac/Linux computer with GitHub CLI authenticated. The default repository name is `transporter-atlas`.

## Publish to a permanent URL and activate automatic weekly updates

1. Create a GitHub repository named, for example, `transporter-atlas` and upload **the contents of this ZIP**, retaining `.github/workflows/update-and-deploy.yml`.
2. Make the default branch `main` and enable Actions. In **Settings → Actions → General → Workflow permissions**, allow **Read and write permissions** for `GITHUB_TOKEN` if your repository settings require it.
3. In **Settings → Pages**, choose **GitHub Actions** as the publishing source. GitHub will publish the `docs` folder through `actions/upload-pages-artifact` and `actions/deploy-pages`.
4. Open **Actions → Update literature and deploy atlas → Run workflow** to perform the first actual Europe PMC fetch and build. This also checks deployment permissions.
5. After deployment the default URL is generally `https://<github-user>.github.io/<repo>/` unless a custom domain is configured. The site is public, even where private-repository Pages is available.
6. The configured schedule searches every Monday at 08:23 America/New_York. GitHub scheduled workflows can be delayed or disabled by platform policies/inactivity; monitor Actions logs and the on-page last-sync date.

A GitHub account and repository are necessary before a public persistent URL can exist. The packaged workflow **does not run on its own** while stored as a ZIP or local HTML file.

## How new papers are handled

- `scripts/update_literature.py` queries the public Europe PMC REST API, using a gene-symbol search for each registry entry. It stores the most recent eight search hits and their identifiers, publication dates, journal, first-seen date, and search timestamp in `data/literature.json`.
- Articles are **unverified search matches**, not confirmed studies of direct transport. Ambiguous gene symbols and changes in aliases can lead to false positives or missed studies.
- The updater never changes a target's `status`, `priority`, or `review_status`. Only a researcher should update `data/targets.json` after reading primary literature.
- Browser-side article flags (`Relevant`, `Not about target`, `Review later`) and evidence assessments are private local notes. Use Export to retain them.

## Edit or expand the site

- `data/targets.json`: add, remove, or revise target hypotheses, compartments, priority and sources.
- `data/curated_references.json`: manually selected reading leads.
- `data/literature.json`: auto-generated publication metadata; do not hand-assign transport evidence from here.
- `site.template.html`: interface and experimental planner (pure HTML, CSS and JS; no build framework).
- Run `python scripts/build_site.py` to rebuild `docs/index.html`.
- Run `python scripts/update_literature.py` when online to refresh literature manually.
- Run `python -m unittest discover -s tests` to check data integrity and update logic.

## Research curation standard

Store experimental observations and computational predictions separately. A CRISPR hit, colocalization, interactor, docking score, or GWAS association is insufficient to demonstrate intrinsic flux. A claim of direct transport should point to its primary paper and include protein identity/isoform, membrane reconstitution or equivalent defined system, substrate, gradient, and relevant controls. A channel claim requires direct membrane conductance and selectivity evidence.

## Important privacy and data-integrity notes

- A public GitHub Pages website is **not** appropriate for private sequences, lab notes, embargoed manuscripts, or patient information.
- The app only saves notes on the local browser/device. It does not provide cloud synchronization or team permissions.
- The weekly updater can only work after deployment to a repository with GitHub Actions enabled and API network access.
- No continuous 24/7 monitoring or guarantee of exhaustive paper retrieval is implied; this is scheduled metadata surveillance with periodic manual evidence review.

## External APIs and documentation

- Europe PMC REST: https://dev.europepmc.org/RestfulWebService
- GitHub Actions schedules: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
