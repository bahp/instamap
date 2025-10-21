def get_geolocations(s, reverse=False):
    """

    Parameters
    :param G:
    :return:
    """
    # Libraries
    from functools import partial
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    # Create Geolocator
    geolocator = Nominatim(timeout=10, user_agent="myGeo")
    method = geolocator.reverse if reverse else geolocator.geocode
    method = RateLimiter(method, min_delay_seconds=1)

    # Compute the geographical locations
    return s.progress_apply(partial(method, language='en'))
