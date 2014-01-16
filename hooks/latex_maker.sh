#!/bin/bash

pdflatex_cmd="pdflatex -halt-on-error -interaction nonstopmode"
bibtex_cmd="bibtex"

file=$(basename "$1")
dir=$(dirname "$1")
pdf="${file%.tex}.pdf";

if [ ! ${file: -4} == ".tex" ] ; then
	echo "Invalid file format"
	exit
fi

echo "Compiling \"$file\" in \"$dir\""

cd /tmp
rm -fr PdfBuilder
git clone git@github.com:kpj/PdfBuilder.git
cd PdfBuilder

cd "$dir"
$pdflatex_cmd "$file"
$bibtex_cmd "$file"
$pdflatex_cmd "$file"
$pdflatex_cmd "$file"
cd -

git add "$dir/$pdf"
git commit -m "pdfupdate - Compiled $file to $pdf" "$dir/$pdf"
git push

cd ..
rm -fr PdfBuilder
