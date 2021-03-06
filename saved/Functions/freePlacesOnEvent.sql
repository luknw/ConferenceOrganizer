USE [nawojows_a]
GO
/****** Object:  UserDefinedFunction [dbo].[freePlacesOnEvent]    Script Date: sob. 21 sty 17 22:22:17 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER FUNCTION [dbo].[freePlacesOnEvent]
(
	@EventID int
)
RETURNS int
AS
BEGIN
	DECLARE @FreePlaces int

	IF NOT EXISTS (SELECT * FROM Events WHERE ID = @EventID)
	BEGIN
		--the conversion will fail reporting error
		RETURN cast('Invalid event' as int);
	END

	SET @FreePlaces =
			(SELECT TOP 1 MaxParticipants FROM Events WHERE ID = @EventID)
			- (SELECT SUM(Participants)
				FROM EventReservations
				JOIN Reservations ON Reservations.ID = EventReservations.ReservationID
				WHERE EventID = @EventID
				AND Reservations.IsCancelled = 0
				AND EventReservations.IsCancelled = 0
				GROUP BY EventID)

	IF (SELECT TOP 1 EventType FROM Events WHERE ID = @EventID) = 'w'
	BEGIN
		DECLARE @DayID int =
			(SELECT TOP 1 ParentEvent
			FROM Events
			join EventReservations on EventReservations.EventID = Events.ID)
		
		DECLARE @FreePlacesOnDay int =
			(SELECT TOP 1 MaxParticipants FROM Events WHERE ID = @DayID)
			- (SELECT SUM(Participants)
				FROM EventReservations
				JOIN Reservations ON Reservations.ID = EventReservations.ReservationID
				WHERE EventID = @DayID
				AND Reservations.IsCancelled = 0
				AND EventReservations.IsCancelled = 0
				GROUP BY EventID)

		SET @FreePlaces =
			(SELECT CASE
				WHEN @FreePlaces < @FreePlacesOnDay
				THEN @FreePlaces
				ELSE @FreePlacesOnDay END)
	END

	RETURN @FreePlaces
END

