.PHONY: clean build publish bump-version tag release

clean:
	rm -rf dist/ build/ *.egg-info/

bump-version:
ifndef VERSION
	$(error VERSION is not set. Use 'make bump-version VERSION=X.Y.Z')
endif
	sed -i '' 's/version = "[^"]*"/version = "$(VERSION)"/' pyproject.toml

tag:
ifndef VERSION
	$(error VERSION is not set. Use 'make tag VERSION=X.Y.Z')
endif
	git add pyproject.toml
	git commit -m "chore: bump version to $(VERSION)"
	git push origin main
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin v$(VERSION)

build: clean
	pip install --upgrade build twine
	python -m build

publish:
	twine check dist/*
	twine upload dist/*

release: bump-version tag build publish 