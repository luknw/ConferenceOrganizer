CREATE PROCEDURE makeWorkshopReservation
	@ReservationID int
,	@EventID int
,	@Participants int
AS
BEGIN
	IF EXISTS (SELECT * FROM EventReservations WHERE ReservationID = @ReservationID
		AND EventID = @EventID)
	BEGIN
		RAISERROR('This customer has already made reservation for chosen workshop',16,1)
		RETURN 1
	END

	DECLARE @WorkshopDay table (ReservationID int, EventID int, MaxParticipants int)
	INSERT INTO @WorkshopDay
		SELECT ReservationID, EventID, MaxParticipants
		FROM EventReservations
		JOIN Events ON Events.ID = EventReservations.EventID
		WHERE ReservationID = @ReservationID
		AND EventID = ParentEvent

	IF (SELECT COUNT(*) FROM @WorkshopDay) != 1
	BEGIN
		RAISERROR('Customer has not made reservation for the day of the workshop',16,2)
		RETURN 2
	END
		
	IF @Participants > dbo.freePlacesOnEvent(@EventID)
	BEGIN
		RAISERROR('Not enough places on chosen workshop',16,3)
		RETURN 3
	END

	INSERT INTO EventReservations VALUES (@ReservationID, @EventID, @Participants, 0)
END
