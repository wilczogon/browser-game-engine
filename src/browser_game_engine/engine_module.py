class EngineModule:
    def add_endpoints(self):
        pass

    def set_engine(self, engine):
        self.engine = engine
        self.add_endpoints()