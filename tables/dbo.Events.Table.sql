USE [nawojows_a]
GO
/****** Object:  Table [dbo].[Events]    Script Date: sob. 03 gru 16 14:48:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Events](
	[ID] [int] NOT NULL,
	[ConferenceID] [int] NOT NULL,
	[ParentEvent] [int] NULL,
	[EventType] [char](1) NOT NULL,
	[Name] [nvarchar](50) NOT NULL,
	[Date] [date] NOT NULL,
	[MaxParticipants] [int] NOT NULL,
 CONSTRAINT [PK_Events] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
ALTER TABLE [dbo].[Events]  WITH CHECK ADD  CONSTRAINT [FK_Events_Conferences] FOREIGN KEY([ConferenceID])
REFERENCES [dbo].[Conferences] ([ID])
GO
ALTER TABLE [dbo].[Events] CHECK CONSTRAINT [FK_Events_Conferences]
GO
ALTER TABLE [dbo].[Events]  WITH CHECK ADD  CONSTRAINT [FK_Events_Events1] FOREIGN KEY([ParentEvent])
REFERENCES [dbo].[Events] ([ID])
GO
ALTER TABLE [dbo].[Events] CHECK CONSTRAINT [FK_Events_Events1]
GO
ALTER TABLE [dbo].[Events]  WITH CHECK ADD  CONSTRAINT [FK_Events_EventTimes] FOREIGN KEY([ID])
REFERENCES [dbo].[EventTimes] ([EventID])
GO
ALTER TABLE [dbo].[Events] CHECK CONSTRAINT [FK_Events_EventTimes]
GO
