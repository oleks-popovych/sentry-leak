from sentry_leak.factory import get_celery


def run():
    for i in range(5):
        print(f"Sending message #{i+1}")
        celery_instance = get_celery()
        celery_instance.send_task(
            "person",
            kwargs={"message": "ignore"},
            queue="person",
        )


if __name__ == "__main__":
    run()
