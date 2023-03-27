ALTER VIEW v_Sucursales AS
SELECT 1 AS id, SucursalID, Nombre, Activo, Direccion FROM Sucursales

ALTER VIEW v_Fabricantes AS
SELECT 1 AS id, FabricanteID, Nombre, Activo, Descripcion FROM Fabricantes

ALTER VIEW v_Proveedores AS
SELECT 1 AS id, ProveedorID, Nombre, Activo, Descripcion, Direccion, Telefono, NombreContacto, FechaRegistro, Notas FROM Proveedores