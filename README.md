# com-ceeg — Club Entrepreneur Étudiant Gaspé

Static, dependency-free version of the CEEG website, migrated from the WordPress multisite (main site `ceegim.com`) on 2026-11-20. Same conventions as `com-rclg`.

## Files

| Path | Purpose |
|---|---|
| `index.html` | Accueil (hero, prochain événement, qui sommes-nous, programmes, dernières nouvelles) |
| `a-propos/` | Mission, vision, membres actuels et anciens |
| `programmes/` + 8 sub-pages | Entreprendre X, Festif, Cantine, Boutique, Éducation financière, Développement professionnel, Simulations, Colloque ACEE |
| `nouvelles/` | Archive of the 22 WordPress posts, one anchor per post |
| `evenements/` | Upcoming events plus archive by year (The Events Calendar data) |
| `partenaires/`, `nous-joindre/`, `gala/`, `beach-party-2023-fin-de-session/`, `privacy-policy/` | Other pages |
| `<old-post-slug>/`, `event/<slug>/`, `events/`, `boutique/` | Redirect stubs so old WordPress links land on the right archive entry |
| `404.html` | Not-found page |
| `assets/site.css`, `assets/site.js` | Shared styles (navy `#003087`, aqua `#2fe0cc`, Poppins) and mobile menu |
| `assets/img/` | Images; `manifest.tsv` maps each one to its original WordPress URL |
| `tools/content.py`, `tools/build.py` | Source content and generator: edit `content.py`, run `python3 tools/build.py`, commit |
| `.github/workflows/fetch-images.yml` | One-time import of the images from ceegim.com (see below) |
| `favicon.svg`, `.nojekyll` | Site icon; serve files as-is |

Removed by decision: the WooCommerce shop (Boutique), the Jetpack contact form (replaced by mailto/phone links), the placeholder post "À déterminer".

## First publish

1. Push this repo to `main`. The workflow **Fetch images from WordPress** runs on its own, downloads the 177 images listed in `assets/img/manifest.tsv` from ceegim.com and commits them. If any fail (warnings in the Actions log), re-run it from the Actions tab. It must run while ceegim.com is still online.
2. Settings → Pages → Deploy from a branch → `main` / root.
3. Once the images are in, the workflow can be deleted.

## Editing

**Home banner photo.** The student photo in the home banner is its own file: `assets/img/hero-etudiants.jpg`. To change it, upload a new photo with that exact name (GitHub → `assets/img` → Add file → Upload files). Any landscape or square photo works; it is cropped to a circle automatically. If the faces sit off-centre, adjust `object-position` on `.hero-photo` in `assets/site.css` (first number = left/right, in %).

Either edit the HTML directly, or (recommended, keeps header/footer in sync) edit `tools/content.py` and run `python3 tools/build.py`. New events go in `EVENTS`; the home page shows the next upcoming one, computed at build time (`TODAY` in `build.py`).

## Moving to the ceegim.com domain later

1. Add a `CNAME` file containing `ceegim.com` and set the same domain in Settings → Pages.
2. At the DNS host:
   ```
   @    A     185.199.108.153
   @    A     185.199.109.153
   @    A     185.199.110.153
   @    A     185.199.111.153
   @    AAAA  2606:50c0:8000::153 / 2606:50c0:8001::153 / 2606:50c0:8002::153 / 2606:50c0:8003::153
   www  CNAME adamnormand.github.io
   ```
   Remove old A/AAAA/CNAME on `@` and `www` (Kinsta). Do not touch MX, SPF/TXT or DKIM. Note that the subdomains `friprix`, `legiongaspe` (and any other multisite subsite) also live on Kinsta: give each a destination before retiring WordPress.
3. Tick "Enforce HTTPS" once the certificate is issued.
