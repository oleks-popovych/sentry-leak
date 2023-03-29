import resource

import numpy as np
from sentry_leak.factory import get_celery

app = get_celery()


@app.task(name="person")
def do_task(
        message: str,
):
    memory_consumed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"Memory ar the beginning of the task: {memory_consumed / 1024} Mb")
    a = [np.random.random((4000, 4000, 3)) for i in range(5)]
