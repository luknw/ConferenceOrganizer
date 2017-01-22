CREATE PROCEDURE addCustomer
	@Name nvarchar(50)
,	@Surname nvarchar(50)
,	@CompanyName nvarchar(50)
,	@Phone nvarchar(20)
,	@Email nvarchar(50)
,	@IsCompany bit
AS
BEGIN
	INSERT INTO Customers VALUES (
		@Name
	,	@Surname
	,	@CompanyName
	,	@Phone
	,	@Email
	,	@IsCompany)
END
