.PHONY: clean

clean:
	find . -type d -name '__pycache__' -print0 | xargs -0 rm -rf
	find . -type d -name '*.egg-info' -print0 | xargs -0 rm -rf
	rm -rf .pytest_cache

test-install:
	pip install -e .

ut: test-install
	pytest -xvv tests/unit_tests/

test: test-install ut

todo:
	@git grep -qnP 'TODO|FIXME' | grep -qv 'THIS_EXACT_LINE_RIGHT_HERE' || true

