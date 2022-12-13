from trainer import Trainer


def test_trainer():
    trainer = Trainer('pokemon')
    assert len(trainer.status_by_id) == 1
    assert trainer.status_by_id[100]['candy_count'] == 10
