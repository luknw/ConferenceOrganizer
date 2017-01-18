CREATE PROCEDURE addWorkshop
	@DayID int
,	@Name nvarchar(50)
,	@MaxParticipants int
AS
BEGIN
	declare @Day table (ID int, ConferenceID int, Date date, MaxParticipants int)
	insert into @Day
		select ID, ConferenceID, Date, MaxParticipants
		from Events
		where ID = @DayID and EventType = 'd'

	if (select COUNT(*) from @Day) != 1
	begin
		raiserror('The day does not exist',16,1)
		return 1
	end

	if (select top 1 MaxParticipants from @Day) < @MaxParticipants
	begin
		raiserror('Too many participants',16,2)
		return 2
	end

	INSERT INTO Events VALUES (
		(select top 1 ConferenceID from @Day)
		, (select top 1 ID from @Day)
		, 'w'
		, @Name
		, (select top 1 Date from @Day)
		, @MaxParticipants
		, 0)
END
