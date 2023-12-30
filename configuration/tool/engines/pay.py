import asyncio
import enum
import types
import uuid
import pyqiwip2p
from pyqiwip2p.p2p_types import Bill
from pyqiwip2p import QiwiP2P
from configuration.tool.tools import *

class WaitForPayResult(enum.Enum):
    EXPIRED = False
    PAYED = True
    EXCEPTION = False

def paid(count: int, user_discord_id: int, bill_id: str):
    # todo: дописать функцию
    ...

class QiwiPayment:
    def __init__(self, qiwi_token):
        self.qiwi_token = qiwi_token
        self.qiwi = QiwiP2P(auth_key=self.qiwi_token)

    async def build_bill(self, user_discord_id: int, count: int, amount: int, comment: str, bill_lifetime) -> tuple[bool, Any, Any, Any]:
        register = is_registered(DiscordType.USER, int(user_discord_id))
        if register[0]:
            try:
                lifetime = bill_lifetime #минут
                bill_id = str(uuid.uuid4()) + "_user_discord_id:" + str(user_discord_id) + "_intermolla"
                bill: Bill = self.qiwi.bill(bill_id=bill_id, amount=amount, lifetime=lifetime, comment=comment)
                url = bill.pay_url
                log.s('build_bill', f'New bill. user_discord_id: {user_discord_id}; amount: {amount} RUB; lifetime: {lifetime} min; url: {url}')
                return True, url, bill_id, count
            except Exception as e:
                log.e('build_bill', e)
                return False, None, None, None

        else:
            return False, None, None, None

    async def wait_for_pay(self, user_discord_id: int, bill_id: str, count: int, check_every_seconds: float, paid_action: types.FunctionType = paid) -> WaitForPayResult:
        while True:
            await asyncio.sleep(check_every_seconds)
            status = self.qiwi.check(bill_id=bill_id).status
            if status == "EXPIRED":
                self.qiwi.reject(bill_id=bill_id)
                log.w('wait_for_pay', f'The bill expired. bill_id: {bill_id}; user_discord_id: {user_discord_id}')
                return WaitForPayResult.EXPIRED
            elif status == "PAID":
                    try:
                        paid_action(count, user_discord_id, bill_id)
                        return WaitForPayResult.PAYED
                    except Exception as e:
                        log.e('wait_for_pay', f'Issue of the item error. Currency count: {count}; user_discord_id: {user_discord_id}; bill_id: {bill_id}.\n\nException: {e}')
                        return WaitForPayResult.EXCEPTION
            else:
                return WaitForPayResult.EXCEPTION