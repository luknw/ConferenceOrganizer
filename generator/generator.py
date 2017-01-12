import collections
import random


# reservation = {
#     'customerID',
#     'conferenceID',
#     'placedOn',
#     'isCancelled',
# }
#
# installment = {
#     'reservationID',
#     'value',
#     'placedOn',
# }
#
# Event = {
#     'conferenceID',
#     'parentEvent',
#     'eventType',
#     'name',
#     'date',
#     'maxParticipants',
# }
#
# EventTime = {
#     'eventID',
#     'startTime',
#     'endTime',
# }
#
# Pricing = {
#     'eventID',
#     'endDate',
#     'price',
# }
#
# EventReservation = {
#     'reservationID',
#     'eventID',
#     'participants',
#     'isCancelled',
# }
#
# Participation = {
#     'eventReservationID',
#     'personID',
# }


# noinspection SqlNoDataSourceInspection
def generate_table_inserts(table, values):
    # zerowanie automatycznego id w tabeli
    # inserts = 'DELETE FROM %s\nDBCC CHECKIDENT (%s, RESEED, 0)' % (table, table)
    inserts = ''
    for row in values:
        inserts += 'INSERT INTO %s VALUES (%s)\n' \
                   % (table, ','.join(map(str, collections.OrderedDict(row).values())))
    return inserts


def read_file(name):
    file = open('res/' + name + '.txt')
    content = file.read().splitlines()
    file.close()
    return content


def is_null(value):
    return value == 'NULL'


def varchar(value):
    if not is_null(value):
        value = value.replace('\'', '\'\'')
        value = '\'' + value + '\''
    return value


customers = []
participants = []
conferences = []
reservations = []


def generate_customers():
    global customers
    names = read_file('customer/names')
    surnames = read_file('customer/surnames')
    company_names = read_file('customer/companyNames')
    phones = read_file('customer/phones')
    emails = read_file('customer/emails')

    for i in range(0, 8000):
        customer = collections.OrderedDict()

        customer['name'] = varchar(names[i])
        customer['surname'] = varchar(surnames[i])
        customer['company_name'] = varchar(company_names[i])
        customer['phone'] = varchar(phones[i])
        customer['email'] = varchar(emails[i])
        customer['is_company'] = 0 if is_null(company_names[i]) else 1

        customers.append(customer)

    return generate_table_inserts('Customers', customers)

# todo debug
# def generate_participants():
#     global customers, participants
#     names = read_file('participant/names')
#     surnames = read_file('participant/surnames')
#     student_ids = read_file('participant/studentIDs')
#
#     ps = 0
#     company_ps = 0
#     for c in range(0, len(customers)):
#         if customers[c]['is_company'] == 1:
#             for i in range(0, random.randint(1, 5)):
#                 participant = collections.OrderedDict()
#
#                 participant['customer_id'] = c + 1
#                 participant['name'] = varchar(names[company_ps])
#                 participant['surname'] = varchar(surnames[company_ps])
#                 participant['is_student'] = 0 if is_null(student_ids[ps]) else 1
#                 participant['student_id'] = varchar(student_ids[ps])
#
#                 participants.append(participant)
#                 ps += 1
#                 company_ps += 1
#         else:
#             participant = collections.OrderedDict()
#
#             participant['customer_id'] = c + 1
#             participant['name'] = customers[c]['name']
#             participant['surname'] = customers[c]['surname']
#             participant['is_student'] = 0 if is_null(student_ids[ps]) else 1
#             participant['student_id'] = student_ids[ps]
#
#             participants.append(participant)
#             ps += 1
#
#     return generate_table_inserts('Participants', participants)


def generate_conferences():
    global conferences
    names = read_file('conference/names')
    venues = read_file('conference/venues')
    start_dates = read_file('conference/startDates')
    end_dates = read_file('conference/endDates')
    student_discounts = read_file('conference/studentDiscounts')
    websites = read_file('conference/websites')
    is_cancelleds = read_file('conference/isCancelleds')

    for i in range(0, 80):
        conference = collections.OrderedDict()

        conference['name'] = varchar(names[i])
        conference['venue'] = varchar(venues[i])
        conference['start_date'] = varchar(start_dates[i])
        conference['end_date'] = varchar(end_dates[i])
        conference['student_discount'] = student_discounts[i]
        conference['website'] = varchar(websites[i])
        conference['is_cancelled'] = is_cancelleds[i]

        conferences.append(conference)

    return generate_table_inserts('Conferences', conferences)

#todo
# def generate_reservations():
#     global reservations, customers, conferences
#
#     names = read_file('conference/names')
#     venues = read_file('conference/venues')
#     start_dates = read_file('conference/startDates')
#     end_dates = read_file('conference/endDates')
#     student_discounts = read_file('conference/studentDiscounts')
#     websites = read_file('conference/websites')
#     is_cancelleds = read_file('conference/isCancelleds')
#
#     for i in range(0, 80):
#         conference = collections.OrderedDict()
#
#         conference['name'] = varchar(names[i])
#         conference['venue'] = varchar(venues[i])
#         conference['start_date'] = varchar(start_dates[i])
#         conference['end_date'] = varchar(end_dates[i])
#         conference['student_discount'] = student_discounts[i]
#         conference['website'] = varchar(websites[i])
#         conference['is_cancelled'] = is_cancelleds[i]
#
#         conferences.append(conference)
#
#     return generate_table_inserts('Conferences', conferences)


def main():
    sql_script = ''
    sql_script += generate_customers()
    # sql_script += generate_participants()
    sql_script += generate_conferences()
    # sql_script += generate_reservations()
    # sql_script += generate_installments()
    # sql_script += generate_events()
    # sql_script += generate_event_times()
    # sql_script += generate_pricings()
    # sql_script += generate_event_reservations()
    # sql_script += generate_participations()

    f = open('generateData.sql', 'w')
    f.write(sql_script)
    f.close()

    return 0


if __name__ == '__main__':
    main()
