
from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "username"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class RegisterForm:
    pass


class CreateProjectForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.access_token = Optional[str] = None
        self.title: Optional[str] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")  
        self.description = form.get("description")
        self.access_token = request.cookies.get("access_token")

    async def is_valid(self):
        if not self.title:
            self.errors.append("Title is required")
        if len(self.title) < 6:
            self.errors.append("The title length must be at least 6 characters")
        if not self.description:
            self.errors.append("Description is required")
        if len(self.description) < 10:
            self.errors.append("The description length must be at least 10 characters")
        if not self.errors:
            return True
        return False

    async def has_token(self):
        if not self.access_token:
            self.errors.append("Must be logged in first")
            return False
        return True