import collections
import random
import datetime

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

customers = []
participants = []
conferences = []
events = []
event_times = []
pricings = []


# reservations = []


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


def generate_customers():
    global customers
    names = read_file('customer/names')
    surnames = read_file('customer/surnames')
    company_names = read_file('customer/companyNames')
    phones = read_file('customer/phones')
    emails = read_file('customer/emails')

    for i in range(8000):
        customer = collections.OrderedDict()

        customer['name'] = varchar(names[i])
        customer['surname'] = varchar(surnames[i])
        customer['company_name'] = varchar(company_names[i])
        customer['phone'] = varchar(phones[i])
        customer['email'] = varchar(emails[i])
        customer['is_company'] = 0 if is_null(company_names[i]) else 1

        customers.append(customer)

    return generate_table_inserts('Customers', customers)


def generate_participants():
    global customers, participants
    names = read_file('participant/names')
    surnames = read_file('participant/surnames')
    student_ids = read_file('participant/studentIDs')

    ps = 0
    company_ps = 0
    for c in range(len(customers)):
        if customers[c]['is_company'] == 1:
            for i in range(0, random.randint(1, 5)):
                participant = collections.OrderedDict()

                participant['customer_id'] = c + 1
                participant['name'] = varchar(names[company_ps])
                participant['surname'] = varchar(surnames[company_ps])
                participant['is_student'] = 0 if is_null(student_ids[ps]) else 1
                participant['student_id'] = varchar(student_ids[ps])

                participants.append(participant)
                ps += 1
                company_ps += 1
        else:
            participant = collections.OrderedDict()

            participant['customer_id'] = c + 1
            participant['name'] = customers[c]['name']
            participant['surname'] = customers[c]['surname']
            participant['is_student'] = 0 if is_null(student_ids[ps]) else 1
            participant['student_id'] = varchar(student_ids[ps])

            participants.append(participant)
            ps += 1

    return generate_table_inserts('Participants', participants)


def generate_conferences():
    global conferences
    names = read_file('conference/names')
    venues = read_file('conference/venues')
    start_dates = read_file('conference/startDates')
    end_dates = read_file('conference/endDates')
    student_discounts = read_file('conference/studentDiscounts')
    websites = read_file('conference/websites')
    is_cancelleds = read_file('conference/isCancelleds')

    for i in range(80):
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


def parse_date(sql_string):
    return datetime.date(
        *map(int, sql_string.strip('\'').split('-')))


def generate_events_event_times():
    global conferences, events, event_times

    names = read_file('event/day/names')

    days = []
    for c in range(len(conferences)):
        start_date = parse_date(conferences[c]['start_date'])
        end_date = parse_date(conferences[c]['end_date'])
        conf_days = (end_date - start_date).days + 1
        for d in range(conf_days):
            day = collections.OrderedDict()

            day['conference_id'] = c + 1
            day['parent_event'] = 'NULL'
            day['event_type'] = varchar('d')
            day['name'] = varchar(random.choice(names))
            day['date'] = varchar((start_date + datetime.timedelta(d)).isoformat())
            day['max_participants'] = random.randint(50, 200)

            days.append(day)

    names = read_file('event/workshop/names')

    workshops = []
    ws = len(days)
    for d in range(len(days)):
        for w in range(random.randint(0, 8)):
            workshop = collections.OrderedDict()

            workshop['conference_id'] = days[d]['conference_id']
            workshop['parent_event'] = d + 1
            workshop['event_type'] = varchar('w')
            workshop['name'] = varchar(random.choice(names))
            workshop['date'] = days[d]['date']
            workshop['max_participants'] = random.randint(10, 50)

            workshops.append(workshop)

            workshop_time = collections.OrderedDict()

            workshop_time['event_id'] = ws + 1
            hour = random.randint(8, 21)
            minute = 15 * random.randint(0, 3)
            second = 0
            workshop_time['start_time'] = \
                varchar('%02d:%02d:%02d' % (hour, minute, second))
            workshop_time['end_time'] = \
                varchar(
                    '%02d:%02d:%02d' % (hour + random.randint(0, 3),
                                        minute + random.choice([0, 5, 10]),
                                        second + 0))
            event_times.append(workshop_time)
            ws += 1

    events += days + workshops

    return \
        generate_table_inserts('Events', events) \
        + generate_table_inserts('EventTimes', event_times)


def generate_pricings():
    global events, pricings

    for e in range(len(events)):
        pricing = collections.OrderedDict()

        pricing['event_id'] = e + 1
        pricing['end_date'] = events[e]['date']
        pricing['price'] = \
            0 if random.randrange(100) < 25 else 10 * random.randint(1, 20)

        pricings.append(pricing)

        if events[e]['event_type'] == '\'d\'' and pricing['price'] >= 20:
            for p in range(random.randint(0, 3)):
                last = pricing
                pricing = collections.OrderedDict()

                pricing['event_id'] = e + 1
                pricing['end_date'] = \
                    varchar((parse_date(events[e]['date']) - datetime.timedelta(random.randint(1, 30))).isoformat())
                pricing['price'] = last['price'] * (0.5 * (1 + random.random()))

                pricings.append(pricing)

    return generate_table_inserts('Pricings', pricings)


# def generate_reservations():
#     global reservations, customers, conferences
#
#     for conf in range(len(conferences)):
#
#         for r in range(random.randint()):
#             reservation = collections.OrderedDict()
#
#
#
#         conferences.append(reservation)
#
#     return generate_table_inserts('Reservations', reservations)


def main():
    sql_script = ''
    sql_script += generate_customers()
    sql_script += generate_participants()
    sql_script += generate_conferences()
    sql_script += generate_events_event_times()
    sql_script += generate_pricings()
    # sql_script += generate_reservations()
    # sql_script += generate_installments()
    # sql_script += generate_event_reservations()
    # sql_script += generate_participations()
    #
    f = open('generateData.sql', 'w')
    f.write(sql_script)
    f.close()

    return 0


if __name__ == '__main__':
    main()
