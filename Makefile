init:
	docker-compose up -d

test:
	docker-compose run --rm web sh -c "pytest ${ARGS}"
