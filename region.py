class Region():
    def __init__(self, name, instances=[]):
        """
        Constructor for initializing a new instance object with specific details about the instance it is reporting on
        Parameters:
        - instance_name: name of the instance being reported
        - instance_id: unique identifier of the isntance created by AWS
        - ami_id: id of the ami that the instance is based on
        - ami_name: name of the ami that the instance is based on, last 6 characters should be the date of the ami creation (yymmdd)
        """
        self.name = name
        self.instances = instances
    
    def get_name(self):
        return self.name

    def get_instances(self):
        return self.instances
    
    def set_name(self, name):
        self.name = name

    def set_instances(self, instances):
        self.instances = instances

    def add_instance(self, instance):
        self.instances.append(instance)