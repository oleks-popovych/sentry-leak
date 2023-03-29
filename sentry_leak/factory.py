import os
import celery
import pydantic
import sentry_sdk
import sentry_sdk.integrations.celery


class Settings(pydantic.BaseSettings):
    CELERY_BROKER_URL: pydantic.AnyUrl = "amqp://guest:guest@127.0.0.1:5672"
    CELERY_RESULT_BACKEND_URL: pydantic.AnyUrl = "redis://127.0.0.1:6379/5"


def fn_route_for_task(
        name: str, *args, **kwargs,
):
    return {"queue": "person"}


def get_celery():
    settings = Settings()

    app = celery.Celery(
        "worker",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND_URL,
    )
    app.conf.task_routes = fn_route_for_task

    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        print("Specify env var: SENTRY_DSN!")
        exit(1)

    sentry_sdk.init(
        dsn=dsn,
        integrations=[sentry_sdk.integrations.celery.CeleryIntegration()],
        release="fair",
        environment="dev",
        traces_sample_rate=1.0,
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )
    return app
