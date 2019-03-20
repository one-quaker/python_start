APP_NAME=python_app

start_docker:
	docker-compose up -d

stop_docker:
	docker-compose stop

app_restart:
	docker-compose stop $(APP_NAME)
	docker-compose up -d $(APP_NAME)

app_logs:
	docker-compose logs -f web_app

app_attach:
	docker-compose exec $(APP_NAME) /bin/zsh

all_logs:
	docker-compose logs -f

down_docker:
	docker-compose down

rebuild_docker:
	docker-compose up --force-recreate --build -d

force_rebuild_docker: down_docker rebuild_docker


# django
RUN=python manage.py
run:
	$(RUN) runserver 0.0.0.0:8000

clean:
	rm -rfv *~*
	find . -name '*.pyc' -exec rm -fv {} \;

shell:
	$(RUN) shell_plus

makemigrations:
	$(RUN) makemigrations

migrate:
	$(RUN) migrate

collectstatic:
	$(RUN) collectstatic --noinput

create_admin:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | $(RUN) shell
