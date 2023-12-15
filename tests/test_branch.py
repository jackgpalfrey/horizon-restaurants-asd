import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.branch.Branch import Branch
from src.utils.Database import Database

branch_name = "Bristol Branch"
branch_address = "15-29 Union St, Bristol BS1 2DF"
save_name = "Oxford Branch"
save_address = "116-118 Lower Borough Walls, Bath BA1 1QU"
new_name = "Manchester Branch"
new_address = "12a Oxford Rd, Manchester M1 5QA"


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.init()

    yield

    Database.close()


def test_create_branch():
    city = CityService.get_by_name("London")
    branch = BranchService.create(branch_name, branch_address, city)
    assert isinstance(branch, Branch)


def test_get_branch_by_name():
    branch = BranchService.get_by_name(branch_name)
    assert isinstance(branch, Branch)


def test_get_branch_by_id():
    city = CityService.get_by_name("Reading")
    created_branch = BranchService.create(
        "Reading Branch", "Unit 17 Horn Hill Rd, Hornhill Road, Worcester WR4 0SX", city)
    got_branch = BranchService.get_by_id(created_branch._branch_id)
    assert type(got_branch) == Branch
    assert type(got_branch._branch_id) == str
    assert created_branch._branch_id == got_branch._branch_id


def test_get_all_branches():
    branch = BranchService.get_all()
    assert len(branch) == 2
    assert type(branch) == list


def test_cannot_create_duplicate_branch():
    city = CityService.get_by_name("Essex")
    with pytest.raises(Exception):
        BranchService.create(branch_name, branch_address, city)


def test_get_branch_id():
    city = CityService.get_by_name("Cardiff")
    created_branch = BranchService.create(
        "Cardiff Branch", "Blackpole Rd, Worcester WR3 8HP", city)
    id = created_branch.get_id()
    assert id == created_branch._branch_id


def test_get_branch_name():
    city = CityService.get_by_name("Oxford")
    created_branch = BranchService.create(
        "Oxford Branch", "Netherton Rd, Ross-on-Wye HR9 7QJ", city)
    name = created_branch.get_name()
    assert name == save_name


def test_get_branch_address():
    city = CityService.get_by_name("Essex")
    created_branch = BranchService.create(
        "Essex Branch", "116-118 Lower Borough Walls, Bath BA1 1QU", city)
    address = created_branch.get_address()
    assert address == save_address


def test_set_branch_name():
    city = CityService.get_by_name("Manchester")
    created_branch = BranchService.create(
        "Manchester", "10 Straits Parade, Fishponds, Bristol BS16 2LA", city)
    created_branch.set_branch_name(new_name)
    assert created_branch.get_name() == new_name


def test_set_branch_address():
    city = CityService.get_by_name("Bath")
    created_branch = BranchService.create(
        "Bath Branch", "4 Eastgate Rd, Bristol BS5 6XX", city)
    created_branch.set_address(new_address)
    assert created_branch.get_address() == new_address


def test_get_by_city():
    city = CityService.get_by_name("Reading")
    got_branch = BranchService.get_by_city(city)
    query = Database.execute_and_fetchone(
        "SELECT city_id FROM branch WHERE id = %s", got_branch._branch_id)
    id = query[0]
    city_id = city.get_id()
    assert city_id == id


def test_get_city():
    city = CityService.get_by_name("Plymouth")
    created_branch = BranchService.create(
        "Plymouth Branch", "12a Oxford Rd, Manchester M1 5QA", city)
    branch_city_id = created_branch.get_city().get_id()
    city_id = city.get_id()
    assert branch_city_id == city_id


def test_set_city():
    city = CityService.get_by_name("Liverpool")
    created_branch = BranchService.create(
        "Liverpool Branch", "67 Broadmead, Bristol BS1 3DX", city)
    new_city = CityService.create("Alexandria")
    created_branch.set_city(new_city)
    city_id = created_branch.get_city().get_id()
    assert city_id == new_city.get_id()
