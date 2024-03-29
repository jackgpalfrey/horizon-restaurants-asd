from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.branch.BranchService import BranchService
from src.utils.errors import InputError

guard = auth_guard
cleanup = auth_cleanup


def post(branch_id: str):
    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        branch.delete()
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK({})
