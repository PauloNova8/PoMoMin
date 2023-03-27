ALTER VIEW v_HistoricoAsignaciones AS
SELECT  ROW_NUMBER() OVER(ORDER BY IE.InventarioID ASC) AS id, IE.InventarioID, IE.EmpleadoID, IE.MotivoAsignacionID, IE.MotivoDesasignacionID, IE.FechaVigente, IE.FechaFin, IE.Notas,
	   I.CodigoInventario, CONCAT(E.Nombre, ' ', E.Apellido) AS NombreCompleto, MASIG.Motivo AS MotivoAsignacion, MDES.Motivo AS MotivoDesasignacion
FROM InventarioEmpleados AS IE 
INNER JOIN Inventario AS I ON IE.InventarioID = I.InventarioID
INNER JOIN v_Empleados AS E ON IE.EmpleadoID = E.EmpleadoID
INNER JOIN MotivosCambio AS MASIG ON IE.MotivoAsignacionID = MASIG.MotivoID
LEFT JOIN MotivosCambio AS MDES ON IE.MotivoDesasignacionID = MDES.MotivoID

