CREATE PROCEDURE changeEventReservationPlaces
	@EventReservationID int
,	@NewPlaces int
AS
BEGIN
	DECLARE @OldPlaces int = (SELECT TOP 1 Participants FROM EventReservations WHERE ID = @EventReservationID)
	DECLARE @EventID int = (SELECT TOP 1 EventID FROM EventReservations WHERE ID = @EventReservationID)

	IF @OldPlaces < @NewPlaces
		OR dbo.freePlacesOnEvent(@EventID) + @OldPlaces >= @NewPlaces
	BEGIN
		UPDATE EventReservations
			SET Participants = @NewPlaces
			WHERE ID = @EventReservationID
		RETURN 0
	END
	ELSE
	BEGIN
		RAISERROR('Not enough places on event',16,1)
		RETURN 1
	END
END
