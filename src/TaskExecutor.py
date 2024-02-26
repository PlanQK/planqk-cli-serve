import concurrent.futures

# The TaskExecutor is used as a container of future objects.
class TaskExecutor(concurrent.futures.ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._futures = {} 

    """
    Submits an async task for execution.
        Parameters:
            fn (callable): The function to execute.
            params (dict): Parameters to pass to the function.
            data (dict): Additional data to pass to the function.
            key (str): A unique key to identify the task.
            is_done_callback (callable): A callback function that will be executed after the task is done.
        Returns: 
            Void
    """
    def submit(self, fn, params, data, key, is_done_callback):
        future = super().submit(fn, params, data)
        future.add_done_callback(is_done_callback)
        self._futures[key] = future

    def get(self, key):
        return self._futures.get(key)

    def delete(self, key):
        if self._futures.get(key):
            del self._futures[key]
