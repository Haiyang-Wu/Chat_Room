import traceback
from conf.settings import *
class Test:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # # print(exc_type.__name__)
        # # print(exc_val)
        # # print(exc_tb.tb_frame)
        # traceback.print_list(exc_tb)


        if exc_type is not None:
            ERROR_LOGGER.error('{}: {} {}'.format(
                exc_type.__name__, exc_val, exc_tb.tb_frame
            ))
        return True

with Test()as t:
    t.xxx

print('aaa')