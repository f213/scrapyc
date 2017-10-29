def test_import():
    from scrapyd_client import ScrapydClient

    assert ScrapydClient is not None
