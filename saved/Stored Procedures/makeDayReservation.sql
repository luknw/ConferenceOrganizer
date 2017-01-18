CREATE PROCEDURE makeDayReservation
	@ReservationID int
,	@EventID int
,	@Participants int
AS
BEGIN
	IF EXISTS (SELECT * FROM EventReservations WHERE ReservationID = @ReservationID
		AND EventID = @EventID)
	BEGIN
		RAISERROR('This customer already made reservation for chosen day',16,1)
		RETURN 1
	END

	IF @Participants > dbo.freePlacesOnEvent(@EventID)
	BEGIN
		RAISERROR('Not enough free places on chosen event',16,2)
		RETURN 2
	END
		
	INSERT INTO EventReservations VALUES (@ReservationID, @EventID, @Participants, 0)
END
