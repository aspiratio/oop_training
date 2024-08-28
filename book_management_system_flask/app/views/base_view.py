from abc import ABC, abstractmethod
from flask import Blueprint, redirect, url_for

class BaseView(ABC):
    def __init__(self, blueprint_name, url_prefix = None):
        self.blueprint = Blueprint(blueprint_name, __name__, url_prefix = url_prefix)
        self.register_routes()
    
    def get_blueprint(self):
        return self.blueprint
        
    def redirect_to(self, endpoint):
        return redirect(url_for(endpoint))
    
    @abstractmethod
    def register_routes(self):
        pass
