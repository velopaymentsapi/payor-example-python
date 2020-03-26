db:
	docker-compose up -d db

env:
ifdef clone
	# make clone=1 key=123 secret=shhh payor=testers env
	cp .env.example .env
	sed -i.bak 's/VELO_API_APIKEY=contact_velo_for_info/VELO_API_APIKEY=$(key)/' .env && rm .env.bak
	sed -i.bak 's/VELO_API_APISECRET=contact_velo_for_info/VELO_API_APISECRET=$(secret)/' .env && rm .env.bak
	sed -i.bak 's/VELO_API_PAYORID=contact_velo_for_info/VELO_API_PAYORID=$(payor)/' .env && rm .env.bak
endif
	- mv .env src/.env

network:
	- docker network create payorexample

build:
	docker-compose build --no-cache api

up: clean network
	docker-compose run -d --service-ports api

sh: clean network
	docker-compose run --service-ports api sh

down:
	docker-compose down

clean:
	- docker-compose rm -f

destroy:
	- docker rmi -f payor-example-python_api

setdep:
	# make version=2.16.18 setdep
	sed -i.bak 's/velo-python==.*/velo-python==${version}/g' src/requirements.txt && rm src/requirements.txt.bak

updatedeps:
	docker-compose run api sh -c 'pur -r requirements.txt'    

dev:
	- docker-compose build api
	docker-compose run --service-ports api

refresh: down clean build up