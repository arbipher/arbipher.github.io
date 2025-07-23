all: local

local:
	bundle exec jekyll serve --port 8090

update:
	dune runtest --auto-promote