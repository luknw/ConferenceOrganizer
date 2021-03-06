USE [nawojows_a]
GO
/****** Object:  Table [dbo].[Pricings]    Script Date: sob. 03 gru 16 14:48:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Pricings](
	[EventID] [int] NOT NULL,
	[EndDate] [date] NOT NULL,
	[Price] [decimal](18, 4) NOT NULL,
 CONSTRAINT [PK_PriceThresholds] PRIMARY KEY CLUSTERED 
(
	[EventID] ASC,
	[EndDate] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
ALTER TABLE [dbo].[Pricings]  WITH CHECK ADD  CONSTRAINT [FK_PriceThresholds_Events] FOREIGN KEY([EventID])
REFERENCES [dbo].[Events] ([ID])
GO
ALTER TABLE [dbo].[Pricings] CHECK CONSTRAINT [FK_PriceThresholds_Events]
GO
