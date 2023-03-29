DOCKER ?= docker

install-deps-no-leak:
	pip install --upgrade -r requirements-1.15.0-no-leak.txt

install-deps-leak:
	pip install --upgrade -r requirements-1.16.0-leak.txt


compose-up:
	docker-compose up

redis-run:
	$(DOCKER) run --rm -it \
		--network="host" \
		--name redis-instance \
		-p 6379:6379 \
		redis:6.2.7

rabbit-run:
	$(DOCKER) run --rm --network="host" \
		--name rabbit \
		-p 15672:15672 \
		-p 5672:5672 \
		rabbitmq:3-management

worker-run:
	celery -q \
		-A sentry_leak.worker \
		worker \
		-n test@%h \
		-l info \
		-c 1 \
		-Q person

send-messages:
	python3 -m sentry_leak.run
