# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Run tests
.PHONY: test
test:
	pytest -v

# Lint the code
.PHONY: lint
lint: 
	python3 -m black app
	pylint app --source-roots=app --disable=C,R

# Run the app locally
.PHONY: run
run:
	streamlit run app/app.py

# Clean the app tmp folder
.PHONY: clean
clean:
	@rm -rf tmp/*
