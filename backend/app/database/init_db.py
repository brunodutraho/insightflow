from app.database.base import Base
from app.database.database import engine

from app.models import (
    user, insight, client, subscription, ad_account, ad_metric,
    social_metric, plan, coupon, app_config, activity, user_profile,
    communication_metric, marketing_metric, GoalHistory, admin_log,
    metric, password_reset_token, email_verification_token,
    permission, invite_token, audit_log
)



def init_db():
    Base.metadata.create_all(bind=engine)