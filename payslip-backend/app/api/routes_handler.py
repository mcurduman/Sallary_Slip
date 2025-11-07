from app.api.routers.auth import auth_router
from app.api.routers.employee import employee_router
from app.api.routers.payroll_record import payroll_record_router
from app.api.routers.mail import mail_router

def register_routes(app):
    app.include_router(auth_router)
    app.include_router(employee_router)
    app.include_router(payroll_record_router)
    app.include_router(mail_router)
