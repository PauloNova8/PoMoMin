ALTER VIEW v_Usuarios AS
SELECT 1 AS id, U.UsuarioID, U.Usuario, U.Clave AS Token, U.PerfilID, 
P.NombrePerfil, CONVERT(VARCHAR, U.FechaCreacion, 23) AS FechaCreacion, CONVERT(VARCHAR, U.FechaUltimaActualizacion, 23) AS FechaUltimaActualizacion,
U.EstadoID, EU.Estado
FROM Usuarios AS U INNER JOIN PerfilesUsuario AS P ON U.PerfilID = P.PerfilID
INNER JOIN EstadosUsuario AS EU ON U.EstadoID = EU.EstadoID