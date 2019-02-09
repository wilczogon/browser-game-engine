class SystemModule:
    def add_endpoints(self):
        pass

    def set_system(self, system):
        self.system = system
        self.add_endpoints()