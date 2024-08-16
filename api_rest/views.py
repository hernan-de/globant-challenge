from django.shortcuts import render
from django.db import transaction, connection
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Department, HiredEmployee
from datetime import datetime
import csv
from django.http import HttpResponse


class DepartmentBulkUpload(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        data = pd.read_csv(file, header=None)
        departments = []
        
        data.fillna(0, inplace=True)

        for index, row in data.iterrows():
            departments.append(Department(id = row[0] if row[0] != 0 else None,
                                          department = row[1] if row[1] != 0 else None))
        
        try:
            Department.objects.bulk_create(departments)
            return Response({"status": "success"}, status = status.HTTP_201_CREATED)
        except:
            return Response({"status": "error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class JobBulkUpload(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        data = pd.read_csv(file, header=None)
        jobs = []
        
        data.fillna(0, inplace=True)

        for index, row in data.iterrows():
            jobs.append(Job(id = row[0] if row[0] != 0 else None,
                            job = row[1] if row[1] != 0 else None))
        
        try:
            Job.objects.bulk_create(jobs)
            return Response({"status": "success"}, status = status.HTTP_201_CREATED)
        except:
            return Response({"status": "error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class HiredEmployeeBulkUpload(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        data = pd.read_csv(file, header=None)
        hired_employees = []
        
        data.fillna(0, inplace=True)

        for index, row in data.iterrows():
            hired_employees.append(HiredEmployee(id = row[0] if row[0] != 0 else None,
                                                 name = row[1] if row[1] != 0 else None,
                                                 date_time = row[2] if row[2] != 0 else None,
                                                 department_id = row[3] if row[3] != 0 else None,
                                                 job_id = row[4] if row[4] != 0 else None)
                                  )

        try:
            HiredEmployee.objects.bulk_create(hired_employees)
            return Response({"status": "success"}, status = status.HTTP_201_CREATED)
        except Exception as e:
            
            return Response({"status": "error", "msg" : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


# Requirement 1
# Number of employees hired for each job and department in 2021 divided by quarter. The
# table must be ordered alphabetically by department and job.
class Requirement1(APIView):
    def get(self, request, *args, **kwargs):
        query = '''
                    SELECT dept.department, jb.job,
	                       COALESCE(SUM(CASE WHEN DATE_PART('quarter', hemp.date_time) = 1 THEN 1 ELSE 0 END), 0) AS Q1,
                           COALESCE(SUM(CASE WHEN DATE_PART('quarter', hemp.date_time) = 2 THEN 1 ELSE 0 END), 0) AS Q2,
                           COALESCE(SUM(CASE WHEN DATE_PART('quarter', hemp.date_time) = 3 THEN 1 ELSE 0 END), 0) AS Q3,
                           COALESCE(SUM(CASE WHEN DATE_PART('quarter', hemp.date_time) = 4 THEN 1 ELSE 0 END), 0) AS Q4
                    FROM public.api_rest_hiredemployee AS hemp
                    JOIN public.api_rest_department    AS dept ON hemp.department_id = dept.id
                    JOIN public.api_rest_job           AS jb   ON hemp.job_id = jb.id
                    WHERE DATE_PART('year', hemp.date_time) = 2021
                    GROUP BY dept.department, jb.job
                    ORDER BY dept.department, jb.job;
                '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()

        result = []

        for row in query_result:
            result.append({
                "department": row[0],
                "job": row[1],
                "Q1": row[2],
                "Q2": row[3],
                "Q3": row[4],
                "Q4": row[5]
            })

        return Response(result, status = status.HTTP_200_OK)
    

# Requirement 2    
# List of ids, name and number of employees hired of each department that hired more
# employees than the mean of employees hired in 2021 for all the departments, ordered
# by the number of employees hired (descending).
class Requirement2(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "requirement2.csv"'

        writer = csv.writer(response)

        query = '''
                    WITH department_hired AS (
                        SELECT dept.id, dept.department, COUNT(*) AS hired
                        FROM public.api_rest_hiredemployee AS hemp
                        JOIN public.api_rest_department    AS dept
                        ON hemp.department_id = dept.id
                        WHERE DATE_PART('year', hemp.date_time) = 2021
                        GROUP BY dept.id, dept.department
                    ),
                    average_hired AS (
                        SELECT AVG(hired) AS avg_hired FROM department_hired
                    )
                    SELECT dh.id, dh.department, dh.hired
                    FROM department_hired dh, average_hired ah
                    WHERE dh.hired > ah.avg_hired
                    ORDER BY dh.hired DESC;
                '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()

        result = []

        writer.writerow(['id','department','hired'])

        for row in query_result:
            writer.writerow([row[0], row[1], row[2]])

            result.append({
                "id": row[0],
                "department": row[1],
                "hired": row[2]
            })

        return response #Response(result, status = status.HTTP_200_OK)
    

class QueryDummy(APIView):
    def get(self, request, *args, **kwargs):
        #departments = Department.objects.all()

        query = "select * from public.api_rest_department"

        with connection.cursor() as cursor:
            cursor.execute(query)
            departments = cursor.fetchall()

        result = []

        for department in departments:
            result.append({
                "id": department[0],
                "department": department[1]
            })

        '''for department in departments:
            result.append({
                "id": department.id,
                "department": department.department
            })'''

        return Response(result, status = status.HTTP_200_OK)

        
