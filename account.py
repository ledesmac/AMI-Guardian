class Account():
    def __init__(self, profile, regions=[]):
        """
        Constructor for initializing a new instance object with specific details about the instance it is reporting on
        Parameters:
        - instance_name: name of the instance being reported
        - instance_id: unique identifier of the isntance created by AWS
        - ami_id: id of the ami that the instance is based on
        - ami_name: name of the ami that the instance is based on, last 6 characters should be the date of the ami creation (yymmdd)
        """
        self.profile = profile
        self.regions = regions
    
    def get_profile(self):
        return self.profile
    
    def get_regions(self):
        return self.regions

    def set_profile(self, profile):
        self.profile = profile

    def set_regions(self, regions):
        self.regions = regions

    def add_region(self, region):
        self.regions.append(region)