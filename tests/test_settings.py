from app.settings import get_settings, clear_settings_cache

def test_test_env_uses_memory_db(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    clear_settings_cache()

    settings = get_settings()
    assert settings.DB_URL == "sqlite:///:memory:"


def test_dev_env_uses_dev_db(monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")
    clear_settings_cache()

    settings = get_settings()
    assert "dev.db" in settings.DB_URL