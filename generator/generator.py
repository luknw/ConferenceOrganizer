import collections
import random
import datetime

customers = []
participants = []
conferences = []
events = []
event_times = []
pricings = []

days = []
workshops = []

# noinspection SqlNoDataSourceInspection
HEADER = \
    """
DELETE FROM Participations
DELETE FROM Installments
DELETE FROM Pricings
DELETE FROM EventTimes
DELETE FROM Participants
DELETE FROM EventReservations
DELETE FROM Reservations
DELETE FROM Customers
DELETE FROM Events
DELETE FROM Conferences
DBCC CHECKIDENT (Installments, RESEED, 0)
DBCC CHECKIDENT (Participants, RESEED, 0)
DBCC CHECKIDENT (Customers, RESEED, 0)
DBCC CHECKIDENT (Reservations, RESEED, 0)
DBCC CHECKIDENT (Conferences, RESEED, 0)
DBCC CHECKIDENT (Events, RESEED, 0)
DBCC CHECKIDENT (EventReservations, RESEED, 0)
"""


# noinspection SqlNoDataSourceInspection
def generate_table_inserts(table, values):
    # zerowanie automatycznego id w tabeli
    # inserts = 'DELETE FROM %s\nDBCC CHECKIDENT (%s, RESEED, 0)' % (table, table)
    inserts = ''
    for row in values:
        inserts += ('INSERT INTO %s VALUES (%s)\n'
                    % (table, ','.join(map(str, collections.OrderedDict(row).values()))))
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


def parse_date(sql_date_string):
    return datetime.date(
        *map(int, sql_date_string.strip('\'').split('-')))


def generate_events_event_times():
    global conferences, events, event_times, days, workshops

    names = read_file('event/day/names')

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
            hour = random.randint(8, 20)
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


def subtract_days(sql_date_string, days_number):
    return varchar((parse_date(sql_date_string) - datetime.timedelta(days_number)).isoformat())


def generate_pricings():
    global events, pricings

    for e in range(len(events)):
        pricing = collections.OrderedDict()

        pricing['event_id'] = e + 1
        pricing['end_date'] = events[e]['date']
        pricing['price'] = \
            0 if random.random() < 0.25 else 10 * random.randint(1, 20)

        pricings.append(pricing)
        if events[e]['event_type'] == '\'d\'' and pricing['price'] >= 20:
            for p in range(random.randint(0, 3)):
                last = pricing
                pricing = collections.OrderedDict()

                pricing['event_id'] = e + 1
                pricing['end_date'] = subtract_days(last['end_date'], random.randint(1, 30))
                pricing['price'] = int(last['price'] * (0.5 * (1 + random.random())))

                pricings.append(pricing)

    return generate_table_inserts('Pricings', pricings)


def generate_reservations():
    global events, participants, pricings, customers, event_times, conferences, days, workshops

    participant_workshops = []
    participant_days = []

    workshop_participants = [[] for _ in workshops]
    day_participants = [[] for _ in days]

    for p in range(len(participants)):
        participant_days.append(set())
        p_w_inds = sorted(random.sample(range(len(workshops)), random.randint(0, len(workshops))),
                          key=lambda i: event_times[i]['start_time'])

        w = 1
        while w < len(p_w_inds) and event_times[p_w_inds[w - 1]]['end_time'] >= event_times[p_w_inds[w]]['start_time']:
            del p_w_inds[w]
            w += 1

        w = 0
        while w < len(p_w_inds):
            workshop_day = workshops[p_w_inds[w]]['parent_event'] - 1
            while w < len(p_w_inds) \
                    and (len(workshop_participants[p_w_inds[w]]) + 1 > workshops[p_w_inds[w]]['max_participants']
                         or (p not in day_participants[workshop_day]
                             and len(day_participants[workshop_day]) + 1 > days[workshop_day]['max_participants'])):
                del p_w_inds[w]
            if w < len(p_w_inds):
                workshop_participants[p_w_inds[w]].append(p)
                if p not in day_participants[workshop_day]:
                    day_participants[workshop_day].append(p)
                    participant_days[p].add(workshop_day)
            w += 1

        participant_workshops.append(p_w_inds)

    for p in range(len(participants)):
        non_workshop_days = random.sample(range(len(days)), random.randint(0, 6))
        for d in non_workshop_days:
            if p not in day_participants[d] and len(day_participants[d]) + 1 <= days[d]['max_participants']:
                day_participants[d].append(p)
                participant_days[p].add(d)

    customer_conferences = [set() for _ in customers]
    customer_days = [collections.Counter() for _ in customers]
    customer_workshops = [collections.Counter() for _ in customers]

    for p in range(len(participants)):
        customer = participants[p]['customer_id'] - 1
        for day in participant_days[p]:
            customer_conferences[customer].add(days[day]['conference_id'] - 1)
            customer_days[customer][day] += 1
        for workshop in participant_workshops[p]:
            customer_workshops[customer][workshop] += 1

    reservations = []
    day_reservations = []
    workshop_reservations = []
    participations = []
    installments = []

    pricings = sorted(pricings, key=lambda p: p['end_date'], reverse=True)

    event_pricing = {e: [] for e in range(len(events))}
    for pricing in pricings:
        event_pricing[pricing['event_id'] - 1].append(pricing)

    rs = 0
    ers = 0
    for customer in range(len(customer_conferences)):
        for conference in customer_conferences[customer]:
            reservation = collections.OrderedDict()
            reservation_cost = 0

            reservation['customer_id'] = customer + 1
            reservation['conference_id'] = conference + 1
            reservation['placed_on'] = subtract_days(conferences[conference]['start_date'], random.randint(7, 120))
            reservation['is_cancelled'] = 0 if random.random() < 0.95 else 1

            reservations.append(reservation)
            for day in filter(lambda d: days[d]['conference_id'] == conference + 1, customer_days[customer].keys()):
                day_reservation = collections.OrderedDict()

                day_reservation['reservation_id'] = rs + 1
                day_reservation['event_id'] = day + 1
                day_reservation['participants'] = customer_days[customer][day]
                day_reservation['is_cancelled'] = 0 if random.random() < 0.95 else 1

                day_reservations.append(day_reservation)

                if day_reservation['is_cancelled'] == 0:
                    p = 0
                    while p < len(event_pricing[day]) - 1 \
                            and reservations[rs]['placed_on'] <= event_pricing[day][p + 1]['end_date']:
                        p += 1
                    eligible_price = event_pricing[day][p]['price']
                    reservation_cost += customer_days[customer][day] * eligible_price

                for participant in filter(lambda p: participants[p]['customer_id'] == customer + 1,
                                          day_participants[day]):
                    participation = collections.OrderedDict()

                    participation['event_reservation_id'] = ers + 1
                    participation['participant_id'] = participant + 1

                    participations.append(participation)
                ers += 1
            for workshop in \
                    filter(lambda w: workshops[w]['conference_id'] == conference + 1, customer_workshops[customer]):
                workshop_reservation = collections.OrderedDict()

                workshop_reservation['reservation_id'] = rs + 1
                workshop_reservation['event_id'] = workshop + 1
                workshop_reservation['participants'] = customer_workshops[customer][workshop]
                workshop_reservation['is_cancelled'] = 0 if random.random() < 0.95 else 1

                workshop_reservations.append(workshop_reservation)

                if workshop_reservation['is_cancelled'] == 0:
                    p = 0
                    while p < len(event_pricing[workshop + len(days)]) - 1 \
                            and reservation[rs]['placed_on'] <= event_pricing[workshop + len(days)][p + 1]['end_date']:
                        p += 1
                    eligible_price = event_pricing[workshop][p]['price']
                    reservation_cost += customer_workshops[customer][workshop] * eligible_price

                for participant in filter(lambda p: participants[p]['customer_id'] == customer + 1,
                                          workshop_participants[workshop]):
                    participation = collections.OrderedDict()

                    participation['event_reservation_id'] = ers + 1
                    participation['participant_id'] = participant + 1

                    participations.append(participation)
                ers += 1
            if reservation['is_cancelled'] == 0:
                if reservation_cost < 100:
                    if random.random() < 0.95:
                        installment = collections.OrderedDict()

                        installment['reservation_id'] = rs + 1
                        installment['value'] = reservation_cost
                        installment['placed_on'] = subtract_days(reservations[rs]['placed_on'], -random.randint(0, 14))

                        installments.append(installment)
                else:
                    installment_count = random.randint(1, 7)
                    zeroth = subtract_days(reservations[rs]['placed_on'], 1)
                    past = 0
                    if random.random() < 0.95:
                        paid = 0
                        rest = reservation_cost
                        while paid < installment_count:
                            installment = collections.OrderedDict()

                            installment['reservation_id'] = rs + 1
                            installment_value = int(reservation_cost / installment_count)
                            installment['value'] = installment_value if paid < installment_count - 1 else rest
                            rest -= installment_value
                            past += random.randint(1, int((7 - past) / installment_count) + 1)
                            installment['placed_on'] = subtract_days(zeroth, -past)

                            installments.append(installment)
                            paid += 1
                    else:
                        paid = 0
                        will_pay = random.randint(0, installment_count)
                        while paid < will_pay:
                            installment = collections.OrderedDict()

                            installment['reservation_id'] = rs + 1
                            installment['value'] = int(reservation_cost / installment_count * (
                                1 if random.random() < 0.95 else 2 * random.random()))
                            past += random.randint(1, 7)
                            installment['placed_on'] = subtract_days(zeroth, -(
                                past * (1 if random.random() < 0.95 else 2 * random.random())))

                            installments.append(installment)
                            paid += 1
            rs += 1

    return \
        generate_table_inserts('Reservations', reservations) \
        + generate_table_inserts('EventReservations', day_reservations + workshop_reservations) \
        + generate_table_inserts('Participations', participations) \
        + generate_table_inserts('Installments', installments)


def main():
    sql_script = HEADER
    sql_script += generate_customers()
    sql_script += generate_participants()
    sql_script += generate_conferences()
    sql_script += generate_events_event_times()
    sql_script += generate_pricings()
    sql_script += generate_reservations()

    f = open('generateData.sql', 'w')
    f.write(sql_script)
    f.close()

    return 0


if __name__ == '__main__':
    main()
