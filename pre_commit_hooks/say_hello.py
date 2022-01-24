import argparse


def say_hello(username: str) -> int:
    """Say hello to username.

    Args:
        username (str): Say hello to ``username``.

    Returns:
        int: Return the status of the function.
    """
    retv = 0
    if isinstance(username, str):
        print(f'Hello {username}')
    else:
        retv = 1

    return retv


def main():
    parser = argparse.ArgumentParser(description='say hello to user')
    parser.add_argument('username', type=str)
    args = parser.parse_args()
    return say_hello(args.username)


if __name__ == '__main__':
    raise SystemExit(main())
