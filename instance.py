class Instance(self, instance_name, instance_id, ami_id, ami_name='', age=0):
    """
    Constructor for initializing a new instance object with specific details about the instance it is reporting on
    Parameters:
    - instance_name: name of the instance being reported
    - instance_id: unique identifier of the isntance created by AWS
    - ami_id: id of the ami that the instance is based on
    - ami_name: name of the ami that the instance is based on, last 6 characters should be the date of the ami creation (yymmdd)
    """