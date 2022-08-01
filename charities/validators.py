from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class RegNumberValidators(validators.RegexValidator):
    regex = r'^\d{10}$'
    message = (
        'لطفا کد را صحیح وارد کنید (کد باید شامل عدد ده رقمی باشد)'
    )
    flags = 0


reg_number_validator = RegNumberValidators()
