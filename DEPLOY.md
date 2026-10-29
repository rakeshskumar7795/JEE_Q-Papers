# Publishing the dashboard so anyone can use it

## Option A: Streamlit Community Cloud (free, easiest)

1. Create a free GitHub account and a new **public** repository (e.g. `jee-papers`).
2. Upload this whole project to it, including your PDFs in `papers/`.
   - Easiest: GitHub Desktop (drag the folder in, Commit, Publish).
   - Each file must be under 100 MB; the whole repo should stay under ~1 GB.
3. Go to https://share.streamlit.io, sign in with GitHub, click **Create app**.
4. Pick the repo, branch `main`, main file `app.py`, then **Deploy**.
5. In a minute or two you get a public link like `https://your-name-jee-papers.streamlit.app` to share.

To add or change papers later, upload them to the repo's `papers/` folder; the app redeploys itself.

## Option B: Hugging Face Spaces (free, supports Docker)

Create a Space with the "Docker" SDK, upload this project (the included `Dockerfile` is used),
and set `app_port: 8501` in the Space's README header.

## Option C: Your own server / Render / Railway / Fly.io

Use the `Dockerfile`:

    docker build -t jee-papers .
    docker run -p 8501:8501 jee-papers

Then point your host at port 8501.

## Before you make it public

- **Copyright:** JEE Main papers come from NTA and JEE Advanced papers from the IITs.
  Both are published on the official sites, but check their terms before hosting copies
  publicly, and consider linking the source on the page. Do not include any coaching-institute
  material (solutions, notes) unless you have permission.
- **Free-tier limits:** free hosts sleep when idle (first load takes ~30 s) and have limited memory.
  Large PDFs are loaded only when someone clicks View or Download.
