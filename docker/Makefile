# docker
start_docker:
	docker-compose up -d
	docker exec -it python_app /bin/zsh

stop_docker:
	docker-compose stop

app_restart:
	docker-compose stop python_app
	docker-compose up -d python_app
	docker exec -it python_app /bin/zsh

down_docker:
	docker-compose down

rebuild_docker:
	docker-compose up --force-recreate --build -d
	docker exec -it python_app /bin/zsh

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
