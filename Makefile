.PHONY: pdf-en pdf-ru arxiv-source test-experiments test-calculator verify

pdf-en:
	cd article && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=output/pdf main_en.tex

pdf-ru:
	cd article && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=output/pdf main.tex

arxiv-source:
	./scripts/build_arxiv_bundle.sh

test-experiments:
	cd article/experiments && uv sync --python 3.13 && uv run pytest -q

test-calculator:
	cd article/calculator && npm ci && npm test && npm run lint && npm audit --omit=dev --registry=https://registry.npmjs.org

verify: pdf-en pdf-ru test-experiments test-calculator arxiv-source
