ALTER VIEW v_Inventario AS
SELECT 1 AS id, I.InventarioID, I.CodigoInventario, C.Categoria, I.Modelo, I.Serie, F.Nombre AS Fabricante, I.CategoriaID, I.FabricanteID, I.CodigoBarra, I.TipoInventarioID,
I.Descripcion, I.SucursalID, S.Nombre AS Sucursal, I.AsignadoA, CASE WHEN I.AsignadoA IS NULL THEN '' ELSE CONCAT(EM.Nombres, ' ', EM.Apellidos) END AS AsignadoNombre, I.ProveedorID, I.EstadoID, E.Estado, I.FechaCompra, I.FechaUtilMaxima, I.FechaUltimoSoporte, I.Notas
FROM Inventario AS I INNER JOIN Categorias AS C ON I.CategoriaID = C.CategoriaID
INNER JOIN Fabricantes AS F ON I.FabricanteID = F.FabricanteID
INNER JOIN Sucursales AS S ON I.SucursalID = S.SucursalID
INNER JOIN EstadosInventario AS E ON I.EstadoID = E.EstadoID
LEFT JOIN Empleados AS EM ON I.AsignadoA = EM.EmpleadoID


ALTER VIEW v_Empleados AS
SELECT 1 AS id, E.EmpleadoID, CASE WHEN CHARINDEX(' ', E.Nombres) = 0 THEN E.Nombres ELSE LEFT(E.Nombres + ' ', CHARINDEX(' ', E.Nombres) - 1) END AS Nombre,
CASE WHEN CHARINDEX(' ', E.Apellidos) = 0 THEN E.Apellidos ELSE LEFT(E.Apellidos + ' ', CHARINDEX(' ', E.Apellidos) - 1) END AS Apellido,
E.SucursalID, E.PuestoID, P.Nombre AS PuestoTexto,E.Nombres, E.Apellidos, CONCAT(E.Nombres, ' ', E.Apellidos) AS NombreCompleto, S.Nombre AS Sucursal, 
E.Identificacion, E.ReportaA, E.TelefonoCelular, E.TelefonoTrabajo, E.Direccion, E.Genero, E.FechaNacimiento, E.FechaAlta, E.FechaBaja, E.EstadoID, 
ES.Estado, E.Notas, D.Nombre AS Departamento, P.DepartamentoID
FROM Empleados AS E INNER JOIN Puestos AS P ON E.PuestoID = P.PuestoID
INNER JOIN Departamentos AS D ON P.DepartamentoID = D.DepartamentoID
INNER JOIN Sucursales AS S ON E.SucursalID = S.SucursalID
INNER JOIN EstadosEmpleado AS ES ON E.EstadoID = ES.EstadoID