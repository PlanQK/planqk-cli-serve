import concurrent.futures

class TaskExecutor(concurrent.futures.ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._futures = {} 

    def submit(self, fn, params, data, key, is_done_callback):
        future = super().submit(fn, params, data)
        future.add_done_callback(is_done_callback)
        self._futures[key] = future

    def get(self, key):
        return self._futures.get(key)

    def delete(self, key):
        if self._futures.get(key):
            del self._futures[key]
