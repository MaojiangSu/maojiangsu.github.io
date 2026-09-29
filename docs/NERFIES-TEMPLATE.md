# Paper project pages

The project-page layout and visual hierarchy are adapted from [Nerfies](https://nerfies.github.io/) by Keunhong Park and collaborators: [source repository](https://github.com/nerfies/nerfies.github.io).

The upstream website template is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). This adaptation retains that license for the adapted project-page template and styles. The license does not relicense research papers, posters, figures, or unrelated website code. Each project page includes visible attribution and a license link.

Changes: integrated the centered paper header, author row, resource buttons, abstract, and citation structure with Hugo; matched the personal site's slate-blue palette; added responsive key-result sections, optional figures/posters, and accessible citation copying. Upstream analytics, sample research content, video assets, jQuery, and carousel scripts are not included.

## Edit a page

- Bibliographic records remain in `data/publications.yml`.
- Hand-maintained project content lives in `data/paper_projects.yml`, keyed by the existing publication slug.
- `python scripts/render_papers.py` connects those records to `layouts/papers/project.html`. Do not edit generated `content/papers/*/index.md` files directly.
- `python scripts/render_papers.py --check` verifies that generated pages are current.
- `python -m unittest discover -s scripts -p 'test_*.py'` runs the generator checks.
- Run `hugo` to build. Existing paper URLs are unchanged.

A project entry needs `venue`, `summary`, `citation_key`, and an abstract either in its project entry or its publication record. `title` can specify the published title while preserving older title aliases in publication matching. `highlights` contains `title` / `text` pairs.

`links` contains a label and exactly one `url` or bundle-relative `file`. Resource links remain hidden when `hidePublicationLinks: true`; this does not hide the local project-page link. Do not add private PDFs to a bundle merely to fill a resource button.

Optional `teaser` and `poster` mappings accept `image`, `alt`, and `caption`. Optional `sections` accept a `title`, Markdown `text`, and an optional `figure` with the same fields. Images are resolved within each paper bundle, and large display images are resized by Hugo without changing originals. Omitted sections do not render placeholders. Only add figures, results, links, and affiliations verified from the paper or provided by its authors.

Scholar sync writes `data/publications.scholar.yml`, not the hand-maintained project data. The 8 explicitly configured accepted papers get project pages; other Scholar entries retain their existing layout and publication-list visibility.
