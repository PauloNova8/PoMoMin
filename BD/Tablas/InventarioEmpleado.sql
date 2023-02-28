USE [PoMoMin]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE TABLE [dbo].[MotivosCambio](
	[MotivoID] [int] IDENTITY(1,1) NOT NULL,
	[Motivo] [nvarchar](200) NOT NULL,
	[Descripcion] [nvarchar](150) NOT NULL,
	[AplicaA] [nvarchar](5) NOT NULL
 CONSTRAINT [PK_MOTIVOSCAMBIO] PRIMARY KEY CLUSTERED 
(
	[MotivoID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]

GO



CREATE TABLE [dbo].[InventarioEmpleados](
	[InventarioID] [bigint] NOT NULL,
	[EmpleadoID] [bigint] NOT NULL,
	[MotivoAsignacionID] [int] NOT NULL,
	[MotivoDesasignacionID] [int] NULL,
	[FechaVigente] [datetime] DEFAULT GETDATE() NOT NULL,
	[FechaFin] [datetime] NULL,
	[Notas] [ntext] NULL,
)
GO

ALTER TABLE [dbo].[InventarioEmpleados]
ADD CONSTRAINT PK_INVENTARIOEMPLEADO PRIMARY KEY CLUSTERED (InventarioID, EmpleadoID, FechaVigente);

ALTER TABLE dbo.[InventarioEmpleados]
ADD CONSTRAINT FK_INVENTARIO_INV
FOREIGN KEY (InventarioID)
REFERENCES dbo.Inventario(InventarioID);

ALTER TABLE dbo.[InventarioEmpleados]
ADD CONSTRAINT FK_INVENTARIO_EMP
FOREIGN KEY (EmpleadoID)
REFERENCES dbo.Empleados(EmpleadoID);

ALTER TABLE dbo.[InventarioEmpleados]
ADD CONSTRAINT FK_INVENTARIO_MOTIVOA
FOREIGN KEY ([MotivoAsignacionID])
REFERENCES dbo.MotivosCambio(MotivoID);

ALTER TABLE dbo.[InventarioEmpleados]
ADD CONSTRAINT FK_INVENTARIO_MOTIVOD
FOREIGN KEY ([MotivoDesasignacionID])
REFERENCES dbo.MotivosCambio(MotivoID);

GO
