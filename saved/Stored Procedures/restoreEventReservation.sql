CREATE PROCEDURE restoreEventReservation
	@EventReservationID int
AS
BEGIN
	DECLARE @EventID int = (SELECT TOP 1 EventID FROM EventReservations WHERE ID = @EventReservationID)
	DECLARE @Participants int = (SELECT TOP 1 Participants FROM EventReservations WHERE ID = @EventReservationID)

	IF dbo.freePlacesOnEvent(@EventID) < @Participants
	BEGIN
		RAISERROR('Not enough places on event',16,1)
		RETURN 1
	END

	UPDATE EventReservations
	SET IsCancelled = 0
	WHERE ID = @EventReservationID
END
