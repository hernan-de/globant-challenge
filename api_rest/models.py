from django.db import models


class Department (models.Model):
    id = models.IntegerField(primary_key=True)       # INTEGER Id of the department
    department = models.CharField(max_length=100, null=True, blank=True) # STRING Name of the department

    def __str__(self):
        return self.department


class Job (models.Model):
    id = models.IntegerField(primary_key=True)       # INTEGER Id of the job
    job = models.CharField(max_length=100, null=True, blank=True)        # STRING Name of the job

    def __str__(self):
        return self.job


class HiredEmployee (models.Model):
    id = models.IntegerField(primary_key=True)       # INTEGER Id of the hired employee
    name = models.CharField(max_length=100, null=True, blank=True)       # STRING Name of the hired employee
    date_time = models.DateTimeField(null=True, blank=True)            # DATETIME Date and time when was hired the employee
    department_id = models.IntegerField(null=True, blank=True) # INTEGER Id of department of the hired employee
    job_id = models.IntegerField(null=True, blank=True) # INTEGER Id of job of the hired employee

    def __str__(self):
        return f'{self.name}, {self.date_time}, {self.job_id}, {self.department_id}'


