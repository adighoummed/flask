from ds.queue import Queue


def test_enqueue_at_first():
    queue = Queue()
    queue.enqueue_at_first('1', ['a'])
    queue_head = queue.head
    assert queue_head.get_key() == '1', 'Key is not correct'
    assert queue_head.get_data() == ['a'], 'Data is not correct'


def test_dequeue_from_last():
    queue = Queue()
    queue.enqueue_at_first('1', ['a'])
    key = queue.dequeue_from_last()
    assert key == '1', 'Key is not correct'


def test_move_to_head():
    queue = Queue()
    node_1 = queue.enqueue_at_first('1', ['a'])
    node_2 = queue.enqueue_at_first('2', ['b'])
    assert queue.head.get_key() == '2', 'Head is not correct'
    assert queue.tail.get_key() == '1', 'Tail is not correct'

    queue.move_to_head(node_1)
    assert queue.head.get_key() == '1', 'Head is not correct'
    assert queue.tail.get_key() == '2', 'Tail is not correct'

    node_3 = queue.enqueue_at_first('3', ['c'])
    assert queue.head.get_key() == '3', 'Head is not correct'
    assert queue.tail.get_key() == '2', 'Tail is not correct'

    queue.move_to_head(node_1)
    assert queue.head.get_key() == '1', 'Head is not correct'
    assert queue.tail.get_key() == '2', 'Tail is not correct'


if __name__ == '__main__':
    test_enqueue_at_first()
    test_dequeue_from_last()
    test_move_to_head()

