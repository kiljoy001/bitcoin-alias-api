from .asset_template import Asset
from .bitcoin_address_format_checker import Checker
from .create_user import User
from bigchaindb_driver import BigchainDB
from settings import AppSettings
from hypothesis import given, settings, Verbosity, assume
from hypothesis.strategies import text

app_setting = AppSettings.get_settings()


def test_good_address():
    chk = Checker('1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
    assert chk.check_address() is True


def test_bad_checksum_address():
    chk = Checker('12Mb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW6')
    assert chk.check_address() is False


def test_short_address():
    chk = Checker('1AMb4wcaZ7wZDLJ8')
    assert chk.check_address() is False


def test_long_address():
    chk = Checker('12Mb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW61AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
    assert chk.check_address() is False


@settings(deadline=None)
@given(text())
def test_create_asset(strategy):
    private_key = '855wuFfcwYnS3NqijD9z9yDiBreERpLkBudLyXiwR6K5'
    public_key = '5cDbUCR38avXsQoZmM5diVvn63epKEr6U9HGE236YkTL'
    try:
        asset = Asset('1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8', public_key, private_key, strategy)
        signed_asset = asset.create_asset()
        assert signed_asset is not None or len(signed_asset) == 0
    except ValueError:
        pass


@settings(deadline=None)
@given(text())
def test_alias_names(strategy):
    assume(strategy is not '')
    user = User(strategy, '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
    assert user.Alias is not None
    assert user.Alias is not ''





