CREATE PROCEDURE cancelEventReservation
	@EventReservationID int
AS
BEGIN
	UPDATE EventReservations
	SET IsCancelled = 1
	WHERE ID = @EventReservationID
END
