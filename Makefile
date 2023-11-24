prod:
	docker compose -f docker-compose.yml up --build app

test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml up --build app --exit-code-from app

test-watch:
	docker compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.test.watch.yml up --build app --exit-code-from app