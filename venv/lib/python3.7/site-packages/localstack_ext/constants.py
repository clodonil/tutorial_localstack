# version of localstack-ext
VERSION = '0.10.66'

# TODO: fix this. Also, not sure which timezone AWS uses - should be UTC, but there
# have been examples of AccessToken validation failure because of local time comparison
TOKEN_EXPIRY_SECONDS = 24 * 60 * 60

# HTTP header used to forward proxy request URLs
HEADER_LOCALSTACK_EDGE_URL = 'x-localstack-edge'
HEADER_LOCALSTACK_TARGET = 'x-localstack-target'
