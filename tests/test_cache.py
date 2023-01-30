from ds.lru_cache import LRUCache


def test_lru_cache() -> None:
    lru_cache: LRUCache = LRUCache(2)

    value_1 = lru_cache.get('1')
    assert not value_1, 'value_1 is not correct'
    assert not lru_cache.queue.size, 'cache queue is not empty'
    assert not lru_cache.map, 'cache map is not empty'

    lru_cache.put('1', ['a'])
    assert lru_cache.queue.size, 'cache queue is empty'
    assert lru_cache.map, 'cache map is empty'

    value_1 = lru_cache.get('1')
    assert value_1 == ['a'], 'value_1 is not correct'
    assert lru_cache.queue.head.get_data() == value_1, 'cache queue is not correct'
    assert lru_cache.map['1'].get_data() == value_1, 'cache map is not empty'

    lru_cache.put('2', ['b'])
    assert lru_cache.capacity == lru_cache.queue.size, 'queue is not full'

    value_2 = lru_cache.get('2')
    assert value_2 == ['b'], 'value_2 is not correct'
    assert lru_cache.queue.head.get_data() == value_2, 'cache queue is not correct'
    assert lru_cache.queue.tail.get_data() == value_1, 'cache queue is not correct'
    assert lru_cache.map['2'].get_data() == value_2, 'cache map is not empty'

    lru_cache.put('3', ['c'])
    assert lru_cache.queue.head.get_key() == '3', 'cache queue is not correct'
    assert lru_cache.queue.tail.get_key() == '2', 'cache queue is not correct'
    assert '1' not in lru_cache.map.keys(), 'cache has an invalidate entry'

    value_3 = lru_cache.get('3')
    assert value_3 == ['c'], 'value_3 is not correct'
    assert lru_cache.queue.head.get_data() == value_3, 'cache queue is not correct'
    assert lru_cache.queue.tail.get_data() == value_2, 'cache queue is not correct'
    assert lru_cache.map['3'].get_data() == value_3, 'cache map is not empty'
    assert lru_cache.map['2'].get_data() == value_2, 'cache map is not empty'

    value_1 = lru_cache.get('1')
    assert value_1 == [], 'value_1 is not correct'
    assert '1' not in lru_cache.map.keys(), 'cache has an invalidate entry'


if __name__ == '__main__':
    test_lru_cache()
