from datetime import datetime


def current_time():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def print_header(title):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)
    