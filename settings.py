# simple in-memory settings
settings = {
    "pregnancy_start_date": "2024-11-02"
}

def set_pregnancy_start_date(new_date_str):
    settings["pregnancy_start_date"] = new_date_str

def get_pregnancy_start_date():
    return settings["pregnancy_start_date"]
