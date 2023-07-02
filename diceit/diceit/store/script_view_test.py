from django.test.utils import setup_test_environment
from django.test import Client
'''Script per accertarsi che le view rispettino i vincoli di permesso'''

setup_test_environment()

client = Client()

response = client.get('/')

print(response.status_code)