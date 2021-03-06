USE [nawojows_a]
GO
/****** Object:  Table [dbo].[EventReservations]    Script Date: sob. 03 gru 16 14:48:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[EventReservations](
	[ID] [int] NOT NULL,
	[ReservationID] [int] NOT NULL,
	[EventID] [int] NOT NULL,
	[Participants] [int] NOT NULL,
	[IsCancelled] [bit] NOT NULL,
 CONSTRAINT [PK_EventReservations] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
ALTER TABLE [dbo].[EventReservations]  WITH CHECK ADD  CONSTRAINT [FK_EventReservations_Events] FOREIGN KEY([EventID])
REFERENCES [dbo].[Events] ([ID])
GO
ALTER TABLE [dbo].[EventReservations] CHECK CONSTRAINT [FK_EventReservations_Events]
GO
ALTER TABLE [dbo].[EventReservations]  WITH CHECK ADD  CONSTRAINT [FK_EventReservations_Reservations] FOREIGN KEY([ReservationID])
REFERENCES [dbo].[Reservations] ([ID])
GO
ALTER TABLE [dbo].[EventReservations] CHECK CONSTRAINT [FK_EventReservations_Reservations]
GO
