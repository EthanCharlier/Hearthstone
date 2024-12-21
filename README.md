`python -m unittest discover -s tests -p "test_*.py"`

`for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"`
