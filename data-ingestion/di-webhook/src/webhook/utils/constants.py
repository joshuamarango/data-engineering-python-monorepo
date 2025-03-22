from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentVariables(BaseSettings):
    lambda_run_id: str = Field(default="", env="LAMBDA_RUN_ID")
    ssm_param_xero: str = Field(..., env="SSM_PARAM_XERO")
