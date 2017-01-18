CREATE PROCEDURE cancelConferenceReservation
	@ReservationID int
AS
BEGIN
	UPDATE Reservations
	SET IsCancelled = 1
	WHERE ID = @ReservationID
END
