import pytest


@pytest.fixture
def construct(lab, award, target):
    return {
        'award': award['uuid'],
        'lab': lab['uuid'],
        'target': target['uuid'],
        'construct_type': 'fusion protein',
        'tags': [
            {
                'name': 'eGFP',
                'location': 'C-terminal'
            }
        ]
    }


@pytest.fixture
def construct_1(construct):
    item = construct.copy()
    item.update({
        'schema_version': '1',
        'status': 'CURRENT',
        'award': '4d462953-2da5-4fcf-a695-7206f2d5cf45'
    })
    return item


def test_construct_upgrade(upgrader, construct_1):
    value = upgrader.upgrade('construct', construct_1, target_version='2')
    assert value['schema_version'] == '2'
    assert value['status'] == 'in progress'


def test_construct_upgrade_status_encode2(upgrader, construct_1):
    construct_1['award'] = '366388ac-685d-415c-b0bb-834ffafdf094'
    value = upgrader.upgrade('construct', construct_1, target_version='2')
    assert value['schema_version'] == '2'
    assert value['status'] == 'released'


def test_construct_upgrade_status_deleted(upgrader, construct_1):
    construct_1['status'] = 'DELETED'
    value = upgrader.upgrade('construct', construct_1, target_version='2')
    assert value['schema_version'] == '2'
    assert value['status'] == 'deleted'
