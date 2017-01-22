CREATE PROCEDURE addParticipant
	@CustomerID int
,	@Name nvarchar(50)
,	@Surname nvarchar(50)
,	@IsStudent bit
,	@StudentID nvarchar(20) = NULL
AS
BEGIN
	INSERT INTO Participants VALUES (
		@CustomerID
	,	@Name
	,	@Surname
	,	@IsStudent
	,	@StudentID)
END
