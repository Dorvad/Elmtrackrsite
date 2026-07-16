# Elmtrackr marketing site — build & quality gate.
#
# One documented command runs the whole gate:
#
#     make ci
#
# which regenerates the content pages and sitemap, validates metadata,
# structured data, locale pairs and internal links, and assembles the final
# static site into _site/. It is deterministic and uses only Python's standard
# library plus the repo's own scripts (no network, no unpublished local files).
#
# Individual targets are available too (see below). Requires python3 and make.

PY      := python3
SCRIPTS := scripts
DIST    := _site
REPORTS := _reports

# Internal, non-site files that must never be published. This mirrors the
# strip step in .github/workflows/deploy-pages.yml so `make dist` produces
# exactly what GitHub Pages serves.
INTERNAL := docs AGENTS.md content templates scripts \
            Makefile README.md .github .git .gitignore \
            _ds dc-runtime node_modules $(DIST) $(REPORTS)

.DEFAULT_GOAL := ci
.PHONY: ci all build content sitemap validate audit dist clean serve check-clean help

## ci: full quality gate — build, validate, assemble final site (the one command)
ci: build validate audit dist
	@echo ""
	@echo "OK  build + validation + audit + dist all passed."

## all: alias for ci
all: ci

## content: (re)generate the locale-aware content pages from content/ + templates/
content:
	$(PY) $(SCRIPTS)/build_content_pages.py

## sitemap: (re)generate sitemap.xml from the route manifest
sitemap:
	$(PY) $(SCRIPTS)/build_sitemap.py

## build: regenerate all generated artifacts (content pages + sitemap)
build: content sitemap

## validate: run every validator (fails on any error)
validate:
	@echo "== content pages up to date =="
	$(PY) $(SCRIPTS)/build_content_pages.py --check
	@echo "== sitemap up to date =="
	$(PY) $(SCRIPTS)/build_sitemap.py --check
	@echo "== metadata + structured data + Play links (validate_seo) =="
	$(PY) $(SCRIPTS)/validate_seo.py
	@echo "== locale pairs (hreflang / language-switch reciprocity) =="
	$(PY) $(SCRIPTS)/check_locales.py
	@echo "== media (images, dimensions, uploads not linked) =="
	$(PY) $(SCRIPTS)/check_media.py
	@echo "== static source (no unresolved templates, anchors, alt) =="
	$(PY) $(SCRIPTS)/check_static_html.py

## audit: run the comprehensive site audit and write a readable report artifact
audit:
	@mkdir -p $(REPORTS)
	$(PY) $(SCRIPTS)/audit_site.py \
		--report $(REPORTS)/audit-report.md \
		--json $(REPORTS)/audit-report.json

## dist: assemble the final publishable static site into _site/
dist:
	@rm -rf $(DIST)
	@mkdir -p $(DIST)
	@# Copy everything except internal/build files, then verify no leakage.
	@tar --exclude-vcs \
		$(foreach d,$(INTERNAL),--exclude=./$(d)) \
		-cf - . | tar -xf - -C $(DIST)
	@touch $(DIST)/.nojekyll
	@echo "Assembled final static site in $(DIST)/ ($$(find $(DIST) -name '*.html' | wc -l | tr -d ' ') HTML pages)."

## check-clean: fail if regenerating would change tracked files (CI determinism)
check-clean: build
	@if ! git diff --quiet -- sitemap.xml '*.html'; then \
		echo "ERROR: generated output differs from committed files. Run 'make build' and commit."; \
		git --no-pager diff --stat -- sitemap.xml '*.html'; \
		exit 1; \
	fi
	@echo "OK  generated output matches committed files."

## serve: preview the assembled site locally on :8000
serve: dist
	cd $(DIST) && $(PY) -m http.server 8000

## clean: remove build outputs
clean:
	rm -rf $(DIST) $(REPORTS)

## help: list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'
