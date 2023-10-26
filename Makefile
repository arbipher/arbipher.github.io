all: local

local:
	bundle exec jekyll serve

update:
	dune runtest --auto-promote