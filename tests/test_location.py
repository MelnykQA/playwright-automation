from pytest import mark


@mark.test_id(362)
def test_location_ok(mobile_app_auth):
    location = mobile_app_auth.get_location()
    assert '48.8:2.3' == location