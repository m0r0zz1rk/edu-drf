from enum import Enum


class PlanningParameters(Enum):
    PLANNING_DAYS = 'planningDays'
    ORDER_DATE_DAYS = 'order_date_days'
    PAY_DATE_DAYS = 'pay_date_days'
    SERVICE_MEMO_DAYS = 'service_memo_days'
    STUDENT_GROUP_STATEMENT_DAYS = 'student_group_statement_days'