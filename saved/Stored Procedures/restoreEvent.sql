CREATE PROCEDURE restoreEvent
	@EventID int
AS
BEGIN
	UPDATE Events
	SET IsCancelled = 0
	WHERE ID = @EventID
END
