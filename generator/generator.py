import collections
import random
import datetime

customers = []
participants = dict()
conferences = dict()
events = dict()
event_times = dict()
pricings = []

days = dict()
workshops = dict()
workshops_by_day = dict()

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


def generate_csv(table, values):
    csv = open('res/' + table + '.csv', mode='w')
    csv.writelines(map(lambda row: ';'.join(map(str, collections.OrderedDict(row).values())) + '\n', values))
    csv.close()


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

        customer['id'] = i + 1
        customer['name'] = varchar(names[i])
        customer['surname'] = varchar(surnames[i])
        customer['company_name'] = varchar(company_names[i])
        customer['phone'] = varchar(phones[i])
        customer['email'] = varchar(emails[i])
        customer['is_company'] = 0 if is_null(company_names[i]) else 1

        customers.append(customer)

    generate_csv('Customers', customers)


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

                participant['id'] = ps + 1
                participant['customer_id'] = customers[c]['id']
                participant['name'] = varchar(names[company_ps])
                participant['surname'] = varchar(surnames[company_ps])
                participant['is_student'] = 0 if is_null(student_ids[ps]) else 1
                participant['student_id'] = varchar(student_ids[ps])

                participants[participant['id']] = participant
                ps += 1
                company_ps += 1
        else:
            participant = collections.OrderedDict()

            participant['id'] = ps + 1
            participant['customer_id'] = customers[c]['id']
            participant['name'] = customers[c]['name']
            participant['surname'] = customers[c]['surname']
            participant['is_student'] = 0 if is_null(student_ids[ps]) else 1
            participant['student_id'] = varchar(student_ids[ps])

            participants[participant['id']] = participant
            ps += 1

    generate_csv('Participants', participants.values())


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

        conference['id'] = i + 1
        conference['name'] = varchar(names[i])
        conference['venue'] = varchar(venues[i])
        conference['start_date'] = varchar(start_dates[i])
        conference['end_date'] = varchar(end_dates[i])
        conference['student_discount'] = float(student_discounts[i])
        conference['website'] = varchar(websites[i])
        conference['is_cancelled'] = int(is_cancelleds[i])

        conferences[conference['id']] = conference

    generate_csv('Conferences', conferences.values())


def parse_date(sql_date_string):
    return datetime.date(
        *map(int, sql_date_string.strip('\'').split('-')))


def generate_events():
    global conferences, events, days, workshops, workshops_by_day

    names = read_file('event/day/names')

    es = 0
    for c in conferences.values():
        start_date = parse_date(c['start_date'])
        end_date = parse_date(c['end_date'])
        conf_days = (end_date - start_date).days + 1
        for d in range(conf_days):
            day = collections.OrderedDict()

            day['id'] = es + 1
            day['conference_id'] = c['id']
            day['parent_event'] = 'NULL'
            day['event_type'] = varchar('d')
            day['name'] = varchar(random.choice(names))
            day['date'] = varchar((start_date + datetime.timedelta(d)).isoformat())
            day['max_participants'] = random.randint(50, 200)
            day['is_cancelled'] = 0 if random.random() < 0.95 else 1

            days[day['id']] = day
            es += 1

    names = read_file('event/workshop/names')

    for d in days.values():
        for w in range(random.randint(0, 8)):
            workshop = collections.OrderedDict()

            workshop['id'] = es + 1
            workshop['conference_id'] = d['conference_id']
            workshop['parent_event'] = d['id']
            workshop['event_type'] = varchar('w')
            workshop['name'] = varchar(random.choice(names))
            workshop['date'] = d['date']
            workshop['max_participants'] = random.randint(10, 50)
            workshop['is_cancelled'] = 0 if random.random() < 0.95 else 1

            workshops[workshop['id']] = workshop
            es += 1

    workshops_by_day = {i: [] for i in days.keys()}
    for w in workshops.values():
        workshops_by_day[w['parent_event']].append(w)

    events = {**days, **workshops}

    generate_csv('Events', events.values())


def generate_event_times():
    global workshops, event_times

    for w in workshops.values():
        workshop_time = collections.OrderedDict()

        workshop_time['event_id'] = w['id']
        hour = random.randint(8, 20)
        minute = 15 * random.randint(0, 3)
        second = 0
        workshop_time['start_time'] = \
            varchar('%02d:%02d:%02d' % (hour, minute, second))
        workshop_time['end_time'] = \
            varchar('%02d:%02d:%02d' % (hour + random.randint(1, 3),
                                        minute + random.choice([0, 5, 10]),
                                        second + 0))
        event_times[workshop_time['event_id']] = workshop_time

    generate_csv('EventTimes', event_times.values())


def subtract_days(sql_date_string, days_number):
    return varchar((parse_date(sql_date_string) - datetime.timedelta(days_number)).isoformat())


def generate_pricings():
    global events, pricings

    for e in events:
        pricing = collections.OrderedDict()

        pricing['event_id'] = events[e]['id']
        pricing['end_date'] = events[e]['date']
        pricing['price'] = \
            0 if random.random() < 0.25 else 10 * random.randint(1, 20)

        pricings.append(pricing)
        if events[e]['event_type'] == '\'d\'' and pricing['price'] >= 20:
            for p in range(random.randint(0, 3)):
                last = pricing
                pricing = collections.OrderedDict()

                pricing['event_id'] = events[e]['id']
                pricing['end_date'] = subtract_days(last['end_date'], random.randint(1, 30))
                pricing['price'] = int(last['price'] * (0.5 * (1 + random.random())))

                pricings.append(pricing)

    generate_csv('Pricings', pricings)


def generate_reservations():
    global events, participants, pricings, customers, event_times, conferences, days, workshops, workshops_by_day

    participant_days = dict()
    day_participants = {i: set() for i in map(lambda day: day['id'], days.values())}

    participant_workshops = dict()
    workshop_participants = {i: set() for i in map(lambda workshop: workshop['id'], workshops.values())}

    for p in participants:
        p_days = list(filter(lambda day: len(day_participants[day['id']]) + 1 <= day['max_participants'],
                             random.sample(list(days.values()), random.randint(1, 2))))

        i = 0
        while i < len(p_days):
            j = i + 1
            while j < len(p_days):
                if p_days[i]['date'] == p_days[j]['date']:
                    del p_days[j]
                    j -= 1
                j += 1
            i += 1

        participant_days[p] = set(map(lambda day: day['id'], p_days))

        p_workshops = []
        for day in participant_days[p]:
            day_participants[day].add(p)

            p_workshops += filter(lambda w: random.random() < 0.5
                                            and len(workshop_participants[w['id']]) + 1 <= w['max_participants'],
                                  workshops_by_day[day])

        i = 0
        while i < len(p_workshops):
            wi = workshops[p_workshops[i]['id']]
            j = i + 1
            while j < len(p_workshops):
                wj = workshops[p_workshops[j]['id']]
                if wi['date'] == wj['date'] \
                        and event_times[wi['id']]['start_time'] <= \
                                event_times[wj['id']]['start_time'] <= \
                                event_times[wi['id']]['end_time']:
                    del p_workshops[j]
                    j -= 1
                j += 1
            i += 1

        participant_workshops[p] = set(map(lambda workshop: workshop['id'], p_workshops))
        for w in participant_workshops[p]:
            workshop_participants[w].add(p)

    customer_conferences = {c['id']: set() for c in customers}
    customer_days = {c['id']: dict() for c in customers}
    customer_workshops = {c['id']: dict() for c in customers}

    for p in participants.values():
        customer = p['customer_id']
        for day in participant_days[p['id']]:
            customer_conferences[customer].add(days[day]['conference_id'])
            customer_days[customer].setdefault(day, []).append(p['id'])
        for workshop in participant_workshops[p['id']]:
            customer_workshops[customer].setdefault(workshop, []).append(p['id'])

    reservations = []
    day_reservations = []
    workshop_reservations = []
    participations = []
    installments = []

    pricings = sorted(pricings, key=lambda p: p['end_date'], reverse=True)

    event_pricing = {i: [] for i in map(lambda e: e['id'], events.values())}
    for pricing in pricings:
        event_pricing[pricing['event_id']].append(pricing)

    rs = 0
    ers = 0
    insts = 0
    for customer in customer_conferences:
        for conference in customer_conferences[customer]:
            reservation = collections.OrderedDict()
            reservation_cost = 0

            reservation['id'] = rs + 1
            reservation['customer_id'] = customer
            reservation['conference_id'] = conference
            reservation['placed_on'] = subtract_days(conferences[conference]['start_date'], random.randint(7, 120))
            reservation['is_cancelled'] = 0 if random.random() < 0.95 else 1

            reservations.append(reservation)
            for day in filter(lambda d: days[d]['conference_id'] == conference, customer_days[customer]):
                day_reservation = collections.OrderedDict()

                day_reservation['id'] = ers + 1
                day_reservation['reservation_id'] = reservation['id']
                day_reservation['event_id'] = days[day]['id']
                day_reservation['participants'] = len(customer_days[customer][day])
                day_reservation['is_cancelled'] = 0 if random.random() < 0.95 else 1

                day_reservations.append(day_reservation)

                if day_reservation['is_cancelled'] == 0 and days[day]['is_cancelled'] == 0:
                    p = 0
                    while p < len(event_pricing[day]) - 1 \
                            and reservation['placed_on'] <= event_pricing[day][p + 1]['end_date']:
                        p += 1
                    eligible_price = event_pricing[day][p]['price']
                    for p in customer_days[customer][day]:
                        reservation_cost += \
                            eligible_price * (
                                1 - conferences[conference]['student_discount']
                                if participants[p]['is_student'] == 1 else 1)

                for participant in filter(lambda p: participants[p]['customer_id'] == customer,
                                          day_participants[day]):
                    participation = collections.OrderedDict()

                    participation['event_reservation_id'] = day_reservation['id']
                    participation['participant_id'] = participant

                    participations.append(participation)
                ers += 1
            for workshop in \
                    filter(lambda w: workshops[w]['conference_id'] == conference, customer_workshops[customer]):
                workshop_reservation = collections.OrderedDict()

                workshop_reservation['reservation_id'] = rs + 1
                workshop_reservation['event_id'] = workshop
                workshop_reservation['participants'] = len(customer_workshops[customer][workshop])
                workshop_reservation['is_cancelled'] = 0 if random.random() < 0.95 else 1

                workshop_reservations.append(workshop_reservation)

                if workshop_reservation['is_cancelled'] == 0 and workshops[workshop]['is_cancelled'] == 0:
                    p = 0
                    while p < len(event_pricing[workshop]) - 1 \
                            and reservation[rs]['placed_on'] <= event_pricing[workshop][p + 1]['end_date']:
                        p += 1
                    eligible_price = event_pricing[workshop][p]['price']
                    for p in customer_workshops[customer][workshop]:
                        reservation_cost += eligible_price * (
                            1 - conferences[conference]['student_discount']
                            if participants[p]['is_student'] == 1 else 1)

                for participant in filter(lambda p: participants[p]['customer_id'] == customer,
                                          workshop_participants[workshop]):
                    participation = collections.OrderedDict()

                    participation['event_reservation_id'] = ers + 1
                    participation['participant_id'] = participant

                    participations.append(participation)
                ers += 1
            if reservation['is_cancelled'] == 0 and conferences[conference]['is_cancelled'] == 0:
                if reservation_cost < 100:
                    if random.random() < 0.95:
                        installment = collections.OrderedDict()

                        installment['id'] = insts + 1
                        installment['reservation_id'] = reservation['id']
                        installment['value'] = reservation_cost
                        installment['placed_on'] = subtract_days(reservation['placed_on'], -random.randint(0, 14))

                        installments.append(installment)
                        insts += 1
                else:
                    installment_count = random.randint(1, 7)
                    zeroth = subtract_days(reservations[rs]['placed_on'], 1)
                    past = 0
                    if random.random() < 0.95:
                        paid = 0
                        rest = reservation_cost
                        while paid < installment_count:
                            installment = collections.OrderedDict()

                            installment['id'] = insts + 1
                            installment['reservation_id'] = reservation['id']
                            installment_value = int(reservation_cost / installment_count)
                            installment['value'] = installment_value if paid < installment_count - 1 else rest
                            rest -= installment_value
                            past += random.randint(1, int((7 - past) / installment_count) + 1)
                            installment['placed_on'] = subtract_days(zeroth, -past)

                            installments.append(installment)
                            insts += 1
                            paid += 1
                    else:
                        paid = 0
                        will_pay = random.randint(0, installment_count)
                        while paid < will_pay:
                            installment = collections.OrderedDict()

                            installment['id'] = insts + 1
                            installment['reservation_id'] = reservation['id']
                            installment['value'] = int(reservation_cost / installment_count * (
                                1 if random.random() < 0.95 else 2 * random.random()))
                            past += random.randint(1, 7)
                            installment['placed_on'] = subtract_days(zeroth, -(
                                past * (1 if random.random() < 0.95 else 2 * random.random())))

                            installments.append(installment)
                            insts += 1
                            paid += 1
            rs += 1

    generate_csv('Reservations', reservations)
    generate_csv('EventReservations', day_reservations + workshop_reservations)
    generate_csv('Participations', participations)
    generate_csv('Installments', installments)


def main():
    generate_customers()
    generate_participants()
    generate_conferences()
    generate_events()
    generate_event_times()
    generate_pricings()
    generate_reservations()

    return 0


if __name__ == '__main__':
    main()
