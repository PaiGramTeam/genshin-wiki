def get_repo_raw(url: str) -> str:
    """Get the raw url of the repo."""
    if 'gitlab.com' in url:
        return url + "/-/raw/master/"
    return url + "/raw/master/"