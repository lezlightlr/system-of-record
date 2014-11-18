from datatypes.core import unicoded

from systemofrecord.repository import chain_repo as chain_repository, blockchain_object_repository

from systemofrecord.services.compression_service import decompress
from tests.teardown_unittest import TeardownUnittest


class ChainRepositoryTestCase(TeardownUnittest):
    def test_can_load_historic_objects_given_chains(self):
        # Here we'll create three items in the global blockchain linked by a sub chain,
        # a->b->c
        # We'll then load the last objects chained to c, which should be b,c
        test_object_id = 'AB12345'

        data_for_a = unicoded({
            'schema_version': 1,

            'object': {
                'object_id': 'AB12345',
                'data': 'data-1',
                'created_by': 'The Mint',
                'initial_request_timestamp': '123456',
                'reason_for_change': "str",

                'chains': [
                    {
                        'chain_name': 'history',
                        'chain_value': 'AB12345',
                    },
                    {
                        'chain_name': 'otherchain',
                        'chain_value': 'foo',
                    }
                ],
            }
        })

        data_for_b = unicoded({
            'schema_version': 1,

            'object': {
                'object_id': 'AB12345',
                'data': 'data-2',
                'created_by': 'The Mint',
                'initial_request_timestamp': '123456',
                'reason_for_change': "str",

                'chains': [
                    {
                        'chain_name': 'history',
                        'chain_value': 'AB12345',
                    },
                    {
                        'chain_name': 'otherchain',
                        'chain_value': 'foo',
                    }
                ],
            }
        })

        data_for_c = unicoded({
            'schema_version': 1,

            'object': {
                'object_id': 'AB12345',
                'data': 'data-3',
                'created_by': 'The Mint',
                'initial_request_timestamp': '123456',
                'reason_for_change': "str",

                'chains': [
                    {
                        'chain_name': 'history',
                        'chain_value': 'AB12345',
                    },
                    {
                        'chain_name': 'otherchain',
                        'chain_value': 'foo',
                    }
                ],
            }
        })

        print "*** PROCESSING A"

        blockchain_object_repository.store_object(object_id=test_object_id, data=data_for_a)
        object_a = blockchain_object_repository.load_most_recent_object_with_id(test_object_id)
        self.assertTrue('data-1' in decompress(object_a.data))

        # Now we only have object A in the blockchain. It has sub-chains, but there should be
        # no historic items for these chains.
        # This means that we should load this object from the repository for the chain heads.
        chain_heads_for_a = chain_repository.load_chain_heads_for_object(object_a)
        print "heads for a" + repr(chain_heads_for_a)

        self.check_chained_object_are_correct(chain_heads_for_a['history'][0], object_a)
        self.check_chained_object_are_correct(chain_heads_for_a['otherchain'][0], object_a)

        print "*** PROCESSING B"

        blockchain_object_repository.store_object(object_id=test_object_id, data=data_for_b)
        object_b = blockchain_object_repository.load_most_recent_object_with_id(test_object_id)
        self.assertTrue('data-2' in decompress(object_b.data))

        # Now, object a should be in our chain for both the chain tags on the test data
        chain_heads_for_b = chain_repository.load_chain_heads_for_object(object_b)
        print "heads for b" + repr(chain_heads_for_b)

        # We're expecting to see 'history' : object_a, 'otherchain': object_a here
        self.check_chained_object_are_correct(chain_heads_for_b['history'][0], object_b)
        self.check_chained_object_are_correct(chain_heads_for_b['history'][1], object_a)
        self.check_chained_object_are_correct(chain_heads_for_b['otherchain'][0], object_b)
        self.check_chained_object_are_correct(chain_heads_for_b['otherchain'][1], object_a)

        print "*** PROCESSING C"

        blockchain_object_repository.store_object(object_id=test_object_id, data=data_for_c)
        object_c = blockchain_object_repository.load_most_recent_object_with_id(test_object_id)
        self.assertTrue('data-3' in decompress(object_c.data))


        # Now lets load the head of the chain for object C
        chain_heads_for_c = chain_repository.load_chain_heads_for_object(object_c)
        print "heads for c" + repr(chain_heads_for_c)

        self.check_chained_object_are_correct(chain_heads_for_c['history'][0], object_c)
        self.check_chained_object_are_correct(chain_heads_for_c['history'][1], object_b)
        self.check_chained_object_are_correct(chain_heads_for_c['otherchain'][0], object_c)
        self.check_chained_object_are_correct(chain_heads_for_c['otherchain'][1], object_b)

    def check_chained_object_are_correct(self, got, expected):
        self.assertIsNotNone(got)
        self.assertIsNotNone(expected)

        self.assertEqual(got.as_dict()['object']['data'], expected.as_dict()['object']['data'])
