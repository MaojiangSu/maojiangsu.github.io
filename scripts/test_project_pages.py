"""Regression checks for curated project pages and Scholar compatibility."""
import tempfile
import re
import unittest
from pathlib import Path

from render_papers import (
    build_front_matter, load_project_pages, load_publications,
    render_publication, validate_local_assets, validate_official_citation,
)


class ProjectPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projects = load_project_pages()
        cls.publications = {p["slug"]: p for p in load_publications()}

    def test_eight_curated_projects_have_complete_content_and_assets(self):
        self.assertEqual(len(self.projects), 8)
        root = Path(__file__).resolve().parents[1]
        for slug, project in self.projects.items():
            publication = self.publications[slug]
            fm = build_front_matter(publication, project)
            self.assertEqual(fm["layout"], "project")
            self.assertEqual(fm["project"], slug)
            self.assertGreater(len(fm["abstract"]), 100)
            validate_local_assets(publication, root / "content" / "papers" / slug, slug, project)

    def test_unpublished_resources_remain_hidden(self):
        for slug in ("flow-matching-rl-sde", "likelihood-free-generative-policy-optimization"):
            fm = build_front_matter(self.publications[slug], self.projects[slug])
            self.assertTrue(fm["hidePublicationLinks"])
            self.assertNotIn("pdf", fm)
            self.assertFalse(self.projects[slug].get("links"))
        self.assertEqual(build_front_matter(self.publications["flow-matching-rl-sde"], self.projects["flow-matching-rl-sde"])["presentation"], "Spotlight")

    def test_scholar_only_entries_keep_their_existing_layout(self):
        for slug, publication in self.publications.items():
            if slug not in self.projects:
                self.assertNotIn("project", build_front_matter(publication))
                self.assertNotIn("layout: project", render_publication(publication))

    def test_published_title_does_not_mutate_source_aliases(self):
        publication = self.publications["paper2"]
        old_title = publication["title"]
        fm = build_front_matter(publication, self.projects["paper2"])
        self.assertEqual(fm["title"], "In-Context Deep Learning via Transformer Models")
        self.assertEqual(publication["title"], old_title)

    def test_paper_metadata_never_uses_poster_pdf(self):
        for slug in ("paper2", "paper3"):
            fm = build_front_matter(self.publications[slug], self.projects[slug])
            self.assertTrue(fm["pdf"].endswith(".pdf"))
            self.assertNotIn("poster", fm["pdf"].lower())

    def test_missing_abstract_fails(self):
        with self.assertRaisesRegex(ValueError, "needs an abstract"):
            build_front_matter(self.publications["flow-matching-rl-sde"], {"summary": "Test"})

    def test_assets_cannot_escape_paper_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "leaves the paper directory"):
                validate_local_assets({}, Path(directory), "test", {"links": [{"file": "../private.pdf"}]})

    def test_six_official_citations_preserve_publication_fields(self):
        expected_pages = {
            "paper1": "6167--6206", "paper2": "67670--67718",
            "paper3": "41254--41289", "paper4": "45820--45932",
            "scholar-kc-bzdyksqc": "98666--98695",
            "scholar-yowf2qjgphmc": "44705--44798",
        }
        self.assertEqual({s for s, p in self.projects.items() if p.get("citation")}, set(expected_pages))
        for slug, pages in expected_pages.items():
            with self.subTest(slug=slug):
                citation = self.projects[slug]["citation"]
                bibtex = citation["bibtex"]
                self.assertIn(pages, bibtex)
                self.assertRegex(bibtex, r"(?m)^\s*volume\s*=")
                self.assertRegex(bibtex, r"(?m)^\s*url\s*=")
                authors = re.search(r"(?m)^\s*author\s*=\s*\{([^}]+)\}", bibtex).group(1)
                names = [" ".join(reversed(a.split(", ", 1))) for a in authors.split(" and ")]
                self.assertEqual(names, self.publications[slug]["authors"])
        self.assertIn("10.52202/085713-1528", self.projects["paper4"]["citation"]["bibtex"])

    def test_official_citations_require_provenance_and_matching_key(self):
        original = self.projects["paper2"]["citation"]
        for missing in ("bibtex", "source_url", "source_name"):
            citation = dict(original)
            del citation[missing]
            with self.assertRaisesRegex(ValueError, "missing required fields"):
                validate_official_citation(citation, "pmlr-v267-wu25aa", "test")
        with self.assertRaisesRegex(ValueError, "official key"):
            validate_official_citation(original, "made-up-key", "test")
        with self.assertRaisesRegex(ValueError, "HTTP or HTTPS"):
            validate_official_citation(dict(original, source_url="javascript:alert(1)"), "pmlr-v267-wu25aa", "test")

    def test_new_neurips_papers_do_not_claim_official_citations(self):
        for slug in ("flow-matching-rl-sde", "likelihood-free-generative-policy-optimization"):
            self.assertNotIn("citation", self.projects[slug])


if __name__ == "__main__":
    unittest.main()
