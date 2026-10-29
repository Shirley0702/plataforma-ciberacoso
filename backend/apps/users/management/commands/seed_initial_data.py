"""Adaptador de Django para cargar el catálogo inicial de la plataforma."""

from initial_data.seed_catalog import SeedInitialDataCommand


class Command(SeedInitialDataCommand):
    """Expone ``python manage.py seed_initial_data`` a Django."""

