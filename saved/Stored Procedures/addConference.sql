CREATE PROCEDURE addConference
	@Name nvarchar(100),
	@Venue nvarchar(100),
	@StartDate date,
	@EndDate date,
	@StudentDiscount decimal (18,4),
	@Website nvarchar(100),
	@IsCancelled bit = 0
AS
BEGIN
	INSERT INTO Conferences VALUES (@Name, @Venue, @StartDate, @EndDate, @StudentDiscount, @Website, @IsCancelled)
END
