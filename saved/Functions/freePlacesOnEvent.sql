CREATE FUNCTION [dbo].[freePlacesOnEvent]
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
			- (SELECT SUM(Participants) FROM EventReservations WHERE EventID = @EventID AND IsCancelled = 0 GROUP BY EventID)

	IF (SELECT TOP 1 EventType FROM Events WHERE ID = @EventID) = 'w'
	BEGIN
		DECLARE @DayID int =
			(SELECT TOP 1 ParentEvent
			FROM Events
			join EventReservations on EventReservations.EventID = Events.ID)
		
		DECLARE @FreePlacesOnDay int =
			(SELECT TOP 1 MaxParticipants FROM Events WHERE ID = @DayID)
			- (SELECT SUM(Participants) FROM EventReservations WHERE EventID = @DayID AND IsCancelled = 0 GROUP BY EventID)

		SET @FreePlaces =
			(SELECT CASE
				WHEN @FreePlaces < @FreePlacesOnDay
				THEN @FreePlaces
				ELSE @FreePlacesOnDay END)
	END

	RETURN @FreePlaces
END

GO


