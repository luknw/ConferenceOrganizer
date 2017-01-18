CREATE PROCEDURE restoreConferenceReservation
	@ReservationID int
AS
BEGIN
	IF EXISTS (
		SELECT *
		FROM EventReservations
		WHERE ReservationID = @ReservationID
		AND IsCancelled = 0
		AND dbo.freePlacesOnEvent(EventID) < Participants)
	BEGIN
		RAISERROR('Some events do not have required amount of places free',16,1)
		RETURN 1
	END

	UPDATE Reservations
	SET IsCancelled = 0
	WHERE ID = @ReservationID
END
