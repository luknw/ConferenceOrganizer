CREATE PROCEDURE addDay
	@ConferenceID int
,	@Name nvarchar(50)
,	@Date date
,	@MaxParticipants int
AS
BEGIN
	declare @Conference table (ID int, StartDate date, EndDate date)
	insert into @Conference
		select ID, StartDate, EndDate
		from Conferences
		where ID = @ConferenceID

	if (select COUNT(*) from @Conference) != 1
	begin
		raiserror('The conference does not exist',16,1)
		return 1
	end

	if (select top 1 StartDate from @Conference) > @Date or (select top 1 EndDate from @Conference) < @Date
	begin
		raiserror('Invalid date',16,2)
		return 2
	end

	if exists (select * from Events where ConferenceID = @ConferenceID and Date = @Date)
	begin
		raiserror('Chosen date is already taken',16,3)
		return 3
	end

	INSERT INTO Events VALUES (@ConferenceID, NULL, 'd', @Name, @Date, @MaxParticipants, 0)
END
