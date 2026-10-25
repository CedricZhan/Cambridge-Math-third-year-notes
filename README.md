# Cedric Zhan's Third-Year Mathematics Notes

This repository contains the LaTeX sources, compiled PDFs, and static website for Cedric Zhan's third-year mathematics lecture notes.

## Editing and compiling notes

Course sources live in `tex/`. Edit the matching `.tex` file, then compile every course from PowerShell:

```powershell
.\scripts\compile-notes.ps1
```

The generated PDFs are written to `dist/pdfs/`, where the website links to them.
After all courses compile successfully, the script updates the homepage's
"Last updated" time in London time (GMT or BST, adjusted automatically).
Publish `dist/index.html` together with the PDFs.
The script also exports each course's original TeX file to `dist/sources/` for the
homepage's source viewer. Publish the entire `dist/` directory together.
To refresh source downloads without compiling or changing the compilation time,
run `.\scripts\export-sources.ps1`.

## Manual announcements

Announcements are written only when Cedric explicitly requests one in chat.
They are independent of note compilation, source exports, and Git hooks.
Preparing a post does not authorize uploading it. Commit and push only when
Cedric explicitly requests an upload for that work.

Prepare an announcement locally (newest dates appear first):

```powershell
python .\scripts\post-update.py --title "A new proof" --message "The proof is ready to read." --important --link "./pdfs/principles-of-statistics.pdf#page=16" --link-label "Read the proof" --date "2026-10-26"
```

The script stores posts in `dist/posts.json` and updates only the marked
announcement region of `dist/index.html`. Text is escaped automatically.
The section uses static HTML and works without JavaScript. Use `--important`
for the Important badge; omit it for an ordinary Update. Earlier posts remain
saved in full. The noticeboard sits directly below Last updated and shows at
most five recent announcements. Click its heading to expand all history; click
again to return to the latest five. Announcement dates contain no time of day.

After reviewing the changes and receiving an explicit upload request, run:

```powershell
.\scripts\publish-posts.ps1
```

This commits the homepage and post data, then pushes the current branch to its
configured upstream. Review any other homepage edits first, since they are
included. If a push fails after committing, retry `git push` once the cause is
resolved. For the initial feature rollout, also commit the new scripts, styles,
and this README using the normal Git workflow.

## Previewing the website

Serve the `dist/` directory with any static web server. For example:

```powershell
python -m http.server 4173 --directory dist
```

Then open `http://localhost:4173`.
