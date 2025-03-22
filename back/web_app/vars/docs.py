from .email import *

ORDER_DATE_DAYS = env.int('ORDER_DATE_DAYS', 10)
PAY_DATE_DAYS = env.int('PAY_DATE_DAYS', 5)
SERVICE_MEMO_DAYS = env.int('SERVICE_MEMO_DAYS', 4)
