from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    db_host: str = Field(..., json_schema_extra={"env": "DB_HOST"})
    db_port: int = Field(..., json_schema_extra={"env": "DB_PORT"})
    db_user: str = Field(..., json_schema_extra={"env": "DB_USER"})
    db_password: str = Field(..., json_schema_extra={"env": "DB_PASSWORD"})
    db_name: str = Field(..., json_schema_extra={"env": "DB_NAME"})


    jwt_secret_key: str = Field(..., description="Secret key for JWT encoding/decoding", json_schema_extra={"env": "JWT_SECRET_KEY"})
    jwt_algorithm: str = Field(default="HS256", description="Algorithm used for JWT", json_schema_extra={"env": "JWT_ALGORITHM"})
    token_ttl_hours: int = Field(default=12, description="Jwt token ttl in hours", json_schema_extra={"env": "TOKEN_TTL_HOURS"})

    @field_validator("jwt_algorithm")
    def validate_algorithm(cls, value: str):
        allowed_algorithms = {"HS256", "RS256", "HS512"}
        if value not in allowed_algorithms:
            raise ValueError(f"Invalid JWT algorithm: {value}. Allowed values are {allowed_algorithms}")
        return value

    class Config:
        env_file = "./.env"


