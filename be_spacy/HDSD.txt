.\docuscan\Scripts\activate

jupyter notebook

python -m spacy train .\config.cfg --output .\output\ --paths.train .\data\train.spacy --paths.dev .\data\test.spacy

pip freeze > requirements_app.txt

python -m venv docapp 
.\docapp\Scripts\activate