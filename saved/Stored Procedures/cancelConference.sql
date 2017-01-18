CREATE PROCEDURE cancelConference
	@ConferenceID int
AS
BEGIN
	UPDATE Conferences
	SET IsCancelled = 1
	WHERE ID = @ConferenceID
END
