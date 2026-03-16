import logging

from src.api import create_app

logging.basicConfig(level=logging.INFO)

app = create_app()
