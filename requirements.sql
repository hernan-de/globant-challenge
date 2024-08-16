select * from public.api_rest_department

truncate public.api_rest_job cascade

select * from public.api_rest_job

-- Requirement 1
-- Number of employees hired for each job and department in 2021 divided by quarter.
-- The table must be ordered alphabetically by department and job.

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


-- Requirement 2
-- List of ids, name and number of employees hired of each department that hired more
-- employees than the mean of employees hired in 2021 for all the departments, ordered
-- by the number of employees hired (descending).

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