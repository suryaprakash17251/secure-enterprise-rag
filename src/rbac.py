ROLE_ACCESS = {
    "finance": ["finance", "general"],
    "hr": ["hr", "general"],
    "marketing": ["marketing", "general"],
    "engineering": ["engineering", "general"],
    "employee": ["general"],
    "c_level": ["finance", "hr", "marketing", "engineering", "general"],
}


def allowed_departments(role: str) -> list[str]:
    # unknown role -> no access
    return ROLE_ACCESS.get(role, [])