from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from .routers import (WebsocketRouter,
                      AuthRouter,
                      CarRouter,
                      CarPredictionRouter,
											CarBrandRouter,
											CarFuelRouter,
											CarTransmissionRouter,
											CarColorRouter)
from .core import limiter

app = FastAPI()


app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.include_router(WebsocketRouter)
app.include_router(AuthRouter)
app.include_router(CarRouter)
app.include_router(CarPredictionRouter)
app.include_router(CarBrandRouter)
app.include_router(CarFuelRouter)
app.include_router(CarTransmissionRouter)
app.include_router(CarColorRouter)
