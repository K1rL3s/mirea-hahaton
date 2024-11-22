# from dishka import Provider, Scope, provide
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from database.repos.sheets import SheetRepo
# from database.repos.users import UserRepo
#
#
# class ReposProvider(Provider):
#     @provide(scope=Scope.REQUEST)
#     def user_repo(self, session: AsyncSession) -> UserRepo:
#         return UserRepo(session)
#
#     @provide(scope=Scope.REQUEST)
#     def sheet_repo(self, session: AsyncSession) -> SheetRepo:
#         return SheetRepo(session)
