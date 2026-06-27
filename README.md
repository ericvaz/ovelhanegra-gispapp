# GISP Prep — support & privacy site

Static pages for the **GISP Prep** iOS app, served under **`ovelhanegra.io/GISPApp/`**.

These two URLs are what you enter in App Store Connect:

- **Support URL** → `https://ovelhanegra.io/GISPApp/`  (or `/GISPApp/index.html`)
- **Privacy Policy URL** → `https://ovelhanegra.io/GISPApp/privacy.html`

## Files
```
GISPApp/
  index.html     # Support center: contact + FAQ
  privacy.html   # Privacy policy (app collects no data)
  styles.css     # Shared styling (matches the app's indigo theme)
```

## Deploying to ovelhanegra.io/GISPApp

The folder is named `GISPApp` so it maps directly to the `/GISPApp/` path. Pick whatever matches
how `ovelhanegra.io` is hosted:

- **Static host (Netlify / Vercel / Cloudflare Pages / GitHub Pages):** publish this repo; the
  `GISPApp/` directory becomes `/GISPApp/`. (If a host serves the repo root as the site root,
  this already gives you the right path.)
- **Existing web server (Nginx/Apache/S3):** copy the `GISPApp/` folder into the site's web root.

Then verify both links load before submitting the app.

## Contact email
- Support/contact email is **hello.ovelhanegra@gmail.com** (in `index.html` and `privacy.html`).
  To change it later, search-replace that address across both files.
