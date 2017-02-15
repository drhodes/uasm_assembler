help:

build: ## unused rule

test: FORCE ## test
	py.test test_discover.py

diff: ## view the diff with current git HEAD
	git diff HEAD

clean: FORCE ## clean all the things
	$(shell bash clean.sh)

work: ## open all files in emacs
	emacs -nw *.py Makefile uasm_assembler.py

setup:
	touch battle-plan.org
	mkdir -p design

add: clean ## add files to the git repo
	git add -A :/

commit: ## git commit -a
	git commit -a

# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
	'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

FORCE:

