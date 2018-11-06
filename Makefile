PROJECT := vue-lb
NAME := web
VERSION := 0.0.1
TAG := $(PROJECT)/$(NAME):$(VERSION)
DOCKER_BUILD_OPTS += -t $(TAG)

.PHONY: install 
install:
	yarn install

.PHONY: dev
dev:
	npm run fix && npm run dev

.PHONY: docker-build
build:
	export DOCKER_BUILDKIT=1
	docker build $(DOCKER_BUILD_OPTS) . --target prod

.PHONY: docker-run
docker-run:
	docker run -it -p 8080:80  --rm $(DOCKER_BUILD_OPTS)
