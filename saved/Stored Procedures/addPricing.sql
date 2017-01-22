CREATE PROCEDURE addPricing
	@EventID int
,	@EndDate date
,	@Price decimal(18, 4)
AS
BEGIN
	INSERT INTO Pricings VALUES (
		@EventID
	,	@EndDate
	,	@Price)
END
