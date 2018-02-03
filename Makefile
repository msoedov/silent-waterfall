GIT_SUMMARY := $(shell git describe --tags --dirty --always)
REPO=app:$(GIT_SUMMARY)

default: repo

repo:
	@echo $(REPO)

build:
	@docker build -t $(REPO) .

run:
	docker run -p 8000:8000 $(REPO)

push:
	@docker push $(REPO)
