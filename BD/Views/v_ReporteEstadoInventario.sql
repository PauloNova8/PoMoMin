CREATE VIEW v_ReporteEstadoInventario AS
SELECT 1 AS Orden,'En uso' AS Estado, COUNT(*) AS Cantidad
FROM Inventario
WHERE AsignadoA IS NOT NULL AND EstadoID = 1
UNION
SELECT 2 AS Orden,'Disponible' AS Estado, COUNT(*) AS Cantidad
FROM Inventario
WHERE AsignadoA IS NULL AND EstadoID = 1
UNION
SELECT 3 AS Orden,'En espera de soporte' AS Estado, COUNT(*) AS Cantidad
FROM Inventario
WHERE EstadoID = 3
GROUP BY EstadoID

SELECT * FROM v_ReporteEstadoInventario