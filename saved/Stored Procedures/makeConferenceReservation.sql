CREATE PROCEDURE makeConferenceReservation
	@CustomerID int
,	@ConferenceID int
,	@PlacedOn date = NULL
AS
BEGIN
	IF EXISTS(SELECT * FROM Reservations WHERE CustomerID = @CustomerID
	 AND ConferenceID = @ConferenceID)
	BEGIN
		RAISERROR('This customer already made reservation for chosen conference',16,1)
		RETURN 1
	END

	IF @PlacedOn IS NULL
		SET @PlacedOn = GETDATE()

	INSERT INTO Reservations VALUES (@CustomerID, @ConferenceID, @PlacedOn, 0)
END
