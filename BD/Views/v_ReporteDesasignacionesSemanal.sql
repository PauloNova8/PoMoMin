CREATE VIEW v_ReporteDesasignacionesSemanal AS
SELECT S.Dia, S.Fecha, SUM(S.Desasignaciones) AS Desasignaciones FROM(
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), -1)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), -1))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 0)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 0))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 1)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 1))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 2)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 2))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 3)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 3))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 4)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 4))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 5)) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 5))) AS Fecha, 0 AS Desasignaciones
	UNION
	SELECT DATENAME(WEEKDAY, FechaFin) AS Dia, DATEADD(dd, 0, DATEDIFF(dd, 0, FechaFin)) AS Fecha, COUNT(*) AS Desasignaciones
	FROM InventarioEmpleados
	WHERE DATEADD(dd, 0, DATEDIFF(dd, 0, FechaFin)) >= DATEADD(wk, DATEDIFF(wk,0,GETDATE()), -1) -- Sunday
	AND DATEADD(dd, 0, DATEDIFF(dd, 0, FechaFin)) <= DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 5) -- Saturday
	GROUP BY DATEADD(dd, 0, DATEDIFF(dd, 0, FechaFin)), DATENAME(WEEKDAY, FechaFin)
) AS S
GROUP BY S.Fecha, S.Dia
--ORDER BY S.Fecha

SELECT * FROM v_ReporteDesasignacionesSemanal ORDER BY Fecha
