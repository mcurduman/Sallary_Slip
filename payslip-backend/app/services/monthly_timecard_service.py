from app.db.models.monthly_timecard import MonthlyTimecard
from app.repositories.monthly_timecard_repository import MonthlyTimecardRepository
from typing import Optional, Iterable
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

class MonthlyTimecardService:
    def __init__(self, monthly_timecard_repository: MonthlyTimecardRepository):
        self.monthly_timecard_repository = monthly_timecard_repository

    async def create_monthly_timecard(self, monthly_timecard: MonthlyTimecard) -> MonthlyTimecard:
        try:
            return await self.monthly_timecard_repository.create(monthly_timecard)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create monthly timecard: {str(e)}")
        
    async def get_monthly_timecard_by_id(self, monthly_timecard_id: str
        ) -> Optional[MonthlyTimecard]:
        try:
            return await self.monthly_timecard_repository.get(monthly_timecard_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve monthly timecard: {str(e)}")
        
    async def get_all_monthly_timecards(self) -> Iterable[MonthlyTimecard]:
        try:
            return await self.monthly_timecard_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve monthly timecards: {str(e)}")
        
    async def delete_monthly_timecard(self, monthly_timecard_id: str) -> None:
        try:
            await self.monthly_timecard_repository.delete(monthly_timecard_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete monthly timecard: {str(e)}")
        
    async def update_monthly_timecard(self, monthly_timecard: MonthlyTimecard
        ) -> MonthlyTimecard:
        try:
            return await self.monthly_timecard_repository.update(monthly_timecard)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update monthly timecard: {str(e)}")
