import os
from pathlib import Path
from typing import Any, Iterable

from supabase import Client, create_client


BASE_DIR = Path(__file__).resolve().parent


def _load_local_env_files() -> None:
    _load_dotenv_file(BASE_DIR / ".env")
    _load_powershell_env_file(BASE_DIR / "env")


def _load_dotenv_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_powershell_env_file(path: Path) -> None:
    if not path.exists():
        return

    prefix = "$env:"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or not line.startswith(prefix):
            continue

        statement = line[len(prefix):]
        if "=" not in statement:
            continue

        key, value = statement.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _normalize_supabase_url(url: str) -> str:
    cleaned = url.strip().rstrip("/")
    if cleaned.endswith("/rest/v1"):
        cleaned = cleaned[: -len("/rest/v1")]
    return cleaned


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            "Set your Supabase project credentials before starting Flask."
        )
    return value


def _get_supabase_client() -> Client:
    supabase_url = _normalize_supabase_url(_require_env("SUPABASE_URL"))
    supabase_key = _require_env("SUPABASE_KEY")
    return create_client(supabase_url, supabase_key)


_load_local_env_files()


class SupabaseCursor:
    def __init__(self, client: Client):
        self.client = client
        self._result: list[tuple[Any, ...]] = []

    def execute(self, query: str, params: Iterable[Any] = ()) -> "SupabaseCursor":
        normalized = " ".join(query.strip().split()).upper()
        params = tuple(params)

        if normalized == "SELECT COUNT(*) FROM BENEFICIARIES":
            count = self._count_rows("beneficiaries")
            self._result = [(count,)]
            return self

        if normalized == "SELECT COUNT(*) FROM VOLUNTEERS":
            count = self._count_rows("volunteers")
            self._result = [(count,)]
            return self

        if normalized == "SELECT SUM(AMOUNT) FROM DONATIONS":
            total = self._sum_donation_amount()
            self._result = [(total,)]
            return self

        if normalized == "SELECT * FROM BENEFICIARIES":
            self._result = self._select_beneficiaries()
            return self

        if normalized == "SELECT * FROM VOLUNTEERS":
            self._result = self._select_volunteers()
            return self

        if normalized == "SELECT * FROM DONATIONS":
            self._result = self._select_donations()
            return self

        if normalized == "INSERT INTO BENEFICIARIES VALUES (NULL,?,?,?,?)":
            if len(params) != 4:
                raise ValueError("Beneficiary insert expects 4 values.")
            self.client.table("beneficiaries").insert(
                {
                    "name": params[0],
                    "age": int(params[1]),
                    "education": params[2],
                    "support_type": params[3],
                }
            ).execute()
            self._result = []
            return self

        if normalized == "INSERT INTO VOLUNTEERS VALUES (NULL,?,?,?)":
            if len(params) != 3:
                raise ValueError("Volunteer insert expects 3 values.")
            self.client.table("volunteers").insert(
                {
                    "name": params[0],
                    "role": params[1],
                    "contact": params[2],
                }
            ).execute()
            self._result = []
            return self

        if normalized == "INSERT INTO DONATIONS VALUES (NULL,?,?,?)":
            if len(params) != 3:
                raise ValueError("Donation insert expects 3 values.")
            self.client.table("donations").insert(
                {
                    "donor": params[0],
                    "amount": float(params[1]),
                    "purpose": params[2],
                }
            ).execute()
            self._result = []
            return self

        if normalized == "DELETE FROM BENEFICIARIES WHERE ID=?":
            self._delete_by_id("beneficiaries", params)
            return self

        if normalized == "DELETE FROM VOLUNTEERS WHERE ID=?":
            self._delete_by_id("volunteers", params)
            return self

        if normalized == "DELETE FROM DONATIONS WHERE ID=?":
            self._delete_by_id("donations", params)
            return self

        raise NotImplementedError(f"Unsupported query for Supabase adapter: {query}")

    def fetchone(self) -> tuple[Any, ...] | None:
        return self._result[0] if self._result else None

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._result

    def _count_rows(self, table_name: str) -> int:
        response = self.client.table(table_name).select("id", count="exact").execute()
        return int(response.count or 0)

    def _sum_donation_amount(self) -> float:
        response = self.client.table("donations").select("amount").execute()
        rows = response.data or []
        total = sum(float(row.get("amount") or 0) for row in rows)
        return total

    def _select_beneficiaries(self) -> list[tuple[Any, ...]]:
        response = (
            self.client.table("beneficiaries")
            .select("id,name,age,education,support_type")
            .order("id")
            .execute()
        )
        return [
            (
                row["id"],
                row["name"],
                row["age"],
                row["education"],
                row["support_type"],
            )
            for row in (response.data or [])
        ]

    def _select_volunteers(self) -> list[tuple[Any, ...]]:
        response = (
            self.client.table("volunteers")
            .select("id,name,role,contact")
            .order("id")
            .execute()
        )
        return [
            (
                row["id"],
                row["name"],
                row["role"],
                row["contact"],
            )
            for row in (response.data or [])
        ]

    def _select_donations(self) -> list[tuple[Any, ...]]:
        response = (
            self.client.table("donations")
            .select("id,donor,amount,purpose")
            .order("id")
            .execute()
        )
        return [
            (
                row["id"],
                row["donor"],
                row["amount"],
                row["purpose"],
            )
            for row in (response.data or [])
        ]

    def _delete_by_id(self, table_name: str, params: tuple[Any, ...]) -> None:
        if len(params) != 1:
            raise ValueError(f"{table_name} delete expects 1 value.")
        self.client.table(table_name).delete().eq("id", params[0]).execute()
        self._result = []


class SupabaseConnection:
    def __init__(self):
        self.client = _get_supabase_client()

    def cursor(self) -> SupabaseCursor:
        return SupabaseCursor(self.client)

    def commit(self) -> None:
        return None

    def close(self) -> None:
        return None


def connect_db() -> SupabaseConnection:
    return SupabaseConnection()


def create_tables() -> None:
    """
    Supabase tables are created in the Supabase SQL Editor.
    This function is kept only for compatibility with app.py.
    """
    return None
