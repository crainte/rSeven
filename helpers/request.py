GROUPS = [
        # safe
        {'id': 'sg-000', 'ingress': [ {'port': 25, 'cidr': '1.2.3.4/32'}] },
        # individuals
        {'id': 'sg-123', 'ingress': [ {'port': 22, 'cidr': '0.0.0.0/0'}] },
        {'id': 'sg-456', 'ingress': [ {'port': 53, 'cidr': '10.10.10.0/24'}] },
        {'id': 'sg-789', 'ingress': [ {'port': 80, 'cidr': '10.0.0.0/8'}] },
        # nested
        {'id': 'sg-aaa', 'ingress': [ {'sg': 'sg-123'}] },
        {'id': 'sg-bbb', 'ingress': [ {'sg': 'sg-aaa'}] },
        {'id': 'sg-ccc', 'ingress': [ {'sg': 'sg-bbb'}, {'port': 443, 'cidr': '0.0.0.0/0'}] },
        {'id': 'sg-ddd', 'ingress': [ {'sg': 'sg-000'}] },
        {'id': 'sg-ggg', 'ingress': [ {'sg': 'sg-ddd'}, {'sg': 'sg-456'}, {'sg': 'sg-789'}] },
]

INSTANCES = [
    {'id': 'i-12345', 'sg': ['sg-123'] },
    {'id': 'i-45678', 'sg': ['sg-456'] },
    {'id': 'i-78901', 'sg': ['sg-789'] },
    {'id': 'i-00000', 'sg': ['sg-aaa'] },
    {'id': 'i-00001', 'sg': ['sg-bbb'] },
    {'id': 'i-00002', 'sg': ['sg-ccc'] },
    {'id': 'i-00003', 'sg': ['sg-123', 'sg-bbb'] },
    {'id': 'i-00004', 'sg': ['sg-ddd', 'sg-ccc'] },
    {'id': 'i-00005', 'sg': ['sg-ddd', 'sg-456', 'sg-000', 'sg-bbb'] },
    {'id': 'i-00006', 'sg': ['sg-ddd'] },
]



class FakeRequest:
    def __init__(self, *args, **kwargs):
        self


    def get(self, url=None):
        if url == 'describe-security-groups':
            return GROUPS
        elif url == 'describe-instances':
            return INSTANCES
        else:
            return None


request = FakeRequest()
