# -*- encoding:utf-8 -*-

from .process_template import ProcessTemplateService
from .stage_template import StageTemplateService
from .process import ProcessService
from .stage import StageService
from .task import TaskService
from .user import UserService
from .company import CompanyService
from .customer import CustomerService
from .item import ItemService
from .permission import PermissionService
from .role import RoleService
from .offer import OfferService
from .team import TeamService


process_template = ProcessTemplateService
stage_template = StageTemplateService
process = ProcessService
stage = StageService
task = TaskService
user = UserService
company = CompanyService
customer = CustomerService
item = ItemService
offer = OfferService
permission = PermissionService
role = RoleService
team = TeamService
