CREATE PROCEDURE restoreConference
	@ConferenceID int
AS
BEGIN
	UPDATE Conferences
	SET IsCancelled = 0
	WHERE ID = @ConferenceID
END
