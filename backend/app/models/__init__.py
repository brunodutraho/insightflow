# Core models (ordem IMPORTANTE para evitar dependência circular)

from .user import User, UserRole, UserStatus
from .client import Tenant

# Auth / Security
from .permission import Permission
from .invite_token import InviteToken
from .email_verification_token import EmailVerificationToken
from .password_reset_token import PasswordResetToken

# User
from .user_profile import UserProfile

# Billing / SaaS
from .plan import Plan
from .subscription import Subscription
from .coupon import Coupon

# Metrics / Data
from .metric import Metric
from .ad_account import AdAccount
from .ad_metric import AdMetric
from .social_metric import SocialMetric
from .goal import GoalHistory
from .communication_metric import CommunicationMetric
from .marketing_metric import MarketingMetric

# Insights / AI
from .insight import Insight

# System / Logs
from .audit_log import AuditLog
from .admin_log import AdminLog
from .activity import ActivityItem

# App Config / Integrations
from .app_config import AppConfig
from .social_collector import collect_social_metrics
from .feature import Feature
from .plan_feature import PlanFeature



__all__ = [
    # Core
    "User",
    "UserRole",
    "UserStatus",
    "Tenant",

    # Auth
    "Permission",
    "InviteToken",
    "EmailVerificationToken",
    "PasswordResetToken",

    # User
    "UserProfile",

    # Billing
    "Plan",
    "Subscription",
    "Coupon",

    # Metrics
    "Metric",
    "AdAccount",
    "AdMetric",
    "SocialMetric",
    "CommunicationMetric",
    "MarketingMetric",

    # Insights
    "Insight",

    # Logs
    "AuditLog",
    "AdminLog",
    "Activity",

    # Config
    "AppConfig",
    "SocialCollector",
]