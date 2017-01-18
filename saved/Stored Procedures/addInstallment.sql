CREATE PROCEDURE addInstallment
	@ReservationID int
,	@Value decimal(18,4)
,	@PlacedOn date = NULL
AS
BEGIN
	IF @PlacedOn IS NULL
	BEGIN
		SET @PlacedOn = CAST(GETDATE() AS date)
	END

	INSERT INTO Installments VALUES (
		@ReservationID
	,	@Value
	,	@PlacedOn)
END
