CREATE PROCEDURE cancelEvent
	@EventID int
AS
BEGIN
	UPDATE Events
	SET IsCancelled = 1
	WHERE ID = @EventID
END
