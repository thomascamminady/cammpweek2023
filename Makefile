init:
	# code .
	poetry config --local virtualenvs.create true
	poetry config --local virtualenvs.in-project true
	# poetry env use 3.10
	poetry install
	poetry update
	git init
	echo ".venv/" >> .gitignore
	echo "logs/" >> .gitignore
	git lfs install
	git lfs track "*.fit"
	git lfs track "*.hdf5"
	git lfs track "*.html"
	git lfs track "*.parquet"
	git lfs track "*.csv"
	git lfs track "*.gpx"
	git add .
	poetry run pre-commit run --all-files
	poetry run pre-commit install
	git commit -am "Initial commit after initializing the project."
	poetry shell

test:
	pytest .

coverage:
	pytest --cov=automatic_climb_detection tests/
