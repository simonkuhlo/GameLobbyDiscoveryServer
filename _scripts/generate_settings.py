settings_path = "../_config/settings.json"


from _lib.settings_structure.settings_structure import save_settings, Settings

settings = Settings()
save_settings(settings_path, settings)

