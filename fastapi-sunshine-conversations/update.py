
import pprint
import requests
import sunshine_conversations_client
from sunshine_conversations_client.rest import ApiException
from datetime import datetime as dt

# Zendesk Sunshine Authentication
# Defining the host is optional and defaults to https://api.smooch.io
# See configuration.py for a list of all supported configuration parameters.
ZENDESK_SUBDOMAIN = "d3v-fyp25s233.zendesk.com"

# API
KEY_ID = "app_681a4ae8b47171b303973d7a"
KEY_SECRET = "HcpACR2Jan82t5jqE1NvTA7vlNPr7V-4zrM7Vnsd4L6xtbJKyEiITr4n7M4pni8SpzuPobiS0KQ1zF-Ey2Wt4A"

# Conversations API
# KEY_ID = "int_688c1b59ff5b5477abd5b82e"
# KEY_SECRET = "Pt_cdFPGDeGb6Ow5Kt7mVmtOd0sj3BNSnmwdxR3iFhqGkRJg1gmU9xuhAwahYTyInT2qjrmZkwye7UA40q1cKw"

url = "http://localhost:8080"
conversation_id = "test_abc"
appName = "apps/customer_support_agent"

configuration = sunshine_conversations_client.Configuration(
    host = f"https://{ZENDESK_SUBDOMAIN}/sc"
)
# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration.username = KEY_ID
configuration.password = KEY_SECRET


# Enter a context with an instance of the API client
# with sunshine_conversations_client.ApiClient(configuration) as api_client:
#     # Create an instance of the API class
#     api_instance = sunshine_conversations_client.SwitchboardsApi(api_client)
#     app_id = '680dd98643546a74cacb2b88' # str | Identifies the app.

#     try:
#         # List Switchboards
#         api_response = api_instance.list_switchboards(app_id)
#         pprint.pp(api_response)
#     except ApiException as e:
#         print("Exception when calling SwitchboardsApi->list_switchboards: %s\n" % e)


# # Enter a context with an instance of the API client
# with sunshine_conversations_client.ApiClient(configuration) as api_client:
#     # Create an instance of the API class
#     api_instance = sunshine_conversations_client.SwitchboardIntegrationsApi(api_client)
#     app_id = '680dd98643546a74cacb2b88' # str | Identifies the app.
#     switchboard_id = '680dd987b3085a44bd8a3917' # str | Identifies the switchboard.
#     switchboard_integration_create_body = {"name":"bot","integrationType":"zd:custom","deliverStandbyEvents":True,"nextSwitchboardIntegrationId":"5ef21b86e933b7355c11c606","messageHistoryCount":10} # SwitchboardIntegrationCreateBody | 

#     try:
#         # Create Switchboard Integration
#         api_response = api_instance.create_switchboard_integration(app_id, switchboard_id, switchboard_integration_create_body)
#         pprint(api_response)
#     except ApiException as e:
#         print("Exception when calling SwitchboardIntegrationsApi->create_switchboard_integration: %s\n" % e)

# Enter a context with an instance of the API client
with sunshine_conversations_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = sunshine_conversations_client.SwitchboardIntegrationsApi(api_client)
    app_id = '680dd98643546a74cacb2b88' # str | Identifies the app.
    switchboard_id = '680dd987b3085a44bd8a3917' # str | Identifies the switchboard.

    try:
        # List Switchboard Integrations
        api_response = api_instance.list_switchboard_integrations(app_id, switchboard_id)
        pprint.pp(api_response)
    except ApiException as e:
        print("Exception when calling SwitchboardIntegrationsApi->list_switchboard_integrations: %s\n" % e)