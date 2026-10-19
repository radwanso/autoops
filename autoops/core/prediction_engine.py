# autoops/core/prediction_engine.py

from autoops.core.predictor import predict_failure


def prediction_failure_handler(payload):

    events = payload.get(
        "events",
        []
    )

    reputation = payload.get(
        "reputation",
        1.0
    )

    return predict_failure(
        events,
        reputation
    )
