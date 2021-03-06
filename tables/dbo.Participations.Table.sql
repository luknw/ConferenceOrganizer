USE [nawojows_a]
GO
/****** Object:  Table [dbo].[Participations]    Script Date: sob. 03 gru 16 14:48:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Participations](
	[EventReservationID] [int] NOT NULL,
	[PersonID] [int] NOT NULL,
 CONSTRAINT [PK_Participations] PRIMARY KEY CLUSTERED 
(
	[EventReservationID] ASC,
	[PersonID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
ALTER TABLE [dbo].[Participations]  WITH CHECK ADD  CONSTRAINT [FK_Participations_EventReservations] FOREIGN KEY([EventReservationID])
REFERENCES [dbo].[EventReservations] ([ID])
GO
ALTER TABLE [dbo].[Participations] CHECK CONSTRAINT [FK_Participations_EventReservations]
GO
ALTER TABLE [dbo].[Participations]  WITH CHECK ADD  CONSTRAINT [FK_Participations_Participants] FOREIGN KEY([PersonID])
REFERENCES [dbo].[Participants] ([ID])
GO
ALTER TABLE [dbo].[Participations] CHECK CONSTRAINT [FK_Participations_Participants]
GO
