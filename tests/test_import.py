def test_import():
    from scrapyc import ScrapydClient

    assert ScrapydClient is not None
