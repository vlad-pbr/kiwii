.PHONY: docker-build-and-run
docker-build-and-run:
	@docker run --rm $(shell docker build -q .) ${CMD}