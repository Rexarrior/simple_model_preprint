#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
repo_root="$(dirname -- "$script_dir")"
article_dir="$repo_root/article"
build_dir="$article_dir/output/arxiv"
dist_dir="$repo_root/dist/arxiv"
tmp_parent="$repo_root/tmp"
archive_name="phase_based_human_agent_planning-v0.1.0.tar.gz"

mkdir -p "$build_dir" "$dist_dir" "$tmp_parent"
stage_root="$(mktemp -d "$tmp_parent/arxiv-source.XXXXXX")"
trap 'rm -rf "$stage_root"' EXIT
stage_dir="$stage_root/source"
verify_dir="$stage_root/verify"
mkdir -p "$stage_dir" "$verify_dir"

(
  cd "$article_dir"
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -outdir="$build_dir" main_en.tex
)

fls_file="$build_dir/main_en.fls"
if [[ ! -f "$fls_file" ]]; then
  echo "Missing LaTeX recorder file: $fls_file" >&2
  exit 1
fi

while IFS= read -r recorded; do
  case "$recorded" in
    "$article_dir"/*) source_path="$recorded" ;;
    ./*) source_path="$article_dir/${recorded#./}" ;;
    *)
      if [[ -f "$article_dir/$recorded" ]]; then
        source_path="$article_dir/$recorded"
      else
        continue
      fi
      ;;
  esac

  [[ -f "$source_path" ]] || continue
  relative_path="${source_path#"$article_dir"/}"

  case "$relative_path" in
    main_en.tex)
      cp "$source_path" "$stage_dir/main.tex"
      ;;
    *.tex|*.png|*.jpg|*.jpeg|*.pdf)
      mkdir -p "$stage_dir/$(dirname -- "$relative_path")"
      cp "$source_path" "$stage_dir/$relative_path"
      ;;
  esac
done < <(awk '/^INPUT / {sub(/^INPUT /, ""); print}' "$fls_file" | sort -u)

cp "$article_dir/references.bib" "$stage_dir/references.bib"
cp "$build_dir/main_en.bbl" "$stage_dir/main.bbl"

if find "$stage_dir" -mindepth 1 -name '.*' -print -quit | grep -q .; then
  echo "Hidden files are not permitted in the arXiv source package" >&2
  exit 1
fi

(
  cd "$stage_dir"
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -outdir="$verify_dir" main.tex
)

archive_path="$dist_dir/$archive_name"
COPYFILE_DISABLE=1 tar -czf "$archive_path" -C "$stage_dir" .
shasum -a 256 "$archive_path" > "$archive_path.sha256"

echo "Created $archive_path"
echo "Verified PDF: $verify_dir/main.pdf"
echo "Files: $(find "$stage_dir" -type f | wc -l | tr -d ' ')"
echo "Archive size: $(du -h "$archive_path" | cut -f1)"
