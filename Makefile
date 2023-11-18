PYTHON = python3
APP_FILE = main.py
RUN_TARGET = run
# Define the targets and their dependencies
$(RUN_TARGET): $(APP_FILE)
	$(PYTHON) $(PYTHON_FLAGS) $(APP_FILE)