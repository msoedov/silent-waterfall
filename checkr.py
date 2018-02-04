import os
import datetime
import aiohttp
import asyncio
import async_timeout

from storage import Repo, Subscriber

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    exit("Missconfigured API_KEY")


async def weather_for(session, city, state):
    wapi_almanac_uwl = 'http://api.wunderground.com/api/{}/almanac/q/{}/{}.json'.format(
        API_KEY, state, city)
    wapi_current_url = 'http://api.wunderground.com/api/{}/conditions/q/{}/{}.json'.format(
        API_KEY, state, city)
    with async_timeout.timeout(10):
        async with session.get(wapi_almanac_uwl) as response:
            almanac_weather_record = await response.json()
    if 'almanac' in almanac_weather_record:
        history_high = float(
            almanac_weather_record['almanac']['temp_high']['normal']['C'])
    else:
        history_high = cur_temp
    if 'almanac' in almanac_weather_record:
        history_low = float(
            almanac_weather_record['almanac']['temp_low']['normal']['C'])
    else:
        history_low = cur_temp
    almanac_avg_temp = (history_low + history_high) / 2
    with async_timeout.timeout(10):
        async with session.get(wapi_current_url) as response:
            cur_weather_record = await response.json()
    cur_temp = cur_weather_record['current_observation']['temp_c']
    cur_weather = cur_weather_record['current_observation']['weather']

    return {
        'almanac_avg_temp': almanac_avg_temp,
        'cur_temp': cur_temp,
        'cur_weather': cur_weather
    }, abs(almanac_avg_temp - cur_temp) >= 5


async def do_once():
    users = await Repo.execute(TestModel.select())
    cache = {}
    async with aiohttp.ClientSession() as session:
        for u in users:
            if (u.cite, u.state) in cache:
                info, anomaly = cache[(u.cite, u.state)]
            else:
                info, anomaly = await (session, u.cite, u.state)
                cache[(u.cite, u.state)] = info, anomaly
            if anomaly:
                await send_sns_email(user=u, payload=info)


async def send_sns_email(user: Subscriber, payload: dict):
    """
    Nothing new here :)
    """
    return


async def schedule():
    current_hour = datetime.datetime.now().hour
    run_at = 6  # 6 am
    to_wait = run_at - current_hour if current_hour < run_at else 24 - current_hour + run_at
    await asyncio.sleep(to_wait * 60 * 60)
    await do_once()
    while True:
        # 24 h
        await asyncio.sleep(24 * 60 * 60)
        await do_once()


def schedule_coro():

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(schedule())