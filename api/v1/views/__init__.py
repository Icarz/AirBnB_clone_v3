#!/usr/bin/python3
"""
Initialize Blueprint for API views
"""

from flask import Blueprint

# Create a Blueprint instance with the prefix /api/v1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views (PEP8 might complain, but it's necessary)
from api.v1.views.index import *

