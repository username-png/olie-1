import dramatiq

from model.model import load_model


@dramatiq.actor(queue_name='default')
def retrain_model():
    load_model(force_retrain=True)
