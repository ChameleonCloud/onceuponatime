BASE_SQL = '''
SELECT
    i.uuid,
    i.memory_mb,
    i.vcpus,
    ia.created_at,
    ia.id AS action_id,
    iae.id AS event_id,
    iae.event,
    iae.start_time,
    iae.finish_time,
    iae.result
FROM
    nova.instances AS i
        JOIN
    nova.instance_actions AS ia ON i.uuid = ia.instance_uuid
        JOIN
    nova.instance_actions_events AS iae ON ia.id = iae.action_id
'''


def events_after_id(db, last_event_id):
    sql = BASE_SQL + '''\
    WHERE
        iae.id >= %s
    '''
    return db.query(sql, args=[int(last_event_id)], limit=1000)


def events_date_range(db, from_date, to_date):
    sql = BASE_SQL + '''\
    WHERE
        ia.created_at >= %s
    AND ia.created_at <= %s
    '''
    return db.query(sql, args=[from_date, to_date], limit=1000)
