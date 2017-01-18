CREATE PROCEDURE addParticipation
	@EventReservationID int
,	@ParticipantID int
AS
BEGIN
	DECLARE @ReservationPlaces int = (SELECT TOP 1 Participants FROM EventReservations WHERE ID = @EventReservationID)
	DECLARE @TakenPlaces int = (SELECT TOP 1 COUNT(*) FROM Participations WHERE EventReservationID = @EventReservationID)
	
	IF @TakenPlaces >= @ReservationPlaces
	BEGIN
		RAISERROR('Not enough places on the reservation',16,1)
		RETURN 1
	END

	INSERT INTO Participations VALUES (@EventReservationID, @ParticipantID)
END
