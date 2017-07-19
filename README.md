# Once Upon A Time

Event provider


## Structure

Tried to use peewee as the ORM/query builder.

```
python -m pwiz --engine=mysql --host=127.0.0.1 --port=3306 --user=readonly nova > nova_models.py
```

Gave up, it's suuuper slow with the (artificial?) join query.

Now using raw queries with the `hammers` package, a la the "neutron reaper" script in it.


## Endpoints

### POST `/events/daterange`

Post a JSON object with `from` and `to` keys.


### GET `/events/afterid/<int>`

Returns up to 1000 events after the provided ID.
