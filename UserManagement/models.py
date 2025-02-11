from django.db import models

# Create your models here.
class Users(models.Model):

    # Note: These functions are purposely seperated. Using a single toggle function could result in future errors and vulnerabilities so it's not really worth it.
    def lock_user(self, target):
        if (self.role == 'basicuser'):
            return PermissionError('User ' + self.name + ' is not an administrator')
        target.status = False
        return {
            'Caller': self.name,
            'Target': target.name,
            'Result': 'Active' if target.status else 'Locked'
        }
    
    def unlock_user(self, target):
        if (self.role == 'basicuser'):
            return PermissionError('User', self.name, 'is not an administrator')
        target.status = True
        return {
            'Caller': self.user,
            'Target': target.user,
            'Result': 'Active' if target.status else 'Locked'
        }

    token = models.CharField(max_length=45, default='')
    name = models.CharField(max_length=45, blank=False, null=False)
    email = models.CharField(max_length=45, unique=True, primary_key=True, blank=False, null=False)
    role = models.CharField(max_length=45, default='basicuser', blank=False, null=False)
    status = models.BooleanField(default=True, blank=False, null=False) # False indicates user is locked