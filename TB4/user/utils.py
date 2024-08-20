import phonenumbers


def normalize_phone_number(phone_number, default_region="RU"):
    _parsed_number = phonenumbers.parse(phone_number, default_region)
    normalized_number = phonenumbers.format_number(
        _parsed_number,
        phonenumbers.PhoneNumberFormat.E164
    )
    return normalized_number
