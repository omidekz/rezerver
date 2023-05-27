from fastapi import Query, HTTPException, status


def admin_access(password: str = Query(...)):
    if password == "omidamm":
        return True
    raise HTTPException(status.HTTP_403_FORBIDDEN)
